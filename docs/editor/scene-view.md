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

## Drag and drop from the Resources Browser

Files dragged from the [Resources Browser](resources.md) can be dropped directly into
the viewport. The editor shows a live preview while you hover, and the change is only
committed (undoably) when you release the mouse:

### Creating entities

| File | Scene type | Result |
| --- | --- | --- |
| Model (GLTF/GLB/OBJ) | 3D | Creates a Model entity at the drop position, named after the file |
| Image | 2D, on empty space | Creates a **Sprite** entity at the drop point, sized to the image |
| Image | UI, on empty space | Creates an **Image** widget at the drop point, sized to the image |

While dragging an image over empty space, a half-transparent ghost of the texture
follows the cursor so you can place it precisely before dropping.

### Modifying the entity under the cursor

Dropping a file *onto* an existing entity assigns it instead of creating something new.
The hovered entity previews the change live; moving away before releasing restores the
original value:

| File | Target entity | Result |
| --- | --- | --- |
| Image | Mesh-based entity (sprite, mesh, model) | Sets the base color texture of the material |
| Image | UI widget | Sets the widget texture |
| Material (`.material`) | Mesh-based entity | Links all submeshes to the material file (live preview while hovering) |
| Font (TTF/OTF) | Text entity | Sets the text font |

This makes texturing a scene fast: drop a texture onto each model to assign it, or
drop a saved material onto several meshes to keep them consistent.

### Shared materials across meshes

When you drop the same `.material` file onto different mesh entities, each submesh
**links** to that file. Editing the material in Properties (while linked) or saving the
`.material` file on disk updates every linked mesh.

To create a new shared material from an existing look:

1. Tune the material on one mesh in Properties.
2. Drag its **material preview** into the Resources Browser to create `Material.material`.
3. Drag that file onto other meshes in the Scene view.

Use the unlink control in Properties when a mesh needs a one-off variation copied from a
shared file.

!!! note "Bundles and scenes drop on the Structure panel"
    `.bundle` and `.scene` files are instanced by dropping them on the
    [Structure panel](structure.md), not the viewport — the tree controls where the
    instance is parented. See [Bundles](bundles.md).

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
