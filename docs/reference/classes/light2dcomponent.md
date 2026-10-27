---
description: Light2DComponent API reference (C++ and Lua).
---

# Light2DComponent

The data behind a [Light2D](light2d.md). In Lua, get it with `light:getLight2DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `color` | C++ \| Lua |
| `intensity` | C++ \| Lua |
| `range` | C++ \| Lua |
| `falloff` | C++ \| Lua |
| `height` | C++ \| Lua |
| `shadows` | C++ \| Lua |
| `shadowBias` | C++ \| Lua |
| `shadowSoftness` | C++ \| Lua |
| `mapResolution` | C++ \| Lua |

`color` is linear here, while the [Light2D](light2d.md) setter takes sRGB.
