---
description: How Doriax handles window sizes, aspect ratios, canvas scaling, and fixed render resolution with upscaling.
---

# Multiple Resolutions

Games run on an enormous range of displays: phones in portrait and landscape, laptops,
4K monitors, ultrawide screens, and resizable desktop windows. Doriax separates the
size your game is *designed* for from the size it is *displayed* at, so one project can
look correct everywhere. This page covers the three concepts involved and how to
combine them:

- **Canvas size and scaling mode** — the logical coordinate space your game is designed
  in, and how it maps onto the real window (project-wide, set on `Engine`).
- **View rect** — the region of the window the game actually occupies after scaling
  (computed automatically; may include letterbox bars).
- **Fixed resolution** — an optional per-scene setting that renders the game at a fixed
  internal resolution and upscales the result to the window, independent of the
  display's real pixel count.

## Canvas size

The **canvas** is the logical coordinate space of your game — the size you design
against. Positions of 2D objects, UI elements, and input coordinates are all expressed
in canvas units, not physical pixels. Pick a canvas size that matches your target
design (for example 1280×720) and the engine maps it to whatever window or screen the
game runs on:

=== "Lua"

    ```lua
    Engine.setCanvasSize(1280, 720)
    Engine.scalingMode = Scaling.LETTERBOX   -- scalingMode is a property in Lua
    ```

=== "C++"

    ```cpp
    Engine::setCanvasSize(1280, 720);
    Engine::setScalingMode(Scaling::LETTERBOX);
    ```

In editor projects, the canvas size and scaling mode are set in **Project Settings**
and applied automatically to exported builds.

## Scaling modes

The scaling mode decides what happens when the window's aspect ratio does not match
the canvas:

| Scaling mode | Behavior |
| --- | --- |
| `FITWIDTH` | Keeps the canvas width fixed; the height floats to match the window's aspect ratio. More or less of the world is visible vertically. |
| `FITHEIGHT` | Keeps the canvas height fixed; the width floats. |
| `LETTERBOX` | Preserves the full canvas and its aspect ratio; empty bands fill the leftover space. |
| `CROP` | Preserves the aspect ratio and fills the window completely; the canvas overflows and its edges are cropped. |
| `STRETCH` | Stretches the canvas to the window size. No bars and no cropping, but the image distorts when aspect ratios differ. |
| `NATIVE` | The canvas equals the physical output size. Coordinates are real pixels. |

Choosing between them is a design decision:

- `FITWIDTH` / `FITHEIGHT` suit games that can safely reveal more of the world on one
  axis (many 2D side-scrollers fix the height and let the width breathe, and vice
  versa).
- `LETTERBOX` guarantees every player sees exactly the same framing — good for puzzle
  boards and fixed compositions. The bands take the scene background color.
- `CROP` guarantees full-screen coverage — keep important gameplay elements away from
  the edges.
- `STRETCH` is rarely what you want unless aspect ratios are guaranteed to match.
- `NATIVE` fits tools and UI-heavy applications more than games.

The result of canvas + scaling is the **view rect**: the on-screen rectangle where the
game is drawn. Input events are converted from window coordinates back into canvas
coordinates through the same mapping, so your gameplay code never needs to know the
real window size. UI elements additionally use
[anchors](user-interface.md#anchors-and-layout) to adapt their layout inside the
canvas.

!!! tip
    You can react to canvas changes (window resize, device rotation) with the
    `Engine::onCanvasChanged` event, for example to reposition elements that are not
    anchor-driven.

## Fixed resolution

Canvas scaling controls *coordinates*, but the scene is still rasterized at the real
window resolution — a 4K monitor renders roughly eight times more pixels than a 720p
one. The **fixed resolution** setting decouples the *render* resolution from the
display: the scene's main camera renders into an internal buffer of an exact size you
choose (say 320×180 or 640×360), and that image is then upscaled to fill the view
rect. The player's desktop resolution never changes.

Two situations call for it:

- **Pixel-art and retro games** — render at a small authentic resolution and upscale
  with nearest-neighbor filtering for crisp, chunky pixels, no matter the display.
- **Performance** — fragment-shader cost scales with pixel count. Rendering at a lower
  internal resolution and upscaling is one of the most effective ways to speed up a
  GPU-bound game, especially on mobile and integrated graphics.

Fixed resolution is a **scene setting**. In the editor it lives in the scene's
Properties panel (select nothing so the scene itself is shown), under **Fixed
Resolution**:

| Setting | Default | Description |
| --- | --- | --- |
| Enabled | off | Renders the main camera at the fixed size and upscales to the view rect. |
| Width / Height | 640 × 360 | The internal render resolution in pixels. |
| Filter | Nearest | How the image is sampled during the upscale: **Nearest** keeps hard pixel edges (pixel-art look), **Linear** interpolates smoothly. |

The same settings are available from code:

=== "Lua"

    ```lua
    scene.fixedResolutionEnabled = true
    scene:setFixedResolutionSize(320, 180)
    scene.fixedResolutionFilter = TextureFilter.NEAREST
    ```

=== "C++"

    ```cpp
    scene.setFixedResolutionEnabled(true);
    scene.setFixedResolutionSize(320, 180);
    scene.setFixedResolutionFilter(TextureFilter::NEAREST);
    ```

### How it interacts with canvas scaling

Fixed resolution layers *under* the canvas system rather than replacing it. The canvas
and scaling mode keep deciding the view rect, framing, letterbox bars, and input
mapping exactly as before; the fixed resolution only changes how many pixels the scene
is rasterized with before being stretched into that view rect. In practice:

- Keep the **canvas aspect ratio equal to the fixed resolution aspect ratio** (for
  example canvas 1280×720 with fixed resolution 320×180 — both 16:9). Mismatched
  ratios produce non-square pixels, since the image is stretched to the view rect.
- Letterbox bars still come from the scaling mode and still use the scene background
  color.
- Object positions, physics, and input are unaffected — they operate in canvas
  coordinates regardless of the render resolution.

### Rules and behavior

- **Main scene only.** The setting takes effect on the scene shown with
  `Engine::setScene`. Scenes added as layers (`Engine::addSceneLayer`) always render at
  native resolution, even if their own setting is enabled.
- **Crisp UI over a low-res game.** Because layers stay native, the standard recipe for
  a pixel-art game with sharp text is: enable fixed resolution on the game scene and
  put the HUD/menus in a separate UI scene added as a layer on top.
- **Editor preview.** In the editor, the scene viewport stays at native resolution
  while editing (so gizmos and selection remain precise) and switches to the fixed
  resolution when you press **Play**.
- **Screen-space effects follow the fixed resolution.** SSAO and SSR run at the
  internal resolution, so they get the same pixelated look — and the same performance
  savings — as the rest of the scene.
- The image is rendered once per frame into the internal buffer and upscaled in a
  single fullscreen pass; the overhead is negligible next to the savings of shading
  fewer pixels.

### Changing resolution at runtime

Width, height, and filter can be changed at any time — the internal buffer is resized
on the next frame with no interruption. This makes a resolution option in a settings
menu, or even dynamic resolution scaling, straightforward:

=== "Lua"

    ```lua
    -- settings menu: apply a render-scale preset
    function applyRenderScale(scene, scale)
        local w = math.floor(1280 * scale)
        local h = math.floor(720 * scale)
        scene:setFixedResolutionSize(w, h)
    end

    applyRenderScale(scene, 0.5)  -- render at 640x360, upscale to the window
    ```

=== "C++"

    ```cpp
    // settings menu: apply a render-scale preset
    void applyRenderScale(Scene& scene, float scale) {
        unsigned int w = (unsigned int)(1280 * scale);
        unsigned int h = (unsigned int)(720 * scale);
        scene.setFixedResolutionSize(w, h);
    }

    applyRenderScale(scene, 0.5f); // render at 640x360, upscale to the window
    ```

Toggling `fixedResolutionEnabled` at runtime also works, but is heavier than a size
change: the engine rebuilds render pipelines for the scene's objects, which can cause
a brief hitch. Prefer leaving it enabled and adjusting the size instead.

!!! tip "Pixel-art checklist"
    - Fixed resolution at your sprite-native size (e.g. 320×180) with **Nearest**
      filter.
    - Canvas size an integer multiple of it with the same aspect ratio (e.g.
      1280×720).
    - `LETTERBOX` scaling so the framing is identical on every display.
    - HUD and text in a separate UI scene layered on top for full-resolution
      crispness — or inside the fixed-resolution scene if you want the UI pixelated
      too.

## Common setups

| Goal | Canvas + scaling | Fixed resolution |
| --- | --- | --- |
| Standard 2D/3D game, sharp at any size | Design-size canvas, `FITWIDTH`/`LETTERBOX` | Off |
| Pixel-art / retro | Canvas multiple of the art size, `LETTERBOX` | On, art-native size, Nearest |
| GPU-bound game on weak hardware | Design-size canvas, any mode | On, reduced size (e.g. 70% of 1080p), Linear |
| Identical framing on all devices | `LETTERBOX` | Optional |
| Tools / UI applications | `NATIVE` | Off |

## Next steps

- [User Interface](user-interface.md) — anchors and layout inside the canvas.
- [2D Graphics](2d-graphics.md) — cameras and coordinates for 2D scenes.
- [Rendering Pipeline](rendering-pipeline.md) — render-to-texture and screen-space
  effects.
- [Scene reference](../reference/classes/scene.md) — the full fixed-resolution API.
- [Engine reference](../reference/classes/engine.md) — canvas size, scaling mode, and
  events.
