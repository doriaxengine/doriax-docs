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

## Property details

### color

The tint multiplied with the widget's texture, as **linear** RGBA — not sRGB.

The object wrappers convert for you: [`Image::setColor`](image.md#color),
[`Text::setColor`](text.md#color) and the `Button` state colours all take an sRGB value
and store the linear one, and their getters convert back. Writing `ui.color` directly,
from C++ or Lua, sets the linear value with no conversion.

The same goes for a colour written into a `.scene` or `.bundle` file by hand or by a
tool: it reaches this field unconverted, so it has to be authored linear. A panel
written as `0.07` renders like sRGB `0.29`, not like the dark value it looks like in the
file. The editor's colour picker already shows and edits the sRGB form of the stored
value, so colours set in the Properties window need nothing.

```lua
-- These two produce the same pixels
image:setColor(Vector4(0.29, 0.29, 0.29, 1.0))   -- sRGB, converted for you
image:getUIComponent().color = Vector4(0.07, 0.07, 0.07, 1.0)  -- linear, as stored
```
