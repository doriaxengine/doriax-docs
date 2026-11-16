---
description: Contact3D API reference (C++ and Lua).
---

# Contact3D

3D contact data.

## Properties

| Name | Languages |
| --- | --- |
| `combinedFriction` | C++ \| Lua |
| `combinedRestitution` | C++ \| Lua |
| `sensor` | C++ \| Lua |

## Methods

| Name | Languages |
| --- | --- |
| `getBaseOffset` | C++ \| Lua |
| `getWorldSpaceNormal` | C++ \| Lua |
| `getPenetrationDepth` | C++ \| Lua |
| `getShapeIndex1` | C++ \| Lua |
| `getShapeIndex2` | C++ \| Lua |
| `getRelativeContactPointsOnA` | C++ \| Lua |
| `getRelativeContactPointsOnB` | C++ \| Lua |

## Contacts of a 3D character

A contact that a [3D character](character3d.md) makes as it moves has one point, where its
capsule touches: `getBaseOffset()` is that point, its relative points are zero,
`getWorldSpaceNormal()` points from the character to the body, and `getShapeIndex1()` is `0`.
`combinedFriction` and `combinedRestitution` read the body's own values. Setting them, or
`sensor`, changes nothing, as no solver moves the character.
