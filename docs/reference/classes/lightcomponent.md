---
description: LightComponent API reference (C++ and Lua).
---

# LightComponent

The data behind a [Light](light.md). In Lua, get it with `light:getLightComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua |
| `direction` | C++ \| Lua |
| `worldDirection` | C++ \| Lua (read-only) |
| `color` | C++ \| Lua |
| `range` | C++ \| Lua |
| `intensity` | C++ \| Lua |
| `innerConeCos` | C++ \| Lua |
| `outerConeCos` | C++ \| Lua |
| `spotMask` | C++ \| Lua (read-only) |
| `shadows` | C++ \| Lua |
| `automaticShadowCamera` | C++ \| Lua |
| `shadowBias` | C++ \| Lua |
| `shadowNormalBias` | C++ \| Lua |
| `mapResolution` | C++ \| Lua |
| `shadowCameraNearFar` | C++ \| Lua |
| `numShadowCascades` | C++ \| Lua |
| `needUpdateShadowCamera` | C++ \| Lua |
| `needUpdateShadowMap` | C++ \| Lua |

`color` is linear here, while the [Light](light.md) setter takes sRGB. `innerConeCos` and `outerConeCos` hold the cosine of half the spot cone angles. Change `type`, `shadows`, and `mapResolution` through the [Light](light.md) setters, which also rebuild the meshes' shaders.
