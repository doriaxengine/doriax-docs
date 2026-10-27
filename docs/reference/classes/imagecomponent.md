---
description: ImageComponent API reference (C++ and Lua).
---

# ImageComponent

The nine-patch settings of an [Image](image.md). In Lua, get it with `image:getImageComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `patchMarginLeft` | C++ \| Lua |
| `patchMarginRight` | C++ \| Lua |
| `patchMarginTop` | C++ \| Lua |
| `patchMarginBottom` | C++ \| Lua |
| `textureScaleFactor` | C++ \| Lua |
| `needUpdatePatches` | C++ \| Lua |

Set `needUpdatePatches` after changing the margins or `textureScaleFactor`.
