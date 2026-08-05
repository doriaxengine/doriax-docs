---
description: Progressbar API reference (C++ and Lua).
---

# Progressbar

**Inherits:** [Image](image.md)  
**C++ type:** `Progressbar`

## Description

A UI widget that displays a value in the `[0, 1]` range as a filled bar. The bar can grow horizontally (left to right) or vertically (bottom to top). Both the background and the fill area support 9-patch textures and independent tint colours.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [ProgressbarType](#progressbartype) | [type](#type) | `HORIZONTAL` | C++ \| Lua |
| float | [value](#value) | `0.0` | C++ \| Lua |
| Vector4 | fillColor | `(1,1,1,1)` | C++ \| Lua |
| float | fillAlpha | `1.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| [Image](image.md) | [getFillObject](#getfillobject) | C++ \| Lua |
| void | [setFillTexture](#setfilltexture) | C++ \| Lua |
| void | [setFillColor](#setfillcolor) | C++ \| Lua |
| void | [setFillPatchMargin](#setfillpatchmargin) | C++ \| Lua |
| void | [setFillMargin](#setfillmargin) | C++ \| Lua |

## Enumerations

### ProgressbarType

* **HORIZONTAL** — Bar fills from left to right.
* **VERTICAL** — Bar fills from bottom to top.

---

## Property details

### type

* *Setter*: void **setType**([ProgressbarType](#progressbartype) type)
* *Getter*: [ProgressbarType](#progressbartype) **getType**() const

Direction of growth.

---

### value

* *Setter*: void **setValue**(float value)
* *Getter*: float **getValue**() const

Current fill amount. `0.0` = empty, `1.0` = full. Clamped to `[0, 1]`.

=== "C++"
    ```cpp
    Progressbar hp(&scene);
    hp.createImage();
    hp.setTexture("ui/progressbar_bg.png");
    hp.setFillTexture("ui/progressbar_fill.png");
    hp.setPatchMargin(6);
    hp.setFillColor(Vector4(0.2f, 0.8f, 0.2f, 1.0f));  // green
    hp.setSize(200, 24);
    hp.setValue(0.75f);
    ```

=== "Lua"
    ```lua
    local hp = Progressbar(scene)
    hp:setTexture("ui/progressbar_bg.png")
    hp:setFillTexture("ui/progressbar_fill.png")
    hp:setPatchMargin(6)
    hp.fillColor = Vector4(0.2, 0.8, 0.2, 1.0)
    hp:setSize(200, 24)
    hp.value = 0.75
    ```

---

## Method details

### getFillObject

* [Image](image.md) **getFillObject**() const

Returns the child [Image](image.md) entity that renders the fill area. Use this to set fill properties directly if you need more control than the convenience setters provide.

---

### setFillTexture

* void **setFillTexture**(const std::string& path)
* void **setFillTexture**(Framebuffer* framebuffer)

Sets the texture for the fill portion of the bar.

---

### setFillColor

* void **setFillColor**(Vector4 color)
* void **setFillColor**(float red, float green, float blue, float alpha)
* void **setFillAlpha**(float alpha)

Tint colour applied to the fill texture.

---

### setFillPatchMargin

* void **setFillPatchMargin**(int margin)
* void **setFillPatchMargin**(int marginLeft, int marginRight, int marginTop, int marginBottom)

9-patch insets for the fill image.

---

### setFillMargin

* void **setFillMargin**(int margin)
* void **setFillMargin**(int marginLeft, int marginRight, int marginTop, int marginBottom)

Pixel offset between the background edges and the fill image.
