---
description: Terrain API reference (C++ and Lua).
---

# Terrain

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Terrain`

## Description

Generates and renders a heightmap-based terrain mesh using a chunked LOD (Level of Detail) approach. The terrain is built from a greyscale heightmap texture where brighter pixels correspond to higher elevation. Up to three blend maps control how up to nine detail layers are mixed over the base texture, three layers per blend map. A layer blends its colour alone, or carries its own PBR surface — see [TerrainSurfaceLayer](#terrainsurfacelayer).

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
| void | [setSurfaceLayer](#setsurfacelayer-getsurfacelayer) | C++ \| Lua |
| TerrainSurfaceLayer | [getSurfaceLayer](#setsurfacelayer-getsurfacelayer) | C++ \| Lua |
| void | [setLayerFromMaterial](#setlayerfrommaterial) | C++ \| Lua |
| void | [removeSurfaceLayer](#removesurfacelayer) | C++ \| Lua |
| unsigned int | [getNumLayers](#getnumlayers) | C++ \| Lua |
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

Sets the **colour** of one detail layer, 0 to 8, and nothing else — a layer that carries a PBR surface keeps its other maps and factors. The vector of layers grows as needed, so assigning layer 4 also creates the empty layers below it; an unassigned layer renders as white.

Every map of every layer is uploaded as one slice of a single texture array, so the whole terrain costs one sampler. Sources are converted to RGBA and resized to a common size, capped at 2048 px. The sampler filters and wrap modes come from the first assigned layer colour; a terrain with any PBR layer or custom tiling also gets mipmaps, which tiled surface maps need to stop aliasing at distance.

On a plain colour layer the texture's **alpha is read as layer height**, not opacity: where two layers overlap, the taller one takes the contact zone. Opaque textures have no height and blend on their blend-map weight alone. A PBR layer takes its height from its height map instead, leaving its colour alpha unused. Layers are also projected triplanarly as the surface turns vertical, and mixed with a coarser tiling rate at a distance to break up repetition.

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

### setSurfaceLayer / getSurfaceLayer

* void **setSurfaceLayer**(unsigned int index, const TerrainSurfaceLayer& layer)
* TerrainSurfaceLayer **getSurfaceLayer**(unsigned int index) const

Replaces or reads one whole layer, maps and factors together. `getSurfaceLayer` returns a **copy**, so editing it changes nothing until it is passed back to `setSurfaceLayer` — read, change, write.

=== "C++"
    ```cpp
    TerrainSurfaceLayer rock;
    rock.pbr = true;
    rock.colorTexture = Texture("terrain/rock_color.png");
    rock.normalTexture = Texture("terrain/rock_normal.png");
    rock.roughnessTexture = Texture("terrain/rock_orm.png");
    rock.metallicTexture = Texture("terrain/rock_orm.png");
    rock.roughnessFactor = 0.9f;
    ground.setSurfaceLayer(0, rock);
    ```

=== "Lua"
    ```lua
    local rock = TerrainSurfaceLayer()
    rock.pbr = true
    rock.colorTexture = Texture("terrain/rock_color.png")
    rock.normalTexture = Texture("terrain/rock_normal.png")
    rock.roughnessFactor = 0.9
    ground:setSurfaceLayer(0, rock)

    -- Read, change, write back
    local layer = ground:getSurfaceLayer(0)
    layer.uvScale = Vector2(2, 2)
    ground:setSurfaceLayer(0, layer)
    ```

---

### setLayerFromMaterial

* void **setLayerFromMaterial**(unsigned int index, const Material& material)

Fills a layer from a [Material](material.md) and turns on its PBR surface: base colour and factor, normal, metallic/roughness (assigned to both the roughness and metallic slots), occlusion, and the roughness and metallic factors.

Emission, alpha mode and secondary UV sets have no meaning on a terrain layer and are dropped. The layer keeps the UV scale and offset it already had, since a material carries no tiling of its own.

---

### removeSurfaceLayer

* void **removeSurfaceLayer**(unsigned int index)

Removes a layer. Blend map channels are positional, so every later layer moves down one channel — onto the paint the removed layer left behind. Only removing the last layer is lossless, which is all the Terrain Editor offers.

---

### getNumLayers

* unsigned int **getNumLayers**() const

How many layers the terrain currently holds, painted or empty.

---

## TerrainSurfaceLayer

One painted surface. The maps are separate inputs so an existing material can fill them without repacking images; the renderer packs them into slices of the terrain's texture array.

| Type | Name | Default | Meaning |
| --- | --- | --- | --- |
| bool | pbr | `false` | Off blends only the colour and leaves the rest to the terrain material |
| [Texture](texture.md) | colorTexture | empty | Surface colour. sRGB-decoded and tinted on a PBR layer; used raw on a colour layer |
| [Texture](texture.md) | normalTexture | empty | Tangent-space normal map, projected with the layer |
| [Texture](texture.md) | roughnessTexture | empty | Read from green, or the only channel of a grayscale map |
| [Texture](texture.md) | metallicTexture | empty | Read from blue, same fallback |
| [Texture](texture.md) | occlusionTexture | empty | Read from red; white is unoccluded |
| [Texture](texture.md) | heightTexture | empty | Biases blending toward this layer where it is taller; never moves geometry |
| Vector4 | colorFactor | `(1,1,1,1)` | Linear tint multiplied with `colorTexture`. PBR layers only |
| float | normalStrength | `1.0` | How far the normal map tilts the surface |
| float | roughnessFactor | `1.0` | Multiplies `roughnessTexture` |
| float | metallicFactor | `0.0` | Multiplies `metallicTexture` |
| float | occlusionStrength | `1.0` | How far `occlusionTexture` darkens ambient light |
| Vector2 | uvScale | `(1,1)` | Multiplies the shared detail tiling, for this layer alone |
| Vector2 | uvOffset | `(0,0)` | Shifts this layer inside its tile |

All fields are readable and writable from both C++ and Lua, and Lua can construct one with `TerrainSurfaceLayer()`.

`uvScale` and `uvOffset` apply whether or not `pbr` is on. Every other field beyond `colorTexture` needs `pbr`.

---

### setTextureDetailRed / setTextureDetailGreen / setTextureDetailBlue

* void **setTextureDetailRed**(const std::string& path)
* void **setTextureDetailGreen**(const std::string& path)
* void **setTextureDetailBlue**(const std::string& path)

Layers 0, 1 and 2 under the names they had when a terrain had a single blend map. Equivalent to `setTextureLayer(0/1/2, path)`, so they set only the layer colour.
