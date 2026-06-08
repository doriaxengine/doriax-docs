---
description: Rect API reference (C++ and Lua).
---

# Rect

**C++ type:** `Rect`

## Description

An axis-aligned rectangle defined by an origin `(x, y)` and size `(width, height)`. Used throughout the engine for screen regions, texture atlas frames, viewport definitions, and UI layouts.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [x](#x-y-width-height) | `0.0` | C++ \| Lua |
| float | [y](#x-y-width-height) | `0.0` | C++ \| Lua |
| float | [width](#x-y-width-height) | `0.0` | C++ \| Lua |
| float | [height](#x-y-width-height) | `0.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setRect](#setrect) | C++ \| Lua |
| Vector4 | [getVector](#getvector) | C++ \| Lua |
| Rect& | [fitOnRect](#fitonrect) | C++ \| Lua |
| bool | [contains](#contains) | C++ \| Lua |
| bool | [isNormalized](#isnormalized) | C++ \| Lua |
| bool | [isZero](#iszero) | C++ \| Lua |
| std::string | [toString](#tostring) | C++ \| Lua |

## Property details

### x / y / width / height

* *Getter/Setter*: float **getX**() / void **setX**(float x)
* *Getter/Setter*: float **getY**() / void **setY**(float y)
* *Getter/Setter*: float **getWidth**() / void **setWidth**(float width)
* *Getter/Setter*: float **getHeight**() / void **setHeight**(float height)

The four components of the rectangle.

=== "C++"
    ```cpp
    Rect r(10.0f, 20.0f, 100.0f, 50.0f);  // x=10, y=20, w=100, h=50
    ```

=== "Lua"
    ```lua
    local r = Rect(10, 20, 100, 50)
    ```

---

## Method details

### setRect

* void **setRect**(float x, float y, float width, float height)
* void **setRect**(Rect rect)

Sets all four components at once.

---

### getVector

* Vector4 **getVector**()

Returns the rect as a `Vector4(x, y, width, height)`.

---

### fitOnRect

* Rect& **fitOnRect**(Rect rect)

Scales and positions this rect to fit inside `rect` while preserving the aspect ratio. Modifies in-place and returns `*this`.

---

### contains

* bool **contains**(Vector2 point)

Returns `true` if `point` lies inside this rectangle (inclusive).

=== "C++"
    ```cpp
    Rect bounds(0, 0, 800, 600);
    if (bounds.contains(Vector2(400, 300))) {
        // point is inside
    }
    ```

=== "Lua"
    ```lua
    local bounds = Rect(0, 0, 800, 600)
    if bounds:contains(Vector2(400, 300)) then
        -- point is inside
    end
    ```

---

### isNormalized

* bool **isNormalized**() const

Returns `true` if all components are in the `[0, 1]` range, as expected for normalised UV or NDC coordinates.

---

### isZero

* bool **isZero**() const

Returns `true` if all four components are zero.

---

### toString

* std::string **toString**() const

Returns a human-readable string like `"Rect(10.000000, 20.000000, 100.000000, 50.000000)"`.
