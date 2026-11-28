---
description: Character3DComponent API reference (C++ and Lua).
---

# Character3DComponent

The data a [Character3D](character3d.md) is built from. In the editor it is **3D Character** in
**New component**. In Lua, get it with `character:getCharacter3DComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Default | Languages |
| --- | --- | --- |
| `height` | `1.8` | C++ \| Lua |
| `radius` | `0.3` | C++ \| Lua |
| `maxSlopeAngle` | `45` | C++ \| Lua |
| `supportAngle` | `90` | C++ \| Lua |
| `stepUp` | `0.4` | C++ \| Lua |
| `stepDown` | `0.5` | C++ \| Lua |
| `mass` | `70` | C++ \| Lua |
| `maxStrength` | `100` | C++ \| Lua |
| `padding` | `0.02` | C++ \| Lua |
| `gravityFactor` | `1` | C++ \| Lua |
| `airControl` | `1` | C++ \| Lua |
| `innerBody` | `true` | C++ \| Lua |
| `kinematic` | `false` | C++ \| Lua |
| `moveVelocity` | `(0,0,0)` | C++ \| Lua |
| `needReloadCharacter` | `true` | C++ \| Lua |

`height` and `radius` size the capsule, which stands on the entity origin and is scaled with the
entity. A height under twice the radius makes it a sphere. `padding` is the gap the character
keeps from what it touches, and `innerBody` gives it the kinematic body that rays and sensors
find (see [Contacts and the inner body](character3d.md#contacts-and-the-inner-body)).

`stepUp`, `stepDown`, `gravityFactor`, `airControl`, `kinematic` and `moveVelocity` are read at
every fixed step. The others are used when the character is built: set `needReloadCharacter`, or call
[Character3D::load](character3d.md#load), after changing them. The [Character3D](character3d.md)
setters for `maxSlopeAngle`, `supportAngle`, `mass` and `maxStrength` change the running
character too.
