---
description: PositionActionComponent API reference (C++ and Lua).
---

# PositionActionComponent

The start and end positions of a [PositionAction](positionaction.md). In Lua, get it with `action:getPositionActionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `endPosition` | C++ \| Lua |
| `startPosition` | C++ \| Lua |
