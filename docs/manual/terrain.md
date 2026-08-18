---
description: Heightmap terrain in Doriax — LOD clipmap rendering, sculpting and painting in the editor, and the runtime Terrain API.
---

# Terrain

Doriax renders large outdoor landscapes with a heightmap-based `Terrain` object. The
terrain is a continuous-LOD quadtree, so the polygon count on screen stays roughly
constant regardless of terrain size, with detail concentrated near the camera.

## Terrain anatomy

| Input | Purpose |
| --- | --- |
| **Heightmap** | Grayscale image that displaces the grid vertically (white = `maxHeight`) |
| **Base texture** | The ground texture tiled across the whole terrain |
| **Blend map** | RGB mask that mixes up to three detail textures over the base |
| **Detail textures** | Red/green/blue channel textures (e.g. grass, rock, path) |

The heightmap and the blend map are stretched once over the whole terrain, so they are
sampled with clamp-to-edge wrapping: the outer row and column of texels define the border
of the terrain instead of blending with the opposite edge. Only the base and detail
textures tile.

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
    terrain.resolution = 32      -- grid segments per LOD node (multiple of 4)
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
    terrain.setResolution(32);
    ```

`Terrain` derives from `Mesh`, so material, shadow, and texture APIs from
[`Mesh`](../reference/classes/mesh.md) apply as well.

## LOD tuning

The terrain is a quadtree: `rootGridSize` × `rootGridSize` root nodes cover the whole
terrain, and each node subdivides into four until `levels` is reached. Every node is
drawn with the same grid of `resolution` × `resolution` segments, so a deeper node covers
less ground with the same number of triangles — that is where the added detail comes
from.

| Property | Controls |
| --- | --- |
| `resolution` | Grid segments per side of every node — higher = denser geometry everywhere |
| `rootGridSize` | Root nodes per side of the terrain — the coarsest node is `size / rootGridSize` |
| `levels` | Quadtree depth — each level halves the node size, so the leaf node is `size / (rootGridSize × 2^(levels-1))` |
| `textureBaseTiles` | How many times the base texture repeats across the terrain |
| `textureDetailTiles` | Repeat count for the detail textures |

Start with the defaults; raise `levels` when the ground near the camera looks too coarse,
and `resolution` when it still does at the highest level. Both are paid for in nodes and
triangles: the quadtree materializes `rootGridSize² × (4^levels - 1) / 3` nodes, so
`levels` grows the node count exponentially and the engine refuses to build a terrain
past its node budget (it logs an error asking for a lower **Levels** or **Root Grid
Size**).

!!! note "Resolution is rounded to a multiple of 4"
    Nodes stitch to their coarser neighbours by morphing only their odd vertices, and the
    internal half-resolution grid (`resolution / 2`) has to keep the same parity. The
    engine rounds `resolution` to the nearest multiple of 4 (minimum 4), writes the
    rounded value back to the component, and logs a warning. Set it in steps of 4 — the
    editor's **Resolution** field already drags that way — or the value you typed will
    not be the value you get.

### LOD ranges

By default (`autoSetRanges`) the engine derives the distance ranges from the node sizes
themselves: the first range is twice the leaf node size and each following level doubles
it, so every level shows roughly the same amount of detail on screen no matter how large
the terrain is. Only the coarsest range is stretched to the camera's far clip, so a
terrain farther away than its own size still renders.

## Terrain collision

For physics, add a `Body3D` with a **height field shape** to the terrain entity — see
[Physics](physics.md). Keep the visual resolution and collision resolution consistent so
objects rest on the visible surface.

## See also

- [Terrain](../reference/classes/terrain.md) — full API reference
- [3D Graphics](3d-graphics.md) — lighting, materials, sky, and fog
- [Physics](physics.md) — height field collision
