---
description: Terrain API reference (C++ and Lua).
---

# Terrain

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Terrain`

## Description

Generates and renders a heightmap-based terrain mesh using a chunked LOD (Level of Detail) approach. The terrain is built from a greyscale heightmap texture where brighter pixels correspond to higher elevation. Up to three blend maps control how up to nine detail texture layers are mixed over the base texture, three layers per blend map.

The terrain geometry is a CDLOD quadtree: `rootGridSize` × `rootGridSize` root nodes cover the terrain and each node subdivides into four until `levels` is reached. Every node is drawn with the same `resolution` × `resolution` grid and morphs into its coarser neighbour, which keeps the polycount roughly constant regardless of terrain size.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [size](#size) | `200.0` | C++ \| Lua |
| float | [maxHeight](#maxheight) | `5.0` | C++ \| Lua |
| int | [resolution](#resolution) | `32` | C++ \| Lua |
| int | [textureBaseTiles](#texturebasetiles-texturedetailtiles) | `1` | C++ \| Lua |
| int | [textureDetailTiles](#texturebasetiles-texturedetailtiles) | `20` | C++ \| Lua |
| int | [rootGridSize](#rootgridsize) | `2` | C++ \| Lua |
| int | [levels](#levels) | `6` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [createTerrain](#createterrain) | C++ |
| void | [setHeightMap](#setheightmap) | C++ \| Lua |
| void | [setBlendMap](#setblendmap) | C++ \| Lua |
| void | [setTextureLayer](#settexturelayer) | C++ \| Lua |
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

Number of grid segments per side of a single LOD node (not the heightmap size). Every node in the quadtree is drawn with this grid, so raising it densifies the geometry everywhere.

Rounded to the nearest multiple of 4 (minimum 4): nodes stitch to coarser neighbours by morphing only their odd vertices, and the internal half-resolution grid (`resolution / 2`) must keep the same parity. A value that is not a multiple of 4 is rewritten on the component and logs a warning, so read the property back if the exact value matters.

---

### textureBaseTiles / textureDetailTiles

* *Setter/Getter*: **setTextureBaseTiles** / **getTextureBaseTiles**, **setTextureDetailTiles** / **getTextureDetailTiles**

How many times the base and detail textures tile across the full terrain. Higher values produce smaller, more repetitive texture patterns; lower values stretch the texture.

---

### rootGridSize

* *Setter*: void **setRootGridSize**(int rootGridSize)
* *Getter*: int **getRootGridSize**() const

The number of root quadtree nodes per side of the terrain. The coarsest node covers `size / rootGridSize` world units, so larger values start the quadtree with smaller nodes. Capped by the terrain node budget together with `levels`.

---

### levels

* *Setter*: void **setLevels**(int levels)
* *Getter*: int **getLevels**() const

Depth of the LOD quadtree. Each level halves the node size, so the leaf node covers `size / (rootGridSize * 2^(levels-1))` world units — more levels means finer geometry near the camera, not a longer view distance.

The quadtree materializes `rootGridSize^2 * (4^levels - 1) / 3` nodes, so the node count grows exponentially with `levels`; past the engine's node budget the terrain refuses to build and logs an error.

With automatic ranges the LOD distances follow from these node sizes: the first range is twice the leaf node size and each level doubles it, with only the last range stretched to the camera's far clip.

---

## Method details

### createTerrain

* bool **createTerrain**()

Explicitly builds the terrain geometry and GPU buffers after its source properties have
been configured. This method is **C++ only** and is normally optional because the mesh
system builds and rebuilds terrain automatically.

=== "C++"
    ```cpp
    Terrain ground(&scene);
    ground.setHeightMap("terrain/heightmap.png");
    ground.setBlendMap("terrain/blendmap.png");
    ground.setTexture("terrain/grass.png");
    ground.setTextureLayer(0, "terrain/rock.png");
    ground.setTextureLayer(1, "terrain/sand.png");
    ground.setTextureLayer(2, "terrain/snow.png");
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
    ground:setTextureLayer(0, "terrain/rock.png")
    ground:setTextureLayer(1, "terrain/sand.png")
    ground:setTextureLayer(2, "terrain/snow.png")
    ground.size = 1000
    ground.maxHeight = 80
    ```

---

### setHeightMap

* void **setHeightMap**(const std::string& path)
* void **setHeightMap**(Framebuffer* framebuffer)

Sets the greyscale heightmap image. Each pixel's brightness maps linearly to height: black = 0, white = `maxHeight`. 8-bit and 16-bit images are both read (the editor's sculpting tools write 16-bit to avoid terracing). The image is stretched once over the terrain and sampled clamp-to-edge, so its outer texels define the terrain border.

Each quadtree node keeps the min/max height of the heightmap texels under its footprint, and that range is the node's bounding box for frustum culling. A framebuffer heightmap has no CPU-side pixels, so its nodes get a flat (zero-height) box and CPU-side height queries such as terrain picking read as flat — the displacement still renders, but do not rely on culling or picking accuracy for procedurally generated heightmaps.

---

### setBlendMap

* void **setBlendMap**(const std::string& path)
* void **setBlendMap**(Framebuffer* framebuffer)
* void **setBlendMap**(unsigned int index, const std::string& path) — Lua: **setBlendMapIndex**

Sets a blend map. Each blend map weights three detail layers through its RGB channels: blend map 0 weights layers 0–2, blend map 1 layers 3–5, and blend map 2 layers 6–8. The one-argument form is blend map 0. Whatever weight the layers leave unclaimed goes to the base texture, so areas with no blend-map colour show the base alone.

Alpha is not a fourth weight — saved maps are opaque, which would read as full strength. Indexes at or above three are rejected with an error.

---

### setTextureLayer

* void **setTextureLayer**(unsigned int index, const std::string& path)

Sets the texture of one detail layer, 0 to 8. The vector of layers grows as needed, so assigning layer 4 also creates the empty layers below it; an unassigned layer renders as white.

Every layer is uploaded as one slice of a texture array, so the slices share a size and a format: smaller layers are resized to the largest one and grayscale layers are widened to RGBA. A layer whose format cannot be reconciled with the others is refused with an error, and the terrain falls back to the base texture. The sampler filters and wrap modes come from the first assigned layer.

The layer texture's **alpha is read as layer height**, not opacity: where two layers overlap, the taller one takes the contact zone. Opaque textures have no height and blend on their blend-map weight alone. Layers are also projected triplanarly as the surface turns vertical, and mixed with a coarser tiling rate at a distance to break up repetition.

=== "C++"
    ```cpp
    ground.setBlendMap("terrain/blendmap.png");
    ground.setTextureLayer(0, "terrain/rock.png");
    ground.setTextureLayer(1, "terrain/sand.png");
    ground.setTextureLayer(2, "terrain/snow.png");
    ```

=== "Lua"
    ```lua
    ground:setBlendMap("terrain/blendmap.png")
    ground:setTextureLayer(0, "terrain/rock.png")
    ground:setTextureLayer(1, "terrain/sand.png")
    ground:setTextureLayer(2, "terrain/snow.png")
    ```

---

### setTextureDetailRed / setTextureDetailGreen / setTextureDetailBlue

* void **setTextureDetailRed**(const std::string& path)
* void **setTextureDetailGreen**(const std::string& path)
* void **setTextureDetailBlue**(const std::string& path)

Layers 0, 1 and 2 under the names they had when a terrain had a single blend map. Equivalent to `setTextureLayer(0/1/2, path)`.
