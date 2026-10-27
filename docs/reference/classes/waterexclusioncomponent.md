---
description: WaterExclusionComponent API reference (C++ and Lua).
---

# WaterExclusionComponent

The data behind a [WaterExclusion](waterexclusion.md). In Lua, get it with `exclusion:getWaterExclusionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `shape` | C++ \| Lua |
| `center` | C++ \| Lua |
| `size` | C++ \| Lua |
| `aabb` | C++ \| Lua (read-only) |
| `worldAABB` | C++ \| Lua (read-only) |

`center` and `size` place a `BOX` or `SPHERE` shape. A `HULL` is built from the entity's meshes.
