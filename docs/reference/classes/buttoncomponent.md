---
description: ButtonComponent API reference (C++ and Lua).
---

# ButtonComponent

`ButtonComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `label` | C++ \| Lua (read-only) |
| `textureNormal` | C++ \| Lua |
| `textureHovered` | C++ \| Lua |
| `texturePressed` | C++ \| Lua |
| `textureDisabled` | C++ \| Lua |
| `colorNormal` | C++ \| Lua |
| `colorHovered` | C++ \| Lua |
| `colorPressed` | C++ \| Lua |
| `colorDisabled` | C++ \| Lua |
| `onPress` | C++ \| Lua |
| `onRelease` | C++ \| Lua |
| `pressed` | C++ \| Lua (read-only) |
| `hovered` | C++ \| Lua (read-only) |
| `disabled` | C++ \| Lua |
| `needUpdateButton` | C++ \| Lua |
