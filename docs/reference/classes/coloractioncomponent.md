---
description: ColorActionComponent API reference (C++ and Lua).
---

# ColorActionComponent

The start and end colors of a [ColorAction](coloraction.md). In Lua, get it with `action:getColorActionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `endColor` | C++ \| Lua |
| `startColor` | C++ \| Lua |
| `useSRGB` | C++ \| Lua |

`useSRGB` tells whether the two colors are sRGB.
