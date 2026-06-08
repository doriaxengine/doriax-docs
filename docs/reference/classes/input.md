---
description: Input API reference — keyboard, mouse, and touch polling, modifiers, and key/button constants.
---

# Input

## Description

`Input` is a static polling class that provides the current keyboard, mouse, and touch state at any point during a frame. Use it inside `onUpdate` or `onFixedUpdate` to check whether a key or button is held down. For event-based input (press/release notifications), subscribe to the [Engine](engine.md) callback events instead.

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    // Inside an update callback:
    if (Input::isKeyPressed(S_KEY_SPACE)) {
        player.jump();
    }
    ```

=== "Lua"

    ```lua
    -- Inside update:
    if Input.isKeyPressed(S_KEY_SPACE) then
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

Key constants are preprocessor `#define` values (C++) and global numeric constants (Lua). Prefix: `S_KEY_`.

| Constant | Value | Description |
| --- | --- | --- |
| `S_KEY_SPACE` | 32 | Space bar |
| `S_KEY_A` … `S_KEY_Z` | 65–90 | Letter keys |
| `S_KEY_0` … `S_KEY_9` | 48–57 | Number row |
| `S_KEY_ESCAPE` | 256 | Escape |
| `S_KEY_ENTER` | 257 | Enter / Return |
| `S_KEY_TAB` | 258 | Tab |
| `S_KEY_BACKSPACE` | 259 | Backspace |
| `S_KEY_INSERT` | 260 | Insert |
| `S_KEY_DELETE` | 261 | Delete |
| `S_KEY_RIGHT` | 262 | Arrow right |
| `S_KEY_LEFT` | 263 | Arrow left |
| `S_KEY_DOWN` | 264 | Arrow down |
| `S_KEY_UP` | 265 | Arrow up |
| `S_KEY_PAGE_UP` | 266 | Page Up |
| `S_KEY_PAGE_DOWN` | 267 | Page Down |
| `S_KEY_HOME` | 268 | Home |
| `S_KEY_END` | 269 | End |
| `S_KEY_CAPS_LOCK` | 280 | Caps Lock |
| `S_KEY_F1` … `S_KEY_F25` | 290–314 | Function keys |
| `S_KEY_KP_0` … `S_KEY_KP_9` | 320–329 | Numpad digits |
| `S_KEY_KP_ENTER` | 335 | Numpad Enter |
| `S_KEY_LEFT_SHIFT` | 340 | Left Shift |
| `S_KEY_LEFT_CONTROL` | 341 | Left Ctrl |
| `S_KEY_LEFT_ALT` | 342 | Left Alt |
| `S_KEY_LEFT_SUPER` | 343 | Left Super (Win/Cmd) |
| `S_KEY_RIGHT_SHIFT` | 344 | Right Shift |
| `S_KEY_RIGHT_CONTROL` | 345 | Right Ctrl |
| `S_KEY_RIGHT_ALT` | 346 | Right Alt |
| `S_KEY_RIGHT_SUPER` | 347 | Right Super |
| `S_KEY_MENU` | 348 | Menu key |

## Mouse buttons

| Constant | Value | Description |
| --- | --- | --- |
| `S_MOUSE_BUTTON_LEFT` | 0 | Left button |
| `S_MOUSE_BUTTON_RIGHT` | 1 | Right button |
| `S_MOUSE_BUTTON_MIDDLE` | 2 | Middle button |
| `S_MOUSE_BUTTON_1` … `S_MOUSE_BUTTON_8` | 0–7 | All buttons |

## Modifiers

Modifier bits returned by [getModifiers](#getmodifiers) and passed to key/mouse callbacks.

| Constant | Bit | Description |
| --- | --- | --- |
| `S_MODIFIER_SHIFT` | `0x0001` | Shift key held |
| `S_MODIFIER_CONTROL` | `0x0002` | Ctrl key held |
| `S_MODIFIER_ALT` | `0x0004` | Alt key held |
| `S_MODIFIER_SUPER` | `0x0008` | Super (Win/Cmd) held |
| `S_MODIFIER_CAPS_LOCK` | `0x0010` | Caps Lock active |
| `S_MODIFIER_NUM_LOCK` | `0x0020` | Num Lock active |

## Method details

### isKeyPressed

* `static bool isKeyPressed(int key)`

Returns `true` while the given key is held down. Use `S_KEY_*` constants for the key code.

=== "C++"

    ```cpp
    if (Input::isKeyPressed(S_KEY_W)) {
        player.moveForward(Engine::getDeltatime() * speed);
    }
    ```

=== "Lua"

    ```lua
    if Input.isKeyPressed(S_KEY_W) then
        player:moveForward(Engine.deltatime * speed)
    end
    ```

---

### isMousePressed

* `static bool isMousePressed(int button)`

Returns `true` while the given mouse button is held down. Use `S_MOUSE_BUTTON_*` constants.

=== "C++"

    ```cpp
    if (Input::isMousePressed(S_MOUSE_BUTTON_LEFT)) {
        // drag logic
    }
    ```

=== "Lua"

    ```lua
    if Input.isMousePressed(S_MOUSE_BUTTON_LEFT) then
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
    if (mods & S_MODIFIER_SHIFT) {
        // Shift is held
    }
    ```

=== "Lua"

    ```lua
    local mods = Input.getModifiers()
    if (mods & S_MODIFIER_SHIFT) ~= 0 then
        -- Shift is held
    end
    ```

---

### findTouchIndex

* `static size_t findTouchIndex(int pointer)`

Returns the index into the [getTouches](#gettouches) array for the given pointer ID. Returns `SIZE_MAX` if not found.
