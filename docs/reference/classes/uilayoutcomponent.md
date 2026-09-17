---
description: UILayoutComponent API reference (C++ and Lua).
---

# UILayoutComponent

`UILayoutComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `width` | C++ \| Lua |
| `height` | C++ \| Lua |
| `anchorPointLeft` | C++ \| Lua |
| `anchorPointTop` | C++ \| Lua |
| `anchorPointRight` | C++ \| Lua |
| `anchorPointBottom` | C++ \| Lua |
| `anchorOffsetLeft` | C++ \| Lua |
| `anchorOffsetTop` | C++ \| Lua |
| `anchorOffsetRight` | C++ \| Lua |
| `anchorOffsetBottom` | C++ \| Lua |
| `positionOffset` | C++ \| Lua |
| `anchorPreset` | C++ \| Lua |
| `usingAnchors` | C++ \| Lua |
| `panel` | C++ \| Lua (read-only) |
| `containerBoxIndex` | C++ \| Lua (read-only) |
| `scissor` | C++ \| Lua |
| `ignoreScissor` | C++ \| Lua |
| `ignoreEvents` | C++ \| Lua |
| `needUpdateSizes` | C++ \| Lua |
