---
description: SpriteComponent API reference (C++ and Lua).
---

# SpriteComponent

The data behind a [Sprite](sprite.md). In Lua, get it with `sprite:getSpriteComponent()`.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `width` | C++ \| Lua |
| `height` | C++ \| Lua |
| `automaticFlipY` | C++ \| Lua |
| `flipY` | C++ \| Lua |
| `textureScaleFactor` | C++ \| Lua |
| `numFramesRect` | C++ \| Lua (read-only) |
| `pivotPreset` | C++ \| Lua |
| `needUpdateSprite` | C++ \| Lua |
| `needUpdateBatch` | C++ \| Lua |

Set `needUpdateSprite` after changing the size, flip, or pivot. A size of 0 uses the texture size. Frames are C++ only; from Lua, use the [Sprite](sprite.md) frame methods. After changing the sprite's `MeshComponent` directly, set `needUpdateBatch`.
