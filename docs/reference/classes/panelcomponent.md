---
description: PanelComponent API reference (C++ and Lua).
---

# PanelComponent

`PanelComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `headerimage` | C++ \| Lua (read-only) |
| `headercontainer` | C++ \| Lua (read-only) |
| `headertext` | C++ \| Lua (read-only) |
| `titleAnchorPreset` | C++ \| Lua |
| `minWidth` | C++ \| Lua |
| `minHeight` | C++ \| Lua |
| `resizeMargin` | C++ \| Lua |
| `canMove` | C++ \| Lua |
| `canResize` | C++ \| Lua |
| `canBringToFront` | C++ \| Lua |
| `headerPointerDown` | C++ \| Lua (read-only) |
| `onMove` | C++ \| Lua |
| `onResize` | C++ \| Lua |
| `needUpdatePanel` | C++ \| Lua |
