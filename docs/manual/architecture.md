---
description: Runtime architecture of Doriax: Engine, Scene, ECS, systems, managers, rendering, physics, and scripting.
---

# Engine Architecture

Doriax is organized around a small runtime core, an ECS, scene-scoped subsystems, and
high-level object wrappers. The editor sits on top of the same runtime concepts and
serializes scenes into data that can be exported to native projects.

## Runtime layers

| Layer | Responsibility |
| --- | --- |
| `Engine` | Global runtime state: scenes, canvas, scaling, timing, platform, events, async loading |
| `Scene` | Entity registry, active camera, lighting state, UI events, and registered subsystems |
| ECS | Entity IDs, component arrays, signatures, and component lifecycle notifications |
| Subsystems | Rendering, mesh processing, physics, audio, actions, UI |
| Object wrappers | Friendly APIs such as `Sprite`, `Model`, `Camera`, `Light`, `Body2D`, `Button` |
| Managers | Scene and bundle factories for runtime loading |
| Platform/render backends | Window, input, graphics, filesystem, and target-specific integration |

## Engine singleton

`Engine` is a static API. It stores the main scene stack, canvas size, scaling mode,
timing values, platform/backend information, event subscriptions, and async-loading
state.

Common responsibilities:

- Set and layer scenes.
- Configure canvas size and scaling.
- Track delta time, framerate, and physics interpolation.
- Forward input and lifecycle events.
- Manage render-to-texture framebuffers.
- Coordinate async loading and queued work committed to the main thread.

## Scenes

`Scene` extends `EntityRegistry`. It owns entities and components, then registers
systems that process those components. Component add/remove notifications are forwarded
to every registered subsystem so render, physics, audio, and UI state can stay in sync.

## Systems

Systems are scene-scoped, not global. This keeps scene state isolated and lets editor
play mode snapshot and restore scene data safely.

| System | Runtime role |
| --- | --- |
| `RenderSystem` | Draws cameras, meshes, sprites, lights, UI, sky, fog, particles, lines, and points |
| `MeshSystem` | Generates and loads mesh data, including GLTF, OBJ, terrain, tilemaps, sprites, and instancing |
| `PhysicsSystem` | Steps 2D/3D physics, contacts, sensors, joints, filters, and body transforms |
| `AudioSystem` | Plays, pauses, seeks, and spatializes sounds through SoLoud |
| `ActionSystem` | Updates actions, animation playback, sprite animation, and keyframe tracks |
| `UISystem` | Handles UI layout, events, text input, and UI rendering support |

## Data flow

1. User or editor code creates entities and components.
2. The scene registry stores component data and updates entity signatures.
3. Subsystems receive lifecycle notifications.
4. Every frame, `Engine` updates scenes and systems.
5. Fixed updates run physics-sensitive behavior.
6. Render systems draw visible scene layers.

## Managers

`SceneManager` and `BundleManager` register factory functions. Use them when runtime
code needs to load scenes or instantiate prefab-like entity hierarchies by ID or name.

## Scripting

Lua and C++ both drive the same runtime. Lua bindings expose engine classes, object
wrappers, components, math types, actions, I/O helpers, and enums. C++ code includes
`Doriax.h` and registers startup code with `DORIAX_INIT`.