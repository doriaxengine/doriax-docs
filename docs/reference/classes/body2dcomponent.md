---
description: Body2DComponent API reference (C++ and Lua).
---

# Body2DComponent

The data a [Body2D](body2d.md) is built from. In Lua, get it with `body:getBody2DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `numShapes` | C++ \| Lua (read-only) |
| `type` | C++ \| Lua |
| `needReloadBody` | C++ \| Lua |
| `needUpdateShapes` | C++ \| Lua |

Set `needReloadBody` to rebuild the body from these fields. To change shapes, or a live body without a rebuild, use the [Body2D](body2d.md) methods.
