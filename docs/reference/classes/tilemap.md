---
description: Tilemap API reference (C++ and Lua).
---

# Tilemap

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Tilemap`

## Description

Renders a 2D tile grid as batched geometry. `Tilemap` works with two concepts:

* **Rect** — a named sub-region of a texture atlas (the source rectangle of a tile graphic).
* **Tile** — an instance placed in the world, referencing a `Rect` and specifying its position and size.

This two-level design lets you define each atlas frame once and place it any number of times with no additional GPU cost. All tiles sharing the same texture atlas are batched together, and larger maps are additionally split into spatial chunks that are [frustum-culled](../../manual/rendering-pipeline.md#high-level-render-flow) individually, so tiles outside the camera view are never submitted.

A single tilemap can render at most **16 383** tiles — the index buffer is 16-bit and each tile is a four-vertex quad. Tiles beyond that limit are dropped with an error in the log; split larger worlds across several tilemaps or scenes.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [textureScaleFactor](#texturescalefactor) | `1.0` | C++ \| Lua |
| unsigned int | [reserveTiles](#reservetiles) | `10` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [createTilemap](#createtilemap) | C++ |
| int | [findRectByString](#findrectbystring-findtilebystring) | C++ \| Lua |
| int | [findTileByString](#findrectbystring-findtilebystring) | C++ \| Lua |
| void | [addRect](#addrect) | C++ \| Lua |
| void | [removeRect](#removerect) | C++ \| Lua |
| void | [clearRects](#clearrects) | C++ \| Lua |
| [TileRectData](tilerectdata.md) | [getRect](#getrect) | C++ \| Lua |
| void | [addTile](#addtile) | C++ \| Lua |
| void | [removeTile](#removetile) | C++ \| Lua |
| void | [clearTiles](#cleartiles) | C++ \| Lua |
| [TileData](tiledata.md) | [getTile](#gettile) | C++ \| Lua |
| unsigned int | [getWidth](#getwidth-getheight) | C++ \| Lua |
| unsigned int | [getHeight](#getwidth-getheight) | C++ \| Lua |
| void | [clearAll](#clearall) | C++ \| Lua |

## Property details

### textureScaleFactor

* *Setter*: void **setTextureScaleFactor**(float textureScaleFactor)
* *Getter*: float **getTextureScaleFactor**() const

A global scale applied to all UV coordinates. Increase this value to make the texture appear smaller (more repeating) across tiles, or decrease it to make it appear larger. Useful when using a high-resolution atlas intended for retina displays.

---

### reserveTiles

* *Setter*: void **setReserveTiles**(unsigned int reserveTiles)
* *Getter*: unsigned int **getReserveTiles**() const

Pre-allocates GPU buffer space for this many tiles. If you know the maximum tile count
in advance, set this before the tilemap is first built to avoid mid-game reallocations.

---

## Method details

### createTilemap

* bool **createTilemap**()

Explicitly builds or rebuilds the tilemap's geometry and GPU buffers. Configure the
texture, rects, and tiles first, then call this method if C++ code needs the geometry
immediately. It is **not bound to Lua**; the mesh system builds and rebuilds tilemaps
automatically during rendering.

=== "C++"
    ```cpp
    Tilemap map(&scene);
    map.setTexture("tiles.png");
    map.addRect("grass", 0, 0, 32, 32);
    map.addTile("grass", Vector2(64, 64), 32, 32);
    map.createTilemap();
    ```

=== "Lua"
    ```lua
    local map = Tilemap(scene)
    map:setTexture("tiles.png")
    map:addRect("grass", 0, 0, 32, 32)
    map:addTile("grass", Vector2(64, 64), 32, 32)
    ```

---

### findRectByString / findTileByString

* int **findRectByString**(const std::string& name)
* int **findTileByString**(const std::string& name)

Look up the integer ID of a rect or tile by name. Returns `-1` if not found.

---

### addRect

Several overloads are available:

* void **addRect**(int id, const std::string& name, const std::string& texture, [TextureFilter](texture.md#texturefilter) texFilter, [Rect](rect.md) rect)
* void **addRect**(int id, const std::string& name, const std::string& texture, [Rect](rect.md) rect)
* void **addRect**(int id, const std::string& name, [Rect](rect.md) rect)
* void **addRect**(const std::string& name, float x, float y, float width, float height)
* void **addRect**(float x, float y, float width, float height)
* void **addRect**([Rect](rect.md) rect)

Defines a named atlas frame. The `texture` path specifies which file to sample from; when omitted, the tilemap uses the default texture set on the mesh. `rect` is the pixel region (x, y, width, height) within the atlas.

The `id` parameter is an explicit integer key; use the simpler overloads when you don't need manual IDs.

=== "C++"
    ```cpp
    map.addRect(0, "water",  "tiles.png", Rect(0,  0,  32, 32));
    map.addRect(1, "ground", "tiles.png", Rect(32, 0,  32, 32));
    map.addRect(2, "wall",   "tiles.png", Rect(64, 0,  32, 32));
    ```

=== "Lua"
    ```lua
    map:addRect(0, "water",  "tiles.png", Rect(0,  0,  32, 32))
    map:addRect(1, "ground", "tiles.png", Rect(32, 0,  32, 32))
    map:addRect(2, "wall",   "tiles.png", Rect(64, 0,  32, 32))
    ```

---

### removeRect

* void **removeRect**(int id)
* void **removeRect**(const std::string& name)

Removes an atlas-frame definition. Any tiles that reference the removed rect will no longer render correctly until they are updated.

---

### clearRects

* void **clearRects**()

Removes all rect definitions. Equivalent to calling `removeRect()` for every registered rect.

---

### getRect

* [TileRectData](tilerectdata.md)& **getRect**(int id)
* [TileRectData](tilerectdata.md)& **getRect**(const std::string& name)

Returns a reference to the [TileRectData](tilerectdata.md) struct for the given rect. You can modify the struct fields in place to update the atlas frame at runtime.

---

### addTile

Several overloads are available:

* void **addTile**(int id, const std::string& name, int rectId, Vector2 position, float width, float height)
* void **addTile**(const std::string& name, int rectId, Vector2 position, float width, float height)
* void **addTile**(int rectId, Vector2 position, float width, float height)
* void **addTile**(const std::string& name, const std::string& rectString, Vector2 position, float width, float height)
* void **addTile**(const std::string& rectString, Vector2 position, float width, float height)

Places a tile instance in world space. `rectId` (or `rectString`) identifies which atlas frame to use; `position` is the 2D world-space centre; `width` and `height` are the tile's display dimensions.

=== "C++"
    ```cpp
    // Build a simple 3x3 ground patch
    for (int x = 0; x < 3; x++) {
        for (int y = 0; y < 3; y++) {
            map.addTile("ground", Vector2(x * 32.0f, y * 32.0f), 32.0f, 32.0f);
        }
    }
    ```

=== "Lua"
    ```lua
    for x = 0, 2 do
        for y = 0, 2 do
            map:addTile("ground", Vector2(x * 32, y * 32), 32, 32)
        end
    end
    ```

---

### removeTile

* void **removeTile**(int id)
* void **removeTile**(const std::string& name)

Removes a specific tile instance.

---

### clearTiles

* void **clearTiles**()

Removes all tile instances. The rect definitions are preserved.

---

### getTile

* [TileData](tiledata.md)& **getTile**(int id)
* [TileData](tiledata.md)& **getTile**(const std::string& name)

Returns a reference to the [TileData](tiledata.md) struct for the given tile. Modify the struct fields in place to move, resize, or remap tiles at runtime.

---

### getWidth / getHeight

* unsigned int **getWidth**()
* unsigned int **getHeight**()

Returns the overall pixel dimensions of the tilemap bounding box (the extent covered by all placed tiles).

---

### clearAll

* void **clearAll**()

Removes all tiles and all rect definitions in one call.
