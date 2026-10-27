---
description: AlphaActionComponent API reference (C++ and Lua).
---

# AlphaActionComponent

The start and end alpha of an [AlphaAction](alphaaction.md). In Lua, get it with `action:getAlphaActionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `endAlpha` | C++ \| Lua |
| `startAlpha` | C++ \| Lua |
