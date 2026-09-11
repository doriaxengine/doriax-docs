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
| `setSpriteFrameRect` | C++ |
| `canMergeStaticModel` | C++ |
| `canEditModelHierarchy` | C++ |
| `loadGLTF` | C++ \| Lua |
| `loadOBJ` | C++ \| Lua |
| `createInstancedMesh` | C++ \| Lua |
| `removeInstancedMesh` | C++ \| Lua |
| `hasPendingAsyncModelLoads` | C++ |
| `isAsyncModelLoadPending` | C++ |
| `cancelAsyncModelLoad` | C++ |
| `cancelAsyncModelLoads` | C++ |
| `cancelAllAsyncModelLoads` | C++ |

## Sprite frame rectangles

`static void setSpriteFrameRect(MeshComponent& mesh, SpriteComponent& sprite, Rect frameRect)`
applies a frame rectangle to the sprite's first submesh. Both components must belong
to the same sprite. This C++ helper is shared by `Sprite::setFrame()` and sprite
animation updates; gameplay code normally uses [Sprite.setFrame](sprite.md#setframe).

Rectangles with all four values in `[0, 1]` are treated as UVs. Other rectangles
are converted from pixels using the texture dimensions. If dimensions are not yet
available, the helper stores one pending rectangle on the sprite for mesh updates
to retry. Subsequent calls replace that request; requests are not queued. Frame
selection also works before the sprite geometry has been built.

## Static model hierarchy

`bool canMergeStaticModel(const ModelComponent& model, const MeshComponent& mesh, std::string* reason = nullptr) const` reports whether a loaded GLTF can flatten its mesh nodes into the root entity (`ModelComponent::mergeStaticMeshes`). Returns `false` with an optional reason for skinned, animated, morph-target, or single-node models, and when the flatten would exceed the root submesh limit. Animated models and models with more than one skin import a full node tree rather than mesh children only — see [3D Graphics — GLTF node hierarchy](../../manual/3d-graphics.md#gltf-node-hierarchy) and [Merging static model meshes](../../manual/3d-graphics.md#merging-static-model-meshes).

`bool canEditModelHierarchy(const ModelComponent& model, std::string* reason = nullptr) const` reports whether the model's child mesh entities may be reparented among themselves. Returns `false` with an optional reason while the model is still loading, when it has no separate mesh parts (a single mesh or a merged model), and for models that import a node hierarchy or carry a skin, whose child transforms the file drives. The editor uses it to decide which parts can be [rearranged in the Structure panel](../../editor/structure.md#organizing-the-parts-of-a-static-model).

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
