---
description: Occluder2D API reference (C++ and Lua).
---

# Occluder2D

**Inherits:** [Object](object.md)  
**C++ type:** `Occluder2D`

## Description

A shadow caster for 2D lights. An `Occluder2D` defines an outline (a quad derived from the entity's mesh, or a custom polygon) that blocks light from every shadow-enabled [Light2D](light2d.md) in the scene.

The typical uses are:

- **Add the component to a sprite** with the default `AUTO_QUAD` shape — the sprite's bounds cast the shadow.
- **Create a standalone occluder entity** with a `POLYGON` shape — an invisible shadow wall you can shape freely. The editor's **2D → 2D Occluder** entry creates one with a starter square; polygon points can be dragged directly in the scene view or edited in Properties.

See [2D Graphics — 2D shadows](../../manual/2d-graphics.md#2d-shadows) for the usage guide.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [Occluder2DShape](#occluder2dshape) | [shape](#shape) | `AUTO_QUAD` | C++ \| Lua |
| bool | [closed](#closed) | `true` | C++ \| Lua |
| bool | [enabled](#enabled) | `true` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setShape](#shape) | C++ \| Lua |
| Occluder2DShape | [getShape](#shape) | C++ \| Lua |
| void | [addVertex](#addvertex) | C++ \| Lua |
| void | [clearVertices](#addvertex) | C++ \| Lua |
| unsigned int | [getVertexCount](#addvertex) | C++ \| Lua |
| void | [setClosed](#closed) | C++ \| Lua |
| bool | [isClosed](#closed) | C++ \| Lua |
| void | [setEnabled](#enabled) | C++ \| Lua |
| bool | [isEnabled](#enabled) | C++ \| Lua |

## Enumerations

### Occluder2DShape

* **AUTO_QUAD** - The outline is derived automatically from the bounds of the mesh on the same entity (for example, a sprite quad). Casts nothing when the entity has no mesh.
* **POLYGON** - The outline is the component's custom point list in local space.

---

## Property details

### shape

* *Setter*: void **setShape**([Occluder2DShape](#occluder2dshape) shape)
* *Getter*: [Occluder2DShape](#occluder2dshape) **getShape**() const

Selects how the occluder outline is defined. See [Occluder2DShape](#occluder2dshape). Calling [addVertex](#addvertex) switches the shape to `POLYGON` automatically.

---

### addVertex

* void **addVertex**(Vector2 vertex)
* void **addVertex**(float x, float y)
* void **clearVertices**()
* unsigned int **getVertexCount**() const

Build a custom polygon outline in local space. Points are connected in order; with [closed](#closed) enabled the last point connects back to the first.

=== "C++"
    ```cpp
    Occluder2D wall(&scene);
    wall.setPosition(Vector3(500, 200, 0));
    wall.addVertex(-60, -20);
    wall.addVertex(60, -20);
    wall.addVertex(60, 20);
    wall.addVertex(-60, 20);
    ```

=== "Lua"
    ```lua
    local wall = Occluder2D(scene)
    wall.position = Vector3(500, 200, 0)
    wall:addVertex(-60, -20)
    wall:addVertex(60, -20)
    wall:addVertex(60, 20)
    wall:addVertex(-60, 20)
    ```

---

### closed

* *Setter*: void **setClosed**(bool closed)
* *Getter*: bool **isClosed**() const

Whether the polygon outline is a closed loop (last point connects to the first) or an open chain. Only relevant for the `POLYGON` shape — `AUTO_QUAD` is always closed.

---

### enabled

* *Setter*: void **setEnabled**(bool enabled)
* *Getter*: bool **isEnabled**() const

Toggles the occluder without removing the component. Disabled occluders cast no shadows.
