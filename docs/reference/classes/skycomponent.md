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
| `customShader` | C++ \| Lua |
| `texture` | C++ \| Lua |
| `color` | C++ \| Lua |
| `rotation` | C++ \| Lua |
| `visible` | C++ \| Lua |
| `needUpdateEnvironment` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `needUpdateSky` | C++ \| Lua |
| `needReload` | C++ \| Lua |

Set `needUpdateTexture` after replacing `texture`, `needUpdateSky` after changing `rotation`, and `needReload` after changing `customShader`.
