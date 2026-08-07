---
description: TextEdit API reference (C++ and Lua).
---

# TextEdit

**Inherits:** [Image](image.md)  
**C++ type:** `TextEdit`

## Description

An interactive single-line text input field. `TextEdit` composes an [Image](image.md) background, a [Text](text.md) display layer, and polygon overlays for the cursor and text selection highlight. It handles keyboard input, clipboard operations, cursor navigation, and optional password masking.

Editing works in text whose direction is not left to right. **Left** and **Right** move the caret one stop across the screen rather than one position along the string, matching where a click would put it, and **Home** and **End** go to the start and end of the line, which in a right-to-left line are its right and left edges. A selection that is contiguous in the string can appear as more than one highlighted block when it crosses a direction change.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [text](#text) | `""` | C++ \| Lua |
| std::string | [textFont](#textfont) | `""` (built-in) | C++ \| Lua |
| unsigned int | [fontSize](#fontsize) | `20` | C++ \| Lua |
| Vector4 | [textColor](#textcolor) | `(1,1,1,1)` | C++ \| Lua |
| unsigned int | [maxTextSize](#maxtextsize) | `100` | C++ \| Lua |
| std::string | [placeholder](#placeholder) | `""` | C++ \| Lua |
| Vector4 | [placeholderColor](#placeholder) | `(0.76,0.76,0.76,1)` | C++ \| Lua |
| bool | [password](#password) | `false` | C++ \| Lua |
| char | [passwordChar](#password) | `'*'` | C++ \| Lua |
| bool | [disabled](#disabled) | `false` | C++ \| Lua |
| int | [cursorIndex](#cursorindex) | `0` | C++ \| Lua |
| float | [cursorBlink](#cursorblink-cursorwidth-cursorcolor) | `0.6` | C++ \| Lua |
| float | [cursorWidth](#cursorblink-cursorwidth-cursorcolor) | `2.0` | C++ \| Lua |
| Vector4 | [cursorColor](#cursorblink-cursorwidth-cursorcolor) | `(0,0,0,1)` | C++ \| Lua |
| Vector4 | [selectionColor](#selectioncolor) | `(0.53,0.70,0.93,0.35)` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| [Text](text.md) | [getTextObject](#gettextobject) | C++ \| Lua |
| void | [setSelection](#setselection) | C++ \| Lua |
| int | [getSelectionAnchor](#setselection) | C++ \| Lua |
| int | [getSelectionFocus](#setselection) | C++ \| Lua |

## Property details

### text

* *Setter*: void **setText**(const std::string& text)
* *Getter*: std::string **getText**() const

The current content of the input field.

=== "C++"
    ```cpp
    TextEdit nameField(&scene);
    nameField.createImage();
    nameField.setTexture("ui/input_bg.png");
    nameField.setPatchMargin(8);
    nameField.setSize(280, 36);
    nameField.setPlaceholder("Enter your name...");
    nameField.setFontSize(18);
    ```

=== "Lua"
    ```lua
    local nameField = TextEdit(scene)
    nameField:setTexture("ui/input_bg.png")
    nameField:setPatchMargin(8)
    nameField:setSize(280, 36)
    nameField.placeholder = "Enter your name..."
    nameField.fontSize = 18
    ```

---

### textColor

* *Setter*: void **setTextColor**(Vector4 color)
* *Getter*: Vector4 **getTextColor**() const

RGBA tint colour applied to the input text glyphs.

---

### textFont

* *Setter*: void **setTextFont**(const std::string& font)
* *Getter*: std::string **getTextFont**() const

Path to the TTF/OTF font file used by the inner [Text](text.md). Falls back to the built-in fonts for codepoints it does not cover, see [Text.font](text.md#font).

---

### fontSize

* *Setter*: void **setFontSize**(unsigned int fontSize)
* *Getter*: unsigned int **getFontSize**() const

Glyph size in pixels.

---

### maxTextSize

* *Setter*: void **setMaxTextSize**(unsigned int maxTextSize)
* *Getter*: unsigned int **getMaxTextSize**() const

Maximum allowed number of characters. `0` means no limit.

---

### placeholder

* *Setter*: void **setPlaceholder**(const std::string& placeholder)
* *Getter*: std::string **getPlaceholder**() const
* *Setter*: void **setPlaceholderColor**(Vector4 color)
* *Getter*: Vector4 **getPlaceholderColor**() const

Ghost text displayed when the field is empty. Typically a prompt like `"Type here…"`.

---

### password

* *Setter*: void **setPassword**(bool password)
* *Getter*: bool **getPassword**() const
* *Setter*: void **setPasswordChar**(char passwordChar)
* *Getter*: char **getPasswordChar**() const

When `password` is `true`, each character is displayed as `passwordChar` (default `'*'`). The actual text is still accessible via `getText()`.

---

### disabled

* *Setter*: void **setDisabled**(bool disabled)
* *Getter*: bool **getDisabled**() const

When `true`, the field ignores keyboard and pointer events.

---

### cursorIndex

* *Setter*: void **setCursorIndex**(int cursorIndex)
* *Getter*: int **getCursorIndex**() const

Current insertion-point position in the string, not on screen (0 = before the first character, `getNumChars()` = after the last).

Where the direction changes, two neighbouring indices can sit on the same pixel. They are still separate insertion points, and typing at one does not give the same result as typing at the other, so arrow keys step through both.

---

### cursorBlink / cursorWidth / cursorColor

* *Setters/Getters*: **setCursorBlink** / **getCursorBlink**, **setCursorWidth** / **getCursorWidth**, **setCursorColor** / **getCursorColor**

Visual properties of the cursor caret. `cursorBlink` is the on/off period in seconds.

Colours are sRGB, matching what a colour picker shows. They are stored linear internally, so the value read back is the sRGB form of the stored one.

---

### selectionColor

* *Setter*: void **setSelectionColor**(Vector4 color)
* *Getter*: Vector4 **getSelectionColor**() const

Background colour of the text selection highlight polygon, in sRGB. The default is a translucent blue.

A selection that crosses a direction change is drawn as several blocks rather than one, since the selected characters are not contiguous on screen.

---

## Method details

### getTextObject

* [Text](text.md) **getTextObject**() const

Returns the child [Text](text.md) entity used for rendering the input content.

---

### setSelection

* void **setSelection**(int anchor, int focus)
* int **getSelectionAnchor**() const
* int **getSelectionFocus**() const

Programmatically set or query the text selection. `anchor` is the fixed end of the selection; `focus` is the cursor end that moves with keyboard navigation. Pass equal values to collapse the selection to a cursor.
