---
description: TextureData API reference (C++ and Lua).
---

# TextureData

CPU pixel buffer for textures. Copying one with `dataOwned` set duplicates its pixels, so
the copy outlives the original. Any other copy points at the same pixels.

## Properties

| Name | Languages |
| --- | --- |
| `dataOwned` | C++ \| Lua |
| `svgScale` | C++ \| Lua |

## Methods

| Name | Languages |
| --- | --- |
| `loadTextureFromFile` | C++ \| Lua |
| `releaseImageData` | C++ \| Lua |
| `hasAlpha` | C++ \| Lua |
| `resizePowerOfTwo` | C++ \| Lua |
| `fitPowerOfTwo` | C++ \| Lua |
| `resize` | C++ \| Lua |
| `crop` | C++ \| Lua |
| `fitSize` | C++ \| Lua |
| `flipVertical` | C++ \| Lua |
| `getColorComponent` | C++ \| Lua |
| `getWidth` | C++ \| Lua |
| `getHeight` | C++ \| Lua |
| `getOriginalWidth` | C++ \| Lua |
| `getOriginalHeight` | C++ \| Lua |
| `getSize` | C++ \| Lua |
| `getColorFormat` | C++ \| Lua |
| `getChannels` | C++ \| Lua |
| `getData` | C++ \| Lua |
| `isTransparent` | C++ \| Lua |
| `getMinNearestPowerOfTwo` | C++ \| Lua |
