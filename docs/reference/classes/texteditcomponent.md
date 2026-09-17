---
description: TextEditComponent API reference (C++ and Lua).
---

# TextEditComponent

`TextEditComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `text` | C++ \| Lua (read-only) |
| `selection` | C++ \| Lua (read-only) |
| `cursor` | C++ \| Lua (read-only) |
| `cursorBlink` | C++ \| Lua |
| `cursorWidth` | C++ \| Lua |
| `cursorColor` | C++ \| Lua |
| `selectionColor` | C++ \| Lua |
| `placeholderColor` | C++ \| Lua |
| `placeholder` | C++ \| Lua |
| `passwordChar` | C++ \| Lua |
| `cursorIndex` | C++ \| Lua |
| `selectionAnchor` | C++ \| Lua |
| `scrollOffset` | C++ \| Lua |
| `disabled` | C++ \| Lua |
| `password` | C++ \| Lua |
| `onChange` | C++ \| Lua |
| `onSubmit` | C++ \| Lua |
| `needUpdateTextEdit` | C++ \| Lua |
