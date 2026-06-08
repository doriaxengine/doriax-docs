---
description: Cameras, render systems, PBR materials, lighting, shadows, shaders, framebuffers, and backend support in Doriax.
---

# Rendering Pipeline

Doriax renders through a flexible pipeline that supports 2D, 3D, UI, and
render-to-texture workflows. The same codebase targets OpenGL, Metal, Direct3D,
WebGL, and Vulkan-like backends through a backend abstraction layer.

## High-level render flow

Each frame, the engine runs the following phases in order:

1. **Camera update** — The active scene camera computes the view matrix and projection
   matrix.
2. **Frustum culling** — Renderables outside the camera frustum are excluded.
3. **Opaque pass** — Opaque geometry is sorted front-to-back and drawn with depth
   testing enabled for early-Z efficiency.
4. **Lighting and shadows** — Shadow maps are rendered for each shadow-casting light,
   then the lighting pass applies directional, point, and spot lights.
5. **Skybox and environment** — The skybox is drawn; global illumination is applied.
6. **Transparent pass** — Objects with blending enabled are sorted back-to-front and
   drawn after opaque geometry.
7. **UI pass** — UI entities are rendered in screen-space canvas coordinates, on top of
   the 3D or 2D scene.
8. **Post-processing** — Fog and other post effects are applied (if configured).

## Cameras

Three camera projection modes are available:

| Projection | Use | Object |
| --- | --- | --- |
| **Perspective** | 3D games | `Camera` with `setType(CameraType::PERSPECTIVE)` |
| **Orthographic** | 2D games, isometric | `Camera` with `setType(CameraType::ORTHO)` |
| **Frustum** | Custom clip planes | `Camera` with manual frustum |

Use `Camera::setNearFarPlane()` to tune depth precision. Set a tight near/far range —
a large ratio (e.g. 0.1 to 100 000) causes depth fighting on distant surfaces.

Multiple cameras can render to separate framebuffers and be composited as a layered
scene:

```cpp
// Game camera renders to screen
gameCamera.setRenderTarget(nullptr);

// Mini-map camera renders to a texture
minimapCamera.setRenderTarget(&minimapFramebuffer);
```

## PBR materials

Doriax uses a **Physically Based Rendering** (PBR) material model with the following
texture slots and scalar properties:

| Slot / Property | Controls |
| --- | --- |
| **Albedo** texture + color | Base surface color |
| **Normal** map | Surface micro-detail |
| **Metallic** scalar + map | Surface reflectivity (0 = dielectric, 1 = metal) |
| **Roughness** scalar + map | Highlight spread (0 = mirror-smooth, 1 = fully rough) |
| **Occlusion** map | Ambient occlusion darkening in crevices |
| **Emission** texture + factor | Self-illuminated areas that ignore lighting |

```cpp
Material mat;
mat.albedoTexture  = "textures/rock_albedo.png";
mat.normalTexture  = "textures/rock_normal.png";
mat.roughnessFactor = 0.85f;
mat.metallicFactor  = 0.0f;

mesh.setMaterial(0, mat);
```

## Lighting

The engine supports three light types plus global illumination:

| Type | Use |
| --- | --- |
| **Directional** | Sun / moon — affects the entire scene |
| **Point** | Omni-directional bulbs, torches |
| **Spot** | Flashlights, stage lighting, headlights |

Global illumination (ambient light) fills shadowed areas. Tune its intensity to match
your scene's mood.

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
| `MAX_LIGHTS` | 8 | Max simultaneous lights |
| `MAX_SHADOWSMAP` | 8 | Spot/point shadow maps |
| `MAX_SHADOWCASCADES` | 4 | Cascades for directional CSM |

Enable **Percentage Closer Filtering (PCF)** on a scene for softer shadow edges:

```cpp
scene.setShadowsPCF(true);
```

## Fog

`Fog` adds atmospheric depth. Two modes are available:

| Mode | Effect |
| --- | --- |
| `LINEAR` | Fog starts at a near distance and is full density at the far distance |
| `EXPONENTIAL` | Density increases exponentially with distance |

```cpp
Fog fog(&scene);
fog.setType(FogType::EXPONENTIAL);
fog.setColor(Vector3(0.7f, 0.7f, 0.8f));
fog.setDensity(0.02f);
```

## Skybox

Add a `Skybox` entity and assign a cubemap texture for realistic sky reflections and
IBL (Image-Based Lighting):

```cpp
Skybox sky(&scene);
sky.setTexture("textures/sky_cubemap.png");
```

## Framebuffers and render-to-texture

`Framebuffer` captures a camera's output to a texture that can be used elsewhere — for
minimaps, portals, mirrors, post-processing stages, or dynamic UI previews:

```cpp
Framebuffer fbo;
fbo.setSize(512, 512);

Camera cam(&scene);
cam.setRenderTarget(&fbo);

// Later, use the framebuffer's color texture on a surface
Image preview(&uiScene);
preview.setTexture(fbo.getColorTexture());
```

## Shaders

Shaders are authored in GLSL and transpiled by the shader builder for each supported
backend. Shader data files are generated at export time.

Supported graphics backends:

| Backend constant | Target |
| --- | --- |
| `GLCORE` | Desktop OpenGL 3.3+ |
| `GLES3` | OpenGL ES 3 (Android, WebGL2) |
| `D3D11` | Windows Direct3D 11 |
| `METAL` | macOS and iOS Metal |

## GPU instancing

Draw large numbers of identical objects (trees, rocks, enemies) efficiently with
`MeshSystem::setInstancingEnabled()` and `InstanceData`. Each instance has its own
transform stored in a GPU buffer, eliminating per-draw CPU overhead.

```cpp
mesh.setInstancingEnabled(true);

InstanceData instances;
for (int i = 0; i < 500; i++) {
    instances.addTransform(Vector3(i * 2.0f, 0, 0), Quaternion(), Vector3(1, 1, 1));
}
mesh.setInstanceData(instances);
```

## Performance guidelines

| Area | Guideline |
| --- | --- |
| Draw calls | Reduce with instancing, atlases, and material sharing |
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
