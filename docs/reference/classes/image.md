---
description: Image API reference (C++ and Lua).
---

# Image

**Inherits:** [UILayout](uilayout.md)  
**C++ type:** `Image`

## Description

The foundational 2D UI visual element. `Image` renders a textured or colour-filled rectangle with optional 9-patch scaling. It is the base class for [Button](button.md), [Panel](panel.md), [Progressbar](progressbar.md), [Scrollbar](scrollbar.md), and [TextEdit](textedit.md).

9-patch scaling (also called *scale-9* or *nine-slice*) divides the image into a 3×3 grid. The four corner pieces are never stretched, while the edges and centre fill the available space. This allows buttons and panel backgrounds to scale to any size without distorting the corners.

All UI elements also expose a rich set of pointer/focus callback events (inherited via `UIComponent`). See the [Callback events](#callback-events) section.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| Vector4 | [color](#color) | `(1,1,1,1)` | C++ \| Lua |
| float | [alpha](#color) | `1.0` | C++ \| Lua |
| bool | [flipY](#flipy) | `false` | C++ \| Lua |
| unsigned int | [patchMarginLeft](#patchmargin) | `0` | C++ \| Lua |
| unsigned int | [patchMarginRight](#patchmargin) | `0` | C++ \| Lua |
| unsigned int | [patchMarginTop](#patchmargin) | `0` | C++ \| Lua |
| unsigned int | [patchMarginBottom](#patchmargin) | `0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [createImage](#createimage) | C++ |
| void | [setTexture](#settexture) | C++ \| Lua |
| void | [setPatchMargin](#patchmargin) | C++ \| Lua |
| void | [setColor](#color) | C++ \| Lua |
| void | [setAlpha](#color) | C++ \| Lua |
| AABB | [getAABB](#getaabb-getworldaabb) | C++ \| Lua |
| AABB | [getWorldAABB](#getaabb-getworldaabb) | C++ \| Lua |

### Callback events

| Callback | Name | Langs |
| --- | --- | --- |
| void() | [onGetFocus](#ongetfocus-onlostfocus) | C++ \| Lua |
| void() | [onLostFocus](#ongetfocus-onlostfocus) | C++ \| Lua |
| void(float,float) | [onPointerEnter](#onpointerenter-onpointerleave) | C++ \| Lua |
| void(float,float) | [onPointerLeave](#onpointerenter-onpointerleave) | C++ \| Lua |
| void(float,float) | [onPointerMove](#onpointermove) | C++ \| Lua |
| void(float,float) | [onPointerDown](#onpointerdown-onpointerup) | C++ \| Lua |
| void(float,float) | [onPointerUp](#onpointerdown-onpointerup) | C++ \| Lua |
| void(float,float) | [onClick](#onclick-ondoubleclick) | C++ \| Lua |
| void(float,float) | [onDoubleClick](#onclick-ondoubleclick) | C++ \| Lua |
| void(float,float) | [onDragStart](#ondragstart-ondrag-ondragend) | C++ \| Lua |
| void(float,float) | [onDrag](#ondragstart-ondrag-ondragend) | C++ \| Lua |
| void(float,float) | [onDragEnd](#ondragstart-ondrag-ondragend) | C++ \| Lua |

## Property details

### color

* *Setter*: void **setColor**(Vector4 color)
* *Setter*: void **setColor**(float red, float green, float blue, float alpha)
* *Setter*: void **setColor**(float red, float green, float blue)
* *Setter*: void **setAlpha**(float alpha)
* *Getter*: Vector4 **getColor**() const
* *Getter*: float **getAlpha**() const

The tint colour multiplied with the texture. `(1,1,1,1)` renders the texture as-is. Changing the colour is a cheap way to create hover/pressed states without separate textures.

---

### flipY

* *Setter*: void **setFlipY**(bool flipY)
* *Getter*: bool **isFlipY**() const

Flips the texture vertically. Useful when a texture is loaded upside-down or for certain rendering passes.

---

### patchMargin

* *Setter*: void **setPatchMargin**(unsigned int margin)
* *Setter*: void **setPatchMargin**(unsigned int left, unsigned int right, unsigned int top, unsigned int bottom)
* Individual getters: **getPatchMarginLeft**, **getPatchMarginRight**, **getPatchMarginTop**, **getPatchMarginBottom**

Sets the 9-patch insets. When all four margins are zero (the default), the image is scaled uniformly. Setting the margins enables 9-patch mode where the corners are preserved.

=== "C++"
    ```cpp
    Image panel(&scene);
    panel.createImage();
    panel.setTexture("ui/panel_bg.png");
    panel.setPatchMargin(20);  // 20px on all sides
    panel.setSize(300, 200);
    ```

=== "Lua"
    ```lua
    local panel = Image(scene)
    panel:setTexture("ui/panel_bg.png")
    panel:setPatchMargin(20)
    panel:setSize(300, 200)
    ```

---

## Method details

### createImage

* bool **createImage**()

Explicitly builds the image geometry and GPU buffers. This method is **C++ only** and
is normally optional because the UI system builds and rebuilds images automatically.
Use it when C++ code needs the geometry immediately.

---

### setTexture

* void **setTexture**(const std::string& path)
* void **setTexture**(const std::string& id, TextureData data)
* void **setTexture**(Framebuffer* framebuffer)

Assigns the texture to display. Pass a file path, in-memory pixel data with a cache id, or a framebuffer for render-to-texture UI.

---

### getAABB / getWorldAABB

* [AABB](aabb.md) **getAABB**() const
* [AABB](aabb.md) **getWorldAABB**() const

Returns the axis-aligned bounding box in local or world space. Useful for hit-testing or layout calculations.

---

## Callback event details

### onGetFocus / onLostFocus

* *Property*: FunctionSubscribe<void()\> **onGetFocus**
* *Property*: FunctionSubscribe<void()\> **onLostFocus**

Called when this element gains or loses keyboard focus.

---

### onPointerEnter / onPointerLeave

* *Property*: FunctionSubscribe<void(float,float)\> **onPointerEnter**
* *Property*: FunctionSubscribe<void(float,float)\> **onPointerLeave**
* *Callback*: void(float x, float y)

Called when the mouse pointer enters or leaves the element boundary.

=== "C++"
    ```cpp
    Image btn(&scene);
    btn.createImage();
    btn.getComponent<UIComponent>().onPointerEnter.add("enter", [&](float x, float y){
        btn.setColor(Vector4(0.8f, 0.8f, 1.0f, 1.0f));  // highlight
    });
    btn.getComponent<UIComponent>().onPointerLeave.add("leave", [&](float x, float y){
        btn.setColor(Vector4(1.0f, 1.0f, 1.0f, 1.0f));  // reset
    });
    ```

=== "Lua"
    ```lua
    local ui = btn:getUIComponent()
    ui.onPointerEnter = function(x, y)
        btn.color = Vector4(0.8, 0.8, 1.0, 1.0)
    end
    ui.onPointerLeave = function(x, y)
        btn.color = Vector4(1.0, 1.0, 1.0, 1.0)
    end
    ```

---

### onPointerMove

* *Property*: FunctionSubscribe<void(float,float)\> **onPointerMove**
* *Callback*: void(float x, float y)

Called each frame the pointer moves while over this element.

---

### onPointerDown / onPointerUp

* *Property*: FunctionSubscribe<void(float,float)\> **onPointerDown**
* *Property*: FunctionSubscribe<void(float,float)\> **onPointerUp**
* *Callback*: void(float x, float y)

Called on mouse/touch press and release.

---

### onClick / onDoubleClick

* *Property*: FunctionSubscribe<void(float,float)\> **onClick**
* *Property*: FunctionSubscribe<void(float,float)\> **onDoubleClick**
* *Callback*: void(float x, float y)

Called on a complete click (press + release inside the element) or double click.

---

### onDragStart / onDrag / onDragEnd

* *Property*: FunctionSubscribe<void(float,float)\> **onDragStart**
* *Property*: FunctionSubscribe<void(float,float)\> **onDrag**
* *Property*: FunctionSubscribe<void(float,float)\> **onDragEnd**
* *Callback*: void(float x, float y)

Fired when the user begins dragging, continues dragging, or releases while dragging this element.
