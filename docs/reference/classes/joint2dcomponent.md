---
description: Joint2DComponent API reference (C++ and Lua).
---

# Joint2DComponent

The data a [Joint2D](joint2d.md) is built from. In Lua, get it with `joint:getJoint2DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua |
| `bodyA` | C++ \| Lua |
| `bodyB` | C++ \| Lua |
| `anchorA` | C++ \| Lua |
| `anchorB` | C++ \| Lua |
| `axis` | C++ \| Lua |
| `target` | C++ \| Lua |
| `autoAnchors` | C++ \| Lua |
| `rope` | C++ \| Lua |
| `needUpdateJoint` | C++ \| Lua |

The [Joint2D](joint2d.md) setters fill these fields and build the joint. Set `needUpdateJoint` to rebuild it from these fields.
