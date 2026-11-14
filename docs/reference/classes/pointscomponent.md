---
description: PointsComponent API reference (C++ and Lua).
---

# PointsComponent

The data behind [Points](points.md). In Lua, get it with `points:getPointsComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `points` | C++ \| Lua |
| `numFramesRect` | C++ \| Lua (read-only) |
| `maxPoints` | C++ \| Lua (read-only) |
| `numVisible` | C++ \| Lua (read-only) |
| `aabb` | C++ \| Lua (read-only) |
| `shader` | C++ \| Lua |
| `shaderUniforms` | C++ |
| `shaderTextures` | C++ |
| `texture` | C++ \| Lua |
| `transparent` | C++ \| Lua |
| `autoTransparency` | C++ \| Lua |
| `needUpdate` | C++ \| Lua |
| `needUpdateBuffer` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `needReload` | C++ \| Lua |

`points` is a list of [PointData](pointdata.md). Set `needUpdate` after assigning it. Only the first `maxPoints` are drawn; raise it with [`Points.maxPoints`](points.md#maxpoints). Set `needReload` after changing `shader`, the points' [shader file](points.md#shader), the scene default when empty. `shaderUniforms` and `shaderTextures` hold its parameter values and textures by name; [setShaderUniform](points.md#setshaderuniform) and [setShaderTexture](points.md#setshadertexture) set them, also from Lua. In Lua, lists are copies: assign the changed table back.
