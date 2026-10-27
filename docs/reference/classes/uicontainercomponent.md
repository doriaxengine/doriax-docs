---
description: UIContainerComponent API reference (C++ and Lua).
---

# UIContainerComponent

The data behind a [Container](container.md). In Lua, get it with `container:getUIContainerComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua |
| `useAllWrapSpace` | C++ \| Lua |
| `wrapCellWidth` | C++ \| Lua |
| `wrapCellHeight` | C++ \| Lua |
| `numBoxes` | C++ \| Lua (read-only) |
