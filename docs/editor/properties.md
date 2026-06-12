---
description: Using the Properties window to inspect, edit, and configure entity components in Doriax.
---

# Properties & Components

The **Properties window** displays every component attached to the selected entity and
lets you read and change their values. It is the primary place to configure transforms,
materials, physics, scripts, UI layout, audio, animations, and any other component
data.

![Properties window with components](../assets/screenshots/editor-inspector-components.png)

## Selecting an entity

Click an entity in the **Structure panel** or directly in the **Scene view** to select
it. The Properties window updates immediately to show its components.

## Adding components

Use the **Add Component** button at the bottom of the Properties window. A searchable
dialog lists all available component types grouped by category. Components are added to
the entity immediately and their defaults appear in the panel for editing.

![Script component in the Properties window](../assets/screenshots/editor-script-component.png)

## Component groups

| Group | Typical components |
| --- | --- |
| **Spatial** | Transform, Camera, Light, Fog, Skybox |
| **2D** | Sprite, Sprite Animation, Tilemap, Polygon |
| **3D** | Mesh, Model, Instanced Mesh, Terrain, Bone |
| **Physics** | Body2D, Body3D, Joint2D, Joint3D |
| **UI** | UILayout, Button, Text, Image, Panel, Scrollbar, Progressbar, TextEdit |
| **Animation** | TimedAction, ActionComponent, Animation |
| **Audio** | SoundComponent |
| **Scripting** | ScriptComponent and script property fields |

## Editing component fields

Most fields are edited with the mouse or keyboard directly in the panel:

| Field type | Editing method |
| --- | --- |
| Numbers (float, int) | Click and drag, or double-click to type a value |
| Vectors (Vector2, Vector3) | Per-component drag or type fields |
| Colors | Color picker with RGBA sliders |
| Booleans | Toggle checkbox |
| Strings | Inline text input |
| Textures / assets | Drag from the Resources Browser or type the asset path |
| Entity references | Drag an entity from the Structure panel |
| Enumerations | Drop-down selection |

## Mesh materials and IBL

The **Mesh** component exposes rendering flags beyond per-submesh material slots:

| Property | Purpose |
| --- | --- |
| **Receive IBL** | When enabled, the mesh is lit with the scene's Sky environment (diffuse irradiance + specular reflections) in addition to punctual lights. Requires a Sky entity with a cubemap texture. |
| **Receive Lights** | Master switch for dynamic lighting (must be on for IBL to apply). |
| **Cast / Receive Shadows** | Shadow map participation. |

Each **Submesh** section contains a **Material** row with a shaded preview sphere. The
preview reflects the current **Receive IBL** setting so you can see environment
reflections before entering play mode.

### Linking material files

The Material row supports three workflows:

1. **Edit inline** — expand the material section and change factors and textures directly
   in the scene (values stored on the mesh component).
2. **Link to a file** — drag a `.material` file from the Resources Browser onto the
   Material row or preview; the mesh submesh links to that file and reloads when it
   changes on disk.
3. **Create a shared file** — drag the material preview **from Properties into the
   Resources Browser**; the editor writes a new `.material` file and links the submesh
   to it automatically.

When linked, the material name shows the file name and an **unlink** button (broken
chain icon) appears. Unlinking keeps the current values on the mesh but stops syncing
with the file.

You can also drop a single **image** onto the Material row to assign only the base colour
texture without replacing the rest of the material.

## Sky component

The **Sky** component controls the scene cubemap background and the IBL environment:

| Property | Purpose |
| --- | --- |
| **Visible** | Draw the sky in the viewport. When off, the sky is hidden but still feeds IBL to meshes with **Receive IBL** enabled. |
| **Texture** | Cubemap source (six faces or bundled layout). Changing it rebuilds IBL maps. |
| **Color** | Tint multiplied with the sky texture. |
| **Rotation** | Rotate the sky around the Y axis. |

Use **Default sky** to restore the built-in editor cubemap.

## Scripts

Two buttons at the bottom of the Properties window create scripts:

- **New Script** — opens a dialog that generates the script files (Lua module, or C++
  header + source), adds a `ScriptComponent` if the entity lacks one, and links an
  enabled entry to the new files — all in one undoable step.
- **New component → ScriptComponent**, then **Add Script** inside the component — adds
  an *empty* script entry without creating files. Use the entry's pencil button to set
  the class name and link existing header/source (or `.lua`) files.

Each script entry shows an enable checkbox, buttons to open its files in the Code
Editor, and a right-click menu to reorder or remove it.

### Script properties

When a script is linked, the Properties window shows every property declared with the
`DPROPERTY` macro (C++) or in the `properties` table (Lua). These fields are serialized
with the scene and injected into the script instance at play and export time.

![Script property fields in the Properties window](../assets/screenshots/editor-script-properties.png)

See [Creating Scripts](../manual/creating-scripts.md) for the full workflow and
[Script Properties](../manual/script-properties.md) for declaring and typing custom
script properties.

## Entity references

Some component fields accept another entity as their value — for example, a physics
joint links two Body entities, a Camera can follow a target entity, and script
properties of pointer types display an entity picker. Drag the target entity from the
Structure panel into the field, or use the picker icon.

Keep referenced entities inside the same scene or a consistently-loaded child scene so
exports can resolve the relationship correctly.

## Transform gizmo

Selecting a transform field highlights the corresponding gizmo in the Scene view.
You can edit numeric values in the Properties window and see the result in the viewport
at the same time, or manipulate the gizmo and watch the numbers update live.

## Undo / redo

Every property edit is recorded in the command history. Use **Ctrl+Z** / **Ctrl+Y** to
step back and forward through changes made in the Properties window or in the viewport.

## Best practices

- Prefer editor-exposed `DPROPERTY` fields for any value a designer should tune,
  rather than hard-coding it in script logic.
- Keep generated or runtime-only data out of serialized component fields.
- After changing physics, script, or animation fields, test in play mode immediately
  because those affect runtime behavior, not just visual appearance.
- Use [bundles](bundles.md) for repeated configured entity hierarchies so the same
  property values do not have to be re-entered manually in many scenes. For entities
  inside a bundle instance, the component header's right-click menu offers
  **Make Unique** (override this instance) and **Revert to Bundle** (re-link to the
  shared values).
