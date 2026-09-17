---
description: ProgressbarComponent API reference (C++ and Lua).
---

# ProgressbarComponent

`ProgressbarComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `fill` | C++ \| Lua (read-only) |
| `type` | C++ \| Lua |
| `value` | C++ \| Lua |
| `fillMarginLeft` | C++ \| Lua |
| `fillMarginRight` | C++ \| Lua |
| `fillMarginTop` | C++ \| Lua |
| `fillMarginBottom` | C++ \| Lua |
| `needUpdateProgressbar` | C++ \| Lua |
