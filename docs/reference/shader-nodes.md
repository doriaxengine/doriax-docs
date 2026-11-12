---
description: Every node of Doriax shader graphs, with its pins, settings, the shader types it fits and the stage it runs in.
---

# Shader Graph Nodes

The nodes a [shader graph](../editor/shader-graphs.md) is built from, generated from the
editor's catalogue (`doriax-editor shader-nodes`). The MCP tool `list_graph_node_types`
answers from the same catalogue.

Pin types:

| Type | Holds |
| --- | --- |
| `float`, `vec2`, `vec3`, `vec4` | Numbers. A float fills every component of a vector, a vector feeds a shorter one with its first components, and a `vec3` feeds a `vec4` with w 0. Other pairs, such as a vector into a float, go through Split or Combine |
| `color` | A `vec4`; a `vec3` feeding it gets alpha 1 |
| `int`, `bool` | An int takes a float, cut to an integer. A bool takes only a bool, which Compare makes |
| `texture2D`, `textureCube` | A texture parameter, named by a node's Texture setting rather than linked |
| `dynamic` | A float or vector that takes the smallest vector linked into the node's dynamic inputs, as Multiply does |

An input that nothing feeds takes its constant, set in the inspector, or its default. A
default such as `uv1` reads that field of the hook's context, as the matching Input node
would. Where a node runs: *any* runs in the stage that reads it; *vertex* and *fragment*
nodes only in that stage. A vertex value read by fragment nodes reaches them through a
varying the graph adds. A [function](../editor/shader-graphs.md#functions) takes every node,
and the graph that calls it decides where each runs.

## Output

### Mesh Output

`output/mesh` · mesh

What the mesh's material draws with.

| Input | Type | Fills |
| --- | --- | --- |
| Vertex Offset (`vertexOffset`) | vec3 | `getVertexOffset`, its return value |
| Base Color (`baseColor`) | vec3 | `getSurface`, `surface.baseColor` |
| Alpha (`alpha`) | float | `getSurface`, `surface.alpha` |
| Normal (`normal`) | vec3 | `getSurface`, `surface.normal` |
| Metallic (`metallic`) | float | `getSurface`, `surface.metallic` |
| Roughness (`roughness`) | float | `getSurface`, `surface.roughness` |
| Occlusion (`occlusion`) | float | `getSurface`, `surface.occlusion` |
| Emissive (`emissive`) | vec3 | `getSurface`, `surface.emissive` |
| Coverage (`coverage`) | float | `getCoverage`, its return value |
| Depth Offset (`depthOffset`) | float | `getDepthOffset`, its return value |
| Final Color (`color`) | color | `getColor`, its return value |

### UI Output

`output/ui` · ui

What a UI component draws with.

| Input | Type | Fills |
| --- | --- | --- |
| Vertex Offset (`vertexOffset`) | vec3 | `getVertexOffset`, its return value |
| Color (`color`) | color | `getColor`, its return value |

### Points Output

`output/points` · points

What a Points component draws with.

| Input | Type | Fills |
| --- | --- | --- |
| Vertex Offset (`vertexOffset`) | vec3 | `getVertexOffset`, its return value |
| Color (`color`) | color | `getColor`, its return value |

### Lines Output

`output/lines` · lines

What a Lines component draws with.

| Input | Type | Fills |
| --- | --- | --- |
| Vertex Offset (`vertexOffset`) | vec3 | `getVertexOffset`, its return value |
| Color (`color`) | color | `getColor`, its return value |

### Sky Output

`output/sky` · sky

The sky's color.

| Input | Type | Fills |
| --- | --- | --- |
| Color (`color`) | color | `getColor`, its return value |

### Water Output

`output/water` · water

The water's color, and what a camera below its surface sees.

| Input | Type | Fills |
| --- | --- | --- |
| Color (`color`) | color | `getColor`, its return value |
| Underwater Color (`underwaterColor`) | color | `getUnderwaterColor`, its return value |

### Post-process Output

`output/postprocess` · postprocess

The color of the pass.

| Input | Type | Fills |
| --- | --- | --- |
| Color (`color`) | color | `getColor`, its return value |

## Input

### UV

`input/uv` · any stage · mesh, ui, points, lines

A UV set as the mesh stores it.

| Output | Type |
| --- | --- |
| UV (`uv`) | vec2 |

| Setting | Takes | Default |
| --- | --- | --- |
| Set (`set`) | one of `1`, `2` | 1 |

### Position

`input/position` · any stage · mesh, ui, points, lines, water

The fragment's or vertex's position.

| Output | Type |
| --- | --- |
| Position (`position`) | vec3 |

| Setting | Takes | Default |
| --- | --- | --- |
| Space (`space`) | one of `world`, `local` | world |

### Normal

`input/normal` · any stage · mesh, water

The world normal, facing the viewer.

| Output | Type |
| --- | --- |
| Normal (`normal`) | vec3 |

### Tangent

`input/tangent` · any stage · mesh

The world tangent frame, along the UV set's u and v.

| Output | Type |
| --- | --- |
| Tangent (`tangent`) | vec3 |
| Bitangent (`bitangent`) | vec3 |

### Vertex Color

`input/vertexColor` · any stage · mesh, ui, points, lines

The vertex color times the instance color.

| Output | Type |
| --- | --- |
| Color (`color`) | vec4 |

### View Direction

`input/viewDirection` · any stage · mesh, water

Unit vector from the surface to the eye.

| Output | Type |
| --- | --- |
| View (`view`) | vec3 |

### Camera

`input/camera` · any stage · mesh

The camera's position and forward axis, whether it is orthographic, and its clip planes as distances.

| Output | Type |
| --- | --- |
| Position (`position`) | vec3 |
| Forward (`forward`) | vec3 |
| Orthographic (`orthographic`) | float |
| Near (`near`) | float |
| Far (`far`) | float |

### Object

`input/object` · any stage · mesh

Where the object is in the world, and its scale; an instance's own with instancing.

| Output | Type |
| --- | --- |
| Position (`position`) | vec3 |
| Scale (`scale`) | vec3 |

### Screen Position

`input/screen` · any stage · every type

Where the fragment is in the view, 0 at the top left, and its pixel.

| Output | Type |
| --- | --- |
| UV (`uv`) | vec2 |
| Pixel (`pixel`) | vec2 |

### Time

`input/time` · any stage · every type

Seconds of the scene clock.

| Output | Type |
| --- | --- |
| Time (`time`) | float |

### Resolution

`input/resolution` · any stage · every type

The target's size in pixels, and one over it.

| Output | Type |
| --- | --- |
| Size (`size`) | vec2 |
| Texel (`texel`) | vec2 |

### Instance

`input/instance` · any stage · mesh

The instance's custom value, set per instance.

| Output | Type |
| --- | --- |
| Value (`value`) | vec4 |

### Front Facing

`input/frontFacing` · fragment stage · mesh

Whether the fragment is on a front face.

| Output | Type |
| --- | --- |
| Front Facing (`frontFacing`) | bool |

### Material

`input/material` · any stage · mesh

The surface the material gives, before this graph changes it.

| Output | Type |
| --- | --- |
| Base Color (`baseColor`) | vec3 |
| Alpha (`alpha`) | float |
| Normal (`normal`) | vec3 |
| Metallic (`metallic`) | float |
| Roughness (`roughness`) | float |
| Occlusion (`occlusion`) | float |
| Emissive (`emissive`) | vec3 |

### Built-in Color

`input/color` · any stage · every type

The color the engine would draw, linear.

| Output | Type |
| --- | --- |
| Color (`color`) | vec4 |

### Built-in Texture

`input/texture` · any stage · ui, points, lines, sky

The texture sample and the tint the engine multiplies, linear.

| Output | Type |
| --- | --- |
| Texture Color (`color`) | vec4 |
| Tint (`tint`) | vec4 |

### Sky Direction

`input/skyDirection` · any stage · sky

The cube map direction, in the sky's own space.

| Output | Type |
| --- | --- |
| Direction (`direction`) | vec3 |

### Underwater

`input/underwater` · any stage · water

The scene before the fade, and the water the view crosses.

| Output | Type |
| --- | --- |
| Scene Color (`sceneColor`) | vec4 |
| Path Length (`pathLength`) | float |

## Scene

### Scene Color

`scene/color` · fragment stage · mesh, postprocess

What is drawn behind, linear; a mesh reading it draws after the opaque scene.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | screenUV |

| Output | Type |
| --- | --- |
| Color (`color`) | vec4 |

### Scene Depth

`scene/depth` · fragment stage · mesh, postprocess

Distance from the eye along the view to what is drawn behind, in world units.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | screenUV |

| Output | Type |
| --- | --- |
| Depth (`depth`) | float |

### Scene Normal

`scene/normal` · fragment stage · postprocess

World normal of what is drawn, needs SSR on.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | screenUV |

| Output | Type |
| --- | --- |
| Normal (`normal`) | vec3 |

### Scene Occlusion

`scene/occlusion` · fragment stage · postprocess

SSAO, 1 without it.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | screenUV |

| Output | Type |
| --- | --- |
| Occlusion (`occlusion`) | float |

## Parameter

### Parameter

`parameter` · any stage · every type

A value of the graph, shown in Properties.

| Output | Type |
| --- | --- |
| Out (`out`) | the parameter's |

| Setting | Takes | Default |
| --- | --- | --- |
| Parameter (`parameter`) | a `float` or `vec2` or `vec3` or `vec4` or `int` or `color` parameter |  |

### Scene Parameter

`parameter/scene` · any stage · every type

A value the whole scene shares, set with set_scene_property shader_parameter:Collection.name.

| Output | Type |
| --- | --- |
| Out (`out`) | the parameter's |

| Setting | Takes | Default |
| --- | --- | --- |
| Type (`valueType`) | one of `float`, `vec2`, `vec3`, `vec4` | float |
| Collection (`collection`) | text |  |
| Name (`name`) | text |  |

### View Parameter

`parameter/view` · any stage · every type

A value each camera sets, for a camera's shader_parameter:Collection.name.

| Output | Type |
| --- | --- |
| Out (`out`) | the parameter's |

| Setting | Takes | Default |
| --- | --- | --- |
| Type (`valueType`) | one of `float`, `vec2`, `vec3`, `vec4` | float |
| Collection (`collection`) | text |  |
| Name (`name`) | text |  |

### Float

`constant/float` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | float |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 0 |

### Vector 2

`constant/vec2` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 0, 0 |

### Vector 3

`constant/vec3` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 0, 0, 0 |

### Vector 4

`constant/vec4` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | vec4 |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 0, 0, 0, 0 |

### Color

`constant/color` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | color |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 1, 1, 1, 1 |

### Integer

`constant/int` · any stage · every type

A fixed value.

| Output | Type |
| --- | --- |
| Out (`out`) | int |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | a number | 0 |

### Boolean

`constant/bool` · any stage · every type

True or false.

| Output | Type |
| --- | --- |
| Out (`out`) | bool |

| Setting | Takes | Default |
| --- | --- | --- |
| Value (`value`) | one of `true`, `false` | true |

## Math

### Add

`math/add` · any stage · every type

A plus B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Subtract

`math/subtract` · any stage · every type

A minus B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Multiply

`math/multiply` · any stage · every type

A times B, component by component.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 1 |
| B (`b`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Divide

`math/divide` · any stage · every type

A over B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 1 |
| B (`b`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Modulo

`math/mod` · any stage · every type

The remainder of A over B, with B's sign.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Minimum

`math/min` · any stage · every type

The smaller of A and B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Maximum

`math/max` · any stage · every type

The larger of A and B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Power

`math/power` · any stage · every type

A to the power of B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 1 |
| B (`b`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Step

`math/step` · any stage · every type

1 where B reaches A, else 0.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Arctangent 2

`math/atan2` · any stage · every type

The angle of the point (B, A), in radians.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Negate

`math/negate` · any stage · every type

Minus the input.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Absolute

`math/abs` · any stage · every type

The input without its sign.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Sign

`math/sign` · any stage · every type

-1, 0 or 1.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Floor

`math/floor` · any stage · every type

Rounded down.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Ceiling

`math/ceil` · any stage · every type

Rounded up.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Round

`math/round` · any stage · every type

Rounded to the nearest whole number.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Fraction

`math/fract` · any stage · every type

The part after the point.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Saturate

`math/saturate` · any stage · every type

Clamped to 0 to 1.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### One Minus

`math/oneMinus` · any stage · every type

1 minus the input.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Reciprocal

`math/reciprocal` · any stage · every type

1 over the input.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Square Root

`math/sqrt` · any stage · every type

The square root.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Exponential

`math/exp` · any stage · every type

e to the input.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Logarithm

`math/log` · any stage · every type

The natural logarithm.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Sine

`math/sin` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Cosine

`math/cos` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Tangent

`math/tan` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Arcsine

`math/asin` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Arccosine

`math/acos` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Arctangent

`math/atan` · any stage · every type

In radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### DDX

`math/ddx` · fragment stage · every type

How fast the input changes across the screen, horizontally.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### DDY

`math/ddy` · fragment stage · every type

How fast the input changes across the screen, vertically.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Fwidth

`math/fwidth` · fragment stage · every type

The sum of DDX and DDY, without their signs.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Clamp

`math/clamp` · any stage · every type

The input kept between Min and Max.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |
| Min (`min`) | dynamic | 0 |
| Max (`max`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Lerp

`math/lerp` · any stage · every type

A when T is 0, B when T is 1.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 1 |
| T (`t`) | dynamic | 0.5 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Smoothstep

`math/smoothstep` · any stage · every type

0 below Edge 1, 1 above Edge 2, a smooth curve between.

| Input | Type | Default |
| --- | --- | --- |
| Edge 1 (`edge1`) | dynamic | 0 |
| Edge 2 (`edge2`) | dynamic | 1 |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Remap

`math/remap` · any stage · every type

The input moved from one range to another.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |
| From Min (`fromMin`) | dynamic | 0 |
| From Max (`fromMax`) | dynamic | 1 |
| To Min (`toMin`) | dynamic | 0 |
| To Max (`toMax`) | dynamic | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

## Vector

### Dot Product

`vector/dot` · any stage · every type

The sum of A times B, component by component.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Cross Product

`vector/cross` · any stage · every type

A vector square to A and B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | vec3 | 1, 0, 0 |
| B (`b`) | vec3 | 0, 1, 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Length

`vector/length` · any stage · every type

How long the vector is.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Distance

`vector/distance` · any stage · every type

How far A is from B.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | dynamic | 0 |
| B (`b`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Normalize

`vector/normalize` · any stage · every type

The vector at length 1.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Reflect

`vector/reflect` · any stage · every type

The input bounced off a surface with that normal.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Normal (`normal`) | vec3 | normal |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Refract

`vector/refract` · any stage · every type

The input bent through a surface, with the ratio of the indices of refraction.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Normal (`normal`) | vec3 | normal |
| Ratio (`ratio`) | float | 0.75 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Fresnel

`vector/fresnel` · any stage · every type

Brighter where the surface turns away from the eye.

| Input | Type | Default |
| --- | --- | --- |
| Normal (`normal`) | vec3 | normal |
| View (`view`) | vec3 | view |
| Power (`power`) | float | 5 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Rotate About Axis

`vector/rotateAboutAxis` · any stage · every type

The vector turned around an axis, angle in radians.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Axis (`axis`) | vec3 | 0, 1, 0 |
| Angle (`angle`) | float | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Split

`vector/split` · any stage · every type

The components of a vector.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec4 |  |

| Output | Type |
| --- | --- |
| X (`x`) | float |
| Y (`y`) | float |
| Z (`z`) | float |
| W (`w`) | float |

### Combine

`vector/combine` · any stage · every type

A vector made of components.

| Input | Type | Default |
| --- | --- | --- |
| X (`x`) | float | 0 |
| Y (`y`) | float | 0 |
| Z (`z`) | float | 0 |
| W (`w`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec4 |
| XYZ (`xyz`) | vec3 |
| XY (`xy`) | vec2 |

### Transform

`vector/transform` · fragment stage · mesh

A direction taken from one space to another: world, tangent or view.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 | 0, 0, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

| Setting | Takes | Default |
| --- | --- | --- |
| Spaces (`spaces`) | one of `tangentToWorld`, `worldToTangent`, `worldToView`, `viewToWorld`, `tangentToView`, `viewToTangent` | tangentToWorld |

### Swizzle

`vector/swizzle` · any stage · every type

Components picked and reordered, as zyx or xxy.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec4 |  |

| Output | Type |
| --- | --- |
| Out (`out`) | as long as the mask |

| Setting | Takes | Default |
| --- | --- | --- |
| Mask (`mask`) | text | xyz |

## Color

### sRGB to Linear

`color/srgbToLinear` · any stage · every type

From the gamma of an image to the linear values lighting uses.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec4 | 1, 1, 1, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec4 |

### Linear to sRGB

`color/linearToSrgb` · any stage · every type

From linear values to the gamma of an image.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec4 | 1, 1, 1, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec4 |

### Luminance

`color/luminance` · any stage · every type

How bright the color looks.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### RGB to HSV

`color/rgbToHsv` · any stage · every type

Hue, saturation and value, each 0 to 1.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### HSV to RGB

`color/hsvToRgb` · any stage · every type

From hue, saturation and value.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Hue Shift

`color/hueShift` · any stage · every type

The hue turned by Shift, 1 is a full turn.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Shift (`shift`) | float | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Saturation

`color/saturation` · any stage · every type

0 is gray, 1 keeps the color, more is stronger.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Amount (`amount`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Contrast

`color/contrast` · any stage · every type

Spread away from mid gray, 1 keeps the color.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 |  |
| Amount (`amount`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Posterize

`color/posterize` · any stage · every type

Cut into that many steps.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |
| Steps (`steps`) | dynamic | 4 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Blend

`color/blend` · any stage · every type

B over A, by Opacity, as a layer mode.

| Input | Type | Default |
| --- | --- | --- |
| Base (`a`) | vec3 |  |
| Blend (`b`) | vec3 |  |
| Opacity (`opacity`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

| Setting | Takes | Default |
| --- | --- | --- |
| Mode (`mode`) | one of `multiply`, `screen`, `overlay`, `add`, `subtract`, `lighten`, `darken` | multiply |

### Gradient

`color/gradient` · any stage · every type

Color 1 at 0 to Color 2 at 1.

| Input | Type | Default |
| --- | --- | --- |
| T (`t`) | float | 0 |
| Color 1 (`color1`) | color | 0, 0, 0, 1 |
| Color 2 (`color2`) | color | 1, 1, 1, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec4 |

## UV

### Tiling and Offset

`uv/tilingOffset` · any stage · every type

UV times Tiling, plus Offset.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Tiling (`tiling`) | vec2 | 1, 1 |
| Offset (`offset`) | vec2 | 0, 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Rotate UV

`uv/rotate` · any stage · every type

UV turned around Center, in radians.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Center (`center`) | vec2 | 0.5, 0.5 |
| Angle (`angle`) | float | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Panner

`uv/panner` · any stage · every type

UV moving at Speed over Time.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Speed (`speed`) | vec2 | 0.10000000149011612, 0 |
| Time (`time`) | float | Engine.time |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Polar

`uv/polar` · any stage · every type

Distance from Center and angle around it, 0 to 1.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Center (`center`) | vec2 | 0.5, 0.5 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Twirl

`uv/twirl` · any stage · every type

UV turned more the farther it is from Center.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Center (`center`) | vec2 | 0.5, 0.5 |
| Strength (`strength`) | float | 10 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Flipbook

`uv/flipbook` · any stage · every type

The tile of a sheet for a frame, left to right, top to bottom.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Columns (`columns`) | float | 4 |
| Rows (`rows`) | float | 4 |
| Frame (`frame`) | float | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec2 |

### Parallax

`uv/parallax` · fragment stage · mesh

UV moved by a height map as the view slants, so a flat surface looks deep. White in the map is high.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Scale (`scale`) | float | 0.05000000074505806 |
| Steps (`steps`) | float | 12 |

| Output | Type |
| --- | --- |
| UV (`uv`) | vec2 |

| Setting | Takes | Default |
| --- | --- | --- |
| Height Map (`texture`) | a `texture2D` parameter |  |

## Texture

### Sample Texture 2D

`texture/sample2D` · any stage · every type

A texture parameter at a UV. Color space turns an image's colors linear; Normal unpacks a normal map to -1 to 1.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |

| Output | Type |
| --- | --- |
| RGBA (`rgba`) | vec4 |

| Setting | Takes | Default |
| --- | --- | --- |
| Space (`space`) | one of `linear`, `color`, `normal` | linear |
| Texture (`texture`) | a `texture2D` parameter |  |

### Sample Texture 2D LOD

`texture/sample2DLod` · any stage · every type

A texture parameter at a UV and a mip level.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| LOD (`lod`) | float | 0 |

| Output | Type |
| --- | --- |
| RGBA (`rgba`) | vec4 |

| Setting | Takes | Default |
| --- | --- | --- |
| Texture (`texture`) | a `texture2D` parameter |  |

### Sample Cubemap

`texture/sampleCube` · any stage · every type

A cube map parameter in a direction.

| Input | Type | Default |
| --- | --- | --- |
| Direction (`direction`) | vec3 | normal |

| Output | Type |
| --- | --- |
| RGBA (`rgba`) | vec4 |

| Setting | Takes | Default |
| --- | --- | --- |
| Texture (`texture`) | a `textureCube` parameter |  |

### Texture Size

`texture/size` · any stage · every type

A texture parameter's size in pixels.

| Output | Type |
| --- | --- |
| Size (`size`) | vec2 |

| Setting | Takes | Default |
| --- | --- | --- |
| Texture (`texture`) | a `texture2D` or `textureCube` parameter |  |

### Normal Unpack

`texture/normalUnpack` · any stage · every type

A normal map's color as a -1 to 1 tangent space normal.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec4 | 0.5, 0.5, 1, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Normal Strength

`texture/normalStrength` · any stage · every type

A tangent space normal made flatter or stronger.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 | 0, 0, 1 |
| Strength (`strength`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Normal Blend

`texture/normalBlend` · any stage · every type

Detail normal B over base normal A, both in tangent space.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | vec3 | 0, 0, 1 |
| B (`b`) | vec3 | 0, 0, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Normal to World

`texture/normalToWorld` · fragment stage · mesh

A tangent space normal turned into the world, for the surface's Normal.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | vec3 | 0, 0, 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Normal From Height

`texture/normalFromHeight` · fragment stage · every type

A tangent space normal from how a height changes across the screen.

| Input | Type | Default |
| --- | --- | --- |
| Height (`height`) | float | 0 |
| Strength (`strength`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

### Triplanar

`texture/triplanar` · fragment stage · every type

A texture parameter projected along the three world axes, for surfaces without good UVs.

| Input | Type | Default |
| --- | --- | --- |
| Position (`position`) | vec3 | worldPosition |
| Normal (`normal`) | vec3 | normal |
| Scale (`scale`) | float | 1 |
| Sharpness (`sharpness`) | float | 4 |

| Output | Type |
| --- | --- |
| RGBA (`rgba`) | vec4 |

| Setting | Takes | Default |
| --- | --- | --- |
| Texture (`texture`) | a `texture2D` parameter |  |

## Noise

### Hash

`noise/hash` · any stage · every type

A random 0 to 1 for each UV, the same each frame.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Scale (`scale`) | float | 10 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Value Noise

`noise/value` · any stage · every type

Smooth blobs, 0 to 1.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Scale (`scale`) | float | 10 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Gradient Noise

`noise/gradient` · any stage · every type

Smooth waves, 0 to 1.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Scale (`scale`) | float | 10 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Voronoi

`noise/voronoi` · any stage · every type

Cells: distance to the nearest cell point, and a random value per cell.

| Input | Type | Default |
| --- | --- | --- |
| UV (`uv`) | vec2 | uv1 |
| Scale (`scale`) | float | 10 |
| Jitter (`jitter`) | float | 1 |

| Output | Type |
| --- | --- |
| Distance (`distance`) | float |
| Cell (`cell`) | float |

## Logic

### Compare

`logic/compare` · any stage · every type

Whether A and B relate as the operation says.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | float | 0 |
| B (`b`) | float | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | bool |

| Setting | Takes | Default |
| --- | --- | --- |
| Operation (`operation`) | one of `less`, `lessEqual`, `greater`, `greaterEqual`, `equal`, `notEqual` | less |

### Branch

`logic/branch` · any stage · every type

True when Condition holds, else False.

| Input | Type | Default |
| --- | --- | --- |
| Condition (`condition`) | bool | true |
| True (`true`) | dynamic | 1 |
| False (`false`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### And

`logic/and` · any stage · every type

Whether both hold.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | bool | true |
| B (`b`) | bool | true |

| Output | Type |
| --- | --- |
| Out (`out`) | bool |

### Or

`logic/or` · any stage · every type

Whether either holds.

| Input | Type | Default |
| --- | --- | --- |
| A (`a`) | bool | false |
| B (`b`) | bool | false |

| Output | Type |
| --- | --- |
| Out (`out`) | bool |

### Not

`logic/not` · any stage · every type

Whether it does not hold.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | bool | false |

| Output | Type |
| --- | --- |
| Out (`out`) | bool |

### Pass Switch

`logic/pass` · any stage · mesh

A value for the color pass and another for the depth, shadow and G-buffer passes.

| Input | Type | Default |
| --- | --- | --- |
| Color Pass (`color`) | dynamic | 1 |
| Other Passes (`other`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

## Effect

### Wind Sway

`effect/wind` · vertex stage · mesh

Sways the mesh in the scene wind (Wind.velocity), with gusts.

| Input | Type | Default |
| --- | --- | --- |
| Sway (`sway`) | float | 0.30000001192092896 |
| Height (`height`) | float | 0 |

| Output | Type |
| --- | --- |
| Offset (`offset`) | vec3 |

### Interaction Push

`effect/interaction` · vertex stage · mesh

Bends the mesh away from Interaction.position, which a script moves.

| Input | Type | Default |
| --- | --- | --- |
| Strength (`strength`) | float | 1 |
| Height (`height`) | float | 0 |

| Output | Type |
| --- | --- |
| Offset (`offset`) | vec3 |

### See-Through

`effect/seeThrough` · fragment stage · mesh

Opens the mesh around SeeThrough.target, as a coverage.

| Output | Type |
| --- | --- |
| Coverage (`coverage`) | float |

### Dissolve

`effect/dissolve` · fragment stage · mesh

Eats the mesh away with noise as Amount goes to 1, as a coverage.

| Input | Type | Default |
| --- | --- | --- |
| Amount (`amount`) | float | 0 |
| Scale (`scale`) | float | 4 |
| Edge (`edge`) | float | 0.05000000074505806 |

| Output | Type |
| --- | --- |
| Coverage (`coverage`) | float |

### Height Clip

`effect/heightClip` · fragment stage · mesh

Removes what is above Clip.height, as a coverage.

| Output | Type |
| --- | --- |
| Coverage (`coverage`) | float |

### Depth Fade

`effect/depthFade` · fragment stage · mesh

0 where the mesh meets what is behind it, 1 a Distance away.

| Input | Type | Default |
| --- | --- | --- |
| Distance (`distance`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Refraction

`effect/refraction` · fragment stage · mesh

What is behind, bent by the normal.

| Input | Type | Default |
| --- | --- | --- |
| Normal (`normal`) | vec3 | normal |
| Strength (`strength`) | float | 0.05000000074505806 |

| Output | Type |
| --- | --- |
| Color (`color`) | vec4 |

### Dither

`effect/dither` · fragment stage · mesh

A fixed pattern to compare a fading value with, 0 to 1.

| Output | Type |
| --- | --- |
| Out (`out`) | float |

### Intersection Foam

`effect/intersectionFoam` · fragment stage · mesh

1 in a band where the mesh meets what is behind it, its edge broken by moving noise, as foam where water meets rocks.

| Input | Type | Default |
| --- | --- | --- |
| Width (`width`) | float | 0.4000000059604645 |
| Scale (`scale`) | float | 3 |
| Speed (`speed`) | float | 0.4000000059604645 |
| Breakup (`breakup`) | float | 1 |

| Output | Type |
| --- | --- |
| Out (`out`) | float |

## Utility

### Reroute

`utility/reroute` · any stage · every type

Passes its input on, to tidy links.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Custom Function

`utility/customFunction` · any stage · every type

GLSL of your own: the signature gives the pins, the body runs, or a .glsl file of the project holds the function.

| Output | Type |
| --- | --- |
| Out (`out`) | vec3 |

| Setting | Takes | Default |
| --- | --- | --- |
| Signature (`signature`) | text | vec3 shade(vec3 color) |
| Body (`body`) | text | return color; |
| File (`file`) | text |  |

### Vertex to Fragment

`utility/vertexToFragment` · any stage · mesh

Works its input out per vertex and passes it to the fragments, interpolated, where it costs less.

| Input | Type | Default |
| --- | --- | --- |
| In (`in`) | dynamic | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | dynamic |

### Subgraph

`utility/subgraph` · any stage · every type

Runs a function graph of the project, a .shader of type function: its Function Inputs are the pins on the left, its Function Outputs those on the right.

| Setting | Takes | Default |
| --- | --- | --- |
| Function (`file`) | a function graph |  |

## Function

### Function Input

`function/input` · any stage · function graphs

A value the calling graph passes in, a pin of its Subgraph node. Default is used when it passes none.

| Input | Type | Default |
| --- | --- | --- |
| Default (`default`) | the Type | 0 |

| Output | Type |
| --- | --- |
| Out (`out`) | the Type |

| Setting | Takes | Default |
| --- | --- | --- |
| Name (`name`) | text | value |
| Type (`valueType`) | one of `float`, `vec2`, `vec3`, `vec4`, `color`, `int`, `bool` | float |

### Function Output

`function/output` · any stage · function graphs

A value the function gives back, a pin on the right of its Subgraph node.

| Input | Type | Default |
| --- | --- | --- |
| Value (`value`) | the Type | 0 |

| Setting | Takes | Default |
| --- | --- | --- |
| Name (`name`) | text | result |
| Type (`valueType`) | one of `float`, `vec2`, `vec3`, `vec4`, `color`, `int`, `bool` | float |
