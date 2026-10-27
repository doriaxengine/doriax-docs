---
description: RenderSystem API reference (C++ and Lua).
---

# RenderSystem

**Inherits:** [SubSystem](subsystem.md)

Draws the scene (meshes, lights, UI, particles).

## Methods

| Name | Languages |
| --- | --- |
| `updateCameraSize` | C++ \| Lua |
| `isAllLoaded` | C++ \| Lua |

`isAllLoaded()` is true once every mesh, UI element, and other drawable in the scene has
loaded. [SceneManager](scenemanager.md) `loadingProgress` reports the same count, together
with sounds, as a fraction.
