---
description: Cameras, render systems, PBR materials, lighting, shadows, shaders, framebuffers, and backend support in Doriax.
---

# Rendering Pipeline

Doriax renders through a flexible pipeline that supports 2D, 3D, UI, and
render-to-texture workflows. The same codebase targets OpenGL, OpenGL ES, Metal,
Direct3D 11, and WebGPU through a backend abstraction layer.

## High-level render flow

Each frame, the engine runs the following phases in order:

1. **Camera update** — The active scene camera computes the view matrix and projection
   matrix.
2. **Frustum culling** — Renderables outside the camera frustum are excluded. Terrain
   and tilemaps cull below entity level: only the terrain nodes and tilemap chunks that
   the camera can see are submitted.
3. **Opaque pass** — Opaque geometry is sorted front-to-back and drawn with depth
   testing enabled for early-Z efficiency.
4. **Lighting and shadows** — Shadow maps are rendered for each shadow-casting light,
   then the lighting pass applies directional, point, and spot lights.
5. **Skybox and IBL** — The sky cubemap is drawn (when visible). Environment maps derived
   from the sky feed **image-based lighting (IBL)** on meshes that opt in.
6. **Transparent pass** — Objects with blending enabled are sorted back-to-front and
   drawn after opaque geometry. Blended submeshes still depth-test, but they do **not**
   write depth in the colour pass, so overlapping translucent surfaces composite instead
   of punching holes in each other. A mesh marked transparent (including by
   `autoTransparency`) is skipped by the SSAO depth pre-pass and the SSR G-buffer;
   shadow maps still render it.
7. **UI pass** — UI entities are rendered in screen-space canvas coordinates, on top of
   the 3D or 2D scene.
8. **Post-processing** — Fog and other post effects are applied (if configured).

Cameras that render to a texture (minimaps, [mirrors](#mirrors-and-planar-reflections),
portals) run this same flow into their own framebuffer before the main view is drawn.

## Cameras

Three camera projection modes are available:

| Projection | Use | Object |
| --- | --- | --- |
| **Perspective** | 3D games | `Camera` with `setType(CameraType::CAMERA_PERSPECTIVE)` |
| **Orthographic** | 2D games, isometric | `Camera` with `setType(CameraType::CAMERA_ORTHO)` |
| **UI** | Screen-space canvas | `Camera` with `setType(CameraType::CAMERA_UI)` |

Use `Camera::setNearClip()` and `Camera::setFarClip()` to tune depth precision. Set a
tight near/far range — a large ratio (e.g. 0.1 to 100 000) causes depth fighting on
distant surfaces. You can also configure the projection in one call with
`setPerspective(yfov, aspect, near, far)` or `setOrtho(left, right, bottom, top, near, far)`.

A camera can render to its own texture instead of the screen — see
[Framebuffers and render-to-texture](#framebuffers-and-render-to-texture) below.

## PBR materials

Doriax uses a **Physically Based Rendering** (PBR) material model with the following
texture slots and scalar properties:

| Slot / Property | Controls |
| --- | --- |
| `baseColorTexture` + `baseColorFactor` | Base surface color (albedo) |
| `alphaMode` | Alpha handling: `AUTO`, `ALPHA_OPAQUE`, `MASK`, or `BLEND` |
| `alphaCutoff` | Cutout threshold for `MASK` materials (default `0.5`) |
| `normalTexture` | Surface micro-detail |
| `metallicRoughnessTexture` + `metallicFactor` | Surface reflectivity (0 = dielectric, 1 = metal) |
| `metallicRoughnessTexture` + `roughnessFactor` | Highlight spread (0 = mirror-smooth, 1 = fully rough) |
| `occlusionTexture` | Ambient occlusion darkening in crevices |
| `emissiveTexture` + `emissiveFactor` | Self-illuminated areas that ignore lighting |

Metallic and roughness share one texture, following the GLTF convention (roughness in
the green channel, metallic in the blue channel).

Alpha is the product of `baseColorFactor.a` and the base-colour texture's alpha.
`ALPHA_OPAQUE` forces the result opaque, `MASK` discards pixels below `alphaCutoff`, and
`BLEND` preserves partial alpha for transparent rendering. `AUTO` keeps the historical
Doriax texture-alpha detection used by editor-created materials. Imported GLTF/GLB
materials preserve their explicit alpha mode. A blended submesh (`BLEND`, or `AUTO` when
the texture or factor is translucent) disables depth writes on its colour pipeline.

The `MASK` test is identical in the lit, shadow/depth, and SSR G-buffer passes. A cutout
therefore casts and contributes to screen-space effects with the same silhouette that
is visible in the colour pass.

```cpp
Material mat;
mat.baseColorTexture = Texture("textures/rock_albedo.png");
mat.normalTexture    = Texture("textures/rock_normal.png");
mat.roughnessFactor  = 0.85f;
mat.metallicFactor   = 0.0f;

mesh.setMaterial(0, mat);   // submesh index, material
```

## Lighting

The engine supports three light types plus global illumination:

| Type | Use |
| --- | --- |
| **Directional** | Sun / moon — affects the entire scene |
| **Point** | Omni-directional bulbs, torches |
| **Spot** | Flashlights, stage lighting, headlights |

**Scene ambient light** (`Scene::setGlobalIllumination`) fills shadowed areas with a flat
tint. It is separate from IBL — ambient light affects all lit meshes uniformly, while IBL
adds directional reflections and diffuse fill derived from the sky environment.

```cpp
Light sun(&scene);
sun.setType(LightType::DIRECTIONAL);
sun.setDirection(Vector3(-0.5f, -1.0f, -0.5f));
sun.setColor(Vector3(1.0f, 0.95f, 0.8f));
sun.setIntensity(3.0f);
sun.setShadows(true);
```

### Shadow maps

Each shadow-casting light renders a depth map. Engine limits (adjustable at build
time):

| Constant | Default | Controls |
| --- | --- | --- |
| `MAX_LIGHTS` | 6 | Max simultaneous lights |
| `MAX_SHADOW_ATLAS_SLOTS` | 9 | Projective atlas slots (one per spot light or directional cascade) |
| `MAX_POINT_SHADOW_ATLAS_SLOTS` | 24 | Point atlas slots, `SHADOW_CUBE_FACES` (6) per light |
| `MAX_POINT_SHADOW_LIGHTS` | 4 | Shadow-casting point lights (derived from the two above) |
| `MAX_SHADOWCASCADES` | 4 | Cascades for directional CSM |

Shadow edge smoothness is a per-scene setting, `Scene::setShadowQuality`, with
**Percentage Closer Filtering (PCF)** kernels of `NONE` (1 tap), `LOW`
(3x3, default), `MEDIUM` (5x5), or `HIGH` (7x7). The kernel size is uniform-driven, so
changing it applies instantly without shader rebuilds:

```cpp
scene.setShadowQuality(ShadowQuality::MEDIUM);
```

Directional and spot shadows sample a depth atlas through a hardware comparison
sampler, so every tap is already filtered across a 2x2 neighbourhood: `NONE` still
softens edges slightly rather than producing hard ones. Point lights keep a packed
colour depth map and stay hard-edged at `NONE`.

## 2D lighting and shadows

2D scenes use a **dedicated forward light path** instead of the PBR model: each
[Light2D](../reference/classes/light2d.md) contributes
`color · intensity · falloff(distance)` and all contributions add on top of the scene's
**2D ambient light** (`Scene::setAmbientLight2D`). The result multiplies the sprite's
base color, so the unlit fast path is preserved — a 2D-lit sprite costs far less than a
PBR-lit mesh. Both paths can coexist: a mesh lit by 3D lights in the same scene simply
adds the 2D contribution on top.

A light's optional `height` places it on a virtual Z above the 2D plane, giving normal
maps a direction to respond to. Sprites, tilemaps, and mesh polygons generate tangents
automatically, so assigning a normal texture to their material is enough.

2D lights ignore the scene's `lightState` flag — that switch controls only the 3D
lighting pass.

### 1D polar shadow maps

Shadows from [Occluder2D](../reference/classes/occluder2d.md) components use per-light
**1D polar shadow maps**: all occluder outlines in the scene are merged into one segment
buffer and rendered into a one-pixel-tall atlas row per shadow-casting light, where the
X axis is the angle around the light and the stored value is the distance to the nearest
occluder. Lit fragments compare their own angle and distance against the row, with a PCF
filter along it for soft edges: the light's `shadowSoftness` sets the penumbra width and
the scene's `shadow2DQuality` (`NONE` / `LOW` / `MEDIUM` / `HIGH` — 1 to 13 taps) sets
how smoothly it is sampled. The tap count is uniform-driven, so quality changes apply
instantly without shader rebuilds.

| Constant | Default | Controls |
| --- | --- | --- |
| `MAX_LIGHTS_2D` | 16 | Max simultaneous 2D lights (and shadow atlas rows) |

The shadow pass renders line segments only (no scene geometry), so it stays cheap even
with many occluders; each shadow-enabled light adds one atlas row at the light's
`mapResolution` width. Each light's shadow attenuates only that light's own
contribution — ambient light is never shadowed. See
[2D Graphics — 2D lighting](2d-graphics.md#2d-lighting) for the usage guide.

## Fog

`Fog` adds atmospheric depth. Two modes are available:

| Mode | Effect |
| --- | --- |
| `LINEAR` | Fog blends from `linearStart` to full density at `linearEnd` |
| `EXPONENTIAL` | Density increases exponentially with distance |
| `EXPONENTIALSQUARED` | Steeper exponential falloff |

```cpp
Fog fog(&scene);
fog.setType(FogType::EXPONENTIAL);
fog.setColor(Vector3(0.7f, 0.7f, 0.8f));
fog.setDensity(0.02f);
// For LINEAR mode use fog.setLinearStartEnd(start, end) instead of density
```

## Skybox

Add a **Sky** entity (Skybox component) and assign either a single cubemap texture or six
cube-face textures. The sky is rendered as an infinite background behind opaque geometry.

```cpp
SkyBox sky(&scene);
sky.setTexture("textures/sky_cubemap.png");

// or per-face:
sky.setTextures("daysky",
    "sky/px.png", "sky/nx.png",
    "sky/py.png", "sky/ny.png",
    "sky/pz.png", "sky/nz.png");
```

In the editor, the Sky component also exposes **Visible**. When disabled, the sky is not
drawn in the viewport but still generates IBL environment maps for meshes that use them.
Use this when you want reflections and indirect lighting from an environment without
showing the sky dome itself (for example, an interior level with a hidden outdoor HDR
environment).

## Image-based lighting (IBL)

When a scene contains a Sky entity with a valid cubemap texture, the engine builds two
environment maps from that sky:

| Map | Purpose |
| --- | --- |
| **Irradiance** | Diffuse ambient fill — soft colour bounced from every direction |
| **Prefiltered specular** | Glossy reflections — sharper highlights on smooth (low-roughness) surfaces |

These maps follow the glTF-style split-sum approximation used in modern PBR pipelines.
Rough surfaces sample blurrier mips; mirror-like surfaces pick up crisp sky detail.

IBL is **per mesh**. Each mesh has a **Receive IBL** flag (default `false` in new scenes).
Only meshes with this enabled combine punctual lights (directional/point/spot) with the
sky environment. Meshes also need **Receive Lights** enabled and a valid normal (tangent
space for normal maps).

Typical workflow:

1. Add a Sky entity and assign a cubemap (HDR or LDR).
2. Select meshes that should reflect the environment (metal, glass, wet stone, etc.).
3. Enable **Receive IBL** on those meshes in the Properties window.
4. Tune **Roughness** and **Metallic** on the material — low roughness makes reflections
   more obvious.

The material preview sphere in the Properties window updates when **Receive IBL** is
toggled, so you can compare lit-only vs environment-lit looks before play mode.

!!! note "One sky per scene"
    The render system uses the first Sky component in the scene for both drawing and IBL
    generation. Keep a single active sky environment unless you know you are replacing it.

## Reflection probes

[IBL](#image-based-lighting-ibl) reflects one sky environment everywhere, which reads as
"outdoors" on every surface. A **Reflection Probe** captures the environment *at a point
in the scene* and applies it to meshes inside a box-shaped influence volume — chrome in a
garage reflects the garage, not the sky. Probe reflections are **box-projected**
(parallax-corrected): reflection rays are projected onto the influence box, so the
reflection stays anchored to the room's walls as objects and the camera move, instead of
floating at infinity.

The simplest way to add one is the **Reflection Probe** entry in the Structure panel's
create menu. Size its **Box Size** to the room or area it represents, and enable
**Receive IBL** (plus **Receive Lights**) on the meshes inside — probes use the same
per-mesh opt-in as sky IBL. A Sky is not required: probes supply the specular
(reflection) term on their own, while diffuse ambient still comes from the sky
irradiance when one is present.

### Static and dynamic probes

| Mode | Behaviour |
| --- | --- |
| **Static** | Uses an authored cubemap when one is assigned; otherwise captures the scene once at load (or when **Refresh Probe** is pressed) and keeps that result. |
| **Dynamic** | Re-captures the scene at runtime according to its update policy. |

An authored cubemap is the best-quality and cheapest option: it is GGX-prefiltered and
cached like the sky environment, so rough surfaces get correct blurry reflections.
Runtime captures have no prefiltered mip chain — rough surfaces approximate the blur
with a small angular filter — so prefer static probes with authored cubemaps for
strongly rough materials.

Dynamic probes choose when to re-capture with **Update**:

| Update | When it captures |
| --- | --- |
| **On Load** | Once when the scene starts |
| **On Move** | Whenever the probe entity moves |
| **Interval** | Every **Update Interval** seconds |
| **Manual** | Only when requested — the **Refresh Probe** button in the editor, or setting `needUpdate = true` from code |

Runtime captures share a strict budget of **one cubemap face per frame**: a full refresh
takes six frames, and multiple pending probes take turns. Even several dynamic probes
therefore cost a fraction of a [mirror's](#mirrors-and-planar-reflections) full extra
scene render per frame — the trade-off is latency, not throughput.

### Influence volume and blending

| Property | Purpose |
| --- | --- |
| **Box Size** | The influence volume's size, scaled by the entity's world scale. The box is world-axis-aligned and centred on the entity. |
| **Box Offset** | Moves the influence box in the entity's local space. The cubemap is still captured at the entity origin (shown as a gold marker in the viewport when they differ). |
| **Blend Distance** | Fade band inside the box edges where the probe blends into the sky IBL, hiding the seam at the volume boundary. Runtime blending is limited to the box's smallest half-extent. |
| **Intensity** | Multiplier on the probe's reflection contribution. |
| **Priority** | When influence boxes overlap, the higher-priority probe wins; on a tie, the probe whose centre is nearest the mesh wins. |

The engine picks **one probe per mesh** (using the mesh's world-bounds centre), so keep
volumes room-sized rather than object-sized: a mesh is either inside a probe's box or it
falls back to the sky environment.

### Capture settings

| Property | Purpose |
| --- | --- |
| **Cubemap** | *(static only)* Authored six-face cubemap. Leave empty to capture at load instead. |
| **Resolution** | Capture cubemap face size (16–1024, default 128). |
| **Near / Far** | Clip planes of the capture cameras. |
| **Include Sky** | Whether the sky (and scene background colour) appears in the capture. |

Individual meshes stay out of captures with **Draw in Probes** on the Mesh component
(`renderInReflectionProbes`). Turn it off for geometry wrapped around a probe — a car
body with a probe at its centre, say — which would otherwise fill its own reflection.
The mesh still renders normally everywhere else. Toggling it re-captures every probe in
the scene, because static and non-interval probes keep their baked cubemap until
something invalidates it.

```cpp
// C++: a dynamic probe covering a 12x6x12 room
ReflectionProbe probe(&scene);
probe.setPosition(0.0f, 2.0f, 0.0f);
probe.setBoxSize(12.0f, 6.0f, 12.0f);
probe.setMode(ReflectionProbeMode::DYNAMIC);
probe.setUpdateMode(ReflectionProbeUpdateMode::MANUAL);
probe.refresh();   // manual re-capture from code
```

```lua
local probe = ReflectionProbe(scene)
probe:setPosition(0, 2, 0)
probe:setBoxSize(12, 6, 12)
probe.mode = ReflectionProbeMode.DYNAMIC
probe.updateMode = ReflectionProbeUpdateMode.MANUAL
probe:refresh()   -- manual re-capture from code
```

With [SSR](#screen-space-reflections-ssr) enabled, surfaces lit by a local probe keep
their probe reflection and SSR adds on-screen detail on top; only sky-IBL surfaces use
SSR's energy-conserving replace path.

!!! note "Capture scope and limitations"
    Runtime captures render opaque meshes and (optionally) the sky. Transparent meshes,
    UI, and particles are skipped. Point and spot shadows are reused in captures, but
    directional shadow cascades are fitted to the main camera, so their coverage inside a
    capture can be partial. A probe never appears in its own capture, and captures do not
    include other probes' reflections (no recursion).

## Ambient occlusion (SSAO)

Screen-space ambient occlusion darkens creases, corners, and contact areas where ambient
light is naturally blocked. Like Godot, Unity, and Unreal, it modulates only the
**ambient/indirect** term (IBL or global illumination) — direct light from your sun, point,
and spot lights is left untouched — so it reads as soft contact shading rather than a
second shadow.

Each frame the render system runs a small depth pre-pass for the main camera, derives
occlusion from a rotated hemisphere kernel, blurs it, and the lit mesh shader multiplies
the result into its ambient term.

SSAO is a scene setting:

```cpp
scene.setSSAOEnabled(true);
scene.setSSAORadius(0.5f);     // view-space sampling radius (world units)
scene.setSSAOIntensity(1.0f);  // strength (exponent on the occlusion factor)
scene.setSSAOBias(0.025f);     // depth bias to avoid self-occlusion acne
```

```lua
scene.ssaoEnabled = true
scene.ssaoRadius = 0.5
scene.ssaoIntensity = 1.0
scene.ssaoBias = 0.025
```

In the editor, the same controls live under **Scene → Ambient Occlusion (SSAO)** in the
Properties window, including a **Debug View** toggle that renders the raw AO buffer so you
can tune radius/intensity/bias directly.

| Parameter | Effect |
| --- | --- |
| **Radius** | How far samples reach in view space — larger is broader/softer, smaller stays in tight creases |
| **Intensity** | Darkening strength; raise to make occlusion more pronounced |
| **Bias** | Pushes samples off the surface to stop flat areas self-occluding (acne) |

Because the effect only touches ambient light, it is most visible with a strong ambient
source — raise **Global Illumination Intensity** or use IBL if SSAO looks too subtle in a
scene lit mainly by direct light.

!!! note "Scope and limitations"
    SSAO is computed for the main camera; render-to-texture cameras and terrain are
    currently excluded (terrain would exceed the shader's sampler limit). Normals are
    reconstructed from depth when SSAO runs alone; when
    [SSR](#screen-space-reflections-ssr) is also enabled SSAO reuses the SSR G-buffer's
    depth **and** geometric normals — a single shared geometry pass, and sharper at
    silhouettes. Enabling SSAO recompiles lit mesh shaders.

## Screen-space reflections (SSR)

Screen-space reflections add real-time reflections of on-screen geometry — wet floors,
polished metal, glossy surfaces — by marching the camera depth buffer in screen space and
sampling the lit scene colour where a reflected ray hits. Like Godot and Unity, SSR is
*energy-conserving*: where a ray finds a hit it **replaces** the surface's
[IBL](#image-based-lighting-ibl) environment reflection rather than adding on top of it, and
where a ray misses (off-screen or occluded) the IBL reflection remains as the fallback. So
SSR refines what IBL already provides instead of double-counting it.

When SSR is enabled the main camera first renders a small **G-buffer** geometry pre-pass —
packed depth, view-space normal, roughness/metallic, and base colour — then runs three
fullscreen passes:

1. **March** — reflect the view ray about the G-buffer normal and step it through depth
   (with a binary-search refine) until it crosses on-screen geometry.
2. **Glossy blur** *(optional)* — blurs the reflection in proportion to surface roughness,
   so rough materials get soft reflections while mirrors stay sharp.
3. **Composite** — recomputes the surface's IBL specular and blends the reflection over it
   with the correct GGX reflectance (including metal tint), writing the final image.

The opaque colour pass is rendered into an offscreen buffer first so the march has a full
scene-colour image to sample. SSR therefore requires a framebuffer destination — the editor
viewport, a [render-to-texture](#framebuffers-and-render-to-texture) camera, or an engine
framebuffer.

SSR is a scene setting:

```cpp
scene.setSSREnabled(true);
scene.setSSRMaxDistance(8.0f);   // max ray length in view-space units
scene.setSSRThickness(0.5f);     // depth-compare tolerance (view-space units)
scene.setSSRMaxSteps(48);        // linear march sample count (quality vs cost)
scene.setSSRIntensity(1.0f);     // reflection strength multiplier
scene.setSSRBlur(0.0f);          // glossy blur amount [0..1] (0 = sharp/mirror)
```

```lua
scene.ssrEnabled = true
scene.ssrMaxDistance = 8.0
scene.ssrThickness = 0.5
scene.ssrMaxSteps = 48
scene.ssrIntensity = 1.0
scene.ssrBlur = 0.0
```

In the editor the same controls live under **Scene → Screen-Space Reflections (SSR)** in the
Properties window, plus a **Debug View** dropdown for tuning.

| Parameter | Effect |
| --- | --- |
| **Max Distance** | How far a reflection ray travels in view space before giving up |
| **Thickness** | Depth tolerance for accepting a hit — smaller is stricter; larger fills gaps but can smear at contacts |
| **Max Steps** | March sample count — higher gives sharper/longer reflections at more cost; raise it if reflections miss thin contacts |
| **Intensity** | Overall reflection strength |
| **Glossy Blur** | `0` = mirror; raise to blur reflections by surface roughness |

**Debug View** renders one G-buffer channel full-screen: `Reflection` (the raw reflection
buffer), `Normal`, `Roughness`, `Metallic`, `Albedo`, or `IBL Specular` (the recomputed
environment term SSR blends against — compare it with the in-scene reflections to confirm
the energy match). `Off` shows the normal render. Per-pixel roughness, metallic, and base
colour come from the material factors and the metallic-roughness / base-colour textures.

!!! note "Scope and limitations"
    SSR is screen-space, so it only reflects what is currently on screen: reflections fade
    out near the screen edges and cannot show off-screen or occluded geometry (IBL fills
    those in). Thin contact lines where an object meets a reflective surface can leave a
    small seam — raise **Max Steps** or lower **Thickness** to tighten it. SSR runs for the
    main camera only and is skipped when there is no framebuffer destination.

## Framebuffers and render-to-texture

A camera can capture its output to a texture instead of the screen — for minimaps,
portals, mirrors, security monitors, or dynamic UI previews. Enable render-to-texture
on the camera and pass its framebuffer wherever a texture is accepted (`Mesh`, `Image`,
`Polygon`, and others have a `setTexture(Framebuffer*)` overload):

```cpp
Camera minimapCam(&scene);
minimapCam.setRenderToTexture(true);
minimapCam.setFramebufferSize(512, 512);

// Use the camera's output as a texture on a UI image
Image preview(&uiScene);
preview.setTexture(minimapCam.getFramebuffer());
```

In the editor, any **Texture** field can use a camera as its source instead of an image
file: click the camera button on the field (or drag a camera entity from the Structure
panel onto it). The chosen camera is switched to render-to-texture and its output feeds
the slot — the basis for the manual mirror setup below. A camera used this way cannot
also be the scene's main camera.

A related mechanism lets the **main camera itself** render offscreen at a fixed
internal resolution that is then upscaled to the window — for pixel-art rendering or
GPU performance scaling. That is a scene setting rather than a camera one; see
[Multiple Resolutions — Fixed resolution](multiple-resolutions.md#fixed-resolution).

## Mirrors and planar reflections

A **Mirror** turns a flat surface into a true planar reflection — the kind used for
mirrors, still water, and polished floors. It is built on render-to-texture: the engine
renders the scene a second time from the viewpoint *reflected across the mirror plane*,
then maps that image back onto the surface.

The simplest way to add one is the **Mirror** entry in the Structure panel's create menu
(or **Basic shape → Wall** plus a **Mirror** component). This creates an upright
[Wall](../reference/classes/shape.md) whose surface normal faces the camera, with a
`MirrorComponent` already attached. No camera or texture wiring is required — the
component manages its own reflection camera internally.

In code, the [Mirror](../reference/classes/mirror.md) class is the same thing: it derives
from `Shape`, so it builds its own surface and attaches the component in one step.

=== "C++"

    ```cpp
    Mirror mirror(&scene);
    mirror.createWall(10.0f, 10.0f);   // vertical quad, +Z normal (faces the camera)
    mirror.setReceiveLights(false);    // optional: show the reflection unshaded
    ```

=== "Lua"

    ```lua
    local mirror = Mirror(scene)
    mirror:createWall(10.0, 10.0)
    mirror.receiveLights = false
    ```

To make an **existing** mesh reflective instead of creating a new one, use
`Mesh::setAsMirror()`, which works on any flat mesh; pass a normal —
`setAsMirror(Vector3(0, 1, 0))` — when the surface isn't a Wall (for example a floor
created with `createPlane`). Use `removeMirror()` / `isMirror()` to toggle or query it.

### How it works

| Stage | What happens |
| --- | --- |
| Reflected camera | Each frame the active camera is mirrored across the surface plane (entity position + normal). This preserves the handedness flip a real mirror has, so reflected geometry is rendered with **reversed face winding** to stay front-facing. |
| Projective sampling | The surface samples the reflection texture by screen position, not by mesh UVs, so the reflection stays correctly aligned regardless of the surface's size or placement. |
| Oblique clipping | The reflection camera's near plane is bent onto the mirror plane (Lengyel oblique projection), so geometry **behind** the mirror cannot leak into the reflection. The sky is excluded from this clip and reflects normally. |

### The Normal field

`MirrorComponent` exposes a single **Normal** — the reflecting surface direction in the
mesh's local space (default `+Z`, matching a Wall), reachable in scripts as
[`Mirror::normal`](../reference/classes/mirror.md#normal). It is transformed by the
entity's rotation to build the world mirror plane, so rotating the mirror entity orients
the reflection automatically.

!!! tip "If the reflection looks wrong"
    The reflection image is the same whichever way the normal points, but the
    behind-the-mirror clipping depends on its sign. If the reflection is clipped on the
    wrong side (showing geometry that should be hidden, or going mostly empty), flip the
    sign of the **Normal**.

### Cost

A mirror renders the visible scene **one additional time per frame** into its own
off-screen target — the same inherent cost planar reflections have in every engine. Use
them deliberately:

- Prefer one hero mirror / water plane over many.
- A mirror never reflects itself, and reflections of other mirrors are not recursive.
- The reflection target matches the canvas resolution by default; lowering it trades
  sharpness for performance.

## Shaders

Shaders are authored in GLSL and transpiled by the shader builder for each supported
backend. Shader data files are generated at export time.

Each renderable type (Mesh, UI, Points, Lines, Sky) has a built-in shader. In the editor
you can **fork** any of them — per component, or as a scene-wide default for that type —
and edit the GLSL; the engine keeps driving the variant system, lighting, and
depth/shadow/G-buffer passes. A shader set on the component wins over the scene default,
which wins over the built-in. See [Custom Shaders](../editor/custom-shaders.md).

Built-in skinned variants bind bone matrices through a **storage buffer** (`sbo_skinning`)
on Vulkan, Metal, and Direct3D 11, or through an **unfilterable RGBA32F bone texture**
sampled with `texelFetch` on OpenGL / OpenGL ES. The colour, depth/shadow, and G-buffer
passes share that path, so large skeletons are not capped by a uniform-block size. Shader
reflection keeps the backend-specific storage-buffer bindings, which Metal requires for
validation. The CPU array is still sized by `MAX_BONES` (default 128); see
[3D Graphics — GLTF compatibility and limits](3d-graphics.md#gltf-compatibility-and-limits).
The editor revisions its compiled shader cache when this built-in shader interface
changes, so an updated editor does not reuse incompatible older skinned variants.

GPU pipeline creation can be deferred by the graphics backend. If a pipeline variant
fails creation or validation, Doriax skips that draw instead of submitting its uniform,
binding, and draw commands against the failed handle. Diagnose the original pipeline
creation message in the Output panel; the dependent validation-error cascade is
suppressed.

Supported graphics backends (`GraphicBackend` enum):

| Backend constant | Target |
| --- | --- |
| `GLCORE` | Desktop OpenGL 3.3+ |
| `GLES3` | OpenGL ES 3 (Android, WebGL2) |
| `D3D11` | Windows Direct3D 11 |
| `METAL` | macOS and iOS Metal |
| `WGPU` | WebGPU |

## GPU instancing

Draw large numbers of identical objects (trees, rocks, enemies) efficiently with mesh
instancing. Each instance has its own transform (and optional color and texture region)
stored in a GPU buffer, eliminating per-draw CPU overhead:

```cpp
mesh.createInstancedMesh();
mesh.setMaxInstances(500);

for (int i = 0; i < 500; i++) {
    mesh.addInstance(Vector3(i * 2.0f, 0, 0), Quaternion(), Vector3(1, 1, 1));
}
```

Instances can be modified later with `updateInstance(index, ...)` and read back with
`getInstance(index)`.

Instancing uses geometry on the **same entity** as the instanced mesh. Multi-node GLTF
models that keep child mesh entities will not draw instances until you
[merge static model meshes](3d-graphics.md#merging-static-model-meshes) into the root
(or build instances on a single-mesh entity / basic shape). In the editor, the Instanced
Mesh panel warns when a model still uses the child-mesh layout.

## Performance guidelines

| Area | Guideline |
| --- | --- |
| Draw calls | Reduce with instancing, atlases, and shared `.material` files |
| IBL cost | Environment maps are rebuilt when the sky texture changes; disable **Receive IBL** on distant or unimportant meshes |
| Shadow casters | Limit shadow-casting lights; cascade only when needed |
| Transparent objects | Keep transparent draw counts low; sort correctly |
| Tilemaps | Chunk culling is automatic, so map size costs little; a tilemap is capped at 16 383 tiles |
| Mobile shaders | Simplify PBR (skip normal maps, lower cascade count) |
| Render targets | Minimize framebuffer resolution for off-screen effects |
| Mirrors | Each mirror re-renders the scene once per frame; keep one hero reflection and lower its target resolution if needed |
| SSR | Adds a G-buffer geometry pass plus fullscreen march/blur/composite passes; lower **Max Steps** for cost, and it shares its geometry pass with SSAO when both are on |
| Textures | Use compressed formats (ETC2/BC) on mobile/desktop respectively |

## See also

- [Camera](../reference/classes/camera.md)
- [Light](../reference/classes/light.md)
- [Material](../reference/classes/material.md)
- [Texture](../reference/classes/texture.md)
- [Fog](../reference/classes/fog.md)
- [Skybox](../reference/classes/skybox.md)
- [ReflectionProbe](../reference/classes/reflectionprobe.md)
- [Mesh](../reference/classes/mesh.md)
- [RenderSystem](../reference/classes/rendersystem.md)
