---
description: Terrain API reference (C++ and Lua).
---

# Terrain

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Terrain`

## Description

Generates and renders a heightmap-based terrain mesh using a chunked LOD (Level of Detail) approach. The terrain is built from a greyscale heightmap texture where brighter pixels correspond to higher elevation. An optional blend map controls how up to four detail textures (base + red, green, blue channels) are layered across the surface.

The terrain geometry uses a *clipmap* style grid hierarchy (`rootGridSize` × `rootGridSize` quads per patch, `levels` LOD rings), which keeps the polycount constant regardless of terrain size.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [size](#size) | `100.0` | C++ \| Lua |
| float | [maxHeight](#maxheight) | `10.0` | C++ \| Lua |
| int | [resolution](#resolution) | `64` | C++ \| Lua |
| int | [textureBaseTiles](#texturebasetiles-texturedetailtiles) | `4` | C++ \| Lua |
| int | [textureDetailTiles](#texturebasetiles-texturedetailtiles) | `32` | C++ \| Lua |
| int | [rootGridSize](#rootgridsize) | `8` | C++ \| Lua |
| int | [levels](#levels) | `4` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [createTerrain](#createterrain) | C++ \| Lua |
| void | [setHeightMap](#setheightmap) | C++ \| Lua |
| void | [setBlendMap](#setblendmap) | C++ \| Lua |
| void | [setTextureDetailRed](#settexturedetailred-settexturedetailgreen-settexturedetailblue) | C++ \| Lua |
| void | [setTextureDetailGreen](#settexturedetailred-settexturedetailgreen-settexturedetailblue) | C++ \| Lua |
| void | [setTextureDetailBlue](#settexturedetailred-settexturedetailgreen-settexturedetailblue) | C++ \| Lua |

## Property details

### size

* *Setter*: void **setSize**(float size)
* *Getter*: float **getSize**() const

World-space width and depth of the terrain in units. The terrain is always square.

---

### maxHeight

* *Setter*: void **setMaxHeight**(float maxHeight)
* *Getter*: float **getMaxHeight**() const

The maximum elevation in world units corresponding to a fully white (255) heightmap pixel.

---

### resolution

* *Setter*: void **setResolution**(int resolution)
* *Getter*: int **getResolution**() const

Number of heightmap samples read per axis. Higher values produce more detailed terrain but use more memory.

---

### textureBaseTiles / textureDetailTiles

* *Setter/Getter*: **setTextureBaseTiles** / **getTextureBaseTiles**, **setTextureDetailTiles** / **getTextureDetailTiles**

How many times the base and detail textures tile across the full terrain. Higher values produce smaller, more repetitive texture patterns; lower values stretch the texture.

---

### rootGridSize

* *Setter*: void **setRootGridSize**(int rootGridSize)
* *Getter*: int **getRootGridSize**() const

The number of quads per side of each LOD patch. Larger values produce coarser transitions between LOD levels.

---

### levels

* *Setter*: void **setLevels**(int levels)
* *Getter*: int **getLevels**() const

Number of LOD rings around the viewer. More levels cover a larger distance with the same polycount.

---

## Method details

### createTerrain

* bool **createTerrain**()

Initialises the terrain geometry and GPU buffers. Must be called after setting the height map and before the terrain is rendered.

=== "C++"
    ```cpp
    Terrain ground(&scene);
    ground.setHeightMap("terrain/heightmap.png");
    ground.setBlendMap("terrain/blendmap.png");
    ground.setTexture("terrain/grass.png");
    ground.setTextureDetailRed("terrain/rock.png");
    ground.setTextureDetailGreen("terrain/sand.png");
    ground.setTextureDetailBlue("terrain/snow.png");
    ground.setSize(1000.0f);
    ground.setMaxHeight(80.0f);
    ground.createTerrain();
    ```

=== "Lua"
    ```lua
    local ground = Terrain(scene)
    ground:setHeightMap("terrain/heightmap.png")
    ground:setBlendMap("terrain/blendmap.png")
    ground:setTexture("terrain/grass.png")
    ground:setTextureDetailRed("terrain/rock.png")
    ground:setTextureDetailGreen("terrain/sand.png")
    ground:setTextureDetailBlue("terrain/snow.png")
    ground:setSize(1000)
    ground:setMaxHeight(80)
    ground:createTerrain()
    ```

---

### setHeightMap

* void **setHeightMap**(const std::string& path)
* void **setHeightMap**(Framebuffer* framebuffer)

Sets the greyscale heightmap image. Each pixel's brightness maps linearly to height: black = 0, white = `maxHeight`. A framebuffer can be used for procedurally generated heightmaps.

---

### setBlendMap

* void **setBlendMap**(const std::string& path)
* void **setBlendMap**(Framebuffer* framebuffer)

Sets the blend map that controls where detail textures appear. The RGB channels select `textureDetailRed`, `textureDetailGreen`, and `textureDetailBlue` respectively. Areas with no blend-map colour show the base texture.

---

### setTextureDetailRed / setTextureDetailGreen / setTextureDetailBlue

* void **setTextureDetailRed**(const std::string& path)
* void **setTextureDetailGreen**(const std::string& path)
* void **setTextureDetailBlue**(const std::string& path)

Set the three detail layer textures. Each texture is used where the corresponding RGB channel of the blend map has a non-zero value.
