---
description: Occluder2DComponent API reference (C++ and Lua).
---

# Occluder2DComponent

The data behind an [Occluder2D](occluder2d.md). In Lua, get it with `occluder:getOccluder2DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `shape` | C++ \| Lua |
| `points` | C++ \| Lua |
| `closed` | C++ \| Lua |
| `enabled` | C++ \| Lua |

`points` is used when `shape` is `Occluder2DShape.POLYGON`. In Lua, lists are copies: assign the changed table back.
