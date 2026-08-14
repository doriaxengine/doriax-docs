---
description: Bone API reference (C++ and Lua).
---

# Bone

**Inherits:** [Object](object.md)  
**C++ type:** `Bone`

Skeletal bone in a hierarchy. On GLTF files that import the
[full node tree](../../manual/3d-graphics.md#gltf-node-hierarchy), the bone is the same
entity as that glTF joint node (it also has a `Transform`). `Model::getBone` finds it
by joint name or by glTF node index.
