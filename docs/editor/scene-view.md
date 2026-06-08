---
description: Viewport navigation, gizmos, cameras, and scene editing tools in the Doriax editor.
---

# Scene View

The **Scene view** is the main canvas for authoring scenes. It renders the current
scene using editor cameras and overlays gizmos, selection highlights, and tool guides
on top. You place, rotate, scale, and test entities here, and you see the result of
component changes made in the Properties window immediately.

![Scene view](../assets/screenshots/editor-scene-view.png)

## Navigation

| Action | Input |
| --- | --- |
| **Orbit** | Right-click drag (3D) |
| **Pan** | Middle-click drag, or Shift + right-click drag |
| **Zoom** | Mouse wheel |
| **Focus on selection** | **F** key |
| **Reset camera** | Home key or double-click empty space |

In 2D mode the camera is orthographic; orbit is replaced with a simple pan.

## Gizmo tools

Select a gizmo mode from the toolbar or with the keyboard:

| Gizmo | Key | Purpose |
| --- | --- | --- |
| **Translate** | W | Move selected entities along axes or planes |
| **Rotate** | E | Rotate selected 3D entities |
| **Scale** | R | Resize entities uniformly or per axis |
| **Object2D** | — | Manipulate 2D objects in canvas space (position and size) |
| **Anchor** | — | Edit UI anchor points and layout bounds |

Hold **Ctrl** while transforming to snap to the configured grid interval. Hold **Alt**
to move in world space instead of local space.

## Selection

Click an entity in the viewport to select it; the Properties window updates
immediately. Hold **Ctrl** and click to add to or remove from a multi-selection.

For fine-grained selection in dense scenes, use the **Structure panel** — clicking a
row there selects the entity without needing to click through overlapping objects.

## Viewport camera vs game camera

The **editor camera** is only for authoring navigation. The **game camera** is a
`Camera` entity you place in your scene; it defines what the player sees at runtime.
Always verify gameplay framing with the game camera preview before testing.

## 2D and tilemap editing

![2D sprite editing](../assets/screenshots/editor-2d-sprite.png)

In a 2D scene the editor uses orthographic projection and a canvas overlay. Sprites,
tilemaps, UI widgets, and polygons should be positioned in a consistent logical
coordinate system so that canvas scaling stays predictable across different screen sizes.

Tilemap cells can be painted directly in the scene view when a Tilemap entity is
selected and the tile-paint mode is active.

![Tilemap in scene](../assets/screenshots/editor-2d-tilemap.png)

## 3D scene editing

3D scenes use perspective projection and full 3D gizmos. Switch between the editor
camera and the game camera preview to check framing. Use the **F** key to center the
view on a selected entity.

## UI scene editing

UI scenes display the canvas in screen-space overlay mode. Anchor gizmos show the
layout boundaries of UI elements. Drag anchors directly to reposition or stretch
widgets relative to their parent.

![UI scene editing](../assets/screenshots/editor-ui.png)

## Physics visualization

When a `Body2D` or `Body3D` is attached, the editor draws the collision shape outline
in the viewport. This lets you verify that the physics shape matches the visual mesh
without running the game.

![Physics visualization](../assets/screenshots/editor-physics.png)

## Play mode in the viewport

Press **Play** to run the scene inside the viewport. All input and logic operate
normally. When you press **Stop**, the scene is restored to the pre-play snapshot.
Use play mode for fast local iteration; export to a real build for platform-specific
testing.
