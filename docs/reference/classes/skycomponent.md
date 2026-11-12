---
description: SkyComponent API reference (C++ and Lua).
---

# SkyComponent

The data behind a [SkyBox](skybox.md). In Lua, get it with `sky:getSkyComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `shader` | C++ \| Lua |
| `shaderUniforms` | C++ |
| `shaderTextures` | C++ |
| `texture` | C++ \| Lua |
| `color` | C++ \| Lua |
| `rotation` | C++ \| Lua |
| `visible` | C++ \| Lua |
| `needUpdateEnvironment` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `needUpdateSky` | C++ \| Lua |
| `needReload` | C++ \| Lua |

Set `needUpdateTexture` after replacing `texture`, `needUpdateSky` after changing `rotation`, and `needReload` after changing `shader`. `shader` is the sky's [shader file](skybox.md#shader), the scene default when empty; `shaderUniforms` and `shaderTextures` hold its parameter values and textures by name; [setShaderUniform](skybox.md#setshaderuniform) and [setShaderTexture](skybox.md#setshadertexture) set them, also from Lua.
