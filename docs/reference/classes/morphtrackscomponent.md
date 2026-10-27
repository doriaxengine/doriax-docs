---
description: MorphTracksComponent API reference (C++ and Lua).
---

# MorphTracksComponent

The key values of a [MorphTracks](morphtracks.md) action, one list of weights per key. In Lua, get it with `tracks:getMorphTracksComponent()`.

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
