---
description: How the Doriax Structure panel represents scenes, child scenes, entities, hierarchy, and non-transform entities.
---

# Structure Panel

The Structure panel is the editor's tree view for scenes and entities. It is also the
clearest way to understand Doriax's ECS model: everything shown under a scene is an
entity, but only entities with a `Transform` participate in the spatial hierarchy.

## Scene root

The top node is the selected scene. Child scenes are shown before entities. If a child
scene is expanded inline, its entities are shown under that child scene node.

## Empty entity vs empty object

![Create entity from the Structure panel](../assets/screenshots/editor-create-entity.png)

The create menu has two intentionally different entries:

| Entry | Components added | Meaning |
| --- | --- | --- |
| Empty entity | None | A pure entity ID. Use it for logic, global scripts, non-spatial data, or components that do not need a transform. |
| Empty object | `Transform` | A spatial entity. It can be positioned, parented, rendered, and shown in the hierarchy. |

This distinction matters because the entity itself owns nothing. Components decide what
the ID can do.

## Hierarchical area

Entities with `Transform` appear in the hierarchy area. Their parent-child relation is
stored in `Transform::parent`, and their order is managed by the scene registry. Moving
a parent updates child world transforms through that parent chain.

Common entities in this area include objects, sprites, models, cameras, lights, 3D
sounds, physics bodies, UI widgets, points, lines, terrain, and mesh polygons.

## Non-hierarchical area

Entities without `Transform` appear separately before the transform hierarchy. They are
valid scene entities, but they do not have a spatial parent or local/world transform.

Typical non-transform entities include:

| Entity type | Why it may not need `Transform` |
| --- | --- |
| Empty entity | Logic-only entity or script host |
| Sound source | Non-spatial audio |
| Sky/Fog | Scene environment data |
| Joints | Constraint data linking physics bodies |
| Actions/animations | Time-based behavior targeting another entity |
| Particles action | Playback behavior targeting another entity |

An entity can be selected and inspected even if it is not in the transform hierarchy.
Add a `Transform` if it should become spatial or parentable.

## Drag and drop rules

Reparenting is a transform operation. Dragging an entity under another entity only
makes sense when the moved entity has `Transform`. Non-transform entities can still be
reordered in their separate area or associated virtually with a target, such as an
action targeting a transformed entity.

## Practical model

Use the Structure panel as a quick diagnostic:

- Entity appears in the tree hierarchy: it has `Transform`.
- Entity appears above the hierarchy: it has no `Transform`.
- Entity cannot be parented: add `Transform` or choose Empty object instead.
- Visual entity is missing from the hierarchy: check whether `Transform` was removed.