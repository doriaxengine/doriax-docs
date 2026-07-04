---
description: Working with 2D graphics in Doriax — sprites, tilemaps, polygons, 2D lighting and shadows.
---

# 2D Graphics

Doriax has full support for 2D game development with sprites, tilemaps, primitive
shapes, and dedicated 2D lighting with shadows, backed by the same ECS used for 3D.

![2D tilemap editor](../assets/screenshots/editor-2d-tilemap.png)

## Polygons

The `Polygon` object lets you build arbitrary 2D shapes from vertices. This is the
simplest way to draw something on screen.

=== "Lua"

    ```lua
    scene = Scene()
    triangle = Polygon(scene)

    triangle:addVertex(0, -100)
    triangle:addVertex(-50, 50)
    triangle:addVertex(50, 50)

    triangle.position = Vector3(300, 300, 0)
    triangle:setColor(0.6, 0.2, 0.6, 1)

    Engine.setCanvasSize(1000, 480)
    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;
    #include "Polygon.h"

    Scene scene;
    Polygon triangle(&scene);

    DORIAX_INIT void init() {
        triangle.addVertex(0, -100);
        triangle.addVertex(-50, 50);
        triangle.addVertex(50, 50);

        triangle.setPosition(Vector3(300, 300, 0));
        triangle.setColor(0.6, 0.2, 0.6, 1);

        Engine::setCanvasSize(1000, 480);
        Engine::setScene(&scene);
    }
    ```

## Sprites

Sprites display images on screen and are the building blocks of most 2D games. In the
editor, the **sprite slicer** tool cuts a sprite sheet into individual frames you can
use for animation.

Common sprite operations include:

| Operation | C++ method |
| --- | --- |
| Set size | `setSize(width, height)` |
| Set texture region | `setTextureRect(rect)` |
| Choose pivot | `setPivotPreset(preset)` |
| Register animation frame | `addFrame(name, x, y, width, height)` |
| Play frame range | `startAnimation(startFrame, endFrame, interval, loop)` |

## Tilemaps

Tilemaps let you compose large 2D worlds from reusable tiles. Use the **tileset
slicer** in the editor to cut a tileset image into tiles, then paint them into a
tilemap in the scene view.

Tilemaps are designed for large grids of repeated texture regions. Keep individual
tiles consistent in size, place collision on separate bodies when possible, and split
very large worlds into scenes or chunks so editing and export remain fast.

## 2D lighting

2D scenes have their own lighting model, separate from the 3D PBR path: a **Light2D**
is a point light living in the scene's XY plane with a radius falloff, designed for the
classic 2D look — torches, lamps, day/night moods.

Light from every 2D light **adds** on top of the scene's **2D ambient light**. Ambient
defaults to full white, so a scene looks unchanged until you dim it — that darkness is
what makes lights visible:

=== "Lua"

    ```lua
    scene:setAmbientLight2D(0.15, Vector3(1, 1, 1))  -- dark scene

    local torch = Light2D(scene)
    torch.position = Vector3(300, 200, 0)
    torch:setRange(250)
    torch:setColor(1.0, 0.8, 0.5)
    torch:setIntensity(1.2)
    ```

=== "C++"

    ```cpp
    scene.setAmbientLight2D(0.15f, Vector3(1, 1, 1)); // dark scene

    Light2D torch(&scene);
    torch.setPosition(Vector3(300, 200, 0));
    torch.setRange(250);
    torch.setColor(1.0f, 0.8f, 0.5f);
    torch.setIntensity(1.2f);
    ```

Key light properties:

| Property | Effect |
| --- | --- |
| `range` | Radius in world units; nothing beyond it is lit |
| `falloff` | Attenuation exponent — `1` linear, higher values concentrate light near the center |
| `height` | Virtual Z height of the light above the 2D plane, used for normal maps (see below) |
| `intensity` / `color` | Brightness and tint, added per light |

Sprites, tilemaps, and mesh polygons receive 2D light automatically (controlled by the
**Receive Lights** flag on their Mesh component). UI objects are not affected. Up to
16 2D lights can be active at once. In the editor, add one from the create menu under
**2D → 2D Light** — selecting it shows its range circle in the scene view.

### Normal maps on sprites

Set a **normal texture** on a sprite's material and give the light a `height` greater
than zero: the light then has a direction relative to the surface, and the normal map
produces relief shading that shifts as the light moves. With `height = 0` the light is
purely radial and normals are ignored.

## 2D shadows

Shadows are cast by **Occluder2D** components. Each shadow-enabled Light2D renders the
occluders around it into a small shadow map, producing radial shadows with optional
soft edges.

An occluder has two shapes:

| Shape | Outline |
| --- | --- |
| `AUTO_QUAD` | The bounds of the mesh on the **same entity** — add the component to a sprite and it casts a shadow matching the sprite quad |
| `POLYGON` | A custom point list in local space, editable in the editor or via code |

=== "Lua"

    ```lua
    torch.shadows = true
    torch.shadowSoftness = 3.0

    local wall = Occluder2D(scene)
    wall.position = Vector3(500, 200, 0)
    wall:addVertex(-60, -20)
    wall:addVertex(60, -20)
    wall:addVertex(60, 20)
    wall:addVertex(-60, 20)
    ```

=== "C++"

    ```cpp
    torch.setShadows(true);
    torch.setShadowSoftness(3.0f);

    Occluder2D wall(&scene);
    wall.setPosition(Vector3(500, 200, 0));
    wall.addVertex(-60, -20);
    wall.addVertex(60, -20);
    wall.addVertex(60, 20);
    wall.addVertex(-60, 20);
    ```

Shadow behavior:

- Each light's shadow darkens **only that light's** contribution — ambient light and
  other lights still reach the shadowed area.
- `shadowSoftness` on the light widens the penumbra (`0` = hard edges); `shadowBias`
  fixes self-shadowing artifacts.
- The scene-wide **filter quality** (`Scene::setShadow2DQuality`) controls how smooth
  the penumbra looks: `NONE`, `LOW` (default), `MEDIUM`, or `HIGH`. Raise it if wide
  penumbras show banding — in the editor it's the **Filter Quality** combo under the
  scene's **2D Shadows** settings.
- Meshes opt out of receiving 2D shadows with the **Receive Shadows** flag.

In the editor, create one from **2D → 2D Occluder** (a standalone polygon), or add an
**Occluder2D component** to an existing sprite for an `AUTO_QUAD` outline. Polygon
points can be dragged directly in the [scene view](../editor/scene-view.md#2d-lights-and-occluders)
or edited as a list in Properties.

For how the technique works under the hood, see
[Rendering Pipeline — 2D lighting](rendering-pipeline.md#2d-lighting-and-shadows).

## Screen scaling

For 2D games it is important to decide how the canvas scales to different screen sizes
and aspect ratios. Doriax provides scaling modes so your game looks correct across
devices and window sizes — configure the canvas size and scaling behavior through the
`Engine` API.

=== "Lua"

    ```lua
    Engine.setCanvasSize(1000, 480)
    Engine.scalingMode = Scaling.FITWIDTH   -- scalingMode is a property in Lua
    ```

=== "C++"

    ```cpp
    Engine::setCanvasSize(1000, 480);
    Engine::setScalingMode(Scaling::FITWIDTH);
    ```

| Scaling mode | Behavior |
| --- | --- |
| `FITWIDTH` | Match the configured canvas width and adjust height |
| `FITHEIGHT` | Match the configured canvas height and adjust width |
| `LETTERBOX` | Preserve aspect ratio with empty bands if necessary |
| `CROP` | Preserve aspect ratio and crop overflow |
| `STRETCH` | Stretch to the output size |
| `NATIVE` | Use the native output size |

## Next steps

For 3D rendering, see [3D Graphics](3d-graphics.md). To add interactions, see
[Physics](physics.md).
