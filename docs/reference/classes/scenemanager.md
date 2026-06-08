---
description: SceneManager API reference (C++ and Lua).
---

# SceneManager

**C++ type:** `SceneManager` (static)

## Description

A registry for named scene stacks that lets you switch between scenes at runtime. A *scene stack* consists of one main [Scene](scene.md) plus zero or more layer scenes (see [Engine::addSceneLayer](engine.md#addscenelayer)).

The typical workflow is:

1. **Register** all scenes at startup, providing a factory function that creates and wires up the scene objects.
2. **Load** a scene by name or ID; the manager calls `Engine::removeAllSceneLayers()`, destroys the previous scene, and invokes the new scene's factory function.

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

Loads a registered scene stack by name or ID. Calls `Engine::removeAllSceneLayers()` first to clean up the previous scene. Returns `false` if the name or ID is not found.

---

### addChildScene / removeChildScene

* static bool **addChildScene**(uint32_t id)
* static bool **addChildScene**(const std::string& name)
* static bool **removeChildScene**(uint32_t id)
* static bool **removeChildScene**(const std::string& name)

Dynamically add or remove a child scene stack from the active scene layer list without triggering a full scene transition. Useful for overlaying UI scenes on top of a game scene.

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
