---
description: UISystem API reference (C++ and Lua).
---

# UISystem

**Inherits:** [SubSystem](subsystem.md)

UI layout, focus, and pointer routing.

## Methods

| Name | Languages |
| --- | --- |
| `getAnchorReferenceRect` | C++ \| Lua |
| `setAnchorReferenceSize` | C++ \| Lua |
| `clearAnchorReferenceSize` | C++ \| Lua |
| `getAnchorReferenceWidth` | C++ \| Lua |
| `getAnchorReferenceHeight` | C++ \| Lua |
| `parentToLayoutSpace` | C++ \| Lua |
| `layoutToParentSpace` | C++ \| Lua |
| `isTextEditFocused` | C++ \| Lua |
| `hasPendingImages` | C++ \| Lua |
| `resetButtonStates` | C++ \| Lua |
| `eventOnCharInput` | C++ \| Lua |
| `eventOnKeyDown` | C++ \| Lua |
| `eventOnPointerDown` | C++ \| Lua |
| `eventOnPointerUp` | C++ \| Lua |
| `eventOnPointerMove` | C++ \| Lua |

An anchored element's offset is measured in the space of its nearest layout parent, and its
position in its own parent's space. `parentToLayoutSpace(entity, point)` and
`layoutToParentSpace(entity, point)` convert a point between the two.

`hasPendingImages()` is true while an image still waits for its texture to build its
geometry. `resetButtonStates()` puts every pressed button back to its normal look, without
calling `onRelease`.
