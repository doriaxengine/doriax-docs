---
description: SceneManager API reference (C++ and Lua).
---

# SceneManager

**C++ type:** `SceneManager` (static)

## Description

A registry for named scene stacks that lets you switch between scenes at runtime. A *scene stack* consists of one main [Scene](scene.md) plus zero or more layer scenes (see [Engine::addSceneLayer](engine.md#addscenelayer)).

The typical workflow is:

1. **Register** all scenes at startup with the factories that build them. In an exported project this is done for you — the editor registers every scene stack.
2. **Load** a scene by name or ID; the manager calls `Engine::removeAllScenes()` to clear the current main scene and all layers, then invokes the new scene's factory function.

Two operations change what is on screen:

- [`loadScene`](#loadscene) is a full **transition** — it tears down everything and builds a new stack. Use it to move between levels, menus, and game-over screens.
- [`addChildScene`](#addchildscene-removechildscene) / [`removeChildScene`](#addchildscene-removechildscene) **overlay** a scene on top of the running stack without a transition. Use them for pause menus, dialogs, and HUD toggles. See [Switching scenes with SceneManager](../../manual/scenes-and-entities.md#switching-scenes-with-scenemanager) for the broader workflow.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static void | [registerScene](#registerscene) | C++ \| Lua |
| static bool | [loadScene](#loadscene) | C++ \| Lua |
| static bool | [isLoadPending](#isloadpending) | C++ \| Lua (`loadPending`) |
| static bool | [addChildScene](#addchildscene-removechildscene) | C++ \| Lua |
| static bool | [removeChildScene](#addchildscene-removechildscene) | C++ \| Lua |
| static uint32_t | [getSceneId](#getsceneid-getscenename) | C++ \| Lua |
| static std::string | [getSceneName](#getsceneid-getscenename) | C++ \| Lua |
| static std::vector\<std::string\> | [getSceneNames](#getscenenames-getscenecount) | C++ \| Lua |
| static int | [getSceneCount](#getscenenames-getscenecount) | C++ \| Lua (`sceneCount`) |
| static uint32_t | [getCurrentSceneId](#getcurrentsceneid-getcurrentscenename) | C++ \| Lua (`currentSceneId`) |
| static std::string | [getCurrentSceneName](#getcurrentsceneid-getcurrentscenename) | C++ \| Lua (`currentSceneName`) |
| static void | [clearAll](#clearall) | C++ \| Lua |
| static void | [setScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |
| static Scene* | [getScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |
| static void | [removeScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |

## Method details

### registerScene

* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> loadFactory)
* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> loadFactory, const std::vector<uint32_t>& sceneIds)
* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> loadFactory, std::function<void()> addFactory)
* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> loadFactory, std::function<void()> addFactory, const std::vector<uint32_t>& sceneIds)

Registers a named scene stack with the functions that build it. A stack has two of them because coming up *as the world* and coming up *on top of the world* are different jobs.

**`loadFactory`** runs on [`loadScene`](#loadscene). It owns the transition: it calls `Engine::setScene()` for the stack's main scene, `Engine::addSceneLayer()` for its layers, and it is free to destroy the stack it replaces.

**`addFactory`** runs on [`addChildScene`](#addchildscene-removechildscene). It only **creates** the stack's scenes and registers each one with [`setScenePtr`](#setsceneptr-getsceneptr-removesceneptr). It must not call `Engine::setScene()` and must not destroy anything, because the stack it is being layered onto keeps running. It does not add layers either — `addChildScene` does that, in stack order. It must be safe to call repeatedly, because `addChildScene` calls it every time.

A stack registered without an add factory can still be loaded. It can only be added as a child once something else has created its scenes.

The optional `sceneIds` vector lists the scenes that come up **together** with this one — the stack's *active* scenes. It is what `addChildScene` puts on screen, the stack's own scene first so it sits below the layers it owns. A braced list works in C++ (`{1, 2}`), and the stack's own id is added when the list leaves it out.

=== "C++"
    ```cpp
    static Scene* menuScene = nullptr;

    void load_MainMenu() {
        if (!menuScene) {
            menuScene = new Scene();
            SceneManager::setScenePtr(1, menuScene);
            // populate scene...
        }
        Engine::setScene(menuScene);
    }

    void add_MainMenu() {
        if (!menuScene) {
            menuScene = new Scene();
            SceneManager::setScenePtr(1, menuScene);
            // populate scene...
        }
        // no setScene, no teardown, no addSceneLayer
    }

    SceneManager::registerScene(1, "MainMenu", load_MainMenu, add_MainMenu);
    SceneManager::loadScene("MainMenu");
    ```

=== "Lua"
    ```lua
    local menuScene = nil

    local function load_MainMenu()
        if not menuScene then
            menuScene = Scene()
            SceneManager.setScenePtr(1, menuScene)
            -- populate scene...
        end
        Engine.setScene(menuScene)
    end

    local function add_MainMenu()
        if not menuScene then
            menuScene = Scene()
            SceneManager.setScenePtr(1, menuScene)
            -- populate scene...
        end
        -- no setScene, no teardown, no addSceneLayer
    end

    SceneManager.registerScene(1, "MainMenu", load_MainMenu, add_MainMenu)
    SceneManager.loadScene("MainMenu")
    ```

---

### loadScene

* static bool **loadScene**(const std::string& name)
* static bool **loadScene**(uint32_t id)

Loads a registered scene stack by name or ID, performing a full scene transition. Calls `Engine::removeAllScenes()` first — this clears the current main scene **and** every layer — then runs the registered factory to build the new stack. Returns `false` if the name or ID is not found.

Because it clears everything, do not call `loadScene` once per layer. Persistent layers (a HUD, shared lighting) should be **start-active child scenes** of the target scene so they come up in the same call.

Called while a frame is running — from a script callback, a physics contact, a button
press — the transition is **deferred to the start of the next frame**, because the factory
tears down the scenes and scripts that are still executing. The call still returns `true`
when the scene exists; the last request made in a frame wins (a replaced request logs a
warning), [`isLoadPending`](#isloadpending) reports the wait, and `getCurrentSceneId`
only changes once the load is applied. Outside a frame (for example in the `init()` entry
point) the stack is built immediately.

=== "Lua"
    ```lua
    SceneManager.loadScene("Level2")
    SceneManager.loadScene(2)
    ```

=== "C++"
    ```cpp
    SceneManager::loadScene("Level2");
    SceneManager::loadScene(2);
    ```

---

### addChildScene / removeChildScene

* static bool **addChildScene**(uint32_t id)
* static bool **addChildScene**(const std::string& name)
* static bool **removeChildScene**(uint32_t id)
* static bool **removeChildScene**(const std::string& name)

Add or remove a scene stack as layers on top of the running scenes **without** a full transition — ideal for overlaying a UI scene (pause menu, dialog) on top of a game scene.

`addChildScene` runs the stack's **add factory**, then adds its active scenes at the **top** of the layer list, in order, so the overlay draws above everything below it and the stack's own scene stays below the layers it owns.

The scene does **not** have to be loaded first. If its scenes do not exist yet the factory creates them on the spot; if they exist already the factory finds nothing to do and the call is cheap. Either way the factory runs on every call, which is what lets it restore a stack whose scripts were torn down earlier.

Unlike [`loadScene`](#loadscene), this takes effect **immediately**, including when called inside a frame, because nothing is destroyed. The scenes it adds update and draw from that same frame on.

It can also be called from a script's `init` while that script's own stack is still loading — a level that opens its HUD from code, say. The stack it adds is kept when the load finishes, rather than torn down with the scenes the transition replaced.

Returns `false` if the scene is unknown, if it has no add factory and its scenes were never created, or if the factory did not produce the whole stack.

`removeChildScene` removes those layers again, keeping the main scene and any other layers intact. It does **not** destroy the scenes, so a later `addChildScene` brings the same ones back with their state intact. Returns `false` if nothing was removed.

See [Preloaded or built on demand](../../manual/scenes-and-entities.md#preloaded-or-built-on-demand) for choosing between a scene that is built with its parent and one built the first time it is shown.

=== "Lua"
    ```lua
    SceneManager.addChildScene("PauseMenu")     -- show overlay
    SceneManager.removeChildScene("PauseMenu")  -- hide it again
    ```

=== "C++"
    ```cpp
    SceneManager::addChildScene("PauseMenu");
    SceneManager::removeChildScene("PauseMenu");
    ```

---

### getSceneId / getSceneName

* static uint32_t **getSceneId**(const std::string& name)
* static std::string **getSceneName**(uint32_t id)

Look up a scene's numeric ID by name, or its name by ID. Returns `0` / `""` if not found.

---

### getSceneNames / getSceneCount

* static std::vector\<std::string\> **getSceneNames**()
* static int **getSceneCount**()

Returns all registered scene names, or the total number of registered scenes.

In Lua the count is the read-only property `SceneManager.sceneCount`, not a call.

---

### isLoadPending

* static bool **isLoadPending**()

`true` between a `loadScene` call made during a frame and the next frame, which applies
it. Lua reads it as the `SceneManager.loadPending` property.

---

### getCurrentSceneId / getCurrentSceneName

* static uint32_t **getCurrentSceneId**()
* static std::string **getCurrentSceneName**()

Returns the ID or name of the most recently loaded scene.

=== "Lua"
    ```lua
    -- read-only properties, not calls
    local id = SceneManager.currentSceneId
    local name = SceneManager.currentSceneName
    ```

=== "C++"
    ```cpp
    uint32_t id = SceneManager::getCurrentSceneId();
    std::string name = SceneManager::getCurrentSceneName();
    ```

---

### clearAll

* static void **clearAll**()

Unregisters all scenes. Used by the editor when resetting state. Does not destroy scene objects.

---

### setScenePtr / getScenePtr / removeScenePtr

* static void **setScenePtr**(uint32_t id, Scene* scene)
* static Scene* **getScenePtr**(uint32_t id)
* static void **removeScenePtr**(uint32_t id)

Associates a live `Scene*` pointer with a registered scene ID. Used when one scene needs to reference entities in another scene (cross-scene entity resolution), and by an add factory to hand [`addChildScene`](#addchildscene-removechildscene) the scenes it created. `getScenePtr` returns `nullptr` (`nil` in Lua) for an ID with no scene.

=== "Lua"
    ```lua
    SceneManager.setScenePtr(2, hudScene)
    local hud = SceneManager.getScenePtr(2)
    SceneManager.removeScenePtr(2)
    ```

=== "C++"
    ```cpp
    SceneManager::setScenePtr(2, &hudScene);
    Scene* hud = SceneManager::getScenePtr(2);
    SceneManager::removeScenePtr(2);
    ```
