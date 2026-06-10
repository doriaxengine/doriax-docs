---
description: Create, instantiate, and edit entity bundles (prefabs) in the Doriax editor with .bundle files.
---

# Bundles

A **bundle** is a reusable entity hierarchy saved as a YAML `.bundle` file — Doriax's
prefab. Build an entity once (a configured enemy, a UI panel, a streetlight with light
and physics), turn it into a bundle, and instance it as many times as you need. Editing
the bundle updates every instance.

A `.bundle` file can live in **any folder of your project directory**, so you can
organize bundles alongside the assets they use (`enemies/`, `ui/`, `props/`, etc.).

## Creating a bundle

Drag an entity from the **Structure panel** into the **Resources Browser**:

1. Build and configure the entity (and its children) in the scene.
2. In the Resources Browser, navigate to the folder where the bundle should be saved.
3. Drag the entity from the Structure panel and drop it on the Resources Browser.

The editor writes `<EntityName>.bundle` into the open folder (a numeric suffix is added
if the name is taken) and **replaces the dragged hierarchy with an instance of the new
bundle** — the entities now live in the bundle, and the scene holds an instance root
pointing at the file. Dragging a multi-entity selection works the same way and stores
all of the selected branches in one bundle. The whole operation is undoable.

## Instancing a bundle

Drag the `.bundle` file from the Resources Browser onto the **Structure panel**:

| Drop target | Result |
| --- | --- |
| Scene root node | Instance added at the top level of the scene |
| An entity with `Transform` | Instance added as a child of that entity |

Each drop creates an independent instance with its own root `Transform`, so instances
can be positioned, rotated, and scaled individually. Bundles can also be instanced
inside other bundles (nested bundles).

## How instances stay in sync

The bundle owns the component data. All instances read from it, so:

- **Editing a component inside any instance edits the bundle** — the change appears in
  every instance of that bundle, in every scene that uses it.
- **To customize a single instance**, right-click the component header in the
  Properties window and choose **Make Unique**. That component becomes a local
  override for this instance and stops following the bundle.
- **Revert to Bundle** on an overridden component discards the local values and
  re-links it to the bundle.

The instance root's `Transform` is always per-instance (that is what lets you place
each copy somewhere different), and it cannot be removed.

## Adding and removing member entities

Right-click entities in the Structure panel to change what belongs to the bundle:

| Menu item | Where | Effect |
| --- | --- | --- |
| **Insert into bundle** | A non-member child under a bundle instance | Entity becomes part of the bundle (appears in all instances) |
| **Remove from bundle** | A member entity inside an instance | Entity leaves the bundle but stays in this scene as a regular entity |
| **Insert to Bundle ▸** | Any entity outside a bundle | Moves the entity into one of the scene's existing bundles |

New entities created under a bundle root from the Structure create menu can join the
bundle directly. Nested bundle instances have matching *(nested)* menu entries to
control membership in the outer bundle.

## Saving

Bundle edits mark the bundle as modified, and modified bundles are written to their
`.bundle` files **when you save the scene** (Ctrl+S). Unsaved bundle changes count
toward the scene's unsaved-changes indicator and the close-confirmation prompts, so
they are not lost silently.

Renaming or moving a `.bundle` file through the Resources Browser context menu updates
the scenes that reference it.

## Bundles vs child scenes

| | Bundle | Child scene |
| --- | --- | --- |
| File | `.bundle` | `.scene` |
| Use for | Repeated entity hierarchies (props, enemies, UI widgets) | Large scene sections, levels, screens |
| Instances per scene | Many | One reference per child scene node |
| Per-instance overrides | Yes (Make Unique per component) | No |

## See also

- [Structure Panel](structure.md) — the tree where bundles are created and instanced
- [Resources Browser](resources.md) — where `.bundle` files live
- [Properties & Components](properties.md) — component editing and override menus
