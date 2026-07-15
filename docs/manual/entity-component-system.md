---
description: Understand the data-oriented Entity Component System that powers Doriax Engine.
---

# Entity Component System

Doriax is built on an Entity Component System. This is not only an internal
implementation detail; it is the mental model used by the editor, the runtime, and the
API.

## Entity

An entity is only an ID:

```cpp
using Entity = unsigned;
#define NULL_ENTITY 0
```

The ID does not own position, rotation, rendering, physics, scripts, audio, hierarchy,
or children. It is just a key used by the scene registry to find component data.

## Component

A component is data attached to an entity. An entity behaves according to the
components it has.

```cpp
Entity player = scene.createUserEntity();

scene.addComponent<Transform>(player);
scene.addComponent<MeshComponent>(player);
scene.addComponent<Body2DComponent>(player);
scene.addComponent<ScriptComponent>(player);
```

This entity is now spatial, renderable, physical, and scriptable because those
components exist. Remove one component and that part of the behavior goes away.

The one-argument form default-constructs the component directly in ECS storage. Prefer
it over passing `{}`, especially for components with large fixed-capacity data. To
attach an already configured component, pass the value instead; its type can be
deduced:

```cpp
Transform transform;
transform.position = Vector3(0.0f, 2.0f, 0.0f);
scene.addComponent(player, transform);
```

## System

A system processes entities with the components it understands. `RenderSystem` cares
about renderable components, `PhysicsSystem` cares about body and joint components,
`AudioSystem` cares about sound components, and so on.

## EntityRegistry and Scene

`Scene` inherits from `EntityRegistry`. The registry creates entities, stores component
arrays, tracks each entity signature, and manages the transform hierarchy.

Important registry methods:

| Method | Purpose |
| --- | --- |
| `createEntity()` | Create from the scene's default entity pool |
| `createUserEntity()` | Create a user entity, starting at `EntityManager::firstUserEntity()` |
| `createSystemEntity()` | Create a system entity from the reserved system range |
| `destroyEntity(entity)` | Destroy an entity and remove its components |
| `addComponent<T>(entity)` | Default-construct a component directly in ECS storage |
| `addComponent(entity, value)` | Attach configured component data; the type is deduced |
| `removeComponent<T>(entity)` | Remove component data |
| `findComponent<T>(entity)` | Return a nullable component pointer |
| `getComponent<T>(entity)` | Return a component reference |
| `getSignature(entity)` | Return the component bitset for the entity |

`EntityManager` reserves IDs `1..1000` for system entities and starts user entities at
`1001`. `NULL_ENTITY` is `0`.

## Transform and hierarchy

The hierarchy is not owned by the entity ID. It is built from the `Transform` component:

```cpp
struct Transform {
    Vector3 position;
    Quaternion rotation;
    Vector3 scale;
    Entity parent;
    bool visible;
    // world transforms and matrices are computed from the parent chain
};
```

Only entities with `Transform` can live in the spatial hierarchy. In the editor's
Structure panel, entities without `Transform` are shown in a separate non-hierarchical
area. Add `Transform` if an entity should be positioned or parented.

Hierarchy operations live on `EntityRegistry` and object wrappers:

| API | Meaning |
| --- | --- |
| `addEntityChild(parent, child, changeTransform)` | Parent one transform entity under another |
| `moveChildToTop/Up/Down/Bottom(entity)` | Change sibling order |
| `findOldestParent(entity)` | Find the root of a transform chain |
| `isParentOf(parent, child)` | Test ancestry |
| `Object::addChild(entity)` | Wrapper convenience for parenting |

Removing `Transform` from an entity removes it from this hierarchy. Its script, sound,
action, or other non-spatial components can still exist, but it no longer has local or
world transform data.

## Wrapper classes

Object classes such as `Sprite`, `Model`, `Camera`, `Button`, and `Sound` are wrapper
APIs around entities and components. They make gameplay code easier to write, but they
do not change the ECS rule: the entity is still an ID, and the data lives in
components.

```cpp
Sprite sprite(&scene);
sprite.setSize(64, 64);
sprite.setPosition(100, 100);
```

This wrapper creates or references an entity and manipulates the components needed to
represent a sprite.

## Built-in component groups

The engine includes a broad set of built-in components. Most are exposed through both
editor inspectors and high-level object wrappers.

| Group | Components |
| --- | --- |
| Core | `Transform`, `ScriptComponent`, `BundleComponent` |
| 2D | `SpriteComponent`, `SpriteAnimationComponent`, `TilemapComponent`, `PolygonComponent` |
| 3D | `MeshComponent`, `ModelComponent`, `InstancedMeshComponent`, `TerrainComponent`, `BoneComponent` |
| Rendering | `CameraComponent`, `LightComponent`, `FogComponent`, `SkyComponent`, `ParticlesComponent`, `LinesComponent`, `PointsComponent` |
| Physics | `Body2DComponent`, `Body3DComponent`, `Joint2DComponent`, `Joint3DComponent` |
| UI | `UIComponent`, `UIContainerComponent`, `UILayoutComponent`, `ButtonComponent`, `TextComponent`, `ImageComponent`, `PanelComponent`, `ScrollbarComponent`, `ProgressbarComponent`, `TextEditComponent` |
| Animation/actions | `ActionComponent`, `TimedActionComponent`, `PositionActionComponent`, `RotationActionComponent`, `ScaleActionComponent`, `ColorActionComponent`, `AlphaActionComponent`, keyframe track components |
| Audio | `SoundComponent` |

## Scene systems

Scenes register subsystem instances that react when relevant components are added or
removed. The major runtime systems are:

| System | Handles |
| --- | --- |
| `RenderSystem` | Mesh, sprite, UI, camera, light, sky, fog, line, point, and particle drawing |
| `MeshSystem` | Procedural meshes, model loading, sprite/tilemap geometry, terrain, and instancing |
| `PhysicsSystem` | Box2D 2D bodies, Jolt 3D bodies, joints, contacts, and collision filtering |
| `AudioSystem` | SoLoud-backed sound playback and 3D audio positioning |
| `ActionSystem` | Time-based actions, sprite animation, skeletal animation, and keyframe tracks |
| `UISystem` | UI layout, button interaction, text editing, and event dispatch |

## Object wrappers

The object classes in `engine/core/object/` are convenience wrappers around entities.
For example, `Sprite` owns an entity and exposes sprite-specific methods, while still
using the same ECS data as editor-created entities.

Use wrappers when writing gameplay code. Drop to raw ECS access when you are building
engine extensions, custom tools, or systems that need to process many entities at once.

## Next steps

See [Creating Scripts](creating-scripts.md) to learn how Lua and C++ drive behavior on
top of entities and components.
