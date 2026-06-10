---
description: Input API reference — keyboard, mouse, and touch polling, modifiers, and key/button constants.
---

# Input

## Description

`Input` is a static polling class that provides the current keyboard, mouse, and touch state at any point during a frame. Use it inside `onUpdate` or `onFixedUpdate` to check whether a key or button is held down. For event-based input (press/release notifications), subscribe to the [Engine](engine.md) callback events instead.

!!! note "Constant naming differs by language"
    Key, mouse-button, and modifier constants are C++ preprocessor macros prefixed `D_`
    (e.g. `D_KEY_SPACE`, `D_MOUSE_BUTTON_LEFT`). In Lua they are static properties on the
    `Input` class with the `D_` prefix dropped (e.g. `Input.KEY_SPACE`,
    `Input.MOUSE_BUTTON_LEFT`).

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
| static int | [getModifiers](#getmodifiers) | C++ \| Lua |
| static size_t | [findTouchIndex](#findtouchindex) | C++ \| Lua |

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
