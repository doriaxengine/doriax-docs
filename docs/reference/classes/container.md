---
description: Container API reference (C++ and Lua).
---

# Container

**Inherits:** [UILayout](uilayout.md)  
**C++ type:** `Container`

## Description

An invisible layout container that automatically arranges child UI elements in a vertical or horizontal stack, with optional wrapping. Add UI children as child entities of the container's [Object](object.md); the container measures and positions them each frame.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [ContainerType](#containertype) | [type](#type) | `VERTICAL` | C++ \| Lua |
| bool | [useAllWrapSpace](#useallwrapspace) | `false` | C++ \| Lua |
| unsigned int | [wrapCellWidth](#wrapcellwidth-wrapcellheight) | `0` | C++ \| Lua |
| unsigned int | [wrapCellHeight](#wrapcellwidth-wrapcellheight) | `0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [resize](#resize) | C++ \| Lua |
| unsigned int | [getContentWidth](#getcontentwidth-getcontentheight) | C++ \| Lua |
| unsigned int | [getContentHeight](#getcontentwidth-getcontentheight) | C++ \| Lua |
| void | [setBoxExpand](#setboxexpand) | C++ \| Lua |

## Enumerations

### ContainerType

* **VERTICAL** — Children stacked top to bottom.
* **HORIZONTAL** — Children placed left to right.
* **VERTICAL_WRAP** — Children stacked vertically; new columns start when height is exhausted.
* **HORIZONTAL_WRAP** — Children placed horizontally; new rows start when width is exhausted.

---

## Property details

### type

* *Setter*: void **setType**([ContainerType](#containertype) type)
* *Getter*: [ContainerType](#containertype) **getType**() const

Layout direction.

=== "C++"
    ```cpp
    Container menu(&scene);
    menu.setAnchorPreset(AnchorPreset::CENTER);
    menu.setType(ContainerType::VERTICAL);

    Button btnPlay(&scene);
    btnPlay.createImage();
    btnPlay.setSize(200, 48);
    btnPlay.setParent(menu);

    Button btnQuit(&scene);
    btnQuit.createImage();
    btnQuit.setSize(200, 48);
    btnQuit.setParent(menu);
    ```

=== "Lua"
    ```lua
    local menu = Container(scene)
    menu:setAnchorPreset(AnchorPreset.CENTER)
    menu:setType(ContainerType.VERTICAL)

    local btnPlay = Button(scene)
    btnPlay:createImage()
    btnPlay:setSize(200, 48)
    btnPlay:setParent(menu)

    local btnQuit = Button(scene)
    btnQuit:createImage()
    btnQuit:setSize(200, 48)
    btnQuit:setParent(menu)
    ```

---

### useAllWrapSpace

* *Setter*: void **setUseAllWrapSpace**(bool useAllWrapSpace)
* *Getter*: bool **isUseAllWrapSpace**() const

When `true` and the layout is a wrap type, the cells are distributed evenly to fill the available space.

---

### wrapCellWidth / wrapCellHeight

* *Setters/Getters*: **setWrapCellWidth** / **getWrapCellWidth**, **setWrapCellHeight** / **getWrapCellHeight**

Fixed cell size used when the layout type is `VERTICAL_WRAP` or `HORIZONTAL_WRAP`.

---

## Method details

### resize

* void **resize**()

Forces an immediate layout recalculation. Normally the container updates automatically each frame, but you can call this after batch-adding children to avoid a one-frame lag.

---

### getContentWidth / getContentHeight

* unsigned int **getContentWidth**() const
* unsigned int **getContentHeight**() const

Returns the total size of all laid-out children. Use this to size a [Scrollbar](scrollbar.md) relative to the visible area.

---

### setBoxExpand

* void **setBoxExpand**(bool expand) — applies to all children
* void **setBoxExpand**(size_t id, bool expand)
* bool **isBoxExpand**(size_t id) const

Controls whether a specific child slot expands to fill available space. When `expand` is `true`, the slot grows to fill the remaining parent area not occupied by fixed-size children.
