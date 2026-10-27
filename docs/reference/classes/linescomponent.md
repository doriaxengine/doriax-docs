---
description: LinesComponent API reference (C++ and Lua).
---

# LinesComponent

The data behind [Lines](lines.md). In Lua, get it with `lines:getLinesComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `lines` | C++ \| Lua |
| `maxLines` | C++ \| Lua (read-only) |
| `customShader` | C++ \| Lua |
| `needUpdateBuffer` | C++ \| Lua |
| `needReload` | C++ \| Lua |

`lines` is a list of [LineData](linedata.md). Set `needUpdateBuffer` after assigning it. Only the first `maxLines` are drawn; raise it with [`Lines.maxLines`](lines.md#maxlines). Set `needReload` after changing `customShader`. In Lua, lists are copies: assign the changed table back.
