---
description: Scrollbar API reference (C++ and Lua).
---

# Scrollbar

**Inherits:** [Image](image.md)  
**C++ type:** `Scrollbar`

## Description

A UI scrollbar widget. The scrollbar consists of a track (the background [Image](image.md)) and a draggable bar handle (a child Image). Both can have independent textures and tint colours. The current scroll position is reported through the `onChange` callback.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [ScrollbarType](#scrollbartype) | [type](#type) | `VERTICAL` | C++ \| Lua |
| float | [barSize](#barsize) | `0.5` | C++ \| Lua |
| float | [step](#step) | `0.0` | C++ \| Lua |
| Vector4 | barColor | `(1,1,1,1)` | C++ \| Lua |
| float | barAlpha | `1.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| [Image](image.md) | [getBarObject](#getbarobject) | C++ \| Lua |
| void | [setBarTexture](#setbartexture) | C++ \| Lua |
| void | [setBarColor](#setbarcolor) | C++ \| Lua |
| void | [setBarPatchMargin](#setbarpatchmargin) | C++ \| Lua |
| void | [setBarMargin](#setbarmargin) | C++ \| Lua |

### Callback events

| Callback | Name | Langs |
| --- | --- | --- |
| void(float) | [onChange](#onchange) | C++ \| Lua |

## Enumerations

### ScrollbarType

* **VERTICAL** — Bar slides up and down.
* **HORIZONTAL** — Bar slides left and right.

---

## Property details

### type

* *Setter*: void **setType**([ScrollbarType](#scrollbartype) type)
* *Getter*: [ScrollbarType](#scrollbartype) **getType**() const

Orientation of the scrollbar.

---

### barSize

* *Setter*: void **setBarSize**(float size)
* *Getter*: float **getBarSize**() const

The relative size of the draggable handle as a fraction of the track length, in `[0, 1]`. Larger values represent a proportionally large viewport relative to the content (e.g. `0.5` means the viewport covers half the content).

---

### step

* *Setter*: void **setStep**(float step)
* *Getter*: float **getStep**() const

Snap increment in `[0, 1]`. When non-zero, the scroll position snaps to multiples of this value. `0` means continuous scrolling.

---

## Method details

### getBarObject

* [Image](image.md) **getBarObject**() const

Returns the child [Image](image.md) handle entity for the draggable bar.

---

### setBarTexture

* void **setBarTexture**(const std::string& path)
* void **setBarTexture**(Framebuffer* framebuffer)

Sets the texture for the bar handle.

---

### setBarColor

* void **setBarColor**(Vector4 color)
* void **setBarColor**(float red, float green, float blue, float alpha)
* void **setBarAlpha**(float alpha)

Tint colour applied to the bar handle texture.

---

### setBarPatchMargin

* void **setBarPatchMargin**(int margin)
* void **setBarPatchMargin**(int marginLeft, int marginRight, int marginTop, int marginBottom)

9-patch insets for the bar handle image.

---

### setBarMargin

* void **setBarMargin**(int margin)
* void **setBarMargin**(int marginLeft, int marginRight, int marginTop, int marginBottom)

Pixel offset between the track edges and the bar handle.

=== "C++"
    ```cpp
    Scrollbar vsb(&scene);
    vsb.createImage();
    vsb.setTexture("ui/scrollbar_track.png");
    vsb.setBarTexture("ui/scrollbar_handle.png");
    vsb.setBarPatchMargin(4);
    vsb.setBarSize(0.3f);
    vsb.setSize(16, 300);

    vsb.getComponent<ScrollbarComponent>().onChange.add("scroll", [&](float value){
        // value is in [0, 1]
        contentContainer.setPositionYOffset(-value * contentHeight);
    });
    ```

=== "Lua"
    ```lua
    local vsb = Scrollbar(scene)
    vsb:setTexture("ui/scrollbar_track.png")
    vsb:setBarTexture("ui/scrollbar_handle.png")
    vsb:setBarPatchMargin(4)
    vsb.barSize = 0.3
    vsb:setSize(16, 300)

    local vsbComp = vsb:getScrollbarComponent()
    vsbComp.onChange = function(value)
        contentContainer.positionYOffset = -value * contentHeight
    end
    ```

---

## Callback event details

### onChange

* *Property*: FunctionSubscribe<void(float)\> **onChange**
* *Callback*: void(float value)

Called whenever the scroll position changes. `value` is in `[0, 1]` where `0` is the start of the track and `1` is the end.
