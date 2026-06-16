---
description: SceneManager API reference (C++ and Lua).
---

# SceneManager

**C++ type:** `SceneManager` (static)

## Description

A registry for named scene stacks that lets you switch between scenes at runtime. A *scene stack* consists of one main [Scene](scene.md) plus zero or more layer scenes (see [Engine::addSceneLayer](engine.md#addscenelayer)).

The typical workflow is:

1. **Register** all scenes at startup, providing a factory function that creates and wires up the scene objects. In an exported project this is done for you — the editor registers every scene stack.
2. **Load** a scene by name or ID; the manager calls `Engine::removeAllScenes()` to clear the current main scene and all layers, then invokes the new scene's factory function.

Two operations change what is on screen:

- [`loadScene`](#loadscene) is a full **transition** — it tears down everything and builds a new stack. Use it to move between levels, menus, and game-over screens.
- [`addChildScene`](#addchildscene-removechildscene) / [`removeChildScene`](#addchildscene-removechildscene) **overlay** a scene on top of the running stack without a transition. Use them for pause menus, dialogs, and HUD toggles. See [Switching scenes with SceneManager](../../manual/scenes-and-entities.md#switching-scenes-with-scenemanager) for the broader workflow.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static void | [registerScene](#registerscene) | C++ \| Lua |
| static bool | [loadScene](#loadscene) | C++ \| Lua |
| static bool | [addChildScene](#addchildscene-removechildscene) | C++ \| Lua |
| static bool | [removeChildScene](#addchildscene-removechildscene) | C++ \| Lua |
| static uint32_t | [getSceneId](#getsceneid-getscenename) | C++ \| Lua |
| static std::string | [getSceneName](#getsceneid-getscenename) | C++ \| Lua |
| static std::vector\<std::string\> | [getSceneNames](#getscenenames-getscenecount) | C++ \| Lua |
| static int | [getSceneCount](#getscenenames-getscenecount) | C++ \| Lua |
| static uint32_t | [getCurrentSceneId](#getcurrentsceneid-getcurrentscenename) | C++ \| Lua |
| static std::string | [getCurrentSceneName](#getcurrentsceneid-getcurrentscenename) | C++ \| Lua |
| static void | [clearAll](#clearall) | C++ \| Lua |
| static void | [setScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |
| static Scene* | [getScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |
| static void | [removeScenePtr](#setsceneptr-getsceneptr-removesceneptr) | C++ \| Lua |

## Method details

### registerScene

* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> factory)
* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> factory, const std::vector<uint32_t>& sceneIds)

Registers a named scene stack. The `factory` function is invoked when the scene is loaded — it should call `Engine::setScene()` and optionally `Engine::addSceneLayer()` to build the scene hierarchy.

The optional `sceneIds` vector lists child scene IDs that should also be loaded as layers alongside this scene.

=== "C++"
    ```cpp
    SceneManager::registerScene(1, "MainMenu", [](){
        static Scene menuScene;
        Engine::setScene(&menuScene);
        // populate scene...
    });

    SceneManager::registerScene(2, "Level1", [](){
        static Scene gameScene;
        static Scene hud;
        Engine::setScene(&gameScene);
        Engine::addSceneLayer(&hud);
    });

    SceneManager::loadScene("MainMenu");
    ```

=== "Lua"
    ```lua
    SceneManager.loadScene("MainMenu")
    ```

---

### loadScene

* static bool **loadScene**(const std::string& name)
* static bool **loadScene**(uint32_t id)

Loads a registered scene stack by name or ID, performing a full scene transition. Calls `Engine::removeAllScenes()` first — this clears the current main scene **and** every layer — then runs the registered factory to build the new stack. Returns `false` if the name or ID is not found.

Because it clears everything, do not call `loadScene` once per layer. Persistent layers (a HUD, shared lighting) should be **start-active child scenes** of the target scene so they come up in the same call.

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

`addChildScene` adds the scene's start-active stack at the **top** of the layer list, so the overlay draws above everything below it. The target scene must already be loaded (its `Scene*` must exist) — in the editor model this is satisfied by a child scene marked **Start active → Off**, which is built with its parent but not shown until you add it. Returns `false` if the scene is unknown or not yet loaded.

`removeChildScene` removes those layers again, keeping the main scene and any other layers intact. Returns `false` if nothing was removed.

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

---

### getCurrentSceneId / getCurrentSceneName

* static uint32_t **getCurrentSceneId**()
* static std::string **getCurrentSceneName**()

Returns the ID or name of the most recently loaded scene.

---

### clearAll

* static void **clearAll**()

Unregisters all scenes. Used by the editor when resetting state. Does not destroy scene objects.

---

### setScenePtr / getScenePtr / removeScenePtr

* static void **setScenePtr**(uint32_t id, Scene* scene)
* static Scene* **getScenePtr**(uint32_t id)
* static void **removeScenePtr**(uint32_t id)

Associates a live `Scene*` pointer with a registered scene ID. Used when one scene needs to reference entities in another scene (cross-scene entity resolution).
