---
description: Text API reference (C++ and Lua).
---

# Text

**Inherits:** [UILayout](uilayout.md)  
**C++ type:** `Text`

## Description

Renders a unicode string with a TrueType or OpenType font. `Text` produces a quad mesh from glyph data at the specified font size. It supports multi-line wrapping, fixed-size constraints, and exposes per-character layout information for custom cursor or selection rendering.

Text is shaped before it is drawn, so scripts that need contextual glyph forms work without any extra setup: Arabic letters join, ligatures and kerning are applied, and right-to-left runs are reordered by the Unicode Bidirectional Algorithm. A line mixing Arabic and Latin is laid out with each run in its own direction.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [text](#text) | `""` | C++ \| Lua |
| std::string | [font](#font) (slot 0) | `""` (built-in) | C++ \| Lua |
| unsigned int | [fontSize](#fontsize) | `20` | C++ \| Lua |
| bool | [multiline](#multiline) | `true` | C++ \| Lua |
| unsigned int | [maxTextSize](#maxtextsize) | `100` | C++ \| Lua |
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
| bool | [createText](#createtext) | C++ |
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
    label.font = "fonts/Roboto-Regular.ttf"
    label.fontSize = 24
    label.text = "Score: 0"
    label.anchorPreset = AnchorPreset.TOP_LEFT
    ```

---

### font

* *Setter*: void **setFont**(const std::string& font)
* *Setter*: void **setFont**(unsigned int index, const std::string& font)
* *Getter*: std::string **getFont**() const
* *Getter*: std::string **getFont**(unsigned int index) const

File path to a TTF/OTF font file, or a TrueType collection (`.ttc`). The `font`
property and the overloads without an index read or write slot `0`, the main font.
Setting the main font does not clear the fallback slots.

Doriax stores a fixed `FontArray` with `MAX_TEXT_FONTS` slots (four by default). Index
`0` is the main font; indexes `1` through `3` are tried in order when an earlier font
does not contain a character. Empty slots are skipped. Indexes are zero-based in both
C++ and Lua.

Two fonts are built into the engine and always close the chain: a Latin subset of Roboto
and an Arabic subset of Noto Sans Arabic. Any codepoint the custom fonts do not cover is
drawn from them, so setting an Arabic-only font still renders Latin, and leaving slot `0`
unset still renders Arabic. A codepoint no font in the chain covers is drawn as the
missing-glyph box.

A missing main-font file prevents that atlas from loading. A missing fallback is logged
and skipped, so later fallbacks and the built-in fonts can still render the text.

Use the indexed overloads to assign fallback fonts:

=== "C++"
    ```cpp
    Text label(&scene);
    label.setFont("fonts/MyLatin.ttf");
    label.setFont(1, "fonts/NotoKufiArabic.ttf");
    label.setFont(2, "fonts/NotoSansCJK.ttc");
    label.setText("hello مرحبا 你好");
    ```

=== "Lua"
    ```lua
    local label = Text(scene)
    label.font = "fonts/MyLatin.ttf"
    label:setFont(1, "fonts/NotoKufiArabic.ttf")
    label:setFont(2, "fonts/NotoSansCJK.ttc")
    label.text = "hello مرحبا 你好"
    ```

!!! note
    Texts only share a glyph atlas when their whole chain matches, so keep the slots
    identical across elements that use the same font.

An out-of-range index is rejected and logged. `getFont(index)` returns an empty string
for an invalid index.

At the component level, `TextComponent::font` is the same `FontArray`, so direct C++
component access uses `text.font[0]` for the main font and `text.font[1]` onward for
fallbacks.

!!! warning "Migrating from fontFallbacks"
    The `fontFallbacks` property and `setFontFallbacks` / `getFontFallbacks` methods no
    longer exist. Replace a semicolon-separated fallback list with one indexed
    `setFont` call per font. The editor still accepts the former scalar `font` scene
    field as slot `0`; newly saved scenes write `font` as an ordered sequence.

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

Number of characters the vertex buffer is preallocated for. It is not a limit: a longer string grows the buffer automatically and logs a warning. Raise it up front for text that is known to be long, to avoid the reallocation.

---

### color

* *Setter*: void **setColor**(Vector4 color)
* *Setter*: void **setAlpha**(float alpha)
* *Getter*: Vector4 **getColor**() const / float **getAlpha**() const

RGBA tint colour applied to all glyphs, in sRGB. It is stored linear internally, so the value read back is the sRGB form of the stored one.

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

Flips glyph texture coordinates vertically. The engine normally picks this automatically from the camera; calling the setter takes over and pins the value.

---

### pivotBaseline / pivotCentered

* *Setter*: void **setPivotBaseline**(bool pivotBaseline) / **setPivotCentered**(bool pivotCentered)
* *Getter*: bool **isPivotBaseline**() / **isPivotCentered**() const

Controls the local-space pivot point. `pivotBaseline` moves the pivot to the text baseline; `pivotCentered` centres it on the bounding box.

---

## Method details

### createText

* bool **createText**()

Explicitly builds the text geometry and GPU buffers. This method is **C++ only** and
is normally optional because the UI system builds and rebuilds text automatically.
Use it when C++ code needs the geometry immediately.

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

Number of codepoints in the current string, excluding line breaks. This differs from `strlen` for multi-byte UTF-8 input, and from the number of glyphs drawn: shaping can merge codepoints into one ligature or expand one into several marks.

---

### getCharPosition

* Vector2 **getCharPosition**(unsigned int index) const

Returns the local-space pen position after the codepoint at `index`, in logical (string) order. Codepoints that shaping merged into a single cluster share one position.

For a caret or a selection in text that can be right-to-left, this is not enough on its own, because logical order and screen order differ. [TextEdit](textedit.md) handles that case internally.

---

### getCharWidth

* float **getCharWidth**(uint32_t codepoint) const

Returns the advance width of `codepoint` in pixels at the current font size, taken from the first font in the chain that covers it. Returns `0` when the font is not loaded yet.

This is the advance of the glyph in isolation. It is not the width the codepoint takes inside a string, where shaping may change the form, apply kerning, or merge it into a ligature.

---

### getAABB / getWorldAABB

* [AABB](aabb.md) **getAABB**() const
* [AABB](aabb.md) **getWorldAABB**() const

Returns the axis-aligned bounding box of the rendered text in local or world space.
