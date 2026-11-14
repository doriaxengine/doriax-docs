---
description: Write shader files for Doriax — hook functions that move vertices, shape the surface, remove fragments, replace the lighting or recolor UI, points, lines, the sky, water and post-process passes — with parameters, textures and varyings, run alike in every render pass.
---

# Shader Files

A **shader file** changes how something draws without replacing the engine's shaders. It
is a `.glsl` file of the project that fills **hooks**: a function that moves the vertices,
one that changes the surface before lighting, one that recolors the final pixel, and so
on. The engine calls them from its own shaders, so lighting, shadows, fog, skinning,
instancing and every [shader variant](shader-variants.md) keep working, and the depth,
shadow and G-buffer passes run the same hooks as the color pass.

A [shader graph](../editor/shader-graphs.md) (`.shader`) is the same thing drawn as
nodes: the editor turns it into a shader file and from then on nothing tells them apart.
Everything below holds for both.

## A first file

```glsl
// Waves the mesh and cuts it above a height
#pragma shader mesh

#pragma stage vertex
#pragma param float waveHeight = 0.2 [0, 2] "Height of the waves in world units"
#pragma param float waveSpeed = 2 [0, 10] "Waves per second"

// offset of each vertex, in world units
vec3 getVertexOffset(VertexContext context){
    return vec3(0.0, sin(Engine.time * params.waveSpeed + context.worldPosition.x) * params.waveHeight, 0.0);
}

#pragma stage fragment
#pragma param float cutHeight = 1000 "World height above which the mesh is cut away"
#pragma param float cutSoftness = 0.2 [0, 5] "Width of the dithered band above the cut"
#pragma coverage_shadows apply

// share of each fragment that stays, 0 to 1
float getCoverage(FragmentContext context){
    return coverageBelowHeight(context.worldPosition, params.cutHeight, params.cutSoftness);
}
```

Give it to a mesh's material (the **Shader** row of the material in Properties, or
`mesh->setShader("shaders/wave.glsl")`), and the mesh waves and is cut, in its shadow too.
The editor writes a file like this one when you create a shader from the Shader row or
the [Resources](../editor/resources.md) **New** menu, one per type.

## The format

| Line | Meaning |
| --- | --- |
| `#pragma shader <type>` | The type the file is for: `mesh`, `ui`, `points`, `lines`, `sky`, `water` or `postprocess`. The build stops when the file is given to another type. |
| `#pragma stage vertex` / `fragment` | Starts the code of that stage. What comes before the first stage line is shared by both: helpers, includes, declarations. |
| `#pragma param`, `scene`, `view` | A value the code reads, see [Declaring parameters](#declaring-parameters). |
| `#pragma param texture2D name = white linear repeat` | A texture, see [Textures](#textures). |
| `#pragma varying vec3 name` | A value the vertex stage hands to the fragment stage, see [Varyings](#varyings). |
| `#pragma shading unlit` | The mesh draws without lights, whatever the material and the scene say. |
| `#pragma surface_replaces baseColor normal` | The material's maps for those surface fields are not sampled, since `getSurface` sets them. Any of `baseColor`, `alpha`, `normal`, `metallic`, `roughness`, `occlusion`, `emissive`. |
| `#pragma coverage_shadows apply` / `keep` | Whether the shadow maps cut what the coverage hook cuts. Shadows keep the whole silhouette by default. |

A parameter declared in a stage belongs to that stage and costs uniform space and texture
slots only there. A file must define at least one hook. `#include` finds a file in the
including file's folder, then at the project root, then in the engine library, so a
shader file can call the engine's helpers and share code with other files of the project.

### Where a file goes

| Draws | Slot | Fields |
| --- | --- | --- |
| Meshes, models, sprites, tilemaps | The material, so each submesh has its own | `shader`, `shaderUniforms`, `shaderTextures` |
| UI, Points, Lines, Sky, Water | The component | `shader`, `shaderUniforms`, `shaderTextures` |
| A post-process pass | The pass | `shader`, `uniforms`, `textures` |
| Everything of a type in a scene | The scene's default shader of that type | as above |

A component without a shader of its own uses the scene default of its type, and without
one the engine's built-in shader. Terrain builds its vertices in its own shader and takes no
shader file. See [Custom Shaders](../editor/custom-shaders.md) for
the editor side.

## Mesh hooks

| Hook | Stage | Runs in |
| --- | --- | --- |
| `vec3 getVertexOffset(VertexContext context)` | vertex | every pass |
| `void getVaryings(VertexContext context, out Varyings varyings)` | vertex | every pass |
| `vec4 getClipPosition(VertexContext context, vec4 clipPosition)` | vertex | the camera passes: color, depth prepass, G-buffer; not shadow maps |
| `float getCoverage(FragmentContext context)` | fragment | every pass |
| `void getSurface(FragmentContext context, inout Surface surface)` | fragment | color and G-buffer; the depth passes run it for `surface.alpha` of a masked material, starting from the material's factors: its maps other than the base color are not sampled there |
| `vec3 getLight(FragmentContext context, Surface surface, LightContext light)` | fragment | color, once per light |
| `vec4 getColor(FragmentContext context, vec4 color)` | fragment | color, last |
| `float getDepthOffset(FragmentContext context)` | fragment | every pass but the shadow maps |

### Vertex offsets

`getVertexOffset` returns how far the vertex moves, in world units. It runs after
skinning, morph targets and instancing and before the instance distance fade.
The mesh's **Max Offset** (`vertexOffsetMax`, in the **Vertex Offset** section of the mesh) is
the longest offset: longer ones are clamped to it, and culling widens the mesh bounds and
each instance's sphere by it, so moved geometry is not cut at the screen edge or out of a
shadow cascade. At 0 nothing is clamped and the bounds stay those of the mesh data.
Lighting keeps the normals of the unmoved surface.

`getClipPosition` receives the projected position and returns it changed, after the
projection; it is the same code in every camera pass, so a depth prepass still matches the
color pass.

| `VertexContext` field | Meaning |
| --- | --- |
| `vec3 localPosition` | The vertex in the mesh's own space, after morph targets and skinning |
| `vec3 worldPosition` | Where it lands before the offset |
| `vec3 normal` | World space; (0, 1, 0) without normals |
| `vec2 uv1`, `uv2` | The UV sets as the mesh stores them; 0 without the set |
| `vec4 color` | The vertex color times the instance color; 1 without either |
| `vec4 instance` | The instance's custom value, see [Per-instance values](#per-instance-values); 0 without instancing |
| `vec3 objectPosition` | The object's origin in world space, an instance's own with instancing |
| `vec3 objectScale` | Its scale |

A field costs an attribute or a computation only in the variants whose hooks read it.

### The surface

`getSurface` changes the surface the material made, before any light reaches it. The
same code runs in the G-buffer, so screen-space reflections and SSAO see the changed
normal and roughness.

| `Surface` field | Meaning |
| --- | --- |
| `vec3 baseColor` | Linear |
| `float alpha` | |
| `vec3 normal` | World space, normal maps applied |
| `float metallic`, `roughness`, `occlusion` | |
| `vec3 emissive` | Linear |

| `FragmentContext` field | Meaning |
| --- | --- |
| `vec3 worldPosition` | The fragment in world space |
| `vec3 normal` | World space, facing the viewer; (0, 1, 0) without normals |
| `vec3 tangent`, `bitangent` | World space, along the first UV set's u and v: the mesh's tangents, or derived from the UVs without them, as the material's normal map uses |
| `vec2 uv1`, `uv2` | As the mesh stores them |
| `vec4 color`, `instance` | As in the vertex stage |
| `vec3 view` | Unit vector to the eye |
| `vec3 eye`, `forward` | The camera's position and view direction |
| `bool perspective` | False for an orthographic camera |
| `vec2 pixel` | The pixel counted from a corner every pass shares |
| `vec2 screenUV` | Where the fragment is in the camera's view, 0 at the top left |
| `bool frontFacing` | |
| `float nearPlane`, `farPlane` | The camera's clip planes, as distances from the eye; 0 in shadow maps |
| `mat3 worldToView` | Turns a world direction into the camera's space, z toward the eye |

### Coverage

`getCoverage` returns how much of the fragment stays: 1 keeps it and 0 removes it. In
between, opaque and alpha-tested surfaces keep a steady 4×4 dithered share of their
pixels, and blended surfaces multiply their alpha instead. The coverage and the
material's alpha test are separate tests that both have to pass. The depth prepass and
the G-buffer cut what the color pass cuts, so SSAO, reflections and depth-based
post-processing match it; the shadow maps cut it too with `#pragma coverage_shadows
apply`.

Every mesh shader file sees the shapes of `includes/coverage_helpers.glsl`:

| Helper | Returns |
| --- | --- |
| `coverageBelowHeight(worldPosition, height, softness)` | 1 below the height, 0 above, with a dithered band of the given width |
| `coverageNoise(position)` | A smooth value noise in [0, 1] |
| `coverageViewOpening(worldPosition, eye, forward, perspective, target, radius, opacity, margin)` | The see-through opening: a cone from a perspective eye, a cylinder along an orthographic view |
| `coverageDitherThreshold(pixel)` | The 4×4 pattern the coverage compares against, 0 to 1 |

### Lighting and the final color

`getLight` replaces the engine's shading of one light: it returns what that light adds,
and the engine adds the results of all lights. Ambient light, reflections and emission stay
the engine's, physically based. The engine's own diffuse term is the base color over π
times the light and N·L, so divide by 3.14 for the same brightness.

| `LightContext` field | Meaning |
| --- | --- |
| `vec3 direction` | From the surface to the light |
| `vec3 color` | Color times intensity times attenuation, linear |
| `float shadow` | 1 lit, 0 in shadow |
| `int type` | `LIGHT_DIRECTIONAL`, `LIGHT_POINT` or `LIGHT_SPOT` |

```glsl
#pragma shader mesh
#pragma stage fragment

// two bands of light, as a toon shader
vec3 getLight(FragmentContext context, Surface surface, LightContext light){
    float lit = step(0.3, max(dot(surface.normal, light.direction), 0.0) * light.shadow);
    return surface.baseColor * light.color * (0.35 + 0.65 * lit);
}
```

`getColor` receives the final linear color, after lighting and fog, and returns it
changed. `getDepthOffset` pushes the fragment's depth away from the eye by the distance it
returns, in every pass but the shadow maps.

### Scene color and depth

A mesh's fragment hooks can read what was drawn before it:

| Function | Returns |
| --- | --- |
| `vec4 sceneColor(vec2 screenUV)` | The scene behind the mesh, linear: in 3D its opaque part, in 2D everything drawn before it |
| `float sceneDepth(vec2 screenUV)` | The distance from the eye along the view to what is drawn behind, in world units |

A mesh that calls them draws with the transparent ones, after the scene it reads, and
stays out of the depth prepass and the G-buffer; its other passes read black and a far
distance. The engine copies the scene for the first such mesh and again only when a water
drew in between, so a glass pane and the river behind it both see the river.
`sceneDepth` compares with `dot(context.worldPosition - context.eye, context.forward)`,
the fragment's own distance, and `context.screenUV` is where the fragment itself is:

```glsl
#pragma shader mesh
#pragma stage fragment
#pragma param float strength = 0.03 [0, 0.2] "How far the glass bends what is behind it"

vec4 getColor(FragmentContext context, vec4 color){
    vec4 behind = sceneColor(context.screenUV + context.normal.xy * params.strength);
    return vec4(mix(behind.rgb, color.rgb, color.a), 1.0);
}
```

### Per-instance values

Each instance of an instanced mesh carries a `vec4` of its own, read as
`context.instance` in both stages, for a color, a growth stage or a random seed per
instance. Set it with `Mesh::setInstanceCustom(index, value)` or the instanced mesh's
`instances[N].custom` property. It travels in the instance matrix's spare row, so it costs
no attribute.

### Pass information

`Engine.pass` is the pass being drawn, `PASS_COLOR`, `PASS_DEPTH`, `PASS_SHADOW` or
`PASS_GBUFFER`, and each pass also defines `IN_COLOR_PASS`, `IN_DEPTH_PASS` or
`IN_GBUFFER_PASS` for code that should not be compiled elsewhere at all.

## UI, points and lines

| Hook | Stage |
| --- | --- |
| `vec3 getVertexOffset(VertexContext context)` | vertex, offset in world units |
| `vec4 getColor(FragmentContext context, vec4 color)` | fragment, the linear color the engine would write |

| `FragmentContext` field | Meaning |
| --- | --- |
| `vec3 worldPosition` | |
| `vec2 uv1` | A point's coordinate after its rotation and texture rect; 0 on lines |
| `vec4 color` | The vertex color, 1 without |
| `vec4 textureColor` | The texture or font sample, linear; 1 without a texture |
| `vec4 tint` | The UI color, 1 on points and lines |
| `vec2 pixel` | |

## Sky

`vec4 getColor(FragmentContext context, vec4 color)` receives the sky color, the cube
map sample times the sky's color, linear.

| `FragmentContext` field | Meaning |
| --- | --- |
| `vec3 direction` | Of the cube map, in the sky's own space |
| `vec4 textureColor` | The cube map sample, linear |
| `vec4 tint` | The sky's color, linear |
| `vec2 pixel` | |

## Water

One file fills both hooks of a water: `vec4 getColor(FragmentContext context, vec4
color)` on the surface, and `vec4 getUnderwaterColor(UnderwaterContext context, vec4
color)` on the fade a camera below the surface sees.

| `FragmentContext` field | Meaning |
| --- | --- |
| `vec3 worldPosition` | |
| `vec3 normal` | The rippled surface, world space |
| `vec3 view` | Toward the eye |
| `vec2 pixel` | |

| `UnderwaterContext` field | Meaning |
| --- | --- |
| `vec2 uv` | Of the view, 0 at the top left |
| `vec4 sceneColor` | What the camera sees before the fade, linear |
| `float pathLength` | Water the view crosses, in world units |
| `vec2 pixel` | |

## Post-process

A post-process pass runs `vec4 getColor(FragmentContext context, vec4 color)` over the
finished image of a scene, where `color` is the previous pass at this pixel. Its
`FragmentContext` has `vec2 uv` (0 at the top left) and `vec2 pixel`, and it can call:

| Function | Returns |
| --- | --- |
| `vec4 sceneColor(vec2 uv)` | The previous pass, linear |
| `float sceneDepth(vec2 uv)` | Distance from the eye in world units, the far plane where nothing was drawn |
| `vec3 sceneNormal(vec2 uv)` | World space, from the G-buffer that screen-space reflections draw; needs SSR on |
| `float sceneOcclusion(vec2 uv)` | SSAO, 1 without it |

An input is bound only when the file calls its function.

```glsl
// Grays the image, more toward the edges
#pragma shader postprocess
#pragma stage fragment
#pragma param float amount = 0.8 [0, 1] "How gray the image gets"

vec4 getColor(FragmentContext context, vec4 color){
    float gray = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
    float edge = smoothstep(0.2, 0.8, length(context.uv - 0.5) * 1.4);
    return vec4(mix(color.rgb, vec3(gray), params.amount * edge), color.a);
}
```

## Declaring parameters

Parameters are values a file reads that belong to the object, to the scene or to a
camera:

```glsl
#pragma param float strength = 0.5 [0, 2] "How far the top moves, in world units"
#pragma param vec4 tint = 1, 0.8, 0.6, 1 color
#pragma scene vec3 Wind.velocity "Air velocity in m/s"
#pragma view float SeeThrough.radius = 0 [0, 20]
```

The type is `float`, `vec2`, `vec3`, `vec4`, `int`, `ivec2`, `ivec3` or `ivec4`. The
numbers after `=` are the default, and a single number fills a whole vector. Integer
types travel as floats and are exact up to 16777216. `[min, max]` is the range of the
inspector field, `color` shows a color picker, `runtime` marks a value that a script or
the engine writes (the inspector shows it read-only), and the quoted text is the tooltip.

| Declared as | Read in GLSL as | Set on |
| --- | --- | --- |
| `#pragma param float strength` | `params.strength` | The material, the component or the pass: `setShaderUniform` |
| `#pragma scene vec3 Wind.velocity` | `Wind.velocity` | The scene: its properties, `Scene::setShaderParameter` |
| `#pragma view float SeeThrough.radius` | `SeeThrough.radius` | A camera: its properties, `Camera::setShaderParameter` |

The collection keeps unrelated values apart: `Wind.speed` and `Water.speed` are two
parameters. A collection is either a scene or a view one. The build stops with an error
that names the file and line when two declarations give a parameter different types, or
use a collection in both scopes. Changing a value rewrites a uniform block at the next
draw; it never rebuilds a shader.

### Textures

```glsl
#pragma param texture2D detail = white linear repeat "Detail map"
#pragma param textureCube environment = black linear clamp
```

The default is `white`, `black` or `normal`, the filter `nearest`, `linear` or
`trilinear` (which builds the texture's mipmaps), and the wrap `repeat`, `clamp` or
`mirror`. The code reads the texture by
its name, as GLSL does: `texture(detail, uv)`, `textureLod(detail, uv, 0.0)`. Helpers of
your own take it as `detail_texture` and `detail_sampler`, the two halves the name stands
for, so the name cannot be a word the file uses otherwise. A texture is bound in every
pass that declares it; textures that share a filter and a wrap share one sampler, so a
file's textures cost one or two samplers. Set one from the editor's texture fields, with
`setShaderTexture(name, texture)`, or from a camera's render target.

### Engine values

Three values need no declaration. A shader that reads them gets them:

| Value | Contents |
| --- | --- |
| `Engine.time` | Seconds since the scene started. The clock holds while the editor scene is stopped or paused, and while the game pauses, and starts over when Play mode stops, so each Play session begins like the exported game. For gameplay-driven time, set a parameter of your own from a script. |
| `Engine.resolution` | `xy` = width and height of the target the shader draws into, `zw` = `1 / width` and `1 / height` |
| `Engine.pass` | The pass being drawn, see [Pass information](#pass-information) |

### Where values come from

An **object parameter** reads the value set on its material, component or pass, then the
value of the scene default shader when the component inherits it, then the declared
default.

A **scene parameter** reads the runtime value a script set, then the value saved with the
scene, then the declared default.

A **view parameter** reads, for the camera a pass is drawn for:

1. the runtime value of that camera, from `Camera::setShaderParameter`;
2. the runtime value of the main view, from `Scene::setMainViewShaderParameter`, while
   that camera renders the scene;
3. the value saved on its Camera component;
4. the declared default.

Runtime values are never saved: stopping Play mode or loading the scene again brings back
the saved ones. Shadow maps are fitted to the camera that renders the scene, so a shader
sees that camera there. A reflection probe capture has no camera and reads the declared
defaults of view parameters.

## Varyings

```glsl
#pragma shader mesh
#pragma varying float height

#pragma stage vertex
void getVaryings(VertexContext context, out Varyings varyings){
    varyings.height = context.localPosition.y;
}

#pragma stage fragment
void getSurface(FragmentContext context, inout Surface surface){
    surface.baseColor *= mix(0.6, 1.0, clamp(varyings.height, 0.0, 1.0));
}
```

A varying is a `float` or `vec2`–`vec4`, written by `getVaryings` and read in the
fragment hooks as `varyings.name`. A file takes at most four, packed by the builder.

## The engine's shader files

The engine ships five mesh shader files under `shaders/`. The Shader row lists them for
a material, and its copy button puts one into the project to change it. Each calls a
function of `effects/`, which a file of your own can call too, to combine them:

| File | Parameters | What it does |
| --- | --- | --- |
| `shaders/wind.glsl` | `windSway` (0.3), `windSwayHeight` (0); scene `Wind.velocity`, `Wind.travel` | Sways the mesh in the wind, with gusts that roll downwind; `windSway(localPosition, worldPosition, sway, swayHeight)` |
| `shaders/interaction.glsl` | `pushStrength` (0.5), `pushHeight` (1); scene `Interaction.position`, `Interaction.radius` (0) | Bends the mesh away from a point; `interactionPush(localPosition, worldPosition, strength, height)` |
| `shaders/see_through.glsl` | view `SeeThrough.target`, `radius` (0), `opacity` (0.3), `margin` (0.5) | Opens a view to a target behind the mesh; `seeThrough(context)` |
| `shaders/height_clip.glsl` | scene `Clip.height` (1000), `Clip.softness` (0) | Cuts away everything above a height; `heightClip(worldPosition)` |
| `shaders/dissolve.glsl` | `dissolve` (0), `dissolveScale` (4), `dissolveEdge` (0.05) | Dissolves the mesh into world-space noise; `dissolve(worldPosition, amount, scale, edge)` |

```glsl
// Sways in the wind and is pushed aside by the player
#pragma shader mesh
#pragma stage vertex
#include "effects/wind.glsl"
#include "effects/interaction.glsl"

vec3 getVertexOffset(VertexContext context){
    return windSway(context.localPosition, context.worldPosition, 0.3, 1.0) +
           interactionPush(context.localPosition, context.worldPosition, 0.6, 1.0);
}
```

### Wind

`windSway` is the bend in 10 m/s of wind, in world units. With `windSwayHeight` above 0
the bend grows as the square of the model height up to that value, so a plant modelled
with its origin at its base keeps its foot still. The engine adds the meters of air blown
past to `Wind.travel` each update, which moves the gusts at the wind's speed without a
jump when it changes. Set the mesh's Max Offset to about `windSway × 2.5` for winds up to
15 m/s, or `windSway × 4` up to 20 m/s. Terrain [foliage layers](terrain.md) keep their
**Wind Sway** control: it runs this file on the layer's instances.

```cpp
scene->setShaderParameter("Wind", "velocity", Vector3(5.0f, 0.0f, -2.0f));

grass.setShader("shaders/wind.glsl");
grass.setShaderUniform("windSway", 0.3f);
grass.setShaderUniform("windSwayHeight", 0.5f);
grass.setVertexOffsetMax(0.8f);
```

```lua
scene:setShaderParameter("Wind", "velocity", Vector3(12, 0, 0)) -- a gale, until cleared
scene:clearShaderParameter("Wind", "velocity")                  -- back to the saved wind
```

### See-through

The opening is a cone from the camera to a sphere of `radius` around the target, so it
keeps one size on screen, and a cylinder along the view for an orthographic camera. It is
full in its inner half and fades out in the outer half. `opacity` is what stays at the
center. Only what lies in front of the target opens, starting `margin` before it and full
at twice that, so the ground under a character stays whole. A radius of 0 turns it off.

The engine does not track the target: a script writes it each frame. The main view values
go to whichever camera renders the scene, so a camera switch keeps the opening:

```lua
scene:setMainViewShaderParameter("SeeThrough", "target", player:getWorldPosition() + Vector3(0, 0.9, 0))
scene:setMainViewShaderParameter("SeeThrough", "radius", 2.5)
```

With two players on split cameras, give each camera its own target with
`camera:setShaderParameter("SeeThrough", "target", ...)`.

### Dissolve, height cut and push

```lua
-- fade a defeated enemy out over a second, shadow included
enemy:setShader("shaders/dissolve.glsl")
enemy:setShaderUniform("dissolve", math.min(elapsed, 1.0))

-- hide the floors above the player in every building of the scene
scene:setShaderParameter("Clip", "height", player:getWorldPosition().y + 2.5)

-- grass bends away from the player
scene:setShaderParameter("Interaction", "position", player:getWorldPosition())
scene:setShaderParameter("Interaction", "radius", 1.5)
```

## In the editor

The Shader row of a material, a component, a scene default or a post-process pass makes,
picks, opens and removes shader files, and lists the engine's; below it, the file's
**Parameters** show the fields its `#pragma param` lines declare, with their ranges,
colors and tooltips. Saving a file rebuilds every shader that uses it, and the parameter
fields follow. The scene properties list the scene parameters its shaders declare, and a
camera's properties its view parameters. See [Custom Shaders](../editor/custom-shaders.md).

## Limits

Each compiled variant must fit the backends' limits, which the builder checks, naming the
variant and the count when one is passed: 16 textures and 16 samplers per stage, 8 uniform
blocks per stage outside OpenGL, and 15 varyings on WebGL 2. A shader file adds at most
one or two samplers and four varyings to what the engine uses.

Sprites drawing with one shader file share a draw call while its hooks read only what
stays the same once they are batched in world space: not the local position, the
object's position or scale, or the normal. See
[Sprite batching](rendering-pipeline.md#sprite-batching) for the rest.

## Export

Saving a scene records the shader variants its components use, and an export compiles
those for every backend and ships them; the games carry no shader compiler. A shader that
only appears at runtime, such as a script giving a mesh `shaders/dissolve.glsl`, goes in
the export overrides like any other variant, the file after `@`:

```text
mesh:Uv1,Puc,Nor@shaders/dissolve.glsl
depth:Uv1@shaders/dissolve.glsl
```

The same specs work with `doriax-editor export --shader`.
