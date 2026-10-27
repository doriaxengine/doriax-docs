---
description: FogComponent API reference (C++ and Lua).
---

# FogComponent

The data behind [Fog](fog.md). In Lua, get it with `fog:getFogComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua |
| `color` | C++ \| Lua |
| `density` | C++ \| Lua |
| `linearStart` | C++ \| Lua |
| `linearEnd` | C++ \| Lua |

`color` is linear here, while the [Fog](fog.md) setter takes sRGB.
