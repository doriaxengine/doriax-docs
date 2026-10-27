---
description: RotationActionComponent API reference (C++ and Lua).
---

# RotationActionComponent

The rotations of a [RotationAction](rotationaction.md). In Lua, get it with `action:getRotationActionComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `endRotation` | C++ \| Lua |
| `startRotation` | C++ \| Lua |
| `shortestPath` | C++ \| Lua |
| `spin` | C++ \| Lua |
| `axis` | C++ \| Lua |
| `angle` | C++ \| Lua |
