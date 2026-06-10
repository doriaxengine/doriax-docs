---
description: Keyboard, mouse, touch, modifier input, and UI event handling in Doriax.
---

# Input

Doriax exposes all input through the static `Input` class. It covers keyboard, mouse,
touch, and modifier state for desktop, mobile, and web targets. All polling APIs are
safe to call from any script or system update.

## Key and button constants

Key and button constants are based on GLFW key codes. The naming differs by language:

| Language | How to access | Example |
| --- | --- | --- |
| **C++** | `D_KEY_*` / `D_MOUSE_BUTTON_*` / `D_MODIFIER_*` preprocessor macros | `D_KEY_SPACE` |
| **Lua** | Static properties on the `Input` class (drop the `D_` prefix) | `Input.KEY_SPACE` |

There is no global `D_KEY_SPACE` in Lua — always use `Input.KEY_SPACE`. The same applies
to mouse buttons (`Input.MOUSE_BUTTON_LEFT`) and modifiers (`Input.MODIFIER_SHIFT`).

## Keyboard

`Input.isKeyPressed(key)` returns `true` while the key is **currently held down**. It is
a polling call: read it every frame inside `onUpdate`. There is no separate
"down/released this frame" polling method — for one-shot press and release *edges*,
subscribe to the [`Engine.onKeyDown` / `Engine.onKeyUp`](../reference/classes/engine.md)
events instead.

=== "Lua"

    ```lua
    if Input.isKeyPressed(Input.KEY_SPACE) then
        player:jump()
    end

    if Input.isKeyPressed(Input.KEY_A) then
        player:moveLeft()
    end
    ```

=== "C++"

    ```cpp
    if (Input::isKeyPressed(D_KEY_SPACE)) {
        player.jump();
    }

    if (Input::isKeyPressed(D_KEY_A)) {
        player.moveLeft();
    }
    ```

### Common key constants

| C++ macro | Lua property | Key |
| --- | --- | --- |
| `D_KEY_A` … `D_KEY_Z` | `Input.KEY_A` … `Input.KEY_Z` | Letter keys |
| `D_KEY_0` … `D_KEY_9` | `Input.KEY_0` … `Input.KEY_9` | Number row |
| `D_KEY_KP_0` … `D_KEY_KP_9` | `Input.KEY_KP_0` … `Input.KEY_KP_9` | Numpad |
| `D_KEY_LEFT`, `D_KEY_RIGHT`, `D_KEY_UP`, `D_KEY_DOWN` | `Input.KEY_LEFT`, … | Arrow keys |
| `D_KEY_SPACE` | `Input.KEY_SPACE` | Spacebar |
| `D_KEY_ENTER`, `D_KEY_ESCAPE`, `D_KEY_BACKSPACE`, `D_KEY_TAB` | `Input.KEY_ENTER`, … | Editing keys |
| `D_KEY_F1` … `D_KEY_F12` | `Input.KEY_F1` … `Input.KEY_F12` | Function keys |
| `D_KEY_LEFT_SHIFT`, `D_KEY_LEFT_CONTROL`, `D_KEY_LEFT_ALT` | `Input.KEY_LEFT_SHIFT`, … | Modifier keys |

See [Input](../reference/classes/input.md) for the full constant list.

## Mouse

Like the keyboard, `Input.isMousePressed(button)` returns `true` while the button is
held down. For click and release edges use the
[`Engine.onMouseDown` / `Engine.onMouseUp`](../reference/classes/engine.md) events.

=== "Lua"

    ```lua
    if Input.isMousePressed(Input.MOUSE_BUTTON_LEFT) then
        local pos = Input.getMousePosition()
        shoot(pos.x, pos.y)
    end
    ```

=== "C++"

    ```cpp
    if (Input::isMousePressed(D_MOUSE_BUTTON_LEFT)) {
        Vector2 pos = Input::getMousePosition();
        shoot(pos.x, pos.y);
    }
    ```

### Mouse methods

| Method | Purpose |
| --- | --- |
| `isMousePressed(button)` | Button is currently held down |
| `isMouseEntered()` | Cursor is inside the canvas |
| `getMousePosition()` | Current cursor position in canvas coordinates |
| `getMouseScroll()` | Accumulated scroll wheel delta `(x, y)` since last frame |

### Mouse button constants

| C++ macro | Lua property | Button |
| --- | --- | --- |
| `D_MOUSE_BUTTON_LEFT` | `Input.MOUSE_BUTTON_LEFT` | Primary / left button |
| `D_MOUSE_BUTTON_RIGHT` | `Input.MOUSE_BUTTON_RIGHT` | Secondary / right button |
| `D_MOUSE_BUTTON_MIDDLE` | `Input.MOUSE_BUTTON_MIDDLE` | Middle button / scroll wheel click |

## Touch

Touch input is the primary interaction model on mobile and web. Use the touch APIs for
multi-touch aware code; configure mouse/touch mirroring in Engine settings if you want
single-touch to also fire mouse events.

=== "Lua"

    ```lua
    if Input.isTouch() then
        local n = Input.numTouches()
        for i = 0, n - 1 do
            local pos = Input.getTouchPosition(i)
            handleTap(pos.x, pos.y)
        end
    end
    ```

=== "C++"

    ```cpp
    if (Input::isTouch()) {
        int n = Input::numTouches();
        for (int i = 0; i < n; i++) {
            Vector2 pos = Input::getTouchPosition(i);
            handleTap(pos.x, pos.y);
        }
    }
    ```

### Touch methods

| Method | Purpose |
| --- | --- |
| `isTouch()` | True while at least one touch point is active |
| `numTouches()` | Number of active touch points |
| `getTouchPosition(index)` | Position of a touch point by index |
| `getTouches()` | Array of all active touch records |

## Modifiers

Modifier key state is available for keyboard shortcuts:

`getModifiers()` returns a bitmask, so test individual modifiers with bitwise AND.

=== "Lua"

    ```lua
    local mods = Input.getModifiers()
    if (mods & Input.MODIFIER_CONTROL) ~= 0 then
        -- Ctrl is held
    end
    ```

=== "C++"

    ```cpp
    int mods = Input::getModifiers();
    if (mods & D_MODIFIER_CONTROL) {
        // Ctrl is held
    }
    ```

Modifier constants (C++ `D_MODIFIER_*` / Lua `Input.MODIFIER_*`): `SHIFT`, `CONTROL`,
`ALT`, `SUPER`, `CAPS_LOCK`, and `NUM_LOCK`.

## Mouse and touch mirroring

Configure the engine to mirror mouse events as touch events or vice versa. The flags are
`callMouseInTouchEvent` (fire mouse callbacks from touch input) and
`callTouchInMouseEvent` (fire touch callbacks from mouse input):

=== "Lua"

    ```lua
    Engine.callMouseInTouchEvent = true   -- touch input also fires mouse callbacks
    Engine.callTouchInMouseEvent = true   -- mouse input also fires touch callbacks
    ```

=== "C++"

    ```cpp
    Engine::setCallMouseInTouchEvent(true);   // touch input also fires mouse callbacks
    Engine::setCallTouchInMouseEvent(true);   // mouse input also fires touch callbacks
    ```

This simplifies cross-platform code — write one input path that works for both desktop
and mobile.

## UI input

UI widgets consume pointer and touch events automatically. To prevent UI clicks from
also triggering gameplay input handlers (for example, shooting when the player taps a
button), call:

=== "Lua"

    ```lua
    Engine.ignoreEventsHandledByUI = true
    ```

=== "C++"

    ```cpp
    Engine::setIgnoreEventsHandledByUI(true);
    ```

## Virtual keyboard (mobile / web)

On platforms without a hardware keyboard, open the system virtual keyboard for text
input:

=== "Lua"

    ```lua
    System.showVirtualKeyboard("")   -- the text argument is required in Lua
    System.hideVirtualKeyboard()
    ```

=== "C++"

    ```cpp
    System::showVirtualKeyboard();   // text argument defaults to L""
    System::hideVirtualKeyboard();
    ```

## Cross-platform advice

- Always provide both keyboard/mouse and touch code paths.
- Use the named key constants (`Input.KEY_*` in Lua, `D_KEY_*` in C++) instead of raw
  numbers so the code stays readable.
- Avoid relying on platform-specific keys (e.g. Windows key, macOS Command) for core
  gameplay mechanics.
- Test canvas/input coordinate scaling together — a touch at screen position (x, y)
  maps to logical canvas coordinates depending on the active scaling mode.

## See also

- [Input](../reference/classes/input.md) — full API reference with all constants
- [System](../reference/classes/system.md) — virtual keyboard and platform utilities
- [User Interface](user-interface.md) — UI event handling
