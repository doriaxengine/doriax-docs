---
description: Working with 3D graphics in Doriax — models, materials, lighting, and the sky system.
---

# 3D Graphics

Doriax provides a complete 3D pipeline with model loading, physically-based rendering,
dynamic lighting, and environment effects.

![3D scene in the Doriax editor](../assets/screenshots/editor-3d-scene.png)

## Models

Doriax loads 3D models in **GLTF** and **OBJ** formats. Import a model as a resource and
add it to a scene as an entity, then position it with its transform.

Models support:

- **Skeletal animation** — animate rigged characters via bones
- **Morph targets** — blend between mesh shapes for facial animation and deformation

![Bone and skeletal animation tools](../assets/screenshots/editor-bones.png)

## PBR materials

Rendering is **physically based (PBR)**, producing realistic surfaces that respond
correctly to lighting. Materials drive how light interacts with each surface, supporting
photorealistic results.

Materials can use albedo, normal, roughness, metallic, and emission data. Imported
GLTF materials are converted into the engine material representation during loading;
editor-created materials are serialized with the project and baked into exported
output.

### Shared material files (`.material`)

Each mesh submesh can reference a standalone **`.material`** file in your project instead
of embedding values only inside the scene. Multiple meshes can link to the same file so
they always stay in sync — change the file once and every linked mesh updates.

**Create a material file from the editor:**

1. Select a mesh and open its **Material** row in the Properties window.
2. Tune base colour, textures, metallic, and roughness as needed.
3. **Drag the material preview** from Properties into the [Resources Browser](../editor/resources.md).
4. The editor creates `Material.material` (or `Material_1.material`, etc.) in the folder
   you drop on and **links** the submesh to that file.

**Apply an existing material file:**

- Drag a `.material` file from the Resources Browser onto a mesh in the [Scene view](../editor/scene-view.md), or
- Drop it onto the **Material** field in Properties (live preview while hovering).

Linked materials reload automatically when the file changes on disk. Use the **unlink**
button (chain icon) next to the material name in Properties to copy the values back into
the scene as a local, unlinked material.

See [Resources Browser — Material files](../editor/resources.md#material-files) and
[Properties — Mesh materials](../editor/properties.md#mesh-materials-and-ibl) for the
full workflow.

## Lighting and shadows

Doriax supports multiple light types with **dynamic shadows**, so moving objects cast
and receive shadows in real time.

| Light type | Best use |
| --- | --- |
| Directional | Sunlight or broad outdoor lighting |
| Point | Lamps, torches, explosions, and local lights |
| Spot | Flashlights, cones, and focused effects |

The runtime supports up to six active lights and cascaded shadow maps for directional
lighting. Tune edge smoothness with `Scene::setShadowQuality` (`NONE` / `LOW` / `MEDIUM` /
`HIGH` PCF filtering).

Enable **screen-space ambient occlusion** with `Scene::setSSAOEnabled(true)` to add soft
contact shading in creases and corners. It affects ambient/indirect light only — see
[Rendering Pipeline — Ambient occlusion (SSAO)](rendering-pipeline.md#ambient-occlusion-ssao).

## Environment

Add atmosphere to your scenes with:

- **Fog** — depth-based atmospheric fog
- **Sky system** — a configurable cubemap background that also drives **image-based
  lighting (IBL)** for reflective surfaces

### Sky and reflections

A **Sky** entity provides the scene background and the lighting environment for IBL.
Assign a cubemap texture (six faces or a single cross layout). Meshes that should pick up
sky reflections and indirect colour need **Receive IBL** enabled on their Mesh
component — see [Rendering Pipeline — IBL](rendering-pipeline.md#image-based-lighting-ibl).

Use **Visible** on the Sky component when you want IBL without drawing the sky dome
(for example, a studio HDR used only for reflections). The sky texture still generates
irradiance and prefiltered maps either way.

IBL gives soft, environment-wide reflections suited to curved and rough surfaces. For a
**sharp, mirror-like reflection on a flat surface**, add a **Mirror** instead — see below.

### Mirrors

For a true planar reflection on a flat surface — a mirror, still water, or a polished
floor — add a **Mirror** from the Structure panel's create menu. It produces an upright
reflective wall that reflects the scene from the viewer's mirrored viewpoint, with no
camera or texture setup required. See
[Rendering Pipeline — Mirrors and planar reflections](rendering-pipeline.md#mirrors-and-planar-reflections)
for how it works and its performance cost.

## Cameras

Cameras define the viewpoint into a 3D scene. Position and orient a camera entity, and
set it as the scene's active camera to control what the player sees.

![Camera and build tools](../assets/screenshots/editor-camera.png)

Cameras can be perspective, orthographic, or UI cameras. A scene owns an active camera
entity; editor scene cameras are separate from game cameras so you can navigate while
preserving the player's view.

## Additional features

The runtime also supports [particle systems](particles.md), [terrain](terrain.md) with
level-of-detail (LOD), and [mesh instancing](rendering-pipeline.md#gpu-instancing) for
efficiently rendering many copies of the same geometry.

## Next steps

Add interactivity with [Physics](physics.md), or learn how to ship your game in
[Export Window](../editor/export.md).
