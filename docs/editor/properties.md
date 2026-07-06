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
| **Spatial** | Transform, Camera, Light, Fog, Skybox, Mirror |
| **2D** | Sprite, Sprite Animation, Tilemap, Polygon, 2D Light, 2D Occluder |
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
| Textures / assets | Drag from the Resources Browser, type the asset path, or pick a **camera** as the source (camera button / drag a camera entity) for render-to-texture. For an `.svg` source, a vector-square button opens an **SVG Scale** control |
| Entity references | Drag an entity from the Structure panel |
| Enumerations | Drop-down selection |

A texture field set to a camera shows that camera's live output (render-to-texture). The
camera is switched to render-to-texture automatically and can no longer be the scene's
main camera. This is the manual building block behind effects like minimaps and monitors;
for reflections, prefer the [Mirror component](#mirror-component), which manages its own
camera.

Once a camera is in render-to-texture mode, its own properties gain a **Render Target**
section for setting the framebuffer **Width**, **Height**, and sampling **Filter**
(Nearest or Linear). These control the resolution and look of the output texture, are
saved with the scene, and are applied in exported projects.

When the field points at an `.svg` file, an extra vector-square button appears next to the
camera button. It opens a popup to set the **SVG Scale** — a multiplier on the vector's
intrinsic size (a slider plus 0.5×–4× presets) — so the image rasterizes crisp when drawn
larger or on high-DPI displays. The scale is stored on the texture reference, so different
slots can use the same SVG at different resolutions. See
[Vector images (SVG)](../manual/resources-and-assets.md#vector-images-svg) for the
underlying behavior.

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

## Custom shaders

Mesh, UI, Points, Lines, and Sky components expose a **Shader** row. By default it shows
**Built-in**; click **Customize** to fork the built-in shader into your project and edit
its GLSL in the Code Editor. **Edit** reopens the assigned shader and **Reset to
Built-in** returns to the engine default. You can also drag an existing `.vert`/`.frag`
from the Resources Browser onto the row.

A scene can also define a **default custom shader per type** (in the scene settings'
**Default Shaders** section); components whose Shader row shows **Built-in** inherit it.
A shader assigned on the component always takes priority over the scene default.

See [Custom Shaders](custom-shaders.md) for the full workflow, scene defaults, includes,
and project settings.

## Sky component

The **Sky** component controls the scene cubemap background and the IBL environment:

| Property | Purpose |
| --- | --- |
| **Visible** | Draw the sky in the viewport. When off, the sky is hidden but still feeds IBL to meshes with **Receive IBL** enabled. |
| **Texture** | Cubemap source (six faces or bundled layout). Changing it rebuilds IBL maps. |
| **Color** | Tint multiplied with the sky texture. |
| **Rotation** | Rotate the sky around the Y axis. |

Use **Default sky** to restore the built-in editor cubemap.

## Mirror component

The **Mirror** component turns its mesh into a planar reflection surface. Add it to a flat
mesh (a [Wall](structure.md#basic-shapes) works out of the box), or use the **Mirror**
entry in the Structure create menu, which sets up the wall and component together.

| Property | Purpose |
| --- | --- |
| **Normal** | The reflecting surface direction in the mesh's local space (default `+Z`, matching a Wall). It is rotated with the entity to form the world mirror plane. |

The reflection camera is created and managed by the engine — there is nothing else to
wire. If the reflection is clipped on the wrong side, flip the sign of **Normal**. See
[Rendering Pipeline — Mirrors and planar reflections](../manual/rendering-pipeline.md#mirrors-and-planar-reflections)
for how it works and its cost.

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
