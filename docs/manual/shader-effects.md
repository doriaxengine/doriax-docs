# Shader Effects

Shader effects change how a mesh draws without forking its shaders. A **vertex offset**
moves its vertices, a **coverage** function removes part of its surface, and **shader
parameters** feed both with values that belong to the mesh, the scene or a camera. The
engine runs them in the color, depth and G-buffer passes alike, so shadows, SSAO and
screen-space reflections agree with what is drawn. Shader parameters also work in forks of
every shader type, as [Custom Shaders](../editor/custom-shaders.md#shader-parameters)
explains.

The engine's wind and see-through are built this way, and so are three small examples it
ships: a dissolve, a height cut, and grass pushed aside by a character.

## How it fits together

| Piece | What it is | Set on |
| --- | --- | --- |
| Vertex offset | One `.glsl` with `vec3 getVertexOffset(vec3 localPosition, vec3 worldPosition)` | Mesh `vertexOffsetShader` |
| Coverage | One `.glsl` with `float getCoverage(CoverageContext context)` | Mesh `coverageShader` |
| Object parameters | Values of one component, declared with `@param` | The component's shader uniforms |
| Scene parameters | `Collection.name` values the whole scene shares, declared with `@scene` | Scene properties, `Scene::setShaderParameter` |
| View parameters | `Collection.name` values of one camera, declared with `@view` | Camera properties, `Camera::setShaderParameter` |

A mesh takes one vertex offset and one coverage function. To combine several effects of
the same kind, write one function that calls the helpers of each (see
[Writing your own](#writing-your-own)). The vertex offset runs after skinning, morph
targets and instancing and before the instance distance fade. The coverage runs at the
start of the fragment stage, before any texture is sampled and before the material's alpha
test.

## Declaring parameters

Parameters are declared in comments, so an effect file stays plain GLSL:

```glsl
// @param float strength = 0.5 [0, 2] "How far the top moves, in world units"
// @param vec4 tint = 1, 0.8, 0.6, 1 color
// @scene vec3 Wind.velocity "Air velocity in m/s"
// @view float SeeThrough.radius = 0 [0, 20]
```

The type is `float`, `vec2`, `vec3`, `vec4`, `int`, `ivec2`, `ivec3` or `ivec4`. The
numbers after `=` are the default, and a single number fills a whole vector. Integer types
travel as floats and are exact up to 16777216. `[min, max]` is the range of the inspector field,
`color` shows a color picker, `runtime` marks a value that a script or the engine writes
(the inspector shows it read-only), and the quoted text is the tooltip.

The code reads each parameter by the name it was declared with:

| Declared as | Read in GLSL as |
| --- | --- |
| `// @param float strength` | `params.strength` |
| `// @scene vec3 Wind.velocity` | `Wind.velocity` |
| `// @view float SeeThrough.radius` | `SeeThrough.radius` |

The collection keeps unrelated values apart: `Wind.speed` and `Water.speed` are two
parameters. A collection is either a scene or a view one. The build stops with an error that
names the file and line when two declarations give a parameter different types, or use a
collection in both scopes, even when one is in the vertex file and the other in the
fragment file. The shader's **Parameters** section shows the same error before any build.
Collection and parameter names take letters, digits and underscores, and `params` and
`Engine` are not collection names.

Annotations are read from the shader file and every file it includes, whatever `#if`
surrounds them. The shader builder packs the declarations of each stage into one uniform
block, `u_vs_params` or `u_fs_params`, with the engine values the code reads. The mesh color
pass appends them to its material block instead, so effects and collections take no extra
uniform block slots there. Changing a value rewrites that block at the next draw. It never
rebuilds a shader or reloads a component.

### Engine values

Two values need no declaration. A shader that reads them gets them:

| Value | Contents |
| --- | --- |
| `Engine.time` | Seconds since the scene started. The clock holds while the editor scene is stopped or paused, and while the game pauses, and starts over when Play mode stops, so each Play session begins like the exported game. For gameplay-driven time, set a parameter of your own from a script. |
| `Engine.resolution` | `xy` = width and height of the target the shader draws into (the camera's framebuffer, the fixed-resolution target, a shadow slot, a reflection probe face, or a post-process target), `zw` = `1 / width` and `1 / height`. |

### Where values come from

An **object parameter** reads the component's shader uniform of the same name, then the
value of the scene default shader when the component inherits it, then the declared
default. A post-process pass keeps its own values.

A **scene parameter** reads the runtime value a script set, then the value saved with the
scene, then the declared default.

A **view parameter** reads, for the camera a pass is drawn for:

1. the runtime value of that camera, from `Camera::setShaderParameter`;
2. the runtime value of the main view, from `Scene::setMainViewShaderParameter`, while that
   camera renders the scene;
3. the value saved on its Camera component;
4. the declared default.

Runtime values are never saved: stopping Play mode or loading the scene again brings back
the saved ones, and `Wind.travel` and the effect clock start over. Each scene keeps its own
values, and so does each copy of it that Play mode runs. Shadow maps are fitted to the
camera that renders the scene, so an effect sees that camera there. A reflection probe
capture has no camera and reads the declared defaults of view parameters.

## Vertex offsets

```glsl
vec3 getVertexOffset(vec3 localPosition, vec3 worldPosition);
```

It returns how far the vertex moves, in world units. `localPosition` is the vertex in the
mesh's own space after skinning, morph targets and instancing, and `worldPosition` is where
it lands before the move. `Engine.time` is the seconds since the scene started (see
[Engine values](#engine-values)).

The mesh's **Max Offset** (`vertexOffsetMax`) is the longest offset. Longer ones are clamped
to it, and culling widens the mesh bounds and each instance's sphere by it, so moved
geometry is not cut at the screen edge or out of a shadow cascade. At 0 nothing is clamped
and the bounds stay those of the mesh data. Lighting keeps the normals of the unmoved
surface, and terrain ignores vertex offsets.

## Coverage

```glsl
float getCoverage(CoverageContext context);
```

It returns how much of the fragment stays: 1 keeps it and 0 removes it. In between, opaque
and alpha-tested surfaces keep a steady 4×4 dithered share of their pixels, and blended
surfaces multiply their alpha instead. The coverage and the material's alpha test are
separate tests that both have to pass.

| `CoverageContext` field | Meaning |
| --- | --- |
| `vec3 worldPosition` | The fragment in world space. |
| `vec2 uv` | The mesh's first UV set as stored, before sprite or instance texture rects; 0 when it has none. Every pass interpolates it for a mesh with coverage. |
| `vec3 eye` | Position of the camera the pass draws for. |
| `vec3 forward` | Its view direction, normalized. |
| `bool perspective` | False for an orthographic camera. |
| `vec2 pixel` | The fragment pixel counted from the corner of the view, the same in every pass, so the depth passes drop the pixels the color pass drops on any viewport offset or flipped target. |

The depth pre-pass and the SSR G-buffer cut what the color pass cuts, so SSAO, reflections
and depth based post-processing match it. Shadow maps keep the whole silhouette unless the
mesh's **Cut Shadows** (`coverageShadows`) is on: a see-through wall should still cast its
shadow, but a dissolving one should not. A skipped coverage still applies the material's
alpha mask to the shadow.

Coverage functions can use the shapes in `includes/coverage_helpers.glsl`, which every
coverage file sees:

| Helper | Returns |
| --- | --- |
| `coverageBelowHeight(worldPosition, height, softness)` | 1 below the height, 0 above, with a dithered band of the given width. |
| `coverageNoise(position)` | A smooth value noise in [0, 1]. |
| `coverageViewOpening(worldPosition, eye, forward, perspective, target, radius, opacity, margin)` | The see-through opening: a cone from a perspective eye, a cylinder along an orthographic view. |

A file can suggest the shadow policy with `// @coverage_shadows apply` or `keep`. The
editor sets **Cut Shadows** from it when the file is picked.

## The engine's effects

| File | Parameters | What it does |
| --- | --- | --- |
| `offsets/wind.glsl` | `windSway` (0.3), `windSwayHeight` (0); scene `Wind.velocity`, `Wind.travel` | Sways the mesh in the wind, with gusts that roll downwind. |
| `offsets/interaction.glsl` | `pushStrength` (0.5), `pushHeight` (1); scene `Interaction.position`, `Interaction.radius` (0) | Bends the mesh away from a point. |
| `coverage/see_through.glsl` | view `SeeThrough.target`, `radius` (0), `opacity` (0.3), `margin` (0.5) | Opens a view to a target behind the mesh. |
| `coverage/height_clip.glsl` | scene `Clip.height` (1000), `Clip.softness` (0) | Cuts away everything above a height. |
| `coverage/dissolve.glsl` | `dissolve` (0), `dissolveScale` (4), `dissolveEdge` (0.05) | Dissolves the mesh into world-space noise. |

### Wind

`windSway` is the bend in 10 m/s of wind, in world units. With `windSwayHeight` above 0 the
bend grows as the square of the model height up to that value, so a plant modelled with its
origin at its base keeps its foot still. The engine adds the meters of air blown past to
`Wind.travel` each update, which moves the gusts at the wind's speed without a jump when it
changes. Set the mesh's Max Offset to about
`windSway × 0.135 × the strongest wind`.

Terrain [foliage layers](terrain.md) keep their **Wind Sway** control: it runs this offset
on the layer's instances, bending them up to their tips.

```cpp
scene->setShaderParameter("Wind", "velocity", Vector3(5.0f, 0.0f, -2.0f));

grass.setVertexOffsetShader("offsets/wind.glsl");
grass.setShaderUniform("windSway", 0.3f);
grass.setShaderUniform("windSwayHeight", 0.5f);
grass.setVertexOffsetMax(0.6f);
```

```lua
scene:setShaderParameter("Wind", "velocity", Vector3(12, 0, 0)) -- a gale, until cleared
scene:clearShaderParameter("Wind", "velocity")                  -- back to the saved wind
```

### See-through

The opening is a cone from the camera to a sphere of `radius` around the target, so it keeps
one size on screen, and a cylinder along the view for an orthographic camera. It is full in
its inner half and fades out in the outer half. `opacity` is what stays at the center. Only
what lies in front of the target opens, starting `margin` before it and full at twice that,
so the ground under a character stays whole. A radius of 0 turns it off.

The engine does not track the target: a script writes it each frame. The main view values
go to whichever camera renders the scene, so a camera switch keeps the opening:

```cpp
// in a C++ script deriving from Object, attached to the player
void PlayerReveal::onUpdate(){
    Vector3 chest = getWorldPosition() + Vector3(0.0f, 0.9f, 0.0f);
    scene->setMainViewShaderParameter("SeeThrough", "target", chest);
    scene->setMainViewShaderParameter("SeeThrough", "radius", 2.5f);
    scene->setMainViewShaderParameter("SeeThrough", "margin", 0.3f);
}
```

```lua
-- the same each frame from Lua, with player an Object handle
scene:setMainViewShaderParameter("SeeThrough", "target", player:getWorldPosition() + Vector3(0, 0.9, 0))
scene:setMainViewShaderParameter("SeeThrough", "radius", 2.5)
```

With two players on split cameras, give each camera its own target:

```lua
leftCamera:setShaderParameter("SeeThrough", "target", playerOne:getWorldPosition())
rightCamera:setShaderParameter("SeeThrough", "target", playerTwo:getWorldPosition())
```

Radius, opacity and margin can also be saved on the camera in the editor, under its
**Shader Parameters**, leaving only the target to the script.

### Dissolve, height cut and push

```lua
-- fade a defeated enemy out over a second, shadow included
enemy.coverageShader = "coverage/dissolve.glsl"
enemy.coverageShadows = true
enemy:setShaderUniform("dissolve", math.min(elapsed, 1.0))

-- hide the floors above the player in every building of the scene
scene:setShaderParameter("Clip", "height", player:getWorldPosition().y + 2.5)

-- grass bends away from the player
scene:setShaderParameter("Interaction", "position", player:getWorldPosition())
scene:setShaderParameter("Interaction", "radius", 1.5)
```

## Writing your own

An effect file is a plain `.glsl` in the project. It finds its includes like a fork: first
in its own folder, then the project root, then the engine library. This one bobs a boat on
the water and sways its sail, reading a scene parameter of its own and the engine's wind:

```glsl
// Bobs the mesh on the water, with the wind on top
// @param float bob = 0.05 [0, 1] "Height of the bobbing, in world units"
// @scene float Water.level "World height of the water surface"
#include "includes/wind.glsl"

vec3 getVertexOffset(vec3 localPosition, vec3 worldPosition){
    float wave = sin(worldPosition.x * 3.0 + Engine.time * 2.0) * params.bob;
    float nearWater = step(worldPosition.y, Water.level + 0.5);
    return vec3(0.0, wave * nearWater, 0.0) + getWindSway(localPosition, worldPosition, 0.2, 1.0);
}
```

A coverage function the same way:

```glsl
// Keeps only what is above the water
// @param float edge = 0.1 [0, 1] "Height of the dithered edge"
// @scene float Water.level
// @coverage_shadows apply

float getCoverage(CoverageContext context){
    return smoothstep(Water.level - params.edge, Water.level, context.worldPosition.y);
}
```

To change an engine effect, copy it into the project (see below) and edit the copy.

### In forks

A color or depth fork runs effect functions when it keeps the lines of the built-in shader
that include `includes/vertex_offset.glsl` and `includes/coverage.glsl`, the
`loadShaderParameters()` call at the top of `main()`, and in the color fork the
`SHADER_PARAMS_FS_MEMBERS` line of its material block. The build warns when a mesh has an
effect function its fork cannot run.

A fork can declare and read parameters in its own code too, after that call, and so can a
fork of any other shader type:

```glsl
// @scene float Weather.wetness = 0 [0, 1] "How wet surfaces look"
// @param vec4 wetTint = 0.6, 0.65, 0.7, 1 color
...
color.rgb = mix(color.rgb, color.rgb * params.wetTint.rgb, Weather.wetness);
```

Every fork that declares `Weather.wetness` reads the same scene value, so one script call
can wet the meshes, the water and a post-process pass together.

## In the editor

The **Shaders** section of a Mesh component has a **Vertex Offset** row and a **Coverage**
row. Each row can create a file from a template, use one of the engine's effects (shown as
*built-in*), pick a project file, copy the built-in effect into the project to change it,
open the file, or remove it. A `.glsl` can also be dropped on the row. **Max Offset** shows
under a vertex offset and **Cut Shadows** under a coverage function.

Below the table, each fork and effect file of the component has its own **Parameters**
section with the fields its `@param` lines declare, with their ranges, colors and tooltips. A
field nobody set shows the value inherited from the scene's default shader, else the declared
default, and the arrow next to a set field drops it. The section also lists the scene and view
parameters the file reads. Saving the file updates the fields. A forked default shader shows
its fields in the scene's **Default Shaders**, where the components using it inherit them, and
a post-process pass shows them under its header.

The scene properties list every scene parameter the scene's shaders declare under
**Shader Parameters**, the wind among them once something sways, and save the values set
there. A camera's properties list the view parameters the same way. Values nothing declares
any more stay listed until their arrow removes them. Every edit is undoable.

## Export

The effect functions are part of the shader name, written `fork#vertexOffset#coverage`,
so each combination compiles to its own variant and each pass gets the variant it needs.
Saving a scene records the variants its meshes use, and an export builds and ships those,
with any project effect files and the files they include. A composition that only appears at
runtime, such as a script giving a mesh a coverage function, goes in the export overrides
like any other variant:

```text
mesh:Uv1,Puc,Nor@##coverage/dissolve.glsl
depth:Uv1@##coverage/dissolve.glsl
mesh:Uv1,Puc,Nor@shaders/myMesh#shaders/sway.glsl#coverage/see_through.glsl
```

The same specs work with `doriax-editor export --shader`. A mesh with a coverage function
and a UV set uses the `Uv1` variants of the depth and G-buffer passes.
