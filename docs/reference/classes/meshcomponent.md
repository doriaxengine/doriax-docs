---
description: MeshComponent API reference (C++ and Lua).
---

# MeshComponent

The data behind a [Mesh](mesh.md) and the objects built on it, such as [Sprite](sprite.md), [Model](model.md), and [Terrain](terrain.md). In Lua, get it with `mesh:getMeshComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `vertexCount` | C++ \| Lua (read-only) |
| `numSubmeshes` | C++ \| Lua (read-only) |
| `customShader` | C++ \| Lua |
| `customDepthShader` | C++ \| Lua |
| `aabb` | C++ \| Lua (read-only) |
| `worldAABB` | C++ \| Lua (read-only) |
| `receiveLights` | C++ \| Lua |
| `receiveIBL` | C++ \| Lua |
| `castShadows` | C++ \| Lua |
| `receiveShadows` | C++ \| Lua |
| `shadowsBillboard` | C++ \| Lua |
| `renderInReflectionProbes` | C++ \| Lua |
| `transparent` | C++ \| Lua |
| `autoTransparency` | C++ \| Lua |
| `lodEnabled` | C++ \| Lua |
| `lodBias` | C++ \| Lua |
| `cullingMode` | C++ \| Lua |
| `windingOrder` | C++ \| Lua |
| `needUpdateAABB` | C++ \| Lua |
| `needUpdateBuffer` | C++ \| Lua |
| `needReload` | C++ \| Lua |

Submeshes, materials, vertex buffers, and morph weights are C++ only; from Lua, use the [Mesh](mesh.md) methods for them.
