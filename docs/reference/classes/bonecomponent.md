---
description: BoneComponent API reference (C++ and Lua).
---

# BoneComponent

The bind pose of a [Bone](bone.md), filled in when its model loads. In Lua, get it with `bone:getBoneComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `model` | C++ \| Lua (read-only) |
| `index` | C++ \| Lua (read-only) |
| `bindPosition` | C++ \| Lua (read-only) |
| `bindRotation` | C++ \| Lua (read-only) |
| `bindScale` | C++ \| Lua (read-only) |
| `offsetMatrix` | C++ \| Lua (read-only) |
