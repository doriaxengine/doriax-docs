---
description: Joint3DComponent API reference (C++ and Lua).
---

# Joint3DComponent

The data a [Joint3D](joint3d.md) is built from. In Lua, get it with `joint:getJoint3DComponent()`.

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
| `anchor` | C++ \| Lua |
| `axis` | C++ \| Lua |
| `normal` | C++ \| Lua |
| `twistAxis` | C++ \| Lua |
| `planeAxis` | C++ \| Lua |
| `axisX` | C++ \| Lua |
| `axisY` | C++ \| Lua |
| `limitsMin` | C++ \| Lua |
| `limitsMax` | C++ \| Lua |
| `normalHalfConeAngle` | C++ \| Lua |
| `planeHalfConeAngle` | C++ \| Lua |
| `twistMinAngle` | C++ \| Lua |
| `twistMaxAngle` | C++ \| Lua |
| `fixedPointA` | C++ \| Lua |
| `fixedPointB` | C++ \| Lua |
| `hingeA` | C++ \| Lua |
| `hingeB` | C++ \| Lua |
| `hinge` | C++ \| Lua |
| `slider` | C++ \| Lua |
| `numTeethGearA` | C++ \| Lua |
| `numTeethGearB` | C++ \| Lua |
| `numTeethRack` | C++ \| Lua |
| `numTeethGear` | C++ \| Lua |
| `rackLength` | C++ \| Lua |
| `pathPoints` | C++ \| Lua |
| `pathPosition` | C++ \| Lua |
| `isLooping` | C++ \| Lua |
| `autoAnchors` | C++ \| Lua |
| `needUpdateJoint` | C++ \| Lua |

The [Joint3D](joint3d.md) setters fill these fields and build the joint. Set `needUpdateJoint` to rebuild it from these fields. `pathPoints` comes to Lua as a table copy.
