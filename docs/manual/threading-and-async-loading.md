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

## Loading screen pattern

A common pattern for level loading:

1. Enable async loading and enter a loading scene with a progress bar.
2. Load (or switch to) the gameplay scene — its resources stream in on worker threads.
3. Drive the progress bar from `ResourceProgress.getOverallProgress().totalProgress`.
4. When `ResourceProgress.hasActiveBuilds()` returns `false` and
   `Engine.getQueuedResourceCount()` reaches zero, hide the loading overlay.

## See also

- [ThreadPoolManager](../reference/classes/threadpoolmanager.md)
- [ResourceProgress](../reference/classes/resourceprogress.md)
- [Data](../reference/classes/data.md)
- [File](../reference/classes/file.md)
