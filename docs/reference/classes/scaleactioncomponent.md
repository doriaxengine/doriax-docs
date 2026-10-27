---
description: ScaleActionComponent API reference (C++ and Lua).
---

# ScaleActionComponent

The start and end scales of a [ScaleAction](scaleaction.md). In Lua, get it with `action:getScaleActionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `endScale` | C++ \| Lua |
| `startScale` | C++ \| Lua |
