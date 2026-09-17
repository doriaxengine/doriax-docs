---
description: TilemapComponent API reference (C++ and Lua).
---

# TilemapComponent

`TilemapComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `width` | C++ \| Lua |
| `height` | C++ \| Lua |
| `automaticFlipY` | C++ \| Lua |
| `flipY` | C++ \| Lua |
| `textureScaleFactor` | C++ \| Lua |
| `reserveTiles` | C++ \| Lua |
| `numTiles` | C++ \| Lua |
| `needUpdateTilemap` | C++ \| Lua |
| `tilesRect` | C++ |
| `tiles` | C++ |
