---
description: ScriptBase API reference (C++ and Lua).
---

# ScriptBase

**C++ type:** `ScriptBase`

## Description

The base class for all C++ gameplay scripts attached to entities. To create a component script in C++, inherit from `ScriptBase` and override the virtual update/event methods provided by the scripting system.

In Lua, scripts are plain Lua tables with lifecycle functions (`init`, `update`, etc.) — the `ScriptBase` class itself is not exposed directly to Lua. See [Creating Scripts](../../manual/creating-scripts.md) for the full guide.

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
            : ScriptBase(scene, entity) {}

        void update(double deltaTime) {
            Object obj(scene, entity);
            if (Input::isKeyPressed(Key::KEY_W)) {
                obj.move(0, 0, -5.0f * deltaTime);
            }
        }
    };
    ```

See [Creating Scripts](../../manual/creating-scripts.md) for instructions on attaching scripts to entities in the editor.
