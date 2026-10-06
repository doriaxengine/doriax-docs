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
| static bool | [setLoadingScene](#setloadingscene-getloadingsceneid) | C++ \| Lua |
| static uint32_t | [getLoadingSceneId](#setloadingscene-getloadingsceneid) | C++ \| Lua (`loadingSceneId`) |
| static void | [setLoadingDelay](#setloadingdelay-getloadingdelay) | C++ \| Lua (`loadingDelay`) |
| static float | [getLoadingDelay](#setloadingdelay-getloadingdelay) | C++ \| Lua (`loadingDelay`) |
| static void | [setLoadingTimeout](#setloadingtimeout-getloadingtimeout) | C++ \| Lua (`loadingTimeout`) |
| static float | [getLoadingTimeout](#setloadingtimeout-getloadingtimeout) | C++ \| Lua (`loadingTimeout`) |
| static bool | [isLoading](#isloading-getloadingprogress) | C++ \| Lua (`loading`) |
| static float | [getLoadingProgress](#isloading-getloadingprogress) | C++ \| Lua (`loadingProgress`) |
| static bool | [holdLoading](#holdloading-releaseloading) | C++ \| Lua |
| static void | [releaseLoading](#holdloading-releaseloading) | C++ \| Lua |
| static bool | [isCoveredByLoading](#iscoveredbyloading) | C++ \| Lua |
| static bool | [preloadScene](#preloadscene-getpreloadprogress-cancelpreload) | C++ \| Lua |
| static float | [getPreloadProgress](#preloadscene-getpreloadprogress-cancelpreload) | C++ \| Lua |
| static void | [cancelPreload](#preloadscene-getpreloadprogress-cancelpreload) | C++ \| Lua |
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
* static void **registerScene**(uint32_t id, const std::string& name, std::function<void()> loadFactory, std::function<void()> addFactory, const std::vector<uint32_t>& sceneIds, std::function\<SceneResources()\> resources = nullptr)

Registers a named scene stack with the functions that build it. A stack has two of them because coming up *as the world* and coming up *on top of the world* are different jobs.

**`loadFactory`** runs on [`loadScene`](#loadscene). It owns the transition: it calls `Engine::setScene()` for the stack's main scene, `Engine::addSceneLayer()` for its layers, and it is free to destroy the stack it replaces.

**`addFactory`** runs on [`addChildScene`](#addchildscene-removechildscene). It only **creates** the stack's scenes and registers each one with [`setScenePtr`](#setsceneptr-getsceneptr-removesceneptr). It must not call `Engine::setScene()` and must not destroy anything, because the stack it is being layered onto keeps running. It does not add layers either — `addChildScene` does that, in stack order. It must be safe to call repeatedly, because `addChildScene` calls it every time.

A stack registered without an add factory can still be loaded. It can only be added as a child once something else has created its scenes.

The optional `sceneIds` vector lists the scenes that come up **together** with this one — the stack's *active* scenes. It is what `addChildScene` puts on screen, the stack's own scene first so it sits below the layers it owns. A braced list works in C++ (`{1, 2}`), and the stack's own id is added when the list leaves it out.

The optional **`resources`** function lists the files the scene loads — its `textures`, `sounds` and `models` — for [`preloadScene`](#preloadscene-getpreloadprogress-cancelpreload). Exported games and the editor's Play pass it for every scene.

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

Called while a scene is running — from a script callback, a physics contact or an input
event — the transition is **deferred to the start of the next frame**, because the factory
tears down the scenes and scripts that are still executing. The replaced scenes are
deleted, which stops their sounds; a [loading delay](#setloadingdelay-getloadingdelay)
lets a click sound finish first. The call returns `true` when the scene exists; the last
request wins (a replaced request logs a warning), [`isLoadPending`](#isloadpending)
reports the wait, and `getCurrentSceneId` only changes once the load is applied. Only
the first load, with nothing on screen yet (the `init()` entry point), builds the stack
immediately. The editor's Play also builds the stack again from the scene files, so a level
loaded a second time (a retry) starts over as it does in an exported game.

With a [loading scene](#setloadingscene-getloadingsceneid) set, the switch also waits for
it to be on screen and for the [loading delay](#setloadingdelay-getloadingdelay).

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

`true` between a deferred `loadScene` call and the frame that replaces the old stack,
loading delay included. Lua reads it as the `SceneManager.loadPending` property.

---

### setLoadingScene / getLoadingSceneId

* static bool **setLoadingScene**(const std::string& name)
* static bool **setLoadingScene**(uint32_t id)
* static uint32_t **getLoadingSceneId**()

Sets a registered scene stack as the **loading screen** that [`loadScene`](#loadscene)
shows over every transition. An empty name or `0` turns it off. Returns `false` if the
scene is unknown. Exported games and the editor's Play set it from
[Project Settings → General → Loading](../../editor/project-settings.md#loading), so most
projects never call it.

A transition then runs in three steps:

1. The loading scene is added **on top** of the running scenes, which keep running
   underneath it. While it is shown, the scenes below it get no UI input: their buttons
   cannot be pressed and their text fields get no keys. Pointer releases still reach them,
   so nothing stays pressed. Engine input events such as `Engine::onKeyDown` still fire.
2. Once it is drawn with its resources loaded and the
   [loading delay](#setloadingdelay-getloadingdelay) has passed, the old stack is replaced.
   The game freezes while the new scenes are built, with the loading scene on screen.
3. When every mesh, UI element, sky and sound of the new stack is loaded,
   [`Engine::onSceneLoaded`](engine.md#onsceneloaded) fires and the loading scene is
   removed, unless a [hold](#holdloading-releaseloading) keeps it up to fade out.

A load that makes no progress for the [loading timeout](#setloadingtimeout-getloadingtimeout)
stops waiting.

It is kept alive between transitions, so its scripts keep their state. Their `onUpdate`
also runs while it is off screen, so check [`isLoading`](#isloading-getloadingprogress)
first. It is not shown for a transition to a stack that includes it.

=== "Lua"
    ```lua
    SceneManager.setLoadingScene("Loading")
    SceneManager.loadingDelay = 0.3
    SceneManager.loadScene("Level2")   -- Loading appears first, then Level2 behind it
    ```

=== "C++"
    ```cpp
    SceneManager::setLoadingScene("Loading");
    SceneManager::setLoadingDelay(0.3f);
    SceneManager::loadScene("Level2");
    ```

---

### setLoadingDelay / getLoadingDelay

* static void **setLoadingDelay**(float seconds)
* static float **getLoadingDelay**()

Seconds the [loading scene](#setloadingscene-getloadingsceneid) covers the old scenes
before they are replaced. Default `0`. The old scenes keep running below it until then,
which leaves time for a fade in (a script on the loading scene can raise its alpha from
`0` to `1` over the delay) and for their last sounds, such as a button click, which stop
when the scenes are deleted.

---

### setLoadingTimeout / getLoadingTimeout

* static void **setLoadingTimeout**(float seconds)
* static float **getLoadingTimeout**()

Seconds a load waits without progress before it gives up. Default `5`. It applies to the
loading scene's own resources before the switch, and to the new stack after it, which logs
a warning naming what did not load. The clock restarts every time another resource
finishes, so a slow load that keeps moving is never cut short.

---

### isLoading / getLoadingProgress

* static bool **isLoading**()
* static float **getLoadingProgress**()

`isLoading` is `true` from a [`loadScene`](#loadscene) call until the new stack has loaded
its resources and every [hold](#holdloading-releaseloading) is released, with or without a
loading scene. It is already `true` while the new stack's scripts are constructed, and for
the start scene too. To start gameplay once the level is ready, handle
[`Engine::onSceneLoaded`](engine.md#onsceneloaded) instead of polling it.

`getLoadingProgress` is the share of the new stack's meshes, UI elements, skies and sounds
that finished loading: `0` until the old stack is replaced, `1` once it has loaded (also
after a timeout, and while holds keep the load open). A sound whose file cannot be loaded
counts as done. The value is updated once per frame and never goes back within a load, even
when the new scenes create more to load. It only moves across several frames with
[async loading](engine.md#asyncloading); otherwise it jumps from `0` to `1`. For a smooth
bar, ease the drawn width toward it.

=== "Lua"
    ```lua
    function LoadingScreen:onUpdate()
        if not SceneManager.loading then return end
        self.bar.width = 360 * SceneManager.loadingProgress
    end
    ```

=== "C++"
    ```cpp
    void LoadingScreen::onUpdate() {
        if (!SceneManager::isLoading()) return;
        barFill->setWidth((unsigned int)(360 * SceneManager::getLoadingProgress()));
    }
    ```

---

### holdLoading / releaseLoading

* static bool **holdLoading**()
* static void **releaseLoading**()

`holdLoading` keeps the current load open after the new stack has loaded: the loading
scene stays on screen and [`isLoading`](#isloading-getloadingprogress) stays `true` until
every hold is released. Returns `false`, and holds nothing, when no load is running.
Each successful `holdLoading` needs one `releaseLoading`.

The usual use is a fade out: a script on the loading scene holds the load when
[`Engine::onSceneLoaded`](engine.md#onsceneloaded) fires, lowers its alpha, then releases
it. The new scene's scripts have already started by then, so the level is ready behind the
fade. A hold has no timeout, so release it in the script's destructor too.

=== "Lua"
    ```lua
    function LoadingScreen:init()
        RegisterEngineEvent(self, "onUpdate")
        RegisterEngineEvent(self, "onSceneLoaded")
    end

    function LoadingScreen:onSceneLoaded()
        -- only when this loading scene is on screen
        if Engine.isSceneRunning(self.scene) and SceneManager.holdLoading() then
            self.fading = 0
        end
    end

    function LoadingScreen:onUpdate()
        if not self.fading then return end
        self.fading = self.fading + Engine.deltatime
        self.backdrop.alpha = math.max(0, 1 - self.fading / 0.3)
        if self.fading >= 0.3 then
            self.fading = nil
            SceneManager.releaseLoading()
        end
    end
    ```

=== "C++"
    ```cpp
    void LoadingScreen::onSceneLoaded() {
        // only when this loading scene is on screen
        if (Engine::isSceneRunning(scene) && SceneManager::holdLoading()) {
            holding = true;
            fadeTimer = 0.0f;
        }
    }

    void LoadingScreen::onUpdate() {
        if (!holding) return;
        fadeTimer += Engine::getDeltatime();
        backdrop->setAlpha(std::max(0.0f, 1.0f - fadeTimer / 0.3f));
        if (fadeTimer >= 0.3f) {
            holding = false;
            SceneManager::releaseLoading();
        }
    }
    ```

---

### isCoveredByLoading

* static bool **isCoveredByLoading**(Scene* scene)

`true` for a running scene below the shown [loading scene](#setloadingscene-getloadingsceneid).
Such a scene gets no UI input, but its scripts still receive engine input events, so a
script can check this to ignore keys while its scene is covered.

=== "Lua"
    ```lua
    function Menu:onKeyDown(key)
        if SceneManager.isCoveredByLoading(self.scene) then return end
        -- menu keys
    end
    ```

=== "C++"
    ```cpp
    void Menu::onKeyDown(int key, bool repeat, int mods) {
        if (SceneManager::isCoveredByLoading(scene)) return;
        // menu keys
    }
    ```

---

### preloadScene / getPreloadProgress / cancelPreload

* static bool **preloadScene**(const std::string& name)
* static bool **preloadScene**(uint32_t id)
* static float **getPreloadProgress**(const std::string& name)
* static float **getPreloadProgress**(uint32_t id)
* static void **cancelPreload**(const std::string& name)
* static void **cancelPreload**(uint32_t id)

`preloadScene` loads the textures, sounds and models of a scene stack in the background
while the current scene keeps running, so a later [`loadScene`](#loadscene) finds them
ready and only has to build the scene. Call it early, for example when the player gets
close to the exit door. It returns `false` for an unknown scene.

The files are held until that scene has loaded, or until `cancelPreload`, which frees the
ones no running scene uses. Scenes of the stack that are already running, such as a shared
HUD, are skipped. Calling `loadScene` before the preload finishes is fine: files still
loading are not loaded twice. `getPreloadProgress` goes from `0` to `1` once the request
starts at the end of the frame, and is `0` for a scene that was never preloaded.

Preloading needs [async loading](engine.md#asyncloading) to stay smooth. Without it, one
file loads per frame on the main thread and models are skipped. Preloading only loads
files: building the scene's entities still happens in `loadScene`. In the editor's Play, a
scene that is not open is read from its file first, which takes a moment.

=== "Lua"
    ```lua
    function ExitDoor:onPlayerNear()
        SceneManager.preloadScene("Level2")
    end

    function ExitDoor:onEnter()
        SceneManager.loadScene("Level2")   -- its files are ready
    end
    ```

=== "C++"
    ```cpp
    void ExitDoor::onPlayerNear() {
        SceneManager::preloadScene("Level2");
    }

    void ExitDoor::onEnter() {
        SceneManager::loadScene("Level2");   // its files are ready
    }
    ```

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
