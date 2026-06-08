---
description: Working with 2D graphics in Doriax — sprites, tilemaps, and polygons.
---

# 2D Graphics

Doriax has full support for 2D game development with sprites, tilemaps, and primitive
shapes, backed by the same ECS used for 3D.

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

## Screen scaling

For 2D games it is important to decide how the canvas scales to different screen sizes
and aspect ratios. Doriax provides scaling modes so your game looks correct across
devices and window sizes — configure the canvas size and scaling behavior through the
`Engine` API.

```lua
Engine.setCanvasSize(1000, 480)
Engine.setScalingMode(Scaling.FITWIDTH)
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
