---
description: UIComponent API reference (C++ and Lua).
---

# UIComponent

`UIComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `loaded` | C++ \| Lua (read-only) |
| `minBufferCount` | C++ \| Lua (read-only) |
| `minIndicesCount` | C++ \| Lua (read-only) |
| `primitiveType` | C++ \| Lua |
| `vertexCount` | C++ \| Lua (read-only) |
| `texture` | C++ \| Lua |
| `color` | C++ \| Lua |
| `onGetFocus` | C++ \| Lua |
| `onLostFocus` | C++ \| Lua |
| `onPointerEnter` | C++ \| Lua |
| `onPointerLeave` | C++ \| Lua |
| `onPointerMove` | C++ \| Lua |
| `onPointerDown` | C++ \| Lua |
| `onPointerUp` | C++ \| Lua |
| `onClick` | C++ \| Lua |
| `onDoubleClick` | C++ \| Lua |
| `onDragStart` | C++ \| Lua |
| `onDrag` | C++ \| Lua |
| `onDragEnd` | C++ \| Lua |
| `automaticFlipY` | C++ \| Lua |
| `flipY` | C++ \| Lua |
| `pointerMoved` | C++ \| Lua (read-only) |
| `focused` | C++ \| Lua (read-only) |
| `needReload` | C++ \| Lua |
| `needUpdateBuffer` | C++ \| Lua |
| `needUpdateTexture` | C++ \| Lua |
| `buffer` | C++ |
| `indices` | C++ |
| `render` | C++ |
| `shader` | C++ |
| `shaderProperties` | C++ |
| `slotVSParams` | C++ |
| `slotFSParams` | C++ |
