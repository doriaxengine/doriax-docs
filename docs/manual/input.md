---
description: Keyboard, mouse, touch, modifier input, and UI event handling in Doriax.
---

# Input

Doriax exposes all input through the static `Input` class. It covers keyboard, mouse,
touch, and modifier state for desktop, mobile, and web targets. All polling APIs are
safe to call from any script or system update.

## Keyboard

Keyboard key constants follow the `S_KEY_*` naming convention and are based on GLFW
key codes.

=== "Lua"

    ```lua
    if Input.isKeyPressed(S_KEY_SPACE) then
        player:jump()
    end

    if Input.isKeyDown(S_KEY_A) then
        player:moveLeft()
    end
    ```

=== "C++"

    ```cpp
    if (Input::isKeyPressed(S_KEY_SPACE)) {
        player.jump();
    }

    if (Input::isKeyDown(S_KEY_A)) {
        player.moveLeft();
    }
    ```

### Key query methods

| Method | Returns true when |
| --- | --- |
| `isKeyDown(key)` | Key is currently held down (every frame) |
| `isKeyPressed(key)` | Key was pressed this frame (fires once) |
| `isKeyReleased(key)` | Key was released this frame (fires once) |

### Common key constants

| Constant | Key |
| --- | --- |
| `S_KEY_A` … `S_KEY_Z` | Letter keys |
| `S_KEY_0` … `S_KEY_9` | Number row |
| `S_KEY_KP_0` … `S_KEY_KP_9` | Numpad |
| `S_KEY_LEFT`, `S_KEY_RIGHT`, `S_KEY_UP`, `S_KEY_DOWN` | Arrow keys |
| `S_KEY_SPACE` | Spacebar |
| `S_KEY_ENTER`, `S_KEY_ESCAPE`, `S_KEY_BACKSPACE`, `S_KEY_TAB` | Editing keys |
| `S_KEY_F1` … `S_KEY_F12` | Function keys |
| `S_KEY_LEFT_SHIFT`, `S_KEY_LEFT_CONTROL`, `S_KEY_LEFT_ALT` | Modifier keys |

See [Input](../reference/classes/input.md) for the full constant list.

## Mouse

=== "Lua"

    ```lua
    if Input.isMousePressed(S_MOUSE_BUTTON_LEFT) then
        local pos = Input.getMousePosition()
        shoot(pos.x, pos.y)
    end
    ```

=== "C++"

    ```cpp
    if (Input::isMousePressed(S_MOUSE_BUTTON_LEFT)) {
        Vector2 pos = Input::getMousePosition();
        shoot(pos.x, pos.y);
    }
    ```

### Mouse methods

| Method | Purpose |
| --- | --- |
| `isMouseDown(button)` | Button held this frame |
| `isMousePressed(button)` | Button pressed this frame (fires once) |
| `isMouseReleased(button)` | Button released this frame (fires once) |
| `getMousePosition()` | Current cursor position in canvas/screen coordinates |
| `getMouseScroll()` | Scroll wheel delta this frame |

### Mouse button constants

| Constant | Button |
| --- | --- |
| `S_MOUSE_BUTTON_LEFT` | Primary / left button |
| `S_MOUSE_BUTTON_RIGHT` | Secondary / right button |
| `S_MOUSE_BUTTON_MIDDLE` | Middle button / scroll wheel click |

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

=== "Lua"

    ```lua
    local mods = Input.getModifiers()
    if mods == S_MODIFIER_CONTROL then
        -- Ctrl is held
    end
    ```

=== "C++"

    ```cpp
    int mods = Input::getModifiers();
    if (mods & S_MODIFIER_CONTROL) {
        // Ctrl is held
    }
    ```

Modifier constants include `S_MODIFIER_SHIFT`, `S_MODIFIER_CONTROL`, `S_MODIFIER_ALT`,
`S_MODIFIER_SUPER`, `S_MODIFIER_CAPS_LOCK`, and `S_MODIFIER_NUM_LOCK`.

## Mouse and touch mirroring

Configure the engine to mirror mouse events as touch events or vice versa:

```cpp
Engine::setMouseAsTouch(true);    // mouse click fires touch callbacks
Engine::setTouchAsMouse(true);    // touch fires mouse callbacks
```

This simplifies cross-platform code — write one input path that works for both desktop
and mobile.

## UI input

UI widgets consume pointer and touch events automatically. To prevent UI clicks from
also triggering gameplay input handlers (for example, shooting when the player taps a
button), call:

=== "Lua"

    ```lua
    Engine.setIgnoreEventsHandledByUI(true)
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
    System.showVirtualKeyboard()
    System.hideVirtualKeyboard()
    ```

=== "C++"

    ```cpp
    System::showVirtualKeyboard();
    System::hideVirtualKeyboard();
    ```

## Cross-platform advice

- Always provide both keyboard/mouse and touch code paths.
- Use `S_KEY_*` names in comments so the code is readable even when constants are
  captured in variables.
- Avoid relying on platform-specific keys (e.g. Windows key, macOS Command) for core
  gameplay mechanics.
- Test canvas/input coordinate scaling together — a touch at screen position (x, y)
  maps to logical canvas coordinates depending on the active scaling mode.

## See also

- [Input](../reference/classes/input.md) — full API reference with all constants
- [System](../reference/classes/system.md) — virtual keyboard and platform utilities
- [User Interface](user-interface.md) — UI event handling
