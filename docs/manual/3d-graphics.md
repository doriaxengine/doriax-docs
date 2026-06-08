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

## Lighting and shadows

Doriax supports multiple light types with **dynamic shadows**, so moving objects cast
and receive shadows in real time.

| Light type | Best use |
| --- | --- |
| Directional | Sunlight or broad outdoor lighting |
| Point | Lamps, torches, explosions, and local lights |
| Spot | Flashlights, cones, and focused effects |

The runtime supports up to six active lights and cascaded shadow maps for directional
lighting. Use `Scene::setShadowsPCF(true)` when you want smoother shadow filtering.

## Environment

Add atmosphere to your scenes with:

- **Fog** — depth-based atmospheric fog
- **Sky system** — a configurable sky for outdoor environments

## Cameras

Cameras define the viewpoint into a 3D scene. Position and orient a camera entity, and
set it as the scene's active camera to control what the player sees.

![Camera and build tools](../assets/screenshots/editor-camera.png)

Cameras can be perspective, orthographic, or UI cameras. A scene owns an active camera
entity; editor scene cameras are separate from game cameras so you can navigate while
preserving the player's view.

## Additional features

The runtime also supports particle systems, terrain with level-of-detail (LOD), and
mesh instancing for efficiently rendering many copies of the same geometry.

!!! note
    Terrain and particle authoring are available at the engine/runtime level; visual
    editor tooling for them is still being integrated.

## Next steps

Add interactivity with [Physics](physics.md), or learn how to ship your game in
[Export Window](../editor/export.md).
