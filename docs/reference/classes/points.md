---
description: Points API reference (C++ and Lua).
---

# Points

**Inherits:** [Object](object.md)  
**C++ type:** `Points`

## Description

Renders a collection of 3D billboard points (sprites). Each point is a camera-facing quad with an individual position, colour, size, rotation, and optional texture atlas frame. Useful for particle-like effects, star fields, or any situation where a large number of individually controlled sprites is needed.

Like [Lines](lines.md), `Points` uses a dynamic GPU buffer. Call `updatePoints()` after modifying point data.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| unsigned int | [maxPoints](#maxpoints) | `100` | C++ \| Lua |
| bool | [transparent](#transparent-autotransparency) | `false` | C++ \| Lua |
| bool | [autoTransparency](#transparent-autotransparency) | `true` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [load](#load) | C++ |
| void | [addPoint](#addpoint) | C++ \| Lua |
| [PointData](pointdata.md) | [getPoint](#getpoint) | C++ \| Lua |
| void | [updatePoint](#updatepoint) | C++ \| Lua |
| void | [removePoint](#removepoint) | C++ \| Lua |
| bool | [isPointVisible](#ispointvisible-setpointvisible) | C++ \| Lua |
| void | [setPointVisible](#ispointvisible-setpointvisible) | C++ \| Lua |
| void | [updatePoints](#updatepoints) | C++ \| Lua |
| size_t | [getNumPoints](#getnumpoints) | C++ \| Lua |
| void | [clearPoints](#clearpoints) | C++ \| Lua |
| void | [addSpriteFrame](#addspriteframe) | C++ \| Lua |
| void | [removeSpriteFrame](#addspriteframe) | C++ \| Lua |
| void | [setTexture](#settexture) | C++ \| Lua |

## Property details

### maxPoints

* *Setter*: void **setMaxPoints**(unsigned int maxPoints)
* *Getter*: unsigned int **getMaxPoints**() const

Pre-allocates GPU buffer space for this many points.

---

### transparent / autoTransparency

* *Setter/Getter*: void **setTransparent**(bool) / bool **isTransparent**()
* *Setter/Getter*: void **setAutoTransparency**(bool) / bool **isAutoTransparency**()

Controls transparency rendering for this points object. See [Mesh](mesh.md#transparent-autotransparency) for details.

---

## Method details

### load

* bool **load**()

Explicitly initialises the GPU buffer. This method is **C++ only** and is normally
optional because the render system initialises points automatically.

---

### addPoint

Several overloads:

* void **addPoint**([PointData](pointdata.md) point)
* void **addPoint**(Vector3 position)
* void **addPoint**(Vector3 position, Vector4 color)
* void **addPoint**(Vector3 position, Vector4 color, float size)
* void **addPoint**(Vector3 position, Vector4 color, float size, float rotation)
* void **addPoint**(Vector3 position, Vector4 color, float size, float rotation, Rect textureRect)

Adds a new billboard point. The most complete overload specifies all visual attributes.

=== "C++"
    ```cpp
    Points stars(&scene);
    stars.setTexture("particles/star.png");
    stars.setMaxPoints(500);
    stars.load();

    for (int i = 0; i < 500; i++) {
        stars.addPoint(
            Vector3(rand() % 200 - 100, rand() % 200 - 100, 0),
            Vector4(1, 1, 1, 1), 2.0f
        );
    }
    stars.updatePoints();
    ```

=== "Lua"
    ```lua
    local stars = Points(scene)
    stars:setTexture("particles/star.png")
    stars.maxPoints = 500

    for i = 1, 500 do
        stars:addPoint(
            Vector3(math.random(-100, 100), math.random(-100, 100), 0),
            Vector4(1, 1, 1, 1), 2.0
        )
    end
    stars:updatePoints()
    ```

---

### getPoint

* [PointData](pointdata.md)& **getPoint**(size_t index)

Returns a reference to the `PointData` at `index`. Modify in-place then call `updatePoints()`.

---

### updatePoint

Overloads mirror `addPoint()`. Replaces data at `index`.

---

### removePoint

* void **removePoint**(size_t index)

Removes the point at `index`.

---

### isPointVisible / setPointVisible

* bool **isPointVisible**(size_t index)
* void **setPointVisible**(size_t index, bool visible) const

Show or hide individual points without removing them from the buffer.

---

### updatePoints

* void **updatePoints**()

Uploads changes to the GPU. Must be called after any modification.

---

### getNumPoints

* size_t **getNumPoints**()

Returns the current number of points.

---

### clearPoints

* void **clearPoints**()

Removes all points.

---

### addSpriteFrame

* void **addSpriteFrame**(int id, const std::string& name, Rect rect)
* void **addSpriteFrame**(const std::string& name, float x, float y, float width, float height)
* void **addSpriteFrame**(float x, float y, float width, float height)
* void **addSpriteFrame**(Rect rect)
* void **removeSpriteFrame**(int id)
* void **removeSpriteFrame**(const std::string& name)

Defines a named atlas frame for use with the `textureRect` field of [PointData](pointdata.md). This enables different points to show different sub-regions of the same texture atlas.

---

### setTexture

* void **setTexture**(const std::string& path)
* void **setTexture**(const std::string& id, TextureData data)
* void **setTexture**(Framebuffer* framebuffer)

Sets the texture used for all points. When using a texture atlas, call [addSpriteFrame](#addspriteframe) to define the atlas regions.
