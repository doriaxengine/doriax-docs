---
description: Async loading, thread pool, queued work, and web threading caveats in Doriax.
---

# Threading & Async Loading

Doriax includes thread utilities and async loading support for resource-heavy work such
as loading large models, generating terrain, or pre-warming audio pools in the
background. Threading support depends on the target platform and build options.

## Why async loading?

Synchronous loading freezes the game loop for the duration of the load. For large
assets (multi-megabyte models, terrain heightmaps, audio files), this produces
noticeable hitches. Async loading moves the heavy work to a worker thread while the
main thread continues rendering a loading screen or animating a progress indicator.

## Automatic async resource loading

The simplest way to use threading is to enable **async loading** and let the engine
handle the rest. When enabled, the resource pools (textures, models, sounds, shaders)
load data on a worker thread pool automatically:

=== "Lua"

    ```lua
    Engine.asyncLoading = true   -- property in Lua
    Engine.setMaxResourceLoadingThreads(4)
    ```

=== "C++"

    ```cpp
    Engine::setAsyncLoading(true);
    Engine::setMaxResourceLoadingThreads(4);
    ```

While resources load, the entity is created immediately and the resource appears when
its data is ready. Query `Engine.getQueuedResourceCount()` to see how many resources
are still pending.

## Async thread scope (manual background work, C++)

For your own background work, bracket it with `Engine::AsyncThreadScope` (an RAII
helper around `Engine::startAsyncThread()` / `Engine::endAsyncThread()`). While inside
an async scope, GPU resource creation is **deferred to a commit queue** instead of
touching the graphics API from the wrong thread. When the outermost scope ends, the
queue is flushed automatically (you can also flush manually with
`Engine::commitThreadQueue()` from the main thread):

=== "C++"

    ```cpp
    #include "Engine.h"

    void loadLevelInBackground() {
        Engine::AsyncThreadScope asyncScope;

        // Heavy work on the worker thread. Engine objects created here defer
        // their GPU-side resources to the commit queue.
        model.loadGLTF("models/level.gltf");

    } // scope ends → queued GPU work is committed
    ```

Use `Engine::isAsyncThread()` to check whether the current code runs inside an async
scope.

## Thread pool

`ThreadPoolManager` is the worker pool behind async resource loading. In C++ you can
also dispatch your own tasks to it. `enqueue` is an instance method — get the singleton
first:

=== "C++"

    ```cpp
    ThreadPoolManager::getInstance().enqueue([]() {
        // parse data, decompress files, run a simulation step, etc.
    });
    ```

The pool is initialized on demand with one thread per hardware core by default;
`Engine::setMaxResourceLoadingThreads(n)` re-initializes it with a specific worker
count. The pool is shared across the engine; avoid blocking workers with long
synchronous operations. (In Lua only `initialize`, `shutdown`, and `getQueueSize` are
exposed — task dispatch is C++-only.)

## Tracking loading progress

`ResourceProgress` is a static tracker that reports per-resource and overall build
progress while async loads are running. Read the overall progress to drive a loading
bar:

=== "Lua"

    ```lua
    function LoadingScreen:onUpdate()
        if ResourceProgress.hasActiveBuilds() then
            local overall = ResourceProgress.getOverallProgress()
            progressBar.value = overall.totalProgress * 100
            statusText.text = overall.currentBuildName
        end
    end
    ```

=== "C++"

    ```cpp
    if (ResourceProgress::hasActiveBuilds()) {
        OverallBuildProgress overall = ResourceProgress::getOverallProgress();
        progressBar.setValue(overall.totalProgress * 100.0f);
    }
    ```

`OverallBuildProgress` carries `totalProgress` (0–1), `totalBuilds`,
`completedBuilds`, `currentBuildName`, `currentBuildType`, and `hasActiveBuilds`. Your
own loaders can participate by calling `ResourceProgress.startBuild(id, type, name)`,
`updateProgress(id, value)`, and `completeBuild(id)` / `failBuild(id)`.

## Platform caveats

| Platform | Threading behavior |
| --- | --- |
| Desktop (Windows, Linux, macOS) | Full `std::thread` support; thread pool fully functional |
| Android | Full thread support via POSIX threads |
| iOS | Full thread support via POSIX threads |
| HTML5 (Emscripten) | Threads require `SharedArrayBuffer` and COOP/COEP headers on the server. Without pthreads, the engine defines `NO_THREAD_SUPPORT` and runs single-threaded |

For web, always test async loading with pthreads enabled in your deployment environment.

## Practical rules

- Prefer the built-in async loading (`Engine.asyncLoading = true`) over manual threads —
  the resource pools already handle the thread-safety details.
- For manual background work, wrap it in `Engine::AsyncThreadScope` so GPU resource
  creation is deferred to the commit queue instead of running on the wrong thread.
- Spawn physics bodies and mutate scene hierarchies **only on the main thread**.
- Do not hold scene references or entity handles on worker threads without synchronization.
- Test async loading on the slowest target device — the loading time and race conditions
  may not reproduce on a fast desktop machine.

## Loading screens

`SceneManager` shows a loading screen for you. Register a UI scene once and every
`loadScene` goes through it:

1. The loading scene appears on top of the running scene, which keeps running below it.
2. After the loading delay, the old scene is replaced behind it. The new scene's entities
   and scripts are built on the main thread, so the game freezes for that moment with the
   loading scene on screen.
3. With async loading on, the new scene's textures, sounds and models stream in on worker
   threads while the loading scene keeps animating. It is removed once they are loaded.

=== "Lua"

    ```lua
    -- once, at startup
    Engine.asyncLoading = true
    SceneManager.setLoadingScene("Loading")
    SceneManager.loadingDelay = 0.3

    -- LoadingScreen.lua, on the Loading scene
    function LoadingScreen:onUpdate()
        if not SceneManager.loading then return end
        self.bar.width = 360 * SceneManager.loadingProgress
    end
    ```

=== "C++"

    ```cpp
    // once, at startup
    Engine::setAsyncLoading(true);
    SceneManager::setLoadingScene("Loading");
    SceneManager::setLoadingDelay(0.3f);

    // LoadingScreen.cpp, on the Loading scene
    void LoadingScreen::onUpdate() {
        if (!SceneManager::isLoading()) return;
        bar->setWidth((unsigned int)(360 * SceneManager::getLoadingProgress()));
    }
    ```

A level script can also wait for `SceneManager.loading` to become `false` before it starts
gameplay. See
[SceneManager.setLoadingScene](../reference/classes/scenemanager.md#setloadingscene-getloadingsceneid).

## See also

- [ThreadPoolManager](../reference/classes/threadpoolmanager.md)
- [ResourceProgress](../reference/classes/resourceprogress.md)
- [Data](../reference/classes/data.md)
- [File](../reference/classes/file.md)
