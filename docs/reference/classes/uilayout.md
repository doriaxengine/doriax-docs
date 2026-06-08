---
description: UILayout API reference (C++ and Lua).
---

# UILayout

**Inherits:** [Object](object.md)  
**C++ type:** `UILayout`

## Description

Base class for all UI elements. `UILayout` extends [Object](object.md) with a pixel-based sizing and anchor system that lets widgets automatically resize and reposition relative to their parent container or the screen edges.

The anchor system works in two modes:

* **Fixed size** — the widget has an explicit `width`/`height`. The anchor points define which corner(s) of the parent the widget is attached to; anchor offsets define the pixel distance from those corners.
* **Stretch mode** — by setting anchor points on all four edges (e.g. `FULL_LAYOUT`), the widget automatically fills the available space, optionally with pixel margins.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| unsigned int | [width](#width-height) | `0` | C++ \| Lua |
| unsigned int | [height](#width-height) | `0` | C++ \| Lua |
| float | [anchorPointLeft](#anchorpoints) | `0.0` | C++ \| Lua |
| float | [anchorPointTop](#anchorpoints) | `0.0` | C++ \| Lua |
| float | [anchorPointRight](#anchorpoints) | `0.0` | C++ \| Lua |
| float | [anchorPointBottom](#anchorpoints) | `0.0` | C++ \| Lua |
| int | [anchorOffsetLeft](#anchoroffsets) | `0` | C++ \| Lua |
| int | [anchorOffsetTop](#anchoroffsets) | `0` | C++ \| Lua |
| int | [anchorOffsetRight](#anchoroffsets) | `0` | C++ \| Lua |
| int | [anchorOffsetBottom](#anchoroffsets) | `0` | C++ \| Lua |
| [AnchorPreset](#anchorpreset) | [anchorPreset](#anchorpreset_1) | `NONE` | C++ \| Lua |
| Vector2 | [positionOffset](#positionoffset) | `(0,0)` | C++ \| Lua |
| bool | [usingAnchors](#usinganchors) | `true` | C++ \| Lua |
| bool | [ignoreScissor](#ignorescissor) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setSize](#width-height) | C++ \| Lua |
| void | [setAnchorPoints](#anchorpoints) | C++ \| Lua |
| void | [setAnchorOffsets](#anchoroffsets) | C++ \| Lua |
| void | [setAnchorPreset](#anchorpreset_1) | C++ \| Lua |
| void | [setPositionOffset](#positionoffset) | C++ \| Lua |

## Enumerations

### AnchorPreset

Convenience presets for common anchor configurations:

* **NONE** — No anchor preset applied.
* **TOP_LEFT / TOP_RIGHT / BOTTOM_LEFT / BOTTOM_RIGHT** — Fixed-size widget anchored to a corner.
* **CENTER_LEFT / CENTER_TOP / CENTER_RIGHT / CENTER_BOTTOM** — Fixed-size widget centred on an edge.
* **CENTER** — Fixed-size widget centred in the parent.
* **LEFT_WIDE / TOP_WIDE / RIGHT_WIDE / BOTTOM_WIDE** — Stretches along one axis, fixed on the other.
* **VERTICAL_CENTER_WIDE** — Stretches vertically, centred horizontally.
* **HORIZONTAL_CENTER_WIDE** — Stretches horizontally, centred vertically.
* **FULL_LAYOUT** — Stretches to fill the entire parent.

---

## Property details

### width / height

* *Setter*: void **setWidth**(unsigned int width) / **setHeight**(unsigned int height)
* *Setter*: void **setSize**(unsigned int width, unsigned int height)
* *Getter*: unsigned int **getWidth**() / **getHeight**() const

Pixel dimensions of the UI element. Only used when the anchor configuration does not stretch the element.

---

### anchorPoints

* *Setter*: void **setAnchorPoints**(float left, float top, float right, float bottom)
* Individual setters/getters: **setAnchorPointLeft**, **setAnchorPointTop**, **setAnchorPointRight**, **setAnchorPointBottom**

Normalised values in `[0, 1]` defining where each edge of this element is attached within the parent. For example, `(0, 0, 0, 0)` pins the top-left corner; `(0, 0, 1, 1)` stretches to fill the parent.

---

### anchorOffsets

* *Setter*: void **setAnchorOffsets**(int left, int top, int right, int bottom)
* Individual setters/getters: **setAnchorOffsetLeft**, **setAnchorOffsetTop**, **setAnchorOffsetRight**, **setAnchorOffsetBottom**

Pixel margins from the anchor points. For a `FULL_LAYOUT` preset with a 10-pixel margin, set all offsets to `10`.

---

### anchorPreset

* *Setter*: void **setAnchorPreset**([AnchorPreset](#anchorpreset) anchorPreset)
* *Getter*: [AnchorPreset](#anchorpreset) **getAnchorPreset**() const

Applies a [AnchorPreset](#anchorpreset) that sets `anchorPoints` automatically.

=== "C++"
    ```cpp
    Image overlay(&scene);
    overlay.createImage();
    overlay.setAnchorPreset(AnchorPreset::FULL_LAYOUT);
    ```

=== "Lua"
    ```lua
    local overlay = Image(scene)
    overlay:createImage()
    overlay:setAnchorPreset(AnchorPreset.FULL_LAYOUT)
    ```

---

### positionOffset

* *Setter*: void **setPositionOffset**(Vector2 positionOffset)
* Individual: **setPositionXOffset**, **setPositionYOffset**
* *Getter*: Vector2 **getPositionOffset**() const

An additional pixel offset applied to the final computed position. Useful for fine-tuning placement without modifying the anchor configuration.

---

### usingAnchors

* *Setter*: void **setUsingAnchors**(bool usingAnchors)
* *Getter*: bool **isUsingAnchors**() const

When `false`, the element is positioned using the standard 3D transform from [Object](object.md) rather than the anchor system.

---

### ignoreScissor

* *Setter*: void **setIgnoreScissor**(bool ignoreScissor)
* *Getter*: bool **isIgnoreScissor**() const

When `true`, this element is not clipped to the parent's scissor rectangle. Use for tooltips or overlays that must extend beyond a scrollable container.
