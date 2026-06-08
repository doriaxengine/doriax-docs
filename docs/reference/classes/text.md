---
description: Text API reference (C++ and Lua).
---

# Text

**Inherits:** [UILayout](uilayout.md)  
**C++ type:** `Text`

## Description

Renders a unicode string with a TrueType or OpenType font. `Text` produces a quad mesh from glyph data at the specified font size. It supports multi-line wrapping, fixed-size constraints, and exposes per-character layout information for custom cursor or selection rendering.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [text](#text) | `""` | C++ \| Lua |
| std::string | [font](#font) | system default | C++ \| Lua |
| unsigned int | [fontSize](#fontsize) | `16` | C++ \| Lua |
| bool | [multiline](#multiline) | `false` | C++ \| Lua |
| unsigned int | [maxTextSize](#maxtextsize) | `0` (unlimited) | C++ \| Lua |
| Vector4 | [color](#color) | `(1,1,1,1)` | C++ \| Lua |
| float | [alpha](#color) | `1.0` | C++ \| Lua |
| bool | [fixedWidth](#fixedwidth-fixedheight) | `false` | C++ \| Lua |
| bool | [fixedHeight](#fixedwidth-fixedheight) | `false` | C++ \| Lua |
| bool | [flipY](#flipy) | `false` | C++ \| Lua |
| bool | [pivotBaseline](#pivotbaseline-pivotcentered) | `false` | C++ \| Lua |
| bool | [pivotCentered](#pivotbaseline-pivotcentered) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [createText](#createtext) | C++ \| Lua |
| float | [getAscent](#getascent-getdescent-getlinegap-getlineheight) | C++ \| Lua |
| float | [getDescent](#getascent-getdescent-getlinegap-getlineheight) | C++ \| Lua |
| float | [getLineGap](#getascent-getdescent-getlinegap-getlineheight) | C++ \| Lua |
| int | [getLineHeight](#getascent-getdescent-getlinegap-getlineheight) | C++ \| Lua |
| unsigned int | [getNumChars](#getnumchars) | C++ \| Lua |
| Vector2 | [getCharPosition](#getcharposition) | C++ \| Lua |
| float | [getCharWidth](#getcharwidth) | C++ \| Lua |
| [AABB](aabb.md) | [getAABB](#getaabb-getworldaabb) | C++ \| Lua |
| [AABB](aabb.md) | [getWorldAABB](#getaabb-getworldaabb) | C++ \| Lua |

## Property details

### text

* *Setter*: void **setText**(const std::string& text)
* *Getter*: std::string **getText**() const

The string to render. Supports UTF-8 encoded unicode.

=== "C++"
    ```cpp
    Text label(&scene);
    label.createText();
    label.setFont("fonts/Roboto-Regular.ttf");
    label.setFontSize(24);
    label.setText("Score: 0");
    label.setAnchorPreset(AnchorPreset::TOP_LEFT);
    ```

=== "Lua"
    ```lua
    local label = Text(scene)
    label:createText()
    label:setFont("fonts/Roboto-Regular.ttf")
    label:setFontSize(24)
    label:setText("Score: 0")
    label:setAnchorPreset(AnchorPreset.TOP_LEFT)
    ```

---

### font

* *Setter*: void **setFont**(const std::string& font)
* *Getter*: std::string **getFont**() const

File path to the TTF/OTF font file. If not set, the engine uses a built-in fallback font.

---

### fontSize

* *Setter*: void **setFontSize**(unsigned int fontSize)
* *Getter*: unsigned int **getFontSize**() const

The glyph render size in pixels (points at 72 DPI).

---

### multiline

* *Setter*: void **setMultiline**(bool multiline)
* *Getter*: bool **getMultiline**() const

When `true`, the text wraps to multiple lines at the element's width boundary.

---

### maxTextSize

* *Setter*: void **setMaxTextSize**(unsigned int maxTextSize)
* *Getter*: unsigned int **getMaxTextSize**() const

Maximum number of characters to render. `0` means unlimited. Used internally by [TextEdit](textedit.md).

---

### color

* *Setter*: void **setColor**(Vector4 color)
* *Setter*: void **setAlpha**(float alpha)
* *Getter*: Vector4 **getColor**() const / float **getAlpha**() const

RGBA tint colour applied to all glyphs.

---

### fixedWidth / fixedHeight

* *Setter*: void **setFixedWidth**(bool fixedWidth) / **setFixedHeight**(bool fixedHeight)
* *Setter*: void **setFixedSize**(bool fixedSize) — sets both at once
* *Getter*: bool **isFixedWidth**() / **isFixedHeight**() const

When `fixedWidth` is `false`, the text element automatically resizes its width to fit the rendered text. Same applies for height. Set to `true` to keep a fixed size and clip/wrap text instead.

---

### flipY

* *Setter*: void **setFlipY**(bool flipY)
* *Getter*: bool **isFlipY**() const

Flips glyph texture coordinates vertically.

---

### pivotBaseline / pivotCentered

* *Setter*: void **setPivotBaseline**(bool pivotBaseline) / **setPivotCentered**(bool pivotCentered)
* *Getter*: bool **isPivotBaseline**() / **isPivotCentered**() const

Controls the local-space pivot point. `pivotBaseline` moves the pivot to the text baseline; `pivotCentered` centres it on the bounding box.

---

## Method details

### createText

* bool **createText**()

Initialises the text rendering buffers. Must be called once before setting any text properties.

---

### getAscent / getDescent / getLineGap / getLineHeight

* float **getAscent**() const
* float **getDescent**() const
* float **getLineGap**() const
* int **getLineHeight**() const

Font metrics in pixels for the current `fontSize`. Useful for precise cursor or selection rendering.

---

### getNumChars

* unsigned int **getNumChars**() const

Number of rendered characters in the current string (may differ from `strlen` for multi-byte UTF-8 input).

---

### getCharPosition

* Vector2 **getCharPosition**(unsigned int index) const

Returns the local-space position (top-left of the glyph bounding box) for the character at `index`.

---

### getCharWidth

* float **getCharWidth**(char c) const

Returns the advance width of character `c` in pixels at the current font size.

---

### getAABB / getWorldAABB

* [AABB](aabb.md) **getAABB**() const
* [AABB](aabb.md) **getWorldAABB**() const

Returns the axis-aligned bounding box of the rendered text in local or world space.
