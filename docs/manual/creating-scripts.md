---
description: Create Lua and C++ scripts in Doriax, attach them to entities, and understand script lifecycle.
---

# Creating Scripts

Scripts attach behavior to entities through `ScriptComponent`. A script does not own
the entity. It receives the entity ID and scene pointer, then reads or changes the
components attached to that entity.

This page covers the full workflow from the Doriax editor through runtime initialization,
export, and cleanup.

## Mental model

```
Entity
  └── ScriptComponent
        └── scripts[]: ScriptEntry
              ├── type        (SUBCLASS | SCRIPT_CLASS | SCRIPT_LUA)
              ├── path        (.lua or .cpp)
              ├── headerPath  (.h for C++; empty for Lua)
              ├── className   (C++ class or Lua module name)
              ├── enabled
              ├── properties[] (inspector values)
              └── instance    (C++ pointer or Lua registry ref)
```

One `ScriptComponent` holds **multiple** script entries. Each entry is independent and
can be enabled or disabled separately.

## Create a script in the editor

1. Select an entity in the **Structure** panel.
2. In the **Properties**, add `ScriptComponent` (or expand it if already present).
3. Click **Add Script** to open the script creation dialog.
4. Choose **Lua Script**, **C++ Subclass**, or **C++ Script Class**.
5. Enter a class/module name and confirm. The editor writes template files into your
   project scripts folder.
6. Enable the script entry and tune properties in the Properties window.
7. Save the scene and press **Play** to test.

The script creation dialog (`ScriptCreateDialog`) generates starter code with example
properties and event registration. The integrated **Code Editor** opens the new files
for editing.

![Script creation dialog](../assets/screenshots/editor-script-create-dialog.png)

## Script types

| Type | Enum value | Generated base | Best use |
| --- | --- | --- | --- |
| Lua Script | `SCRIPT_LUA` | Lua table module | Fast iteration, UI glue, triggers, controllers |
| C++ Subclass | `SUBCLASS` | `Object`, `Mesh`, `Camera`, `Light`, or `EntityHandle` | Behavior that calls wrapper methods like `getPosition()` |
| C++ Script Class | `SCRIPT_CLASS` | `ScriptBase` | Logic that accesses scene/entity explicitly without a wrapper |

### How the editor picks a C++ subclass base

The editor inspects the selected entity's components:

| Entity has | Default base class |
| --- | --- |
| `CameraComponent` | `Camera` |
| `MeshComponent` / `ModelComponent` | `Mesh` |
| `LightComponent` | `Light` |
| `Transform` (and none of the above) | `Object` |
| None of the above | `EntityHandle` |

### When to use each type

- **Lua** — Prototyping, gameplay that changes often, designers tuning values in the
  Properties, UI event handlers.
- **C++ Subclass** — Movement, animation control, or physics on entities that already
  have mesh/camera/light wrappers. You get `setPosition()`, `getBody2D()`, etc. directly.
- **C++ ScriptBase** — Managers, score trackers, spawners, or logic that touches many
  entities through `getScene()` and `getEntity()`.

## Lua script format

A Lua script file **must return a table**. The table is the script prototype; Doriax
creates a per-entity instance at runtime.

### Minimal template

```lua
local PlayerController = {
    properties = {
        { name = "speed", displayName = "Speed", type = "float", default = 5.0 }
    }
}

function PlayerController:init()
    RegisterEngineEvent(self, "onUpdate")
end

function PlayerController:onUpdate()
    local object = Object(self.scene, self.entity)
    if Input.isKeyPressed(S_KEY_RIGHT) then
        object.position = object.position + Vector3(self.speed * Engine.deltatime, 0, 0)
    end
end

return PlayerController
```

### Required conventions

| Rule | Detail |
| --- | --- |
| Return a table | `return MyScript` at end of file |
| Properties table | Optional `properties = { ... }` for Properties fields |
| `init()` | Optional lifecycle hook called after properties are injected |
| Event methods | Name methods to match events (`onUpdate`, `onClick`, etc.) and register in `init()` |
| `self.scene` | Injected `Scene*` — use for systems and entity wrappers |
| `self.entity` | Injected entity ID |

### Module loading

`require("myscript")` resolves through the virtual filesystem:

1. `lua://lua/myscript.lua`
2. `lua://myscript.lua`

`ScriptComponent` entries store a relative path loaded as `lua://` + path.

## Lua runtime lifecycle

When a scene loads, `LuaBinding::initializeLuaScripts(scene)` runs three passes:

### Pass 1 — Create instances

For each enabled `SCRIPT_LUA` entry:

1. Load and execute the Lua module with `require`.
2. Verify the return value is a table.
3. Create an instance table with the module table as `__index`.
4. Set `__name` to the script class name.
5. Inject `scene` and `entity`.
6. Copy Properties property values onto the instance (`self.speed = 5.0`, etc.).
7. Store a Lua registry reference in `ScriptEntry.instance`.

### Pass 2 — Resolve entity references

Pointer/entity properties (`EntityReference`) are resolved:

- If the target entity has a matching enabled Lua script, the reference becomes that
  Lua script instance.
- Otherwise Doriax pushes a typed wrapper (`Object`, `Mesh`, `Camera`, `EntityHandle`,
  etc.) based on `ptrTypeName`.

### Pass 3 — Call `init()`

If the instance has an `init` function, Doriax calls `self:init()`.

Register events inside `init()` so `self` and resolved references are ready.

### Cleanup

`LuaBinding::cleanupLuaScripts(scene)` runs on scene unload:

1. Remove all `FunctionSubscribe` callbacks whose tag contains the script instance
   address (`Engine::removeSubscriptionsByTag` and `Scene::removeSubscriptionsByTag`).
2. `luaL_unref` the script instance.
3. Clear `ScriptEntry.instance`.

## C++ subclass script

A subclass script derives from an object wrapper and calls wrapper methods directly.

### Header (`PlayerMover.h`)

```cpp
#pragma once

#include "Object.h"
#include "ScriptProperty.h"

class PlayerMover : public doriax::Object {
public:
    DPROPERTY("Speed")
    float speed = 5.0f;

    PlayerMover(doriax::Scene* scene, doriax::Entity entity);
    ~PlayerMover();

    void onUpdate();
};
```

### Implementation (`PlayerMover.cpp`)

```cpp
#include "PlayerMover.h"

using namespace doriax;

PlayerMover::PlayerMover(Scene* scene, Entity entity) : Object(scene, entity) {
    REGISTER_ENGINE_EVENT(onUpdate);
}

PlayerMover::~PlayerMover() {
    UNREGISTER_ENGINE_EVENT(onUpdate);
}

void PlayerMover::onUpdate() {
    Vector3 position = getPosition();
    if (Input::isKeyPressed(S_KEY_RIGHT)) {
        setPosition(position + Vector3(speed * Engine::getDeltatime(), 0, 0));
    }
}
```

The editor's **Factory** generates instantiation code when you export or build the
project. Subclass scripts are compiled into the game binary.

## C++ ScriptBase script

Use `ScriptBase` when you want a behavior class without implying any object wrapper.

```cpp
#pragma once

#include "ScriptBase.h"
#include "ScriptProperty.h"

class ScoreTracker : public doriax::ScriptBase {
public:
    DPROPERTY("Score")
    int score = 0;

    ScoreTracker(doriax::Scene* scene, doriax::Entity entity);
    ~ScoreTracker();

    void onUpdate();
};
```

```cpp
#include "ScoreTracker.h"

ScoreTracker::ScoreTracker(Scene* scene, Entity entity) : ScriptBase(scene, entity) {
    REGISTER_ENGINE_EVENT(onUpdate);
}

ScoreTracker::~ScoreTracker() {
    UNREGISTER_ENGINE_EVENT(onUpdate);
}

void ScoreTracker::onUpdate() {
    // getScene(), getEntity() available from ScriptBase
}
```

## Property sync at runtime

Properties values are stored in `ScriptEntry.properties`. At play/export:

- **C++** — `ScriptProperty::syncToMember()` writes values into the `memberPtr` captured
  during editor parsing.
- **Lua** — values are set as fields on the instance table before `init()`.

See [Script Properties](script-properties.md) for the full type mapping.

## Editor serialization and export

| Step | What happens |
| --- | --- |
| Scene save | `ScriptComponent` entries serialize to YAML with paths, types, and property values |
| Property parse | C++: `ScriptParser` reads `DPROPERTY` from headers. Lua: editor loads `properties` table |
| Play mode | Editor calls `initializeLuaScripts` on scene load |
| Export | `Generator` emits C++ that registers scenes, creates C++ script instances, and calls `initializeLuaScripts` |

## Common patterns

### UI button handler (Lua)

```lua
local MenuButton = {}

function MenuButton:init()
    local ui = self.scene:findComponent(UIComponent, self.entity)
    RegisterEvent(self, ui.onClick, "onClick")
end

function MenuButton:onClick(x, y)
    print("clicked at", x, y)
end

return MenuButton
```

### Physics contact (C++)

```cpp
void Trap::onBeginContact(Body2D bodyA, int shapeA, Body2D bodyB, int shapeB) {
    // registered with REGISTER_EVENT(physics->beginContact2D, onBeginContact)
}
```

### Referencing another entity (Lua)

```lua
local Follower = {
    properties = {
        { name = "target", displayName = "Target", type = "entity", default = nil }
    }
}

function Follower:onUpdate()
    if self.target then
        local obj = Object(self.scene, self.entity)
        obj.position = self.target.position
    end
end

return Follower
```

## Troubleshooting

| Problem | Likely cause |
| --- | --- |
| `init()` never runs | Script entry disabled, wrong type, or Lua module does not return a table |
| Event handler not called | Forgot `RegisterEngineEvent` / `REGISTER_ENGINE_EVENT` in constructor or `init()` |
| Property not in Properties | `DPROPERTY` not immediately above member; unsupported type; header path wrong |
| Entity reference is nil | Target entity missing, wrong scene, or referenced script disabled |
| Duplicate event callbacks | Same tag registered twice; use `UNREGISTER_*` in destructor |

## Next steps

- [Events](events.md) — full event list, macros, and Lua registration
- [Script Properties](script-properties.md) — `DPROPERTY` and Lua `properties` tables
- [Engine](../reference/classes/engine.md) — runtime API
- [API Index](../reference/index.md) — all classes
