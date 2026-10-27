---
description: TextComponent API reference (C++ and Lua).
---

# TextComponent

The data behind a [Text](text.md). In Lua, get it with `text:getTextComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `font` | C++ \| Lua |
| `text` | C++ \| Lua |
| `fontSize` | C++ \| Lua |
| `multiline` | C++ \| Lua |
| `maxTextSize` | C++ \| Lua |
| `charPositions` | C++ \| Lua (read-only) |
| `fixedWidth` | C++ \| Lua |
| `fixedHeight` | C++ \| Lua |
| `pivotBaseline` | C++ \| Lua |
| `pivotCentered` | C++ \| Lua |
| `needReloadAtlas` | C++ \| Lua |
| `needUpdateText` | C++ \| Lua |

Set `needUpdateText` after changing the text or layout fields, and also `needReloadAtlas` after changing `font` or `fontSize`. `font` comes to Lua as a table of four font paths, and takes back only a table of four.
