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
2. **Frustum culling** — Renderables outside the camera frustum are excluded.
3. **Opaque pass** — Opaque geometry is sorted front-to-back and drawn with depth
   testing enabled for early-Z efficiency.
4. **Lighting and shadows** — Shadow maps are rendered for each shadow-casting light,
   then the lighting pass applies directional, point, and spot lights.
5. **Skybox and IBL** — The sky cubemap is drawn (when visible). Environment maps derived
   from the sky feed **image-based lighting (IBL)** on meshes that opt in.
6. **Transparent pass** — Objects with blending enabled are sorted back-to-front and
   drawn after opaque geometry.
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
| `normalTexture` | Surface micro-detail |
| `metallicRoughnessTexture` + `metallicFactor` | Surface reflectivity (0 = dielectric, 1 = metal) |
| `metallicRoughnessTexture` + `roughnessFactor` | Highlight spread (0 = mirror-smooth, 1 = fully rough) |
| `occlusionTexture` | Ambient occlusion darkening in crevices |
| `emissiveTexture` + `emissiveFactor` | Self-illuminated areas that ignore lighting |

Metallic and roughness share one texture, following the GLTF convention (roughness in
the green channel, metallic in the blue channel).

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
| `MAX_SHADOWSMAP` | 6 | 2D shadow maps (directional/spot) |
| `MAX_SHADOWSCUBEMAP` | 1 | Cube shadow maps (point lights) |
| `MAX_SHADOWCASCADES` | 4 | Cascades for directional CSM |

Enable **Percentage Closer Filtering (PCF)** on a scene for softer shadow edges:

```cpp
scene.setShadowsPCF(true);
```

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
    currently excluded (terrain would exceed the shader's sampler limit). Surface normals
    are reconstructed from depth, which is fast but slightly softer at silhouettes than a
    dedicated normal buffer. Enabling SSAO recompiles lit mesh shaders.

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

```cpp
// C++: a wall mesh that reflects the scene
Shape mirror(&scene);
mirror.createWall(10.0f, 10.0f);   // vertical quad, +Z normal (faces the camera)
mirror.setAsMirror();              // one call — engine manages the reflection camera
mirror.setReceiveLights(false);    // optional: show the reflection unshaded
```

`Mesh::setAsMirror()` works on any flat mesh; pass a normal — `setAsMirror(Vector3(0, 1, 0))`
— when the surface isn't a Wall (for example a floor created with `createPlane`). Use
`removeMirror()` / `isMirror()` to toggle or query it.

### How it works

| Stage | What happens |
| --- | --- |
| Reflected camera | Each frame the active camera is mirrored across the surface plane (entity position + normal). This preserves the handedness flip a real mirror has, so reflected geometry is rendered with **reversed face winding** to stay front-facing. |
| Projective sampling | The surface samples the reflection texture by screen position, not by mesh UVs, so the reflection stays correctly aligned regardless of the surface's size or placement. |
| Oblique clipping | The reflection camera's near plane is bent onto the mirror plane (Lengyel oblique projection), so geometry **behind** the mirror cannot leak into the reflection. The sky is excluded from this clip and reflects normally. |

### The Normal field

`MirrorComponent` exposes a single **Normal** — the reflecting surface direction in the
mesh's local space (default `+Z`, matching a Wall). It is transformed by the entity's
rotation to build the world mirror plane, so rotating the mirror entity orients the
reflection automatically.

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

## Performance guidelines

| Area | Guideline |
| --- | --- |
| Draw calls | Reduce with instancing, atlases, and shared `.material` files |
| IBL cost | Environment maps are rebuilt when the sky texture changes; disable **Receive IBL** on distant or unimportant meshes |
| Shadow casters | Limit shadow-casting lights; cascade only when needed |
| Transparent objects | Keep transparent draw counts low; sort correctly |
| Mobile shaders | Simplify PBR (skip normal maps, lower cascade count) |
| Render targets | Minimize framebuffer resolution for off-screen effects |
| Mirrors | Each mirror re-renders the scene once per frame; keep one hero reflection and lower its target resolution if needed |
| Textures | Use compressed formats (ETC2/BC) on mobile/desktop respectively |

## See also

- [Camera](../reference/classes/camera.md)
- [Light](../reference/classes/light.md)
- [Material](../reference/classes/material.md)
- [Texture](../reference/classes/texture.md)
- [Fog](../reference/classes/fog.md)
- [Skybox](../reference/classes/skybox.md)
- [Mesh](../reference/classes/mesh.md)
- [RenderSystem](../reference/classes/rendersystem.md)
