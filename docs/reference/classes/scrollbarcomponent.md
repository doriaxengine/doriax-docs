---
description: ScrollbarComponent API reference (C++ and Lua).
---

# ScrollbarComponent

`ScrollbarComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `bar` | C++ \| Lua (read-only) |
| `type` | C++ \| Lua |
| `onChange` | C++ \| Lua |
| `barSize` | C++ \| Lua |
| `step` | C++ \| Lua |
| `barMarginLeft` | C++ \| Lua |
| `barMarginRight` | C++ \| Lua |
| `barMarginTop` | C++ \| Lua |
| `barMarginBottom` | C++ \| Lua |
| `barPointerDown` | C++ \| Lua (read-only) |
| `barPointerPos` | C++ \| Lua (read-only) |
| `needUpdateScrollbar` | C++ \| Lua |
