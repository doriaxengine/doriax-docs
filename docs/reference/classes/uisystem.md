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
| `isTextEditTyping` | C++ \| Lua |
| `hasPendingImages` | C++ \| Lua |
| `resetButtonStates` | C++ \| Lua |
| `setFocus` | C++ \| Lua |
| `eventOnCharInput` | C++ \| Lua |
| `eventOnKeyDown` | C++ \| Lua |
| `eventOnPointerDown` | C++ \| Lua |
| `eventOnPointerUp` | C++ \| Lua |
| `eventOnPointerMove` | C++ \| Lua |
| `eventOnNavigate` | C++ \| Lua |
| `eventOnSubmitDown` | C++ \| Lua |
| `eventOnSubmitUp` | C++ \| Lua |
| `eventOnSubmitCancel` | C++ \| Lua |

An anchored element's offset is measured in the space of its nearest layout parent, and its
position in its own parent's space. `parentToLayoutSpace(entity, point)` and
`layoutToParentSpace(entity, point)` convert a point between the two.

`hasPendingImages()` is true while an image still waits for its texture to build its
geometry. `resetButtonStates()` puts every pressed button back to its normal look, without
calling `onRelease`, and keeps the keyboard and gamepad focus. The engine calls it when it
removes a scene and when it adds one, so a button focused before the scene runs stays
focused.

`isTextEditTyping()` is true while a focused text edit is also visible and enabled. While
one is, in any scene, the engine leaves the arrows and the submit keys to it.

`setFocus(entity)` gives an entity the keyboard and gamepad focus and shows it, and
`NULL_ENTITY` clears it. The engine calls `eventOnNavigate` with a
[NavigationDirection](engine.md#navigationdirection) for the arrow keys, Tab, the d-pad, and
the left stick, and `eventOnSubmitDown` / `eventOnSubmitUp` for Enter, Space, and the A
button. `eventOnSubmitCancel` lets go of the pressed button without a click, for a
controller that was unplugged or a scene that stopped taking UI events. Each returns `true`
when the scene used the event. See
[Keyboard and gamepad navigation](../../manual/user-interface.md#keyboard-and-gamepad-navigation).
