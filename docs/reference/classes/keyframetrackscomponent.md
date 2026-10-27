---
description: KeyframeTracksComponent API reference (C++ and Lua).
---

# KeyframeTracksComponent

The key times and easings shared by a [KeyframeTracks](keyframetracks.md) action and the track types built on it. In Lua, get it with `tracks:getKeyframeTracksComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `times` | C++ \| Lua |
| `easings` | C++ \| Lua |
| `loop` | C++ \| Lua |
| `relative` | C++ \| Lua |
| `index` | C++ \| Lua (read-only) |
| `interpolation` | C++ \| Lua (read-only) |

`index` and `interpolation` are playback state. In Lua, lists are copies: assign the changed table back.
