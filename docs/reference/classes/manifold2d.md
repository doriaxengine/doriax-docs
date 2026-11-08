---
description: Manifold2D API reference (C++ and Lua).
---

# Manifold2D

`Manifold2D` API exposed to Lua and C++ gameplay code.

## Methods

| Name | Languages |
| --- | --- |
| `getManifoldPointAnchorA` | C++ \| Lua |
| `getManifoldPointAnchorB` | C++ \| Lua |
| `getManifoldPointPosition` | C++ \| Lua |
| `getManifoldPointNormalImpulse` | C++ \| Lua |
| `getManifoldPointNormalVelocity` | C++ \| Lua |
| `getManifoldPointTangentImpulse` | C++ \| Lua |
| `getManifoldPointSeparation` | C++ \| Lua |
| `isManifoldPointPersisted` | C++ \| Lua |
| `getNormal` | C++ \| Lua |
| `getPointCount` | C++ \| Lua |

Positions, anchors and separation are in points and the normal velocity in points per
second, like [Body2D](body2d.md#linearvelocity). Impulses stay in Box2D units (N·s). The
normal is a unit vector from shape A to shape B. Anchors start from each body's origin in
`preSolve2D` and from its center of mass in a contact from `getBodyContacts`;
`getManifoldPointPosition` is the world point either way. A contact keeps the position it had
when it was read, even if its body moves or is removed afterwards. A point index from `0` to
`getPointCount() - 1` is valid; another one logs an error and returns zero.
