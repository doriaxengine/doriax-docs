---
description: TranslateTracksComponent API reference (C++ and Lua).
---

# TranslateTracksComponent

The key values of a [TranslateTracks](translatetracks.md) action. In Lua, get it with `tracks:getTranslateTracksComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `values` | C++ \| Lua |
| `inTangents` | C++ \| Lua |
| `outTangents` | C++ \| Lua |

In Lua, lists are copies: assign the changed table back.
