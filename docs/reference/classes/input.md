---
description: Input API reference — keyboard, mouse, touch, and gamepad polling, modifiers, and key/button constants.
---

# Input

## Description

`Input` is a static polling class that provides the current keyboard, mouse, touch, and gamepad state at any point during a frame. Use it inside `onUpdate` or `onFixedUpdate` to check whether a key or button is held down. For event-based input (press/release and controller connect/disconnect notifications), subscribe to the [Engine](engine.md) callback events instead.

!!! note "Constant naming differs by language"
    Key, mouse-button, gamepad, and modifier constants are C++ preprocessor macros prefixed
    `D_` (e.g. `D_KEY_SPACE`, `D_MOUSE_BUTTON_LEFT`, `D_GAMEPAD_BUTTON_A`). In Lua they are
    static properties on the `Input` class with the `D_` prefix dropped (e.g.
    `Input.KEY_SPACE`, `Input.MOUSE_BUTTON_LEFT`, `Input.GAMEPAD_BUTTON_A`).

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    // Inside an update callback:
    if (Input::isKeyPressed(D_KEY_SPACE)) {
        player.jump();
    }
    ```

=== "Lua"

    ```lua
    -- Inside update:
    if Input.isKeyPressed(Input.KEY_SPACE) then
        player:jump()
    end
    ```

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| static bool | [isKeyPressed](#iskeypressed) | C++ \| Lua |
| static bool | [isMousePressed](#ismousepressed) | C++ \| Lua |
| static bool | [isTouch](#istouch) | C++ \| Lua |
| static bool | [isMouseEntered](#ismouseentered) | C++ \| Lua |
| static Vector2 | [getMousePosition](#getmouseposition) | C++ \| Lua |
| static Vector2 | [getMouseScroll](#getmousescroll) | C++ \| Lua |
| static Vector2 | [getTouchPosition](#gettouchposition) | C++ \| Lua |
| static std::vector\<Touch\> | [getTouches](#gettouches) | C++ \| Lua |
| static size_t | [numTouches](#numtouches) | C++ \| Lua |
| static bool | [isGamepadConnected](#isgamepadconnected) | C++ \| Lua |
| static std::string | [getGamepadName](#getgamepadname) | C++ \| Lua |
| static bool | [isGamepadButtonPressed](#isgamepadbuttonpressed) | C++ \| Lua |
| static float | [getGamepadAxis](#getgamepadaxis) | C++ \| Lua |
| static std::vector\<Gamepad\> | [getGamepads](#getgamepads) | C++ |
| static size_t | [numGamepads](#numgamepads) | C++ \| Lua |
| static int | [getGamepadId](#getgamepadid) | C++ \| Lua |
| static int | [getModifiers](#getmodifiers) | C++ \| Lua |
| static size_t | [findTouchIndex](#findtouchindex) | C++ \| Lua |
| static size_t | [findGamepadIndex](#findgamepadindex) | C++ |

## Keys

Key constants are preprocessor `#define` values in C++ (prefix `D_KEY_`) and static properties on `Input` in Lua (prefix `Input.KEY_`). The table below lists the C++ form; for Lua, replace `D_KEY_` with `Input.KEY_`.

| Constant | Value | Description |
| --- | --- | --- |
| `D_KEY_SPACE` | 32 | Space bar |
| `D_KEY_A` … `D_KEY_Z` | 65–90 | Letter keys |
| `D_KEY_0` … `D_KEY_9` | 48–57 | Number row |
| `D_KEY_ESCAPE` | 256 | Escape |
| `D_KEY_ENTER` | 257 | Enter / Return |
| `D_KEY_TAB` | 258 | Tab |
| `D_KEY_BACKSPACE` | 259 | Backspace |
| `D_KEY_INSERT` | 260 | Insert |
| `D_KEY_DELETE` | 261 | Delete |
| `D_KEY_RIGHT` | 262 | Arrow right |
| `D_KEY_LEFT` | 263 | Arrow left |
| `D_KEY_DOWN` | 264 | Arrow down |
| `D_KEY_UP` | 265 | Arrow up |
| `D_KEY_PAGE_UP` | 266 | Page Up |
| `D_KEY_PAGE_DOWN` | 267 | Page Down |
| `D_KEY_HOME` | 268 | Home |
| `D_KEY_END` | 269 | End |
| `D_KEY_CAPS_LOCK` | 280 | Caps Lock |
| `D_KEY_F1` … `D_KEY_F25` | 290–314 | Function keys |
| `D_KEY_KP_0` … `D_KEY_KP_9` | 320–329 | Numpad digits |
| `D_KEY_KP_ENTER` | 335 | Numpad Enter |
| `D_KEY_LEFT_SHIFT` | 340 | Left Shift |
| `D_KEY_LEFT_CONTROL` | 341 | Left Ctrl |
| `D_KEY_LEFT_ALT` | 342 | Left Alt |
| `D_KEY_LEFT_SUPER` | 343 | Left Super (Win/Cmd) |
| `D_KEY_RIGHT_SHIFT` | 344 | Right Shift |
| `D_KEY_RIGHT_CONTROL` | 345 | Right Ctrl |
| `D_KEY_RIGHT_ALT` | 346 | Right Alt |
| `D_KEY_RIGHT_SUPER` | 347 | Right Super |
| `D_KEY_MENU` | 348 | Menu key |

## Mouse buttons

In Lua, replace the `D_MOUSE_BUTTON_` prefix with `Input.MOUSE_BUTTON_`.

| C++ constant | Lua property | Value | Description |
| --- | --- | --- | --- |
| `D_MOUSE_BUTTON_LEFT` | `Input.MOUSE_BUTTON_LEFT` | 0 | Left button |
| `D_MOUSE_BUTTON_RIGHT` | `Input.MOUSE_BUTTON_RIGHT` | 1 | Right button |
| `D_MOUSE_BUTTON_MIDDLE` | `Input.MOUSE_BUTTON_MIDDLE` | 2 | Middle button |
| `D_MOUSE_BUTTON_1` … `D_MOUSE_BUTTON_8` | `Input.MOUSE_BUTTON_1` … `Input.MOUSE_BUTTON_8` | 0–7 | All buttons |

## Modifiers

Modifier bits returned by [getModifiers](#getmodifiers) and passed to key/mouse callbacks. In Lua, replace the `D_MODIFIER_` prefix with `Input.MODIFIER_`.

| C++ constant | Lua property | Bit | Description |
| --- | --- | --- | --- |
| `D_MODIFIER_SHIFT` | `Input.MODIFIER_SHIFT` | `0x0001` | Shift key held |
| `D_MODIFIER_CONTROL` | `Input.MODIFIER_CONTROL` | `0x0002` | Ctrl key held |
| `D_MODIFIER_ALT` | `Input.MODIFIER_ALT` | `0x0004` | Alt key held |
| `D_MODIFIER_SUPER` | `Input.MODIFIER_SUPER` | `0x0008` | Super (Win/Cmd) held |
| `D_MODIFIER_CAPS_LOCK` | `Input.MODIFIER_CAPS_LOCK` | `0x0010` | Caps Lock active |
| `D_MODIFIER_NUM_LOCK` | `Input.MODIFIER_NUM_LOCK` | `0x0020` | Num Lock active |

## Gamepad buttons

Button indices follow the standard Xbox-style layout. In Lua, replace the `D_GAMEPAD_BUTTON_` prefix with `Input.GAMEPAD_BUTTON_`. The PlayStation-style aliases are the same underlying values.

| C++ constant | Lua property | Value | Description |
| --- | --- | --- | --- |
| `D_GAMEPAD_BUTTON_A` | `Input.GAMEPAD_BUTTON_A` | 0 | A (alias `CROSS`) |
| `D_GAMEPAD_BUTTON_B` | `Input.GAMEPAD_BUTTON_B` | 1 | B (alias `CIRCLE`) |
| `D_GAMEPAD_BUTTON_X` | `Input.GAMEPAD_BUTTON_X` | 2 | X (alias `SQUARE`) |
| `D_GAMEPAD_BUTTON_Y` | `Input.GAMEPAD_BUTTON_Y` | 3 | Y (alias `TRIANGLE`) |
| `D_GAMEPAD_BUTTON_LEFT_BUMPER` | `Input.GAMEPAD_BUTTON_LEFT_BUMPER` | 4 | Left bumper / L1 |
| `D_GAMEPAD_BUTTON_RIGHT_BUMPER` | `Input.GAMEPAD_BUTTON_RIGHT_BUMPER` | 5 | Right bumper / R1 |
| `D_GAMEPAD_BUTTON_BACK` | `Input.GAMEPAD_BUTTON_BACK` | 6 | View / Back / Share |
| `D_GAMEPAD_BUTTON_START` | `Input.GAMEPAD_BUTTON_START` | 7 | Menu / Start / Options |
| `D_GAMEPAD_BUTTON_GUIDE` | `Input.GAMEPAD_BUTTON_GUIDE` | 8 | Guide / PS button |
| `D_GAMEPAD_BUTTON_LEFT_THUMB` | `Input.GAMEPAD_BUTTON_LEFT_THUMB` | 9 | Left stick click / L3 |
| `D_GAMEPAD_BUTTON_RIGHT_THUMB` | `Input.GAMEPAD_BUTTON_RIGHT_THUMB` | 10 | Right stick click / R3 |
| `D_GAMEPAD_BUTTON_DPAD_UP` | `Input.GAMEPAD_BUTTON_DPAD_UP` | 11 | D-pad up |
| `D_GAMEPAD_BUTTON_DPAD_RIGHT` | `Input.GAMEPAD_BUTTON_DPAD_RIGHT` | 12 | D-pad right |
| `D_GAMEPAD_BUTTON_DPAD_DOWN` | `Input.GAMEPAD_BUTTON_DPAD_DOWN` | 13 | D-pad down |
| `D_GAMEPAD_BUTTON_DPAD_LEFT` | `Input.GAMEPAD_BUTTON_DPAD_LEFT` | 14 | D-pad left |

The aliases `D_GAMEPAD_BUTTON_CROSS`, `CIRCLE`, `SQUARE`, and `TRIANGLE` (Lua `Input.GAMEPAD_BUTTON_CROSS`, …) resolve to `A`, `B`, `X`, and `Y` respectively.

## Gamepad axes

Axis values range from `-1.0` to `1.0`. Sticks are **down-positive** on the Y axis (up is `-1`), and triggers **rest at `-1`**, reaching `+1` when fully pressed. In Lua, replace the `D_GAMEPAD_AXIS_` prefix with `Input.GAMEPAD_AXIS_`.

| C++ constant | Lua property | Value | Range |
| --- | --- | --- | --- |
| `D_GAMEPAD_AXIS_LEFT_X` | `Input.GAMEPAD_AXIS_LEFT_X` | 0 | Left stick X: `-1` left … `+1` right |
| `D_GAMEPAD_AXIS_LEFT_Y` | `Input.GAMEPAD_AXIS_LEFT_Y` | 1 | Left stick Y: `-1` up … `+1` down |
| `D_GAMEPAD_AXIS_RIGHT_X` | `Input.GAMEPAD_AXIS_RIGHT_X` | 2 | Right stick X: `-1` left … `+1` right |
| `D_GAMEPAD_AXIS_RIGHT_Y` | `Input.GAMEPAD_AXIS_RIGHT_Y` | 3 | Right stick Y: `-1` up … `+1` down |
| `D_GAMEPAD_AXIS_LEFT_TRIGGER` | `Input.GAMEPAD_AXIS_LEFT_TRIGGER` | 4 | Left trigger: `-1` released … `+1` pressed |
| `D_GAMEPAD_AXIS_RIGHT_TRIGGER` | `Input.GAMEPAD_AXIS_RIGHT_TRIGGER` | 5 | Right trigger: `-1` released … `+1` pressed |

## Method details

### isKeyPressed

* `static bool isKeyPressed(int key)`

Returns `true` while the given key is held down. Use `D_KEY_*` constants in C++ and `Input.KEY_*` in Lua for the key code.

=== "C++"

    ```cpp
    if (Input::isKeyPressed(D_KEY_W)) {
        player.moveForward(Engine::getDeltatime() * speed);
    }
    ```

=== "Lua"

    ```lua
    if Input.isKeyPressed(Input.KEY_W) then
        player:moveForward(Engine.deltatime * speed)
    end
    ```

---

### isMousePressed

* `static bool isMousePressed(int button)`

Returns `true` while the given mouse button is held down. Use `D_MOUSE_BUTTON_*` constants in C++ and `Input.MOUSE_BUTTON_*` in Lua.

=== "C++"

    ```cpp
    if (Input::isMousePressed(D_MOUSE_BUTTON_LEFT)) {
        // drag logic
    }
    ```

=== "Lua"

    ```lua
    if Input.isMousePressed(Input.MOUSE_BUTTON_LEFT) then
        -- drag logic
    end
    ```

---

### isTouch

* `static bool isTouch()`

Returns `true` if there is at least one active touch contact.

---

### isMouseEntered

* `static bool isMouseEntered()`

Returns `true` while the mouse cursor is inside the canvas boundary.

---

### getMousePosition

* `static Vector2 getMousePosition()`

Current cursor position in canvas coordinates. Updated every frame; use for hover detection in `onUpdate`.

This value can also be set manually with [Engine.setMousePosition](engine.md#setmouseposition). When [Engine.mouseLocked](engine.md#mouselocked) is enabled, the position is a virtual canvas-space position accumulated from relative mouse movement and may move outside the normal canvas range.

=== "C++"

    ```cpp
    Vector2 pos = Input::getMousePosition();
    ```

=== "Lua"

    ```lua
    local pos = Input.getMousePosition()
    ```

---

### getMouseScroll

* `static Vector2 getMouseScroll()`

Accumulated scroll wheel delta since the last frame, in `(xoffset, yoffset)`. Reset each frame.

---

### getTouchPosition

* `static Vector2 getTouchPosition(int pointer)`

Returns the current position of the touch contact identified by `pointer`. Use [findTouchIndex](#findtouchindex) to convert a pointer ID to an array index if needed.

---

### getTouches

* `static std::vector<Touch> getTouches()`

Returns all active touch contacts. Each `Touch` has `int pointer` and `Vector2 position`.

=== "C++"

    ```cpp
    for (const auto& touch : Input::getTouches()) {
        drawCircle(touch.position.x, touch.position.y, 10.0f);
    }
    ```

=== "Lua"

    ```lua
    local touches = Input.getTouches()
    for i = 1, #touches do
        drawCircle(touches[i].position.x, touches[i].position.y, 10)
    end
    ```

---

### numTouches

* `static size_t numTouches()`

Returns the count of currently active touch contacts.

---

### isGamepadConnected

* `static bool isGamepadConnected(int id)`

Returns `true` while a controller with the given id is connected. Ids are assigned per platform and are **sparse** — enumerate connected controllers with [getGamepadId](#getgamepadid), not by assuming ids `0..numGamepads()-1`.

=== "C++"

    ```cpp
    if (Input::isGamepadConnected(0)) {
        // controller 0 is present
    }
    ```

=== "Lua"

    ```lua
    if Input.isGamepadConnected(0) then
        -- controller 0 is present
    end
    ```

---

### getGamepadName

* `static std::string getGamepadName(int id)`

Returns the human-readable name of the controller with the given id, or an empty string if it is not connected.

---

### isGamepadButtonPressed

* `static bool isGamepadButtonPressed(int id, int button)`

Returns `true` while the given button is held down on controller `id`. Use `D_GAMEPAD_BUTTON_*` constants in C++ and `Input.GAMEPAD_BUTTON_*` in Lua. Returns `false` for an unknown controller.

=== "C++"

    ```cpp
    if (Input::isGamepadButtonPressed(0, D_GAMEPAD_BUTTON_A)) {
        player.jump();
    }
    ```

=== "Lua"

    ```lua
    if Input.isGamepadButtonPressed(0, Input.GAMEPAD_BUTTON_A) then
        player:jump()
    end
    ```

---

### getGamepadAxis

* `static float getGamepadAxis(int id, int axis)`

Returns the current value of an analog axis on controller `id`, in the range `-1.0`…`1.0`. Use `D_GAMEPAD_AXIS_*` constants in C++ and `Input.GAMEPAD_AXIS_*` in Lua. Returns `0.0` for an unknown controller.

Sticks are down-positive on the Y axis (up is `-1`). **Triggers rest at `-1`** and reach `+1` when fully pressed — a released trigger reads `-1` from the moment the controller connects, not `0`.

=== "C++"

    ```cpp
    float x = Input::getGamepadAxis(0, D_GAMEPAD_AXIS_LEFT_X);
    if (fabsf(x) > 0.15f) {  // dead zone
        player.strafe(x);
    }
    ```

=== "Lua"

    ```lua
    local x = Input.getGamepadAxis(0, Input.GAMEPAD_AXIS_LEFT_X)
    if math.abs(x) > 0.15 then  -- dead zone
        player:strafe(x)
    end
    ```

---

### getGamepads

* `static std::vector<Gamepad> getGamepads()`
* C++ only

Returns all connected controllers. Each `Gamepad` holds an `int id`, a `std::string name`, and the current button and axis state. In Lua, iterate with [numGamepads](#numgamepads) and [getGamepadId](#getgamepadid) instead.

---

### numGamepads

* `static size_t numGamepads()`

Returns the count of currently connected controllers. This is a count, **not** the highest id — combine it with [getGamepadId](#getgamepadid) to iterate.

---

### getGamepadId

* `static int getGamepadId(size_t index)`

Returns the real id of the `index`-th connected controller, or `-1` if `index` is out of range. Because gamepad ids are sparse (they can have gaps after a disconnect), this is the correct way to enumerate connected controllers:

=== "C++"

    ```cpp
    for (size_t i = 0; i < Input::numGamepads(); i++) {
        int id = Input::getGamepadId(i);
        // poll controller `id`
    }
    ```

=== "Lua"

    ```lua
    for i = 0, Input.numGamepads() - 1 do
        local id = Input.getGamepadId(i)
        -- poll controller `id`
    end
    ```

---

### getModifiers

* `static int getModifiers()`

Returns the current modifier key bitmask. Check individual modifiers with bitwise AND.

=== "C++"

    ```cpp
    int mods = Input::getModifiers();
    if (mods & D_MODIFIER_SHIFT) {
        // Shift is held
    }
    ```

=== "Lua"

    ```lua
    local mods = Input.getModifiers()
    if (mods & Input.MODIFIER_SHIFT) ~= 0 then
        -- Shift is held
    end
    ```

---

### findTouchIndex

* `static size_t findTouchIndex(int pointer)`

Returns the index into the [getTouches](#gettouches) array for the given pointer ID. Returns `SIZE_MAX` if not found.

---

### findGamepadIndex

* `static size_t findGamepadIndex(int id)`
* C++ only

Returns the internal index of the controller with the given id, or `SIZE_MAX` if it is not connected. Most code should use [isGamepadConnected](#isgamepadconnected) and [getGamepadId](#getgamepadid) instead.
