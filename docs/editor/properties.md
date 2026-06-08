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

## Script properties

When a `ScriptComponent` is present, the Properties window shows every property
declared with the `DPROPERTY` macro (C++) or in the `properties` table (Lua). These
fields are serialized with the scene and injected into the script instance at play and
export time.

![Script property fields in the Properties window](../assets/screenshots/editor-script-properties.png)

See [Script Properties](../manual/script-properties.md) for full details on declaring
and typing custom script properties.

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
- Use bundles for repeated configured entity hierarchies so the same property values do
  not have to be re-entered manually in many scenes.
