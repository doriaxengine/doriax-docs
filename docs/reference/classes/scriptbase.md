---
description: ScriptBase API reference (C++ and Lua).
---

# ScriptBase

**C++ type:** `ScriptBase`

## Description

The base class for all C++ gameplay scripts attached to entities. To create a component script in C++, inherit from `ScriptBase` and register engine events with `REGISTER_ENGINE_EVENT` (there are no virtual `update` overrides).

In Lua, scripts are plain Lua tables with lifecycle functions (`init`, `onUpdate`, etc.) — the `ScriptBase` class itself is not exposed directly to Lua. See [Creating Scripts](../../manual/creating-scripts.md) for the full guide.

### Properties

| Type | Name | Langs |
| --- | --- | --- |
| Scene* | [scene](#scene-entity) | C++ |
| Entity | [entity](#scene-entity) | C++ |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| Scene* | [getScene](#scene-entity) | C++ |
| Entity | [getEntity](#scene-entity) | C++ |

## Property details

### scene / entity

* Scene* **getScene**() const
* Entity **getEntity**() const

The scene this script belongs to, and the entity it is attached to. Use these to access [Object](object.md) transforms, add/remove components, or query the ECS.

=== "C++"
    ```cpp
    class PlayerController : public ScriptBase {
    public:
        PlayerController(Scene* scene, Entity entity)
            : ScriptBase(scene, entity) {
            REGISTER_ENGINE_EVENT(onUpdate);
        }

        ~PlayerController() {
            UNREGISTER_ENGINE_EVENT(onUpdate);
        }

        void onUpdate() {
            Object obj(getScene(), getEntity());
            if (Input::isKeyPressed(D_KEY_W)) {
                obj.setPosition(obj.getPosition() + Vector3(0, 0, -5.0f * Engine::getDeltatime()));
            }
        }
    };
    ```

See [Creating Scripts](../../manual/creating-scripts.md) for instructions on attaching scripts to entities in the editor.
