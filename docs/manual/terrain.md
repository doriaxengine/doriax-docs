---
description: Heightmap terrain in Doriax — LOD clipmap rendering, detail layers, foliage scattering, sculpting and painting in the editor, and the runtime Terrain API.
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
| **Blend maps** | Up to three RGB masks; each channel weights one detail layer |
| **Detail layers** | Up to nine textures (grass, rock, path, …) mixed over the base |
| **Foliage layers** | Meshes scattered over the surface from painted density maps |

The heightmap and the blend maps are stretched once over the whole terrain, so they are
sampled with clamp-to-edge wrapping: the outer row and column of texels define the border
of the terrain instead of blending with the opposite edge. Only the base and detail
textures tile.

## Detail layers

Detail layers are numbered from 1 and grouped in threes: layers 1–3 are weighted by the
RGB channels of the first blend map, 4–6 by the second, 7–9 by the third. Whatever weight
the layers leave unclaimed goes to the base texture, so an unpainted terrain shows the
base alone.

All layers are uploaded as a single texture array, which keeps the sampler count flat as
layers are added. Slices smaller than the largest layer are resized and grayscale layers
are widened to RGBA; a layer whose format cannot be reconciled with the others is refused
with an error and the terrain falls back to the base texture.

Three things shape how the layers meet on screen:

- **Height blending.** A detail texture's alpha is read as *layer height*, not opacity.
  Where two layers overlap, the taller one takes the contact zone — gravel settles between
  cobbles instead of cross-fading into them. Fully opaque textures have no height and blend
  on their blend-map weight alone.
- **Triplanar projection on slopes.** A flat top-down projection stretches over a cliff, so
  as the surface turns vertical the layers fade into side projections taken along X and Z.
- **Distance tile break.** Past a few tiles of distance a second, coarser tiling rate fades
  in and mixes with the first, breaking up the repeating pattern of tiled ground.

## Foliage

A terrain can carry foliage layers: a mesh, a painted density map, and the rules for
scattering it. Instances are not stored in the scene — they are resolved from the density
map at runtime, in fixed cells batched into per-chunk instanced entities around the
camera, and re-resolved when the camera moves. Each layer filters by ground slope and
height, jitters scale and yaw, can lean instances along the surface normal, and has its
own draw distance, with instances scaling in over the last quarter of it instead of
popping.

Foliage entities belong to the engine, not to the authored scene: they are not listed in
the editor's Structure panel and clicking one selects its terrain.

For props that need to be real entities — collision, scripts, animation, or just a
hand-placed look — use the Terrain Editor's object placement brush instead, which
parents ordinary models or bundles to the terrain.

## Editing terrain in the editor

Select an entity with a Terrain component and click **Open Terrain Editor** in the
Properties window. The window paints every map the terrain uses:

| Section | Tools |
| --- | --- |
| **Sculpt** | Raise, Lower, Smooth, Flatten, Sharpen, Noise, Terrace, Stamp, Erode, Ramp |
| **Texture Paint** | Paint the base or any detail layer into the blend maps, optionally masked by slope and height |
| **Foliage** | Add layers and paint their density maps |
| **Objects** | Scatter models or bundles as children of the terrain, instanced or as individual entities |

Brushes have configurable size, strength, shape (circle/square), falloff, and an optional
grayscale mask. See [Terrain Editor](../editor/terrain-editor.md) for the full window
reference.

## Creating terrain in code

=== "Lua"

    ```lua
    terrain = Terrain(scene)
    terrain:setHeightMap("terrain/heightmap.png")
    terrain:setTexture("terrain/grass_base.png")

    -- Layers 0-2 are weighted by the RGB channels of blend map 0
    terrain:setBlendMap("terrain/blendmap.png")
    terrain:setTextureLayer(0, "terrain/rock.png")
    terrain:setTextureLayer(1, "terrain/grass_detail.png")
    terrain:setTextureLayer(2, "terrain/path.png")

    -- Layers 3-5 need a second blend map
    terrain:setBlendMapIndex(1, "terrain/blendmap1.png")
    terrain:setTextureLayer(3, "terrain/snow.png")

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

    // Layers 0-2 are weighted by the RGB channels of blend map 0
    terrain.setBlendMap("terrain/blendmap.png");
    terrain.setTextureLayer(0, "terrain/rock.png");
    terrain.setTextureLayer(1, "terrain/grass_detail.png");
    terrain.setTextureLayer(2, "terrain/path.png");

    // Layers 3-5 need a second blend map
    terrain.setBlendMap(1, "terrain/blendmap1.png");
    terrain.setTextureLayer(3, "terrain/snow.png");

    terrain.setSize(2000.0f);
    terrain.setMaxHeight(80.0f);
    terrain.setResolution(32);
    ```

`Terrain` derives from `Mesh`, so material, shadow, and texture APIs from
[`Mesh`](../reference/classes/mesh.md) apply as well — `setTexture` sets the base ground
texture through the material.

`setTextureDetailRed` / `Green` / `Blue` still work: they are layers 0, 1 and 2 under the
names they had when a terrain had a single blend map. Foliage layers have no runtime
setters — they are authored in the editor and read back from the component.

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

- [Terrain Editor](../editor/terrain-editor.md) — sculpting, painting, foliage and object placement
- [Terrain](../reference/classes/terrain.md) — full API reference
- [3D Graphics](3d-graphics.md) — lighting, materials, sky, and fog
- [Physics](physics.md) — height field collision
