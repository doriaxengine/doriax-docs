---
description: Panel API reference (C++ and Lua).
---

# Panel

**Inherits:** [Image](image.md)  
**C++ type:** `Panel`

## Description

A draggable, resizable floating window panel. `Panel` extends [Image](image.md) with a header bar that can display a title, and an optional container area below it. Users can drag the header to move the panel, drag the edges to resize it, and click to bring it to the front of other panels.

All child UI elements placed inside the panel are automatically clipped to the panel's content area.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [title](#title) | `""` | C++ \| Lua |
| [AnchorPreset](uilayout.md#anchorpreset) | [titleAnchorPreset](#title) | `CENTER` | C++ \| Lua |
| Vector4 | [titleColor](#title) | `(1,1,1,1)` | C++ \| Lua |
| std::string | [titleFont](#title) | system default | C++ \| Lua |
| unsigned int | [titleFontSize](#title) | `16` | C++ \| Lua |
| Vector4 | [headerColor](#header) | `(1,1,1,1)` | C++ \| Lua |
| int | [headerMarginLeft](#header) | `0` | C++ \| Lua |
| int | [headerMarginTop](#header) | `0` | C++ \| Lua |
| int | [headerMarginRight](#header) | `0` | C++ \| Lua |
| int | [headerMarginBottom](#header) | `0` | C++ \| Lua |
| int | [minWidth](#minwidth-minheight) | `0` | C++ \| Lua |
| int | [minHeight](#minwidth-minheight) | `0` | C++ \| Lua |
| int | [resizeMargin](#resizemargin) | `6` | C++ \| Lua |
| bool | [canMove](#windowproperties) | `true` | C++ \| Lua |
| bool | [canResize](#windowproperties) | `true` | C++ \| Lua |
| bool | [canBringToFront](#windowproperties) | `true` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [hasHeader](#hasheader) | C++ \| Lua |
| [Image](image.md) | [getHeaderImageObject](#header) | C++ \| Lua |
| [Container](container.md) | [getHeaderContainerObject](#header) | C++ \| Lua |
| [Text](text.md) | [getHeaderTextObject](#header) | C++ \| Lua |
| void | [setHeaderPatchMargin](#header) | C++ \| Lua |
| void | [setHeaderTexture](#header) | C++ \| Lua |
| void | [setHeaderMargin](#header) | C++ \| Lua |
| void | [setMinSize](#minwidth-minheight) | C++ \| Lua |
| void | [setWindowProperties](#windowproperties) | C++ \| Lua |

## Property details

### title

* *Setter*: void **setTitle**(const std::string& text)
* *Getter*: std::string **getTitle**() const
* *Setter*: void **setTitleAnchorPreset**([AnchorPreset](uilayout.md#anchorpreset) preset)
* *Setter*: void **setTitleColor**(Vector4 color)
* *Setter*: void **setTitleFont**(const std::string& font)
* *Setter*: void **setTitleFontSize**(unsigned int fontSize)

The window title shown in the header bar. Setting a non-empty title automatically creates child [Text](text.md) and [Container](container.md) entities for the header.

=== "C++"
    ```cpp
    Panel win(&scene);
    win.createImage();
    win.setTexture("ui/window_bg.png");
    win.setHeaderTexture("ui/window_header.png");
    win.setHeaderPatchMargin(8);
    win.setTitle("Settings");
    win.setSize(400, 300);
    win.setAnchorPreset(AnchorPreset::CENTER);
    ```

=== "Lua"
    ```lua
    local win = Panel(scene)
    win:setTexture("ui/window_bg.png")
    win:setHeaderTexture("ui/window_header.png")
    win:setHeaderPatchMargin(8)
    win.title = "Settings"
    win:setSize(400, 300)
    win.anchorPreset = AnchorPreset.CENTER
    ```

---

### header

* *Setter*: void **setHeaderTexture**(const std::string& path)
* *Setter*: void **setHeaderColor**(Vector4 color)
* *Setter*: void **setHeaderPatchMargin**(int margin)
* *Setter*: void **setHeaderMargin**(int left, int top, int right, int bottom)
* *Getters*: **getHeaderMarginLeft**, **getHeaderMarginTop**, **getHeaderMarginRight**, **getHeaderMarginBottom**
* *Accessors*: **getHeaderImageObject**, **getHeaderContainerObject**, **getHeaderTextObject**

Configuration for the panel's header bar. `setHeaderMargin()` defines the pixel inset from the panel edges to where the header bar begins.

---

### minWidth / minHeight

* *Setter*: void **setMinSize**(int minWidth, int minHeight)
* *Setter*: void **setMinWidth**(int minWidth) / **setMinHeight**(int minHeight)
* *Getter*: int **getMinWidth**() / **getMinHeight**() const

Minimum dimensions when [canResize](#windowproperties) is `true`.

---

### resizeMargin

* *Setter*: void **setResizeMargin**(int resizeMargin)
* *Getter*: int **getResizeMargin**() const

The width in pixels of the invisible hit area at the panel edges that triggers resize drag. Default is `6`.

---

### windowProperties

* *Setter*: void **setWindowProperties**(bool canMove, bool canResize, bool canBringToFront)
* *Setter/Getter*: **setCanMove** / **isCanMove**
* *Setter/Getter*: **setCanResize** / **isCanResize**
* *Setter/Getter*: **setCanBringToFront** / **isCanBringToFront**

Controls interactive window behaviours:

* **canMove** — user can drag the header to move the window.
* **canResize** — user can drag the edges to resize the window.
* **canBringToFront** — clicking anywhere on the panel raises its Z-order above siblings.

---

## Method details

### hasHeader

* bool **hasHeader**() const

Returns `true` if a header bar has been created (i.e. `setTitle()` has been called or a header texture has been set).
