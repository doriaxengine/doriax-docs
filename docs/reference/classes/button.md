---
description: Button API reference (C++ and Lua).
---

# Button

**Inherits:** [Image](image.md)  
**C++ type:** `Button`

## Description

An interactive UI button widget. `Button` extends [Image](image.md) with four visual states — *normal*, *hovered*, *pressed*, and *disabled* — each of which can have a distinct texture or tint colour. An optional text label can be embedded inside the button.

Use the `onPress` / `onRelease` callbacks to respond to user interaction.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [label](#label) | `""` | C++ \| Lua |
| Vector4 | [labelColor](#label) | `(1,1,1,1)` | C++ \| Lua |
| std::string | [labelFont](#label) | system font | C++ \| Lua |
| unsigned int | [labelFontSize](#label) | `16` | C++ \| Lua |
| Vector4 | [colorNormal](#statecolors) | `(1,1,1,1)` | C++ \| Lua |
| Vector4 | [colorHovered](#statecolors) | `(1,1,1,1)` | C++ \| Lua |
| Vector4 | [colorPressed](#statecolors) | `(1,1,1,1)` | C++ \| Lua |
| Vector4 | [colorDisabled](#statecolors) | `(1,1,1,1)` | C++ \| Lua |
| bool | [disabled](#disabled) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [hasLabel](#haslabel) | C++ \| Lua |
| [Text](text.md) | [getLabelObject](#getlabelobject) | C++ \| Lua |
| void | [setTextureNormal](#statetextures) | C++ \| Lua |
| void | [setTextureHovered](#statetextures) | C++ \| Lua |
| void | [setTexturePressed](#statetextures) | C++ \| Lua |
| void | [setTextureDisabled](#statetextures) | C++ \| Lua |

### Callback events

| Callback | Name | Langs |
| --- | --- | --- |
| void() | [onPress](#onpress-onrelease) | C++ \| Lua |
| void() | [onRelease](#onpress-onrelease) | C++ \| Lua |

*All pointer events from [Image](image.md) are also available.*

## Property details

### label

* *Setter*: void **setLabel**(const std::string& text)
* *Getter*: std::string **getLabel**() const
* *Setter*: void **setLabelColor**(Vector4 color)
* *Setter*: void **setLabelFont**(const std::string& font)
* *Setter*: void **setLabelFontSize**(unsigned int fontSize)

The text displayed inside the button. Setting a non-empty label automatically creates a child [Text](text.md) entity. Font and colour apply to that label text.

---

### stateColors

* *Setter/Getter*: void **setColorNormal** / **getColorNormal**
* *Setter/Getter*: void **setColorHovered** / **getColorHovered**
* *Setter/Getter*: void **setColorPressed** / **getColorPressed**
* *Setter/Getter*: void **setColorDisabled** / **getColorDisabled**

Per-state tint colours multiplied with the current state texture. Use these to create hover and press effects with a single texture.

=== "C++"
    ```cpp
    Button btn(&scene);
    btn.createImage();
    btn.setTexture("ui/button.png");
    btn.setPatchMargin(12);
    btn.setSize(160, 48);
    btn.setLabel("Play");
    btn.setColorNormal(Vector4(1.0f, 1.0f, 1.0f, 1.0f));
    btn.setColorHovered(Vector4(0.85f, 0.85f, 1.0f, 1.0f));
    btn.setColorPressed(Vector4(0.7f, 0.7f, 1.0f, 1.0f));
    ```

=== "Lua"
    ```lua
    local btn = Button(scene)
    btn:setTexture("ui/button.png")
    btn:setPatchMargin(12)
    btn:setSize(160, 48)
    btn.label = "Play"
    btn.colorNormal = Vector4(1.0, 1.0, 1.0, 1.0)
    btn.colorHovered = Vector4(0.85, 0.85, 1.0, 1.0)
    btn.colorPressed = Vector4(0.7, 0.7, 1.0, 1.0)
    ```

---

### disabled

* *Setter*: void **setDisabled**(bool disabled)
* *Getter*: bool **getDisabled**() const

When `true`, the button ignores pointer events and displays with `colorDisabled` / `textureDisabled`. Use to grey out unavailable actions.

---

### statetextures

* void **setTextureNormal**(const std::string& path)
* void **setTextureHovered**(const std::string& path)
* void **setTexturePressed**(const std::string& path)
* void **setTextureDisabled**(const std::string& path)

Assigns a unique texture for each interaction state. If not set, all states use the base texture from [Image](image.md) tinted by the state colour.

---

## Method details

### hasLabel

* bool **hasLabel**() const

Returns `true` if a label child entity has been created for this button.

---

### getLabelObject

* [Text](text.md) **getLabelObject**() const

Returns a handle to the child [Text](text.md) entity. Useful for advanced label manipulation such as alignment or size.

---

## Callback event details

### onPress / onRelease

* *Property*: FunctionSubscribe<void()\> **onPress**
* *Property*: FunctionSubscribe<void()\> **onRelease**

`onPress` fires when the mouse button is pressed over the button element. `onRelease` fires when it is released.

=== "C++"
    ```cpp
    btn.getComponent<ButtonComponent>().onPress.add("pressed", [&](){
        Log::print("Button pressed!");
    });
    ```

=== "Lua"
    ```lua
    local btnComp = btn:getButtonComponent()
    btnComp.onPress = function()
        Log.print("Button pressed!")
    end
    ```
