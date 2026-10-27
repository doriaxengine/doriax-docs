---
description: Transform API reference (C++ and Lua).
---

# Transform

Position, rotation, and scale of an entity, plus the world values and matrices the scene derives from them. Every [Object](object.md) has one. In Lua, get it with `object:getTransform()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `position` | C++ \| Lua |
| `rotation` | C++ \| Lua |
| `scale` | C++ \| Lua |
| `worldPosition` | C++ \| Lua (read-only) |
| `worldRotation` | C++ \| Lua (read-only) |
| `worldScale` | C++ \| Lua (read-only) |
| `localMatrix` | C++ \| Lua (read-only) |
| `modelMatrix` | C++ \| Lua (read-only) |
| `visible` | C++ \| Lua |
| `parent` | C++ \| Lua (read-only) |
| `distanceToCamera` | C++ \| Lua (read-only) |
| `billboardRotation` | C++ \| Lua |
| `billboard` | C++ \| Lua |
| `fakeBillboard` | C++ \| Lua |
| `cylindricalBillboard` | C++ \| Lua |
| `needUpdateChildVisibility` | C++ \| Lua |
| `needUpdate` | C++ \| Lua |

Set `needUpdate` after writing `position`, `rotation`, `scale`, or `billboardRotation`, and `needUpdateChildVisibility` after `visible`. Reparent with [`addChild`](object.md#addchild).
