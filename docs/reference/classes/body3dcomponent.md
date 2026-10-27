---
description: Body3DComponent API reference (C++ and Lua).
---

# Body3DComponent

The data a [Body3D](body3d.md) is built from. In Lua, get it with `body:getBody3DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `numShapes` | C++ \| Lua (read-only) |
| `overrideMassProperties` | C++ \| Lua |
| `solidBoxSize` | C++ \| Lua |
| `solidBoxDensity` | C++ \| Lua |
| `type` | C++ \| Lua |
| `motionQuality` | C++ \| Lua |
| `gravityFactor` | C++ \| Lua |
| `buoyancy` | C++ \| Lua |
| `waterDrag` | C++ \| Lua |
| `waterAngularDrag` | C++ \| Lua |
| `allowedDOFs` | C++ \| Lua |
| `sensor` | C++ \| Lua |
| `needReloadBody` | C++ \| Lua |
| `needUpdateShapes` | C++ \| Lua |

Set `needReloadBody` to rebuild the body from these fields. To change shapes, or a live body without a rebuild, use the [Body3D](body3d.md) methods. `allowedDOFs` is a bit mask: X, Y, Z translation, then X, Y, Z rotation.
