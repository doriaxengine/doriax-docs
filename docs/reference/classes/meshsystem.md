---
description: MeshSystem API reference (C++ and Lua).
---

# MeshSystem

Creates meshes, loads models, builds sprites and tilemaps.

## Methods

| Name | Languages |
| --- | --- |
| `createPlane` | C++ \| Lua |
| `createBox` | C++ \| Lua |
| `createSphere` | C++ \| Lua |
| `createCylinder` | C++ \| Lua |
| `createCapsule` | C++ \| Lua |
| `createTorus` | C++ \| Lua |
| `loadGLTF` | C++ \| Lua |
| `loadOBJ` | C++ \| Lua |
| `createInstancedMesh` | C++ \| Lua |
| `removeInstancedMesh` | C++ \| Lua |
| `hasPendingAsyncModelLoads` | C++ |
| `isAsyncModelLoadPending` | C++ |
| `cancelAsyncModelLoad` | C++ |
| `cancelAsyncModelLoads` | C++ |
| `cancelAllAsyncModelLoads` | C++ |

## Asynchronous model-load control

These C++-only methods inspect or stop model loads started by the asynchronous resource
pipeline:

| Method | Scope |
| --- | --- |
| `bool hasPendingAsyncModelLoads() const` | Reports whether this system's scene has pending model work |
| `bool isAsyncModelLoadPending(Entity entity, const std::string& filename) const` | Reports whether the named model is pending for this system's scene |
| `void cancelAsyncModelLoad(Entity entity, const std::string& filename)` | Stops the named pending load from being applied |
| `void cancelAsyncModelLoads()` | Stops all pending model loads for this system's scene |
| `static void cancelAllAsyncModelLoads()` | Stops pending model loads across all scenes |

Cancellation is synchronous: if a worker is already decoding a model, the cancellation
method waits for that task to finish, removes its pending result, and marks its resource
build as failed before returning. This guarantees that the worker cannot outlive scene,
project, or resource-pool teardown.
