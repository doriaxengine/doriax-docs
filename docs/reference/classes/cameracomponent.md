---
description: CameraComponent API reference (C++ and Lua).
---

# CameraComponent

The data behind a [Camera](camera.md). In Lua, get it with `camera:getCameraComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `type` | C++ \| Lua |
| `projectionMatrix` | C++ \| Lua (read-only) |
| `viewMatrix` | C++ \| Lua (read-only) |
| `viewProjectionMatrix` | C++ \| Lua (read-only) |
| `target` | C++ \| Lua |
| `worldTarget` | C++ \| Lua (read-only) |
| `up` | C++ \| Lua |
| `direction` | C++ \| Lua (read-only) |
| `right` | C++ \| Lua (read-only) |
| `worldUp` | C++ \| Lua (read-only) |
| `worldDirection` | C++ \| Lua (read-only) |
| `worldRight` | C++ \| Lua (read-only) |
| `leftClip` | C++ \| Lua |
| `rightClip` | C++ \| Lua |
| `bottomClip` | C++ \| Lua |
| `topClip` | C++ \| Lua |
| `yfov` | C++ \| Lua |
| `aspect` | C++ \| Lua |
| `nearClip` | C++ \| Lua |
| `farClip` | C++ \| Lua |
| `renderToTexture` | C++ \| Lua |
| `framebuffer` | C++ \| Lua (read-only) |
| `framebufferWidth` | C++ \| Lua |
| `framebufferHeight` | C++ \| Lua |
| `framebufferFilter` | C++ \| Lua |
| `transparentSort` | C++ \| Lua |
| `depthTest` | C++ \| Lua |
| `useTarget` | C++ \| Lua |
| `autoResize` | C++ \| Lua |
| `hasCustomViewMatrix` | C++ \| Lua |
| `customViewMatrix` | C++ \| Lua |
| `invertCulling` | C++ \| Lua |
| `needUpdate` | C++ \| Lua |

Set `needUpdate` after changing the projection, clip, or target fields. `framebuffer` is the render target used when `renderToTexture` is on.
