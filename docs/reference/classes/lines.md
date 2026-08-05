---
description: Lines API reference (C++ and Lua).
---

# Lines

**Inherits:** [Object](object.md)  
**C++ type:** `Lines`

## Description

Renders a collection of 3D line segments. Useful for debug overlays, grids, trajectory paths, and other wireframe visuals. Each line is defined by two endpoints and an optional per-endpoint colour for gradient lines.

The `Lines` object maintains an internal dynamic buffer. Call `updateLines()` after modifying line data to upload changes to the GPU.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| unsigned int | [maxLines](#maxlines) | `100` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [load](#load) | C++ |
| void | [addLine](#addline) | C++ \| Lua |
| [LineData](linedata.md) | [getLine](#getline) | C++ \| Lua |
| void | [updateLine](#updateline) | C++ \| Lua |
| void | [removeLine](#removeline) | C++ \| Lua |
| void | [updateLines](#updatelines) | C++ \| Lua |
| size_t | [getNumLines](#getnumlines) | C++ \| Lua |
| void | [clearLines](#clearlines) | C++ \| Lua |

## Property details

### maxLines

* *Setter*: void **setMaxLines**(unsigned int maxLines)
* *Getter*: unsigned int **getMaxLines**() const

Pre-allocates buffer space for this many lines. Resize before calling `load()` for best performance.

---

## Method details

### load

* bool **load**()

Explicitly initialises the GPU buffer. This method is **C++ only** and is normally
optional because the render system initialises lines automatically.

---

### addLine

Several overloads are available:

* void **addLine**([LineData](linedata.md) line)
* void **addLine**(Vector3 pointA, Vector3 pointB)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector3 color)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector4 color)
* void **addLine**(Vector3 pointA, Vector3 pointB, Vector4 colorA, Vector4 colorB)

Adds a new line segment. The last overload lets each endpoint have a different colour.

=== "C++"
    ```cpp
    Lines debug(&scene);
    debug.load();
    debug.addLine(Vector3(0,0,0), Vector3(1,0,0), Vector4(1,0,0,1));  // red X axis
    debug.addLine(Vector3(0,0,0), Vector3(0,1,0), Vector4(0,1,0,1));  // green Y axis
    debug.addLine(Vector3(0,0,0), Vector3(0,0,1), Vector4(0,0,1,1));  // blue Z axis
    debug.updateLines();
    ```

=== "Lua"
    ```lua
    local debug = Lines(scene)
    debug:addLine(Vector3(0,0,0), Vector3(1,0,0), Vector4(1,0,0,1))
    debug:addLine(Vector3(0,0,0), Vector3(0,1,0), Vector4(0,1,0,1))
    debug:addLine(Vector3(0,0,0), Vector3(0,0,1), Vector4(0,0,1,1))
    debug:updateLines()
    ```

---

### getLine

* [LineData](linedata.md)& **getLine**(size_t index)

Returns a reference to the [LineData](linedata.md) at the given index. Modify in-place then call `updateLines()`.

---

### updateLine

* void **updateLine**(size_t index, ...)

Overwrites an existing line's endpoints and/or colour. Multiple overloads mirror `addLine()`. Call `updateLines()` afterwards.

---

### removeLine

* void **removeLine**(size_t index)

Removes the line at `index`. All subsequent indices shift down.

---

### updateLines

* void **updateLines**()

Uploads all pending line changes to the GPU. Must be called after any `addLine`, `updateLine`, or `removeLine` call.

---

### getNumLines

* size_t **getNumLines**()

Returns the current number of line segments.

---

### clearLines

* void **clearLines**()

Removes all line segments.
