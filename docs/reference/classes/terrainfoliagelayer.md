---
description: TerrainFoliageLayer API reference (C++ and Lua).
---

# TerrainFoliageLayer

One foliage layer of a [Terrain](terrain.md): which model it scatters, where, and how densely. `TerrainFoliageLayer()` creates one in Lua.

## Properties

| Name | Languages |
| --- | --- |
| `meshPath` | C++ \| Lua |
| `densityMap` | C++ \| Lua |
| `density` | C++ \| Lua |
| `minScale` | C++ \| Lua |
| `maxScale` | C++ \| Lua |
| `rotationJitter` | C++ \| Lua |
| `alignToNormal` | C++ \| Lua |
| `minSlope` | C++ \| Lua |
| `maxSlope` | C++ \| Lua |
| `minHeight` | C++ \| Lua |
| `maxHeight` | C++ \| Lua |
| `drawDistance` | C++ \| Lua |
| `minDrawDistance` | C++ \| Lua |
| `seed` | C++ \| Lua |
| `castShadows` | C++ \| Lua |

Slopes are in degrees. `minHeight` and `maxHeight` are fractions of the terrain's `maxHeight`.
