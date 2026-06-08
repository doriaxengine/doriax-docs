---
description: Importing, browsing, previewing, and organizing resources in the Doriax editor.
---

# Resources Browser

The **Resources Browser** is the file manager for your project's assets. It lets you
import new files, preview existing resources, drag assets into scenes, assign them to
components, and open specialized tool windows such as the Sprite Slicer and Tileset
Slicer.

## Supported resource types

| Type | Extensions | Typical use |
| --- | --- | --- |
| Textures | PNG, JPG, BMP, TGA, PSD, HDR | Sprites, UI images, albedo/normal/roughness/metallic maps, skyboxes |
| Models | GLTF, GLB, OBJ | 3D meshes, skeletons, animations, morph targets |
| Audio | OGG, WAV, MP3, FLAC | Sound effects, music, 3D spatial audio |
| Fonts | TTF, OTF | Text and UI rendering |
| Scenes | YAML scene files | Saved scenes and child scene references |
| Bundles | YAML bundle files | Reusable entity hierarchies (prefab-like) |
| Shaders | Shader data files | Built, serialized, and loaded shader programs |
| Scripts | LUA, CPP, H | Gameplay logic files |

## Previews

The browser includes inline preview renderers. Select a resource to see:

- **Texture preview** — full image with mip-level and channel controls.
- **Model preview** — interactive 3D view with orbit navigation, lighting, and material
  display.
- **Material preview** — shaded sphere with the PBR material applied.
- **Font preview** — sample text at the font's supported sizes.
- **Audio preview** — waveform display and play button.

Use previews to catch missing textures, wrong scale, or broken imports before dropping
assets into a scene.

## Importing assets

Copy files into your project folder or drag them from your OS file manager into the
Resources Browser. The editor scans the asset directories on startup and whenever the
project folder changes.

!!! tip "File naming"
    Use lowercase, hyphen-or-underscore-separated file names without spaces. Consistent
    naming avoids case-sensitivity issues on Linux and Android and makes asset paths
    predictable in scripts.

## Dragging assets into scenes

Drag a texture, model, audio file, or scene directly from the Resources Browser:

| Asset type | Drop target | Result |
| --- | --- | --- |
| Texture | Scene view | Creates a Sprite entity with the texture assigned |
| Model (GLTF/OBJ) | Scene view | Creates a Model entity and loads the file |
| Audio | Scene view | Creates a Sound entity with the file assigned |
| Scene / bundle | Scene view or hierarchy | Adds the scene as a child scene or creates a bundle instance |
| Texture | A component field | Assigns the texture to that field |

## Context menu

Right-click any resource to access:

- **Open** — opens the file with the appropriate editor tool.
- **Open in Sprite Slicer** — opens the texture in the [Sprite Slicer](sprite-slicer.md) tool.
- **Open in Tileset Slicer** — opens the texture in the [Tileset Slicer](tileset-slicer.md) tool.
- **Rename** — renames the file on disk and updates scene references.
- **Delete** — removes the file from the project.
- **Show in OS** — reveals the file in the system file manager.

## Sprite and tileset slicing

Two dedicated slicer tools process sprite sheets and tilesets:

### Sprite Slicer

The **Sprite Slicer** divides a texture into named frames for sprite animation or
individual sprite display. Supports grid-based slicing (uniform cell size) and
free-form rectangle drawing for irregular layouts.

![Sprite Slicer](../assets/screenshots/editor-sprite-slicer.png)

See [Sprite Slicer](sprite-slicer.md) for the complete workflow.

### Tileset Slicer

The **Tileset Slicer** splits a tileset texture into uniformly-sized tiles and assigns
each tile a numeric ID. Those IDs are used when painting tiles in the Tilemap editor
and when defining tile data in scripts.

See [Tileset Slicer](tileset-slicer.md) for the complete workflow.

## Organization guidelines

- Keep source art, imported assets, and generated data in separate folders.
- Separate audio by category: `sounds/effects/`, `sounds/music/`, etc.
- Prefer GLTF for animated or material-rich 3D assets; OBJ for simple static geometry.
- Store collision meshes separately from visual meshes.
- Remove unused large assets before exporting mobile or web builds to keep bundle
  sizes small.

## See also

- [Sprite Slicer](sprite-slicer.md)
- [Tileset Slicer](tileset-slicer.md)
- [Resources & Assets](../manual/resources-and-assets.md)
- [2D Graphics](../manual/2d-graphics.md)
