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

## Async thread scope

Mark background work with `Engine::AsyncThreadScope`. The engine tracks when a scope
enters and exits so it can gate certain operations appropriately:

=== "C++"

    ```cpp
    #include "Engine.h"

    void loadLevelInBackground() {
        Engine::AsyncThreadScope asyncScope;

        // Load raw resource data on the worker thread
        Data modelData;
        FileData file("models/level.gltf");
        file.read(modelData);
        file.close();

        // Commit main-thread work (GPU upload, scene mutation) via the queue
        Engine::queueMainThread([modelData = std::move(modelData)]() {
            // This runs on the main thread at the next safe point
            model.loadData(modelData);
        });
    }
    ```

## Thread pool

`ThreadPoolManager` dispatches work items to a pool of worker threads. It is suited for
parallelizable tasks that do not need the main thread:

=== "C++"

    ```cpp
    ThreadPoolManager::enqueue([]() {
        // parse data, decompress files, run a simulation step, etc.
    });
    ```

Worker count is determined at startup based on available hardware concurrency. The pool
is shared across the engine; avoid blocking workers with long synchronous operations.

## Queued main-thread commits

Any GPU, physics, or scene operation that is not thread-safe must be committed back to
the main thread. Use `Engine::queueMainThread()` to schedule a lambda for execution at
the next safe processing point:

=== "C++"

    ```cpp
    Engine::queueMainThread([&]() {
        // safe to create GPU resources, modify the scene, or register entities here
        Sprite sprite(&scene);
        sprite.setTexture(loadedTexturePath);
    });
    ```

Call `Engine::commitThreadQueue()` in the main update loop to flush queued work. This
is called automatically by the engine at the end of each frame.

## ResourceProgress

Track loading state with `ResourceProgress`:

```cpp
ResourceProgress progress;
progress.setState(ResourceProgressState::LOADING);

// Later, on completion:
progress.setState(ResourceProgressState::FINISHED);
progress.setProgress(1.0f);
```

Show progress in a UI `Progressbar` widget by reading `progress.getProgress()` in the
update loop:

```lua
function onUpdate()
    progressBar.value = ResourceProgress.getGlobalProgress()
end
```

## Platform caveats

| Platform | Threading behavior |
| --- | --- |
| Desktop (Windows, Linux, macOS) | Full `std::thread` support; thread pool fully functional |
| Android | Full thread support via POSIX threads |
| iOS | Full thread support via POSIX threads |
| HTML5 (Emscripten) | Threads require `SharedArrayBuffer` and COOP/COEP headers on the server. Without pthreads, the engine defines `NO_THREAD_SUPPORT` and runs single-threaded |

For web, always test async loading with pthreads enabled in your deployment environment.

## Practical rules

- Load raw file data (read bytes, decompress) on worker threads.
- Create GPU resources (textures, meshes), spawn physics bodies, and mutate scene
  hierarchies **only on the main thread**.
- Use `Engine::queueMainThread` to bridge worker results back to the main thread.
- Do not hold scene references or entity handles on worker threads without synchronization.
- Test async loading on the slowest target device — the loading time and race conditions
  may not reproduce on a fast desktop machine.

## Loading screen pattern

A common pattern for level loading:

1. Enter a loading scene with a progress bar.
2. Launch a worker thread that loads asset data and reports progress.
3. Each loaded asset queues a main-thread commit to create the in-scene object.
4. When all objects are committed, the main thread transitions to the gameplay scene.

=== "C++"

    ```cpp
    void startLevelLoad(const std::string& levelPath) {
        ThreadPoolManager::enqueue([levelPath]() {
            Engine::AsyncThreadScope scope;
            // ... load data ...

            Engine::queueMainThread([]() {
                SceneManager::loadScene("Level1");
            });
        });
    }
    ```

## See also

- [ThreadPoolManager](../reference/classes/threadpoolmanager.md)
- [ResourceProgress](../reference/classes/resourceprogress.md)
- [Data](../reference/classes/data.md)
- [File](../reference/classes/file.md)
