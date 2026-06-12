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
