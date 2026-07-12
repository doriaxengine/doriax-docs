---
description: Keyboard, mouse, touch, gamepad, modifier input, and UI event handling in Doriax.
---

# Input

Doriax exposes all input through the static `Input` class. It covers keyboard, mouse,
touch, gamepad, and modifier state for desktop, mobile, and web targets. All polling APIs
are safe to call from any script or system update.

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

### Cursor visibility, locking, and positioning

Use `Input` to read the current mouse state. Use `Engine` to control how the OS cursor behaves:

| API | Purpose |
| --- | --- |
| `Engine.showCursor` / `Engine::setShowCursor(bool)` | Show or hide the OS cursor |
| `Engine.mouseLocked` / `Engine::setMouseLocked(bool)` | Capture the mouse for relative movement |
| `Engine.setMousePosition(x, y)` / `Engine::setMousePosition(x, y)` | Set the mouse position in canvas coordinates |

Hiding the cursor does not lock it. For first-person cameras or free-look controls, lock the mouse so movement keeps generating input without letting the pointer escape the window.

=== "Lua"

    ```lua
    function PlayerLook:init()
        Engine.showCursor = false
        Engine.mouseLocked = true
        RegisterEngineEvent(self, "onMouseMove")
    end

    function PlayerLook:onMouseMove(x, y, mods)
        local pos = Input.getMousePosition()
        -- Compare pos with the previous frame, or use the event values directly.
    end
    ```

=== "C++"

    ```cpp
    class PlayerLook : public doriax::ScriptBase {
    public:
        PlayerLook(doriax::Scene* scene, doriax::Entity entity)
            : ScriptBase(scene, entity) {
            Engine::setShowCursor(false);
            Engine::setMouseLocked(true);
            REGISTER_ENGINE_EVENT(onMouseMove);
        }

        ~PlayerLook() {
            UNREGISTER_ENGINE_EVENT(onMouseMove);
        }

        void onMouseMove(float x, float y, int mods) {
            Vector2 pos = Input::getMousePosition();
            // Compare pos with the previous frame, or use x/y directly.
        }
    };
    ```

To place the cursor manually, pass logical canvas coordinates:

=== "Lua"

    ```lua
    Engine.setMousePosition(Engine.canvasWidth * 0.5, Engine.canvasHeight * 0.5)
    ```

=== "C++"

    ```cpp
    Engine::setMousePosition(
        Engine::getCanvasWidth() * 0.5f,
        Engine::getCanvasHeight() * 0.5f
    );
    ```

Desktop GLFW builds also move the OS cursor. On platforms that do not expose cursor warping, the engine updates its internal input position and the next real mouse event may replace it.

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

## Gamepad

Gamepad (controller) input is available on desktop (Windows, Linux, macOS), mobile
(Android, iOS), and web. Buttons and axes follow the standard Xbox-style layout, so a
single code path works across controllers and platforms.

Each connected controller has a numeric **id**. Poll a specific controller by id, or
subscribe to the [`Engine.onGamepad*`](../reference/classes/engine.md#callback-events)
events for connect/disconnect and button/axis edges.

=== "Lua"

    ```lua
    -- Poll the first controller (id 0)
    if Input.isGamepadConnected(0) then
        if Input.isGamepadButtonPressed(0, Input.GAMEPAD_BUTTON_A) then
            player:jump()
        end

        local moveX = Input.getGamepadAxis(0, Input.GAMEPAD_AXIS_LEFT_X)
        local moveY = Input.getGamepadAxis(0, Input.GAMEPAD_AXIS_LEFT_Y)
        player:move(moveX, moveY)
    end
    ```

=== "C++"

    ```cpp
    if (Input::isGamepadConnected(0)) {
        if (Input::isGamepadButtonPressed(0, D_GAMEPAD_BUTTON_A)) {
            player.jump();
        }

        float moveX = Input::getGamepadAxis(0, D_GAMEPAD_AXIS_LEFT_X);
        float moveY = Input::getGamepadAxis(0, D_GAMEPAD_AXIS_LEFT_Y);
        player.move(moveX, moveY);
    }
    ```

### Enumerating connected controllers

Gamepad ids are **sparse** — after a controller disconnects, the remaining ids can have
gaps (for example ids `0` and `2` with `1` missing). `numGamepads()` is a *count*, not
the highest id, so never loop `for i = 0, numGamepads() - 1` and treat `i` as an id.
Instead map a dense index to a real id with `getGamepadId(index)`:

=== "Lua"

    ```lua
    for i = 0, Input.numGamepads() - 1 do
        local id = Input.getGamepadId(i)
        if Input.isGamepadButtonPressed(id, Input.GAMEPAD_BUTTON_START) then
            pauseGame()
        end
    end
    ```

=== "C++"

    ```cpp
    for (size_t i = 0; i < Input::numGamepads(); i++) {
        int id = Input::getGamepadId(i);
        if (Input::isGamepadButtonPressed(id, D_GAMEPAD_BUTTON_START)) {
            pauseGame();
        }
    }
    ```

### Events

For one-shot press/release and connect/disconnect notifications, subscribe to the engine
events instead of polling:

=== "Lua"

    ```lua
    function Controller:init()
        RegisterEngineEvent(self, "onGamepadConnect")
        RegisterEngineEvent(self, "onGamepadButtonDown")
    end

    function Controller:onGamepadConnect(gamepad)
        print("Controller connected: " .. Input.getGamepadName(gamepad))
    end

    function Controller:onGamepadButtonDown(gamepad, button)
        if button == Input.GAMEPAD_BUTTON_A then
            player:jump()
        end
    end
    ```

=== "C++"

    ```cpp
    class Controller : public doriax::ScriptBase {
    public:
        Controller(doriax::Scene* scene, doriax::Entity entity)
            : ScriptBase(scene, entity) {
            REGISTER_ENGINE_EVENT(onGamepadConnect);
            REGISTER_ENGINE_EVENT(onGamepadButtonDown);
        }

        ~Controller() {
            UNREGISTER_ENGINE_EVENT(onGamepadConnect);
            UNREGISTER_ENGINE_EVENT(onGamepadButtonDown);
        }

        void onGamepadConnect(int gamepad) { /* ... */ }

        void onGamepadButtonDown(int gamepad, int button) {
            if (button == D_GAMEPAD_BUTTON_A) player.jump();
        }
    };
    ```

The full event list is `onGamepadConnect`, `onGamepadDisconnect`, `onGamepadButtonDown`,
`onGamepadButtonUp`, and `onGamepadAxisMove` — see
[Engine](../reference/classes/engine.md#callback-events).

### Gamepad methods

| Method | Purpose |
| --- | --- |
| `isGamepadConnected(id)` | True while a controller with this id is connected |
| `getGamepadName(id)` | Human-readable controller name |
| `isGamepadButtonPressed(id, button)` | Button is currently held down |
| `getGamepadAxis(id, axis)` | Current axis value, `-1.0`…`1.0` |
| `numGamepads()` | Number of connected controllers |
| `getGamepadId(index)` | Real id of the `index`-th connected controller (`-1` if out of range) |

### Gamepad button constants

Buttons use the standard Xbox layout. In Lua, replace the `D_GAMEPAD_BUTTON_` prefix with
`Input.GAMEPAD_BUTTON_`. PlayStation-style aliases map to the same values.

| C++ constant | Value | Xbox | PlayStation alias |
| --- | --- | --- | --- |
| `D_GAMEPAD_BUTTON_A` | 0 | A | `D_GAMEPAD_BUTTON_CROSS` |
| `D_GAMEPAD_BUTTON_B` | 1 | B | `D_GAMEPAD_BUTTON_CIRCLE` |
| `D_GAMEPAD_BUTTON_X` | 2 | X | `D_GAMEPAD_BUTTON_SQUARE` |
| `D_GAMEPAD_BUTTON_Y` | 3 | Y | `D_GAMEPAD_BUTTON_TRIANGLE` |
| `D_GAMEPAD_BUTTON_LEFT_BUMPER` | 4 | LB | L1 |
| `D_GAMEPAD_BUTTON_RIGHT_BUMPER` | 5 | RB | R1 |
| `D_GAMEPAD_BUTTON_BACK` | 6 | View / Back | Share |
| `D_GAMEPAD_BUTTON_START` | 7 | Menu / Start | Options |
| `D_GAMEPAD_BUTTON_GUIDE` | 8 | Guide | PS |
| `D_GAMEPAD_BUTTON_LEFT_THUMB` | 9 | Left stick click | L3 |
| `D_GAMEPAD_BUTTON_RIGHT_THUMB` | 10 | Right stick click | R3 |
| `D_GAMEPAD_BUTTON_DPAD_UP` | 11 | D-pad up | |
| `D_GAMEPAD_BUTTON_DPAD_RIGHT` | 12 | D-pad right | |
| `D_GAMEPAD_BUTTON_DPAD_DOWN` | 13 | D-pad down | |
| `D_GAMEPAD_BUTTON_DPAD_LEFT` | 14 | D-pad left | |

### Gamepad axis constants

Axis values range from `-1.0` to `1.0`. In Lua, replace `D_GAMEPAD_AXIS_` with
`Input.GAMEPAD_AXIS_`.

| C++ constant | Value | Range |
| --- | --- | --- |
| `D_GAMEPAD_AXIS_LEFT_X` | 0 | Left stick, `-1` left … `+1` right |
| `D_GAMEPAD_AXIS_LEFT_Y` | 1 | Left stick, `-1` up … `+1` down |
| `D_GAMEPAD_AXIS_RIGHT_X` | 2 | Right stick, `-1` left … `+1` right |
| `D_GAMEPAD_AXIS_RIGHT_Y` | 3 | Right stick, `-1` up … `+1` down |
| `D_GAMEPAD_AXIS_LEFT_TRIGGER` | 4 | Left trigger, `-1` released … `+1` pressed |
| `D_GAMEPAD_AXIS_RIGHT_TRIGGER` | 5 | Right trigger, `-1` released … `+1` pressed |

!!! note "Stick and trigger conventions"
    The Y axes are **down-positive** (up is `-1`), matching screen coordinates.
    **Triggers rest at `-1`** and reach `+1` when fully pressed — a released trigger reads
    `-1`, not `0`, and this holds from the moment a controller connects. Apply a small dead
    zone to the sticks (for example, ignore values under `0.15`) to avoid drift from analog
    noise.

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
