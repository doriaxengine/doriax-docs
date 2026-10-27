---
description: ModelComponent API reference (C++ and Lua).
---

# ModelComponent

The data behind a [Model](model.md). In Lua, get it with `model:getModelComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `skeleton` | C++ \| Lua (read-only) |
| `bonesNameMapping` | C++ \| Lua (read-only) |
| `morphNameMapping` | C++ \| Lua (read-only) |
| `animations` | C++ \| Lua (read-only) |
| `filename` | C++ \| Lua |
| `mergeStaticMeshes` | C++ \| Lua |
| `needUpdateModel` | C++ \| Lua |

`bonesNameMapping` maps bone names to entities and `morphNameMapping` maps morph target names to indices. Both come to Lua as tables. `animations` lists the model's [Animation](animation.md) entities.
