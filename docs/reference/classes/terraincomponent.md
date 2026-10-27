---
description: TerrainComponent API reference (C++ and Lua).
---

# TerrainComponent

The data behind a [Terrain](terrain.md). In Lua, get it with `terrain:getTerrainComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `heightMap` | C++ \| Lua |
| `blendMaps` | C++ \| Lua |
| `surfaceLayers` | C++ \| Lua |
| `foliageLayers` | C++ \| Lua |
| `foliageDistanceScale` | C++ \| Lua |
| `heightMapLoaded` | C++ \| Lua (read-only) |
| `offset` | C++ \| Lua |
| `terrainSize` | C++ \| Lua |
| `maxHeight` | C++ \| Lua |
| `textureBaseTiles` | C++ \| Lua |
| `textureDetailTiles` | C++ \| Lua |
| `autoSetRanges` | C++ \| Lua (read-only) |
| `ranges` | C++ \| Lua (read-only) |
| `resolution` | C++ \| Lua (read-only) |
| `rootGridSize` | C++ \| Lua (read-only) |
| `levels` | C++ \| Lua (read-only) |
| `needUpdateTerrain` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `needUpdateFoliage` | C++ \| Lua |

Change `resolution`, `rootGridSize`, and `levels` with the [Terrain](terrain.md) setters, which rebuild the terrain. Set `needUpdateTexture` after changing the maps or surface layers, and `needUpdateFoliage` after changing `foliageLayers`. In Lua, lists are copies: assign the changed table back.
