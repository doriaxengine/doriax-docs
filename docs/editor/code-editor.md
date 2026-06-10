---
description: Writing Lua and C++ scripts in the Doriax integrated code editor.
---

# Code Editor

The integrated code editor lets you write and edit Lua and C++ scripts without leaving
the Doriax editor. It provides syntax highlighting, API completion, script creation
dialogs, and a live output panel for compile and export messages.

![Integrated code editor](../assets/screenshots/editor-code.png)

## Supported workflows

| Workflow | Notes |
| --- | --- |
| **Lua scripts** | Fast iteration — script-only changes take effect immediately in play mode without rebuilding |
| **C++ scripts** | Compiled at export/build time for native performance; require a rebuild to take effect |
| **Script templates** | Create new Lua or C++ script files from boilerplate using the **New Script** dialog |
| **API completion** | Engine API suggestions generated from Lua bindings; covers classes, methods, and constants |
| **Build output** | Compiler errors, warnings, and export messages stream into the Output panel |

## Creating a new script

1. Select an entity and click **New Script** at the bottom of the **Properties** window.
2. Choose **Lua Script**, **C++ Subclass**, or **C++ Script Class**.
3. Enter the class/module name and confirm.

The editor generates the files from templates, attaches a `ScriptComponent` entry to
the entity, and opens the new files here in the Code Editor. To link *existing* files
instead, add an empty entry with **Add Script** inside the ScriptComponent and pick the
files in its edit dialog — see
[Creating Scripts](../manual/creating-scripts.md#create-a-script-in-the-editor).

![Script creation dialog](../assets/screenshots/editor-script-create-dialog.png)

## Drag entities into your code

Drag an entity from the **Structure panel** onto a script open in the Code Editor to
create an entity reference property:

- **Lua file** — a typed entry is appended to the `properties` table.
- **C++ header** — a `DPROPERTY` line and pointer member are inserted (with the
  `#include` when the type is another script class). Dropping on a `.cpp` shows a
  reminder to use the header.

The property type comes from the dropped entity (its script class, or wrapper type such
as `Object`/`Mesh`/`Camera`), and the entity is assigned as the property value
automatically. See
[Script Properties](../manual/script-properties.md#insert-entity-references-by-drag-and-drop).

## Script entry point

Scripts subscribe to the engine events they need (`onUpdate`, `onFixedUpdate`,
`onPause`, `onResume`, `onShutdown`, and the input events). Lua scripts register in
`init()`; C++ scripts register in the constructor and unregister in the destructor:

=== "Lua"

    ```lua
    local Player = {}

    function Player:init()
        RegisterEngineEvent(self, "onUpdate")
    end

    function Player:onUpdate()
        -- called every frame
    end

    return Player
    ```

=== "C++"

    ```cpp
    #include "ScriptBase.h"

    class Player : public doriax::ScriptBase {
    public:
        Player(doriax::Scene* scene, doriax::Entity entity);
        ~Player();

        void onUpdate();
    };
    ```

    ```cpp
    Player::Player(Scene* scene, Entity entity) : ScriptBase(scene, entity) {
        REGISTER_ENGINE_EVENT(onUpdate);
    }

    Player::~Player() {
        UNREGISTER_ENGINE_EVENT(onUpdate);
    }
    ```

See [Creating Scripts](../manual/creating-scripts.md) for the full lifecycle and event
system documentation.

## DPROPERTY and script properties

Properties declared with `DPROPERTY` (C++) or in the `properties` table (Lua) appear
as editable fields in the **Properties window** automatically.

![DPROPERTY macro in C++ script](../assets/screenshots/editor-code-spROPERTY.png)

```cpp
DPROPERTY("Speed")
float speed = 5.0f;

DPROPERTY("Jump Force")
float jumpForce = 12.0f;
```

The editor parser reads `DPROPERTY` from C++ headers and populates the Properties
window without requiring a build. See
[Script Properties](../manual/script-properties.md) for syntax and type mapping details.

## Project entry points

A project can have both Lua and C++ startup paths. Set which one is active in project
settings, or keep both and use `NO_CPP_INIT` / `NO_LUA_INIT` to disable one at
compile time.

=== "C++ startup"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Scene scene;

    DORIAX_INIT void init() {
        Engine::setScene(&scene);
    }
    ```

=== "Lua startup"

    ```lua
    scene = Scene()
    Engine.setScene(scene)
    ```

## Practical tips

- Keep startup code small — move gameplay behavior into scripts or systems.
- Use `DPROPERTY` for values that designers should tune; avoid hard-coding magic
  numbers inside script logic.
- Watch the Output panel after every C++ edit or export; it shows the first compiler
  error clearly.
- Lua scripts iterate faster during development — prototype in Lua, port to C++ for
  performance-critical paths.
- Use the built-in [Log](../reference/classes/log.md) API for runtime diagnostics
  rather than relying on `print`.
