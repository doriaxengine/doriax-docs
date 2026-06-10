---
description: Heightmap terrain in Doriax — LOD clipmap rendering, sculpting and painting in the editor, and the runtime Terrain API.
---

# Terrain

Doriax renders large outdoor landscapes with a heightmap-based `Terrain` object. The
terrain uses a clipmap-style LOD grid, so the polygon count on screen stays roughly
constant regardless of terrain size, with detail concentrated near the camera.

## Terrain anatomy

| Input | Purpose |
| --- | --- |
| **Heightmap** | Grayscale image that displaces the grid vertically (white = `maxHeight`) |
| **Base texture** | The ground texture tiled across the whole terrain |
| **Blend map** | RGB mask that mixes up to three detail textures over the base |
| **Detail textures** | Red/green/blue channel textures (e.g. grass, rock, path) |

## Editing terrain in the editor

Select an entity with a Terrain component and click **Open Terrain Editor** in the
Properties window. The Terrain Editor provides brush-based authoring:

| Tool | Effect |
| --- | --- |
| **Raise / Lower** | Sculpt the heightmap up or down |
| **Smooth** | Soften height transitions |
| **Flatten** | Level an area to a uniform height |
| **Paint Red / Green / Blue** | Paint detail textures into the blend map channels |

Brushes have configurable size, strength, shape (circle/square), and falloff.

## Creating terrain in code

=== "Lua"

    ```lua
    terrain = Terrain(scene)
    terrain:setHeightMap("terrain/heightmap.png")
    terrain:setTexture("terrain/grass_base.png")

    terrain:setBlendMap("terrain/blendmap.png")
    terrain:setTextureDetailRed("terrain/rock.png")
    terrain:setTextureDetailGreen("terrain/grass_detail.png")
    terrain:setTextureDetailBlue("terrain/path.png")

    -- Dimensions and LOD are properties in Lua
    terrain.size = 2000          -- world units per side
    terrain.maxHeight = 80       -- world height of a white heightmap pixel
    terrain.resolution = 256     -- heightmap sampling resolution
    ```

=== "C++"

    ```cpp
    Terrain terrain(&scene);
    terrain.setHeightMap("terrain/heightmap.png");
    terrain.setTexture("terrain/grass_base.png");

    terrain.setBlendMap("terrain/blendmap.png");
    terrain.setTextureDetailRed("terrain/rock.png");
    terrain.setTextureDetailGreen("terrain/grass_detail.png");
    terrain.setTextureDetailBlue("terrain/path.png");

    terrain.setSize(2000.0f);
    terrain.setMaxHeight(80.0f);
    terrain.setResolution(256);
    ```

`Terrain` derives from `Mesh`, so material, shadow, and texture APIs from
[`Mesh`](../reference/classes/mesh.md) apply as well.

## LOD tuning

| Property | Controls |
| --- | --- |
| `rootGridSize` | Quads per side of each patch — higher = denser geometry |
| `levels` | Number of LOD rings around the camera — higher = larger view range |
| `textureBaseTiles` | How many times the base texture repeats across the terrain |
| `textureDetailTiles` | Repeat count for the detail textures |

Start with the defaults; raise `levels` for very large terrains and `rootGridSize` when
close-up silhouettes look too coarse.

## Terrain collision

For physics, add a `Body3D` with a **height field shape** to the terrain entity — see
[Physics](physics.md). Keep the visual resolution and collision resolution consistent so
objects rest on the visible surface.

## See also

- [Terrain](../reference/classes/terrain.md) — full API reference
- [3D Graphics](3d-graphics.md) — lighting, materials, sky, and fog
- [Physics](physics.md) — height field collision
