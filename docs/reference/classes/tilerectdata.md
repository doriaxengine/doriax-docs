---
description: TileRectData API reference (C++ and Lua).
---

# TileRectData

`TileRectData` API exposed to Lua and C++ gameplay code.

## Properties

| Name | Languages |
| --- | --- |
| `name` | C++ \| Lua |
| `submeshId` | C++ \| Lua |
| `rect` | C++ \| Lua |
| `collision` | C++ \| Lua |

`collision` is `true` by default. Set it to `false` to leave this rect's tiles out of a [tilemap shape](body2d.md#createtilemapshape).
