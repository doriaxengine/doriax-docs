---
description: Current and recommended screenshots for the Doriax documentation.
---

# Screenshot Checklist

Place documentation screenshots under `docs/assets/screenshots/`. Use PNG at 1440px
wide or larger. Keep UI scale readable and avoid personal file paths or desktop clutter.

## Existing screenshots

| File | Used in |
| --- | --- |
| `editor-3d-scene.png` | Home page, editor overview, 3D graphics |
| `editor-2d-tilemap.png` | 2D graphics, editor tour, scene view |
| `editor-2d-sprite.png` | 2D sprite editing, scene view |
| `editor-animation.png` | Animation timeline |
| `editor-bones.png` | Skeletal animation / bone tools |
| `editor-camera.png` | Camera and export context |
| `editor-code.png` | Code editor |
| `editor-code-spROPERTY.png` | Script properties, code editor |
| `editor-create-entity.png` | Entity creation workflow |
| `editor-export-window.png` | Export window |
| `editor-inspector-components.png` | Properties window — component groups |
| `editor-physics.png` | Physics page |
| `editor-scene-view.png` | Scene view page |
| `editor-script-component.png` | Creating scripts, Properties window |
| `editor-script-create-dialog.png` | Script creation dialog |
| `editor-script-properties.png` | Script properties |
| `editor-sprite-slicer.png` | Sprite Slicer tool |
| `editor-tileset-slicer.png` | Tileset Slicer tool |
| `editor-ui.png` | UI manual, user-interface |
| `runtime-first-2d-scene.png` | First 2D scene tutorial |
| `runtime-first-3d-scene.png` | First 3D scene tutorial |
| `runtime-first-ui-scene.png` | First UI scene tutorial |
| `runtime-lua-debug.png` | Scripting manual |
| `sprite-slicer-tool-all-screen.png` | Sprite Slicer full-screen view |
| `sprite-slicer-tool.png` | Sprite Slicer detail |

## Priority screenshots for next iteration

These would further improve the documentation. Capture them in the Doriax editor and
save to `docs/assets/screenshots/`.

| File | Page | What to capture |
| --- | --- | --- |
| `editor-project-settings.png` | `editor/project-workflow.md` | Project settings dialog showing startup scene and export targets |
| `editor-resources-browser.png` | `editor/resources.md` | Resources Browser with tree on the left, asset thumbnails, and preview panel |
| `editor-structure-hierarchy.png` | `editor/structure.md` | Structure panel showing parent/child entities and the non-hierarchical area |
| `editor-tileset-slicer-full.png` | `editor/tileset-slicer.md` | Tileset Slicer with grid overlay and tile ID labels visible |
| `editor-bundle.png` | `manual/scenes-and-entities.md` | Bundle in the Resources Browser and an instance placed in a scene |
| `editor-3d-play.png` | `tutorials/first-3d-scene.md` | 3D scene in play mode with a rotating model |

## How to add a screenshot to a page

```markdown
![Short description](../assets/screenshots/filename.png)
*Optional caption below the image.*
```

Use a relative path from the markdown file location. Reference the file with the exact
filename (case-sensitive on Linux).

## After adding files

1. Place PNGs in `docs/assets/screenshots/`.
2. Add the `![...](...)` markdown to the target page.
3. Move the corresponding row from the priority table to the Existing table above.
