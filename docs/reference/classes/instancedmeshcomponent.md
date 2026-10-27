---
description: InstancedMeshComponent API reference (C++ and Lua).
---

# InstancedMeshComponent

The instances of a [Mesh](mesh.md) drawn in a single call. In Lua, `mesh:getInstancedMeshComponent()` returns it, or `nil` until the mesh is instanced with `createInstancedMesh()` or `addInstance()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `instances` | C++ \| Lua |
| `maxInstances` | C++ \| Lua (read-only) |
| `numVisible` | C++ \| Lua (read-only) |
| `cullInstances` | C++ \| Lua |
| `cullDistance` | C++ \| Lua |
| `distanceFade` | C++ \| Lua |
| `fadeStart` | C++ \| Lua |
| `fadeEnd` | C++ \| Lua |
| `instancedBillboard` | C++ \| Lua |
| `instancedCylindricalBillboard` | C++ \| Lua |
| `needUpdateBuffer` | C++ \| Lua |
| `needUpdateInstances` | C++ \| Lua |

`instances` is a list of [InstanceData](instancedata.md). Set `needUpdateInstances` after assigning it. Only the first `maxInstances` are drawn; raise it with [`Mesh.maxInstances`](mesh.md). In Lua, lists are copies: assign the changed table back.
