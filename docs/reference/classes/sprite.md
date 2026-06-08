---
description: Sprite API reference — 2D images, texture atlas frames, pivot, and sprite animation.
---

# Sprite

## Description

`Sprite` is the primary class for 2D images and sprite sheets. It renders a textured quad, supports texture atlas frames for manual sprite selection, and provides a simple frame animation player for looping sequences.

**Inherits:** [Mesh](mesh.md) → [Object](object.md) → [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Sprite sprite(&scene);
    sprite.setTexture("sprites/character.png");
    sprite.setSize(64, 64);
    sprite.createSprite();
    ```

=== "Lua"

    ```lua
    local sprite = Sprite(scene)
    sprite:setTexture("sprites/character.png")
    sprite:setSize(64, 64)
    sprite:createSprite()
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| unsigned int | [width](#width-height) | `0` | C++ \| Lua |
| unsigned int | [height](#width-height) | `0` | C++ \| Lua |
| bool | [flipY](#flipy) | `false` | C++ \| Lua |
| float | [textureScaleFactor](#texturescalefactor) | `1.0` | C++ \| Lua |
| Rect | [textureRect](#texturerect) | full texture | C++ \| Lua |
| [PivotPreset](#pivotpreset) | [pivotPreset](#pivotpreset_1) | `CENTER` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| bool | [createSprite](#createsprite) | C++ \| Lua |
| void | [setSize](#setsize) | C++ \| Lua |
| void | setWidth | C++ \| Lua |
| void | setHeight | C++ \| Lua |
| unsigned int | getWidth | C++ \| Lua |
| unsigned int | getHeight | C++ \| Lua |
| void | setFlipY | C++ \| Lua |
| bool | isFlipY | C++ \| Lua |
| void | setTextureScaleFactor | C++ \| Lua |
| float | getTextureScaleFactor | C++ \| Lua |
| void | [setTextureRect](#settexturerect) | C++ \| Lua |
| Rect | getTextureRect | C++ \| Lua |
| void | setPivotPreset | C++ \| Lua |
| PivotPreset | getPivotPreset | C++ \| Lua |
| void | [addFrame](#addframe) | C++ \| Lua |
| void | [removeFrame](#removeframe) | C++ \| Lua |
| void | [setFrame](#setframe) | C++ \| Lua |
| void | [startAnimation](#startanimation) | C++ \| Lua |
| void | [pauseAnimation](#pauseanimation) | C++ \| Lua |
| void | [resumeAnimation](#resumeanimation) | C++ \| Lua |
| void | [stopAnimation](#stopanimation) | C++ \| Lua |

## Enumerations

### PivotPreset

Controls the origin point used for position and rotation.

* **CENTER** — Origin at the geometric center of the sprite (default).
* **TOP_LEFT** — Origin at the top-left corner.
* **TOP_CENTER** — Origin at the top-center.
* **TOP_RIGHT** — Origin at the top-right corner.
* **CENTER_LEFT** — Origin at the center-left edge.
* **CENTER_RIGHT** — Origin at the center-right edge.
* **BOTTOM_LEFT** — Origin at the bottom-left corner.
* **BOTTOM_CENTER** — Origin at the bottom-center.
* **BOTTOM_RIGHT** — Origin at the bottom-right corner.

## Property details

### width / height

* *Setter:* `void setWidth(unsigned int width)` / `void setHeight(unsigned int height)`
* *Setter combined:* `void setSize(unsigned int width, unsigned int height)`
* *Getter:* `unsigned int getWidth() const` / `unsigned int getHeight() const`

Physical size of the rendered quad in world units. If both are zero, the sprite uses the texture dimensions automatically after `createSprite()`.

---

### flipY

* *Setter:* `void setFlipY(bool flipY)`
* *Getter:* `bool isFlipY() const`

Flips the texture vertically. Useful when loading textures from APIs that use a top-left origin (e.g. some framebuffer captures).

---

### textureScaleFactor

* *Setter:* `void setTextureScaleFactor(float textureScaleFactor)`
* *Getter:* `float getTextureScaleFactor() const`

Scales the texture coordinates, effectively tiling or shrinking the mapped texture without changing the quad size.

---

### textureRect

* *Setter:* `void setTextureRect(float x, float y, float width, float height)`
* *Setter:* `void setTextureRect(Rect textureRect)`
* *Getter:* `Rect getTextureRect() const`

Defines the sub-rectangle of the texture to display, in **pixel** coordinates. Use to select a region from a texture atlas without defining named frames.

---

### pivotPreset

* *Setter:* `void setPivotPreset(PivotPreset pivotPreset)`
* *Getter:* `PivotPreset getPivotPreset() const`

Sets the pivot (origin) point used for position placement and rotation. See [PivotPreset](#pivotpreset).

## Method details

### createSprite

* `bool createSprite()`

Builds the quad geometry and uploads it to the GPU. Must be called at least once after setting the texture and size. Returns `true` on success.

=== "C++"

    ```cpp
    Sprite sprite(&scene);
    sprite.setTexture("ui/button.png");
    sprite.setSize(128, 64);
    sprite.createSprite();
    ```

=== "Lua"

    ```lua
    local sprite = Sprite(scene)
    sprite:setTexture("ui/button.png")
    sprite:setSize(128, 64)
    sprite:createSprite()
    ```

---

### setSize

* `void setSize(unsigned int width, unsigned int height)`

Sets both width and height in a single call. Equivalent to calling `setWidth` and `setHeight` separately.

---

### setTextureRect

* `void setTextureRect(float x, float y, float width, float height)`
* `void setTextureRect(Rect textureRect)`

Restricts rendering to a sub-region of the texture. Coordinates are in **pixels** from the top-left of the texture image.

=== "C++"

    ```cpp
    // Show only the 64×64 region starting at (0,0) of the atlas
    sprite.setTextureRect(0.0f, 0.0f, 64.0f, 64.0f);
    ```

=== "Lua"

    ```lua
    sprite:setTextureRect(0, 0, 64, 64)
    ```

---

### addFrame

* `void addFrame(int id, const std::string& name, Rect rect)`
* `void addFrame(const std::string& name, float x, float y, float width, float height)`
* `void addFrame(float x, float y, float width, float height)` *(auto-increment id)*
* `void addFrame(Rect rect)` *(auto-increment id)*

Registers a named frame in the sprite sheet. Frames are used by [setFrame](#setframe) and [startAnimation](#startanimation).

=== "C++"

    ```cpp
    sprite.addFrame(0, "idle",  Rect(  0, 0, 64, 64));
    sprite.addFrame(1, "run_1", Rect( 64, 0, 64, 64));
    sprite.addFrame(2, "run_2", Rect(128, 0, 64, 64));
    ```

=== "Lua"

    ```lua
    sprite:addFrame(0, "idle",  Rect(  0, 0, 64, 64))
    sprite:addFrame(1, "run_1", Rect( 64, 0, 64, 64))
    sprite:addFrame(2, "run_2", Rect(128, 0, 64, 64))
    ```

---

### removeFrame

* `void removeFrame(int id)`
* `void removeFrame(const std::string& name)`

Removes a registered frame by ID or name.

---

### setFrame

* `void setFrame(int id)`
* `void setFrame(const std::string& name)`

Immediately displays the registered frame with the given ID or name, overriding any active animation.

=== "C++"

    ```cpp
    sprite.setFrame("idle");
    ```

=== "Lua"

    ```lua
    sprite:setFrame("idle")
    ```

---

### startAnimation

* `void startAnimation(std::vector<int> frames, std::vector<int> framesTime, bool loop)`
* `void startAnimation(int startFrame, int endFrame, int interval, bool loop)`
* `void startAnimation(const std::string& name, int interval, bool loop)`

Plays a frame animation. Time values are in milliseconds.

* The first overload accepts explicit frame ID lists and per-frame durations.
* The second overload plays a contiguous range of frame IDs at a fixed interval.
* The third overload plays all frames whose names begin with `name` at a fixed interval.

=== "C++"

    ```cpp
    // Play frames 1 and 2 alternating, 150 ms each, looping
    sprite.startAnimation({1, 2}, {150, 150}, true);
    // or range:
    sprite.startAnimation(1, 2, 150, true);
    ```

=== "Lua"

    ```lua
    sprite:startAnimation(1, 2, 150, true)
    ```

---

### pauseAnimation

* `void pauseAnimation()`

Freezes the animation at the current frame. Call [resumeAnimation](#resumeanimation) to continue.

---

### resumeAnimation

* `void resumeAnimation()`

Resumes a paused animation from where it was stopped.

---

### stopAnimation

* `void stopAnimation()`

Stops the animation and resets to the first frame of the sequence.
