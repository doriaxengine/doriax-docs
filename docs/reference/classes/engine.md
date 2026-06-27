---
description: Engine API reference — canvas, scenes, timing, input events, and platform state.
---

# Engine

## Description

Control engine properties and define defaults used across the whole project. `Engine` is entirely static — never instantiated. It manages the scene stack, canvas size and scaling, the update loop, platform queries, and all frame/input callback events.

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Scene scene;

    DORIAX_INIT void init() {
        Engine::setCanvasSize(1000, 480);
        Engine::setScalingMode(Scaling::FITWIDTH);
        Engine::setScene(&scene);
    }
    ```

=== "Lua"

    ```lua
    scene = Scene()
    Engine.setCanvasSize(1000, 480)
    Engine.scalingMode = Scaling.FITWIDTH
    Engine.setScene(scene)
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| static [Scaling](#scaling) | [scalingMode](#scalingmode) | `FITWIDTH` | C++ \| Lua |
| static [TextureStrategy](#texturestrategy) | [textureStrategy](#texturestrategy_1) | `RESIZE` | C++ \| Lua |
| static bool | [callMouseInTouchEvent](#callmouseintouchevent) | `false` | C++ \| Lua |
| static bool | [callTouchInMouseEvent](#calltouchinmouseevent) | `false` | C++ \| Lua |
| static bool | [useDegrees](#usedegrees) | `true` | C++ \| Lua |
| static bool | [allowEventsOutCanvas](#alloweventsoutcanvas) | `false` | C++ \| Lua |
| static bool | [ignoreEventsHandledByUI](#ignoreeventshandledbyui) | `false` | C++ \| Lua |
| static float | [updateTime](#updatetime) | `0.03` | C++ \| Lua |
| static double | [interpolationAlpha](#interpolationalpha) | — | C++ \| Lua |
| static int | [canvasWidth](#canvaswidth-canvasheight) | — | C++ \| Lua |
| static int | [canvasHeight](#canvaswidth-canvasheight) | — | C++ \| Lua |
| static int | [preferredCanvasWidth](#preferredcanvaswidth-preferredcanvasheight) | — | C++ \| Lua |
| static int | [preferredCanvasHeight](#preferredcanvaswidth-preferredcanvasheight) | — | C++ \| Lua |
| static Rect | [viewRect](#viewrect) | — | C++ \| Lua |
| static float | [deltatime](#deltatime) | — | C++ \| Lua |
| static float | [maxDeltatime](#maxdeltatime) | `0.25` | C++ \| Lua |
| static float | [framerate](#framerate) | — | C++ \| Lua |
| static double | [systemTime](#systemtime) | — | C++ \| Lua |
| static [Platform](#platform) | [platform](#platform_1) | — | C++ \| Lua |
| static [GraphicBackend](#graphicbackend) | [graphicBackend](#graphicbackend_1) | — | C++ \| Lua |
| static bool | [openGL](#opengl) | — | C++ \| Lua |
| static bool | [asyncLoading](#asyncloading) | `false` | C++ \| Lua |
| static [CursorType](#cursortype) | [mouseCursor](#mousecursor) | `ARROW` | C++ \| Lua |
| static Framebuffer* | [framebuffer](#framebuffer) | — | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| static void | [setScene](#setscene) | C++ \| Lua |
| static Scene* | [getScene](#getscene) | C++ \| Lua |
| static void | [addSceneLayer](#addscenelayer) | C++ \| Lua |
| static void | [executeSceneOnce](#executesceneonce) | C++ \| Lua |
| static void | [removeScene](#removescene) | C++ \| Lua |
| static void | [removeAllSceneLayers](#removeallscenelayers) | C++ \| Lua |
| static void | [removeAllScenes](#removeallscenes) | C++ \| Lua |
| static bool | [isSceneRunning](#isscenerunning) | C++ \| Lua |
| static Scene* | [getMainScene](#getmainscene) | C++ \| Lua |
| static Scene* | [getLastScene](#getlastscene) | C++ \| Lua |
| static void | [pauseGameEvents](#pausegameevents) | C++ \| Lua |
| static void | [setCanvasSize](#setcanvassize) | C++ \| Lua |
| static Rect | [getViewRect](#getviewrect) | C++ \| Lua |
| static void | [setUpdateTimeMS](#setupdatetimems) | C++ \| Lua |
| static bool | [isUIEventReceived](#isuieventreceived) | C++ \| Lua |
| static bool | [isViewLoaded](#isviewloaded) | C++ \| Lua |
| static void | [setMaxResourceLoadingThreads](#setmaxresourceloadingthreads) | C++ \| Lua |
| static size_t | [getQueuedResourceCount](#getqueuedresourcecount) | C++ \| Lua |
| static void | [clearAllSubscriptions](#clearallsubscriptions) | C++ \| Lua |
| static void | [startAsyncThread](#startasyncthread-committhreadqueue-endasyncthread-isasyncthread) | C++ \| Lua |
| static void | [commitThreadQueue](#startasyncthread-committhreadqueue-endasyncthread-isasyncthread) | C++ \| Lua |
| static void | [endAsyncThread](#startasyncthread-committhreadqueue-endasyncthread-isasyncthread) | C++ \| Lua |
| static bool | [isAsyncThread](#startasyncthread-committhreadqueue-endasyncthread-isasyncthread) | C++ \| Lua |

### Callback events

| Callback | Name | Languages |
| --- | --- | --- |
| void() | [onViewLoaded](#onviewloaded) | C++ \| Lua |
| void() | [onCanvasChanged](#oncanvaschanged) | C++ \| Lua |
| void() | [onViewDestroyed](#onviewdestroyed) | C++ \| Lua |
| void() | [onDraw](#ondraw) | C++ \| Lua |
| void() | [onUpdate](#onupdate) | C++ \| Lua |
| void() | [onFixedUpdate](#onfixedupdate) | C++ \| Lua |
| void() | [onPostUpdate](#onpostupdate) | C++ \| Lua |
| void() | [onPause](#onpause) | C++ \| Lua |
| void() | [onResume](#onresume) | C++ \| Lua |
| void() | [onShutdown](#onshutdown) | C++ \| Lua |
| void(int,float,float) | [onTouchStart](#ontouchstart) | C++ \| Lua |
| void(int,float,float) | [onTouchEnd](#ontouchend) | C++ \| Lua |
| void(int,float,float) | [onTouchMove](#ontouchmove) | C++ \| Lua |
| void() | [onTouchCancel](#ontouchcancel) | C++ \| Lua |
| void(int,float,float,int) | [onMouseDown](#onmousedown) | C++ \| Lua |
| void(int,float,float,int) | [onMouseUp](#onmouseup) | C++ \| Lua |
| void(float,float,int) | [onMouseMove](#onmousemove) | C++ \| Lua |
| void(float,float,int) | [onMouseScroll](#onmousescroll) | C++ \| Lua |
| void() | [onMouseEnter](#onmouseenter) | C++ \| Lua |
| void() | [onMouseLeave](#onmouseleave) | C++ \| Lua |
| void(int,bool,int) | [onKeyDown](#onkeydown) | C++ \| Lua |
| void(int,bool,int) | [onKeyUp](#onkeyup) | C++ \| Lua |
| void(wchar_t) | [onCharInput](#oncharinput) | C++ \| Lua |

## Enumerations

### Scaling

* **FITWIDTH** — Keeps canvas width fixed; height floats to match aspect ratio.
* **FITHEIGHT** — Keeps canvas height fixed; width floats.
* **LETTERBOX** — Keeps both dimensions; empty bars appear on screen edges.
* **CROP** — Keeps both dimensions; parts of the canvas may be cropped off screen.
* **STRETCH** — Stretches to fill the screen; objects may deform.
* **NATIVE** — Uses the native window resolution as-is.

---

### TextureStrategy

* **FIT** — Adjusts non-power-of-two textures using a fit algorithm.
* **RESIZE** — Resizes textures to the next power of two.
* **NONE** — No automatic texture resizing.

---

### Platform

* **MacOS** — Running on macOS.
* **iOS** — Running on iOS.
* **Web** — Running in WebGL/HTML5.
* **Android** — Running on Android.
* **Linux** — Running on Linux.
* **Windows** — Running on Windows.

---

### GraphicBackend

* **GLCORE** — OpenGL Core (desktop).
* **GLES3** — OpenGL ES 3 (mobile/web).
* **D3D11** — Direct3D 11 (Windows).
* **METAL** — Metal (Apple platforms).
* **WGPU** — WebGPU.
* **VULKAN** — Vulkan (Linux and Windows).

---

### CursorType

`ARROW`, `IBEAM`, `CROSSHAIR`, `POINTING_HAND`, `RESIZE_EW`, `RESIZE_NS`, `RESIZE_NWSE`, `RESIZE_NESW`, `RESIZE_ALL`, `NOT_ALLOWED`

## Property details

### scalingMode

* *Setter:* `static void setScalingMode(Scaling scalingMode)`
* *Getter:* `static Scaling getScalingMode()`

Controls how the logical canvas is mapped to the physical window. See [Scaling](#scaling) for each mode.

---

### textureStrategy

* *Setter:* `static void setTextureStrategy(TextureStrategy textureStrategy)`
* *Getter:* `static TextureStrategy getTextureStrategy()`

Controls automatic resizing of non-power-of-two textures on hardware that requires it.

---

### callMouseInTouchEvent

* *Setter:* `static void setCallMouseInTouchEvent(bool callMouseInTouchEvent)`
* *Getter:* `static bool isCallMouseInTouchEvent()`

When `true`, receiving a touch event also fires the equivalent mouse event. Useful for cross-platform testing.

---

### callTouchInMouseEvent

* *Setter:* `static void setCallTouchInMouseEvent(bool callTouchInMouseEvent)`
* *Getter:* `static bool isCallTouchInMouseEvent()`

When `true`, receiving a mouse event also fires the equivalent touch event.

---

### useDegrees

* *Setter:* `static void setUseDegrees(bool useDegrees)`
* *Getter:* `static bool isUseDegrees()`

When `true` (default), angle parameters in the API expect degrees. Set to `false` to use radians throughout.

---

### allowEventsOutCanvas

* *Setter:* `static void setAllowEventsOutCanvas(bool allowEventsOutCanvas)`
* *Getter:* `static bool isAllowEventsOutCanvas()`

When `true`, mouse move and scroll events are delivered even when the cursor is outside the canvas bounds.

---

### ignoreEventsHandledByUI

* *Setter:* `static void setIgnoreEventsHandledByUI(bool ignoreEventsHandledByUI)`
* *Getter:* `static bool isIgnoreEventsHandledByUI()`

When `true`, gameplay input callbacks are skipped for events already consumed by a UI widget.

---

### updateTime

* *Setter:* `static void setUpdateTime(float updateTime)`
* *Getter:* `static float getUpdateTime()`

Fixed-update interval in **seconds**. Used by `onFixedUpdate` and the physics simulation step. Also accepted in milliseconds via [setUpdateTimeMS](#setupdatetimems).

---

### interpolationAlpha

* *Getter:* `static double getInterpolationAlpha()`

Value in `[0, 1)` representing how far the current rendered frame is between the previous and next fixed-update steps. Use to visually interpolate physics-driven entities and avoid temporal aliasing.

---

### canvasWidth / canvasHeight

* *Getter:* `static int getCanvasWidth()` / `static int getCanvasHeight()`

Logical canvas dimensions after scaling is applied. These may differ from [preferredCanvasWidth](#preferredcanvaswidth-preferredcanvasheight) when a non-NATIVE scaling mode is active.

---

### preferredCanvasWidth / preferredCanvasHeight

* *Getter:* `static int getPreferredCanvasWidth()` / `static int getPreferredCanvasHeight()`

The dimensions originally passed to [setCanvasSize](#setcanvassize), unaffected by scaling.

---

### viewRect

* *Getter:* `static Rect getViewRect()`

Viewport rectangle computed from canvas size, screen size, and scaling mode.

---

### deltatime

* *Getter:* `static float getDeltatime()`

Time elapsed in **seconds** since the last draw frame. Multiply movement speeds by `deltatime` inside `onUpdate` to make motion frame-rate independent.

The value is **clamped** to [maxDeltatime](#maxdeltatime). After a long stall — the first frame of a scene (which includes load time), a debugger break, or an alt-tab — the real elapsed time can be several seconds. Returning that unclamped would teleport anything driven by `deltatime` in a single step (and could trigger a physics "spiral of death"). Clamping makes the simulation skip the lost time instead. This matches Unity's `Time.deltaTime` / `Time.maximumDeltaTime` and Godot's max-step behaviour.

> **Tip:** Even with clamping, prefer [`Vector3::moveTowards`](vector3.md#movetowards) over `direction * speed * deltatime` for "move to a target" logic — it clamps the step to the remaining distance so it can never overshoot, regardless of frame time.

---

### maxDeltatime

* *Getter:* `static float getMaxDeltatime()`
* *Setter:* `static void setMaxDeltatime(float seconds)`
* *Default:* `0.25`

Upper bound, in **seconds**, for the value returned by [deltatime](#deltatime) and used by the update loop. Lower it for stricter clamping; raise it to allow larger single steps. Must be greater than `0`. Equivalent to Unity's `Time.maximumDeltaTime`.

---

### framerate

* *Getter:* `static float getFramerate()`

Current frames-per-second estimate. Computed from the **raw** (unclamped) frame time, so it stays accurate even on stalled frames where [deltatime](#deltatime) is clamped.

---

### systemTime

* *Getter:* `static double getSystemTime()`

Monotonic wall-clock time in **seconds**, independent of scene pausing and update loop throttling.

---

### platform

* *Getter:* `static Platform getPlatform()`

Returns the [Platform](#platform) the engine is currently running on.

---

### graphicBackend

* *Getter:* `static GraphicBackend getGraphicBackend()`

Returns the active [GraphicBackend](#graphicbackend).

---

### openGL

* *Getter:* `static bool isOpenGL()`

Returns `true` when any OpenGL backend (GLCORE, GLES3) is active.

---

### asyncLoading

* *Setter:* `static void setAsyncLoading(bool enable)`
* *Getter:* `static bool isAsyncLoading()`

Enable background resource loading. When active, GPU resource creation must be committed on the main thread via [commitThreadQueue](#startasyncthread-committhreadqueue-endasyncthread-isasyncthread).

---

### mouseCursor

* *Setter:* `static void setMouseCursor(CursorType type)`
* *Getter:* `static CursorType getMouseCursor()`

Changes the OS mouse cursor shape. See [CursorType](#cursortype).

---

### framebuffer

* *Setter:* `static void setFramebuffer(Framebuffer* framebuffer)`
* *Getter:* `static Framebuffer* getFramebuffer()`

Off-screen render target for the full frame output. When set, the engine renders to this framebuffer instead of the window surface.

## Method details

### setScene

* `static void setScene(Scene* scene)`

Sets the main scene. Pass `nullptr` (C++) or `nil` (Lua) to clear the main scene.

---

### getScene

* `static Scene* getScene()`

Returns the current main scene, or `nullptr`/`nil` if none is set.

---

### addSceneLayer

* `static void addSceneLayer(Scene* scene)`

Renders an additional scene as a layer on top of the main scene. Commonly used for HUDs, overlays, or pause menus.

---

### executeSceneOnce

* `static void executeSceneOnce(Scene* scene)`

Adds a scene that runs for exactly one update/draw cycle, then is automatically removed. Useful for single-frame splash transitions.

---

### removeScene

* `static void removeScene(Scene* scene)`

Removes a specific scene from the active scene stack.

---

### removeAllSceneLayers

* `static void removeAllSceneLayers(bool removeOneTimeScenes)`

Removes all layered scenes. When `removeOneTimeScenes` is `true`, one-time scenes added via [executeSceneOnce](#executesceneonce) are also removed.

---

### removeAllScenes

* `static void removeAllScenes()`

Removes all scenes, including the main scene and all layers.

---

### isSceneRunning

* `static bool isSceneRunning(Scene* scene)`

Returns `true` if the given scene is currently in the active scene stack.

---

### getMainScene

* `static Scene* getMainScene()`

Returns the scene set with [setScene](#setscene).

---

### getLastScene

* `static Scene* getLastScene()`

Returns the top-most scene in the stack (the most recently added layer, or the main scene if no layers exist).

---

### pauseGameEvents

* `static void pauseGameEvents(bool pause)`

Pauses delivery of gameplay events (onUpdate, onFixedUpdate, input callbacks) without stopping the render loop. The editor uses this when the project is not in play mode.

---

### setCanvasSize

* `static void setCanvasSize(int canvasWidth, int canvasHeight)`

Sets the preferred logical canvas dimensions. The actual [canvasWidth](#canvaswidth-canvasheight)/[canvasHeight](#canvaswidth-canvasheight) reported at runtime may differ depending on the active [scalingMode](#scalingmode).

---

### getViewRect

* `static Rect getViewRect()`

Returns the viewport rectangle calculated from canvas size, window size, and scaling mode.

---

### setUpdateTimeMS

* `static void setUpdateTimeMS(unsigned int updateTimeMS)`

Same as [updateTime](#updatetime) but accepts the interval in **milliseconds**.

---

### isUIEventReceived

* `static bool isUIEventReceived()`

Returns `true` if any UI widget consumed a pointer event during the current frame. Use with [ignoreEventsHandledByUI](#ignoreeventshandledbyui) to prevent gameplay from reacting to UI clicks.

---

### isViewLoaded

* `static bool isViewLoaded()`

Returns `true` after the graphics surface is ready (after [onViewLoaded](#onviewloaded) fires).

---

### clearAllSubscriptions

* `static void clearAllSubscriptions(bool includeLifecycle)`

Removes all registered callbacks from all engine events. When `includeLifecycle` is `false`, lifecycle events such as `onViewLoaded` are preserved.

---

### setMaxResourceLoadingThreads

* `static void setMaxResourceLoadingThreads(size_t maxThreads)`

Sets the maximum number of worker threads used for background asset loading.

---

### getQueuedResourceCount

* `static size_t getQueuedResourceCount()`

Returns the number of resources still waiting to be loaded on background threads.

---

### startAsyncThread / commitThreadQueue / endAsyncThread / isAsyncThread

Used to safely create GPU resources from background threads:

1. Call `startAsyncThread()` at the beginning of the worker function.
2. Create textures, meshes, etc.
3. Call `commitThreadQueue()` periodically (or at the end) to flush pending GPU uploads on the main thread.
4. Call `endAsyncThread()` when the worker is finished.

`AsyncThreadScope` (C++ RAII) wraps start/end automatically.

## Callback event details

### onViewLoaded

* `static FunctionSubscribe<void()> onViewLoaded`

Called once when the graphics backend surface is ready for rendering.

---

### onCanvasChanged

* `static FunctionSubscribe<void()> onCanvasChanged`
* Callback: `void()`

Called when the canvas or window size changes. Re-query [canvasWidth](#canvaswidth-canvasheight)/[canvasHeight](#canvaswidth-canvasheight) or reposition UI elements here.

---

### onViewDestroyed

* `static FunctionSubscribe<void()> onViewDestroyed`
* Callback: `void()`

Called when the graphics surface is being destroyed (e.g. app going to background on mobile).

---

### onDraw

* `static FunctionSubscribe<void()> onDraw`
* Callback: `void()`

Called every frame after the scene is drawn. Use for custom rendering passes.

---

### onUpdate

* `static FunctionSubscribe<void()> onUpdate`
* Callback: `void()`

Called every frame for variable-step gameplay logic. Multiply movement by [deltatime](#deltatime) to ensure frame-rate independence.

---

### onFixedUpdate

* `static FunctionSubscribe<void()> onFixedUpdate`
* Callback: `void()`

Called at a fixed interval defined by [updateTime](#updatetime). Use for physics, deterministic simulation, and anything that must not depend on frame rate.

---

### onPostUpdate

* `static FunctionSubscribe<void()> onPostUpdate`
* Callback: `void()`

Called after the regular update and fixed-update passes each frame. Useful for late-stage logic such as camera follow that must run after all objects have moved.

---

### onPause

* `static FunctionSubscribe<void()> onPause`
* Callback: `void()`

Called when the system suspends the application (e.g. phone call received, app moved to background).

---

### onResume

* `static FunctionSubscribe<void()> onResume`
* Callback: `void()`

Called when the application returns to the foreground after a pause.

---

### onShutdown

* `static FunctionSubscribe<void()> onShutdown`
* Callback: `void()`

Called when the application is closing. Use to flush saves or clean up persistent state.

---

### onTouchStart

* `static FunctionSubscribe<void(int,float,float)> onTouchStart`
* Callback: `void(int pointer, float x, float y)`
    * **pointer** — Touch identifier for multitouch tracking.
    * **x** — Horizontal position in canvas coordinates.
    * **y** — Vertical position in canvas coordinates.

Called when a new touch contact begins.

---

### onTouchEnd

* `static FunctionSubscribe<void(int,float,float)> onTouchEnd`
* Callback: `void(int pointer, float x, float y)`
    * **pointer** — Touch identifier.
    * **x** — Final horizontal position in canvas coordinates.
    * **y** — Final vertical position in canvas coordinates.

Called when a touch contact is lifted.

---

### onTouchMove

* `static FunctionSubscribe<void(int,float,float)> onTouchMove`
* Callback: `void(int pointer, float x, float y)`
    * **pointer** — Touch identifier.
    * **x** — Updated horizontal position.
    * **y** — Updated vertical position.

Called whenever a touch contact moves.

---

### onTouchCancel

* `static FunctionSubscribe<void()> onTouchCancel`
* Callback: `void()`

Called when the system cancels the current touch sequence (e.g. an incoming call interrupts input).

---

### onMouseDown

* `static FunctionSubscribe<void(int,float,float,int)> onMouseDown`
* Callback: `void(int button, float x, float y, int mods)`
    * **button** — Mouse button index; see [Input](input.md#mouse-buttons) constants.
    * **x** — Horizontal position in canvas coordinates.
    * **y** — Vertical position in canvas coordinates.
    * **mods** — Modifier key bitmask; see [Input](input.md#modifiers).

Called when a mouse button is pressed.

---

### onMouseUp

* `static FunctionSubscribe<void(int,float,float,int)> onMouseUp`
* Callback: `void(int button, float x, float y, int mods)`
    * **button** — Mouse button index.
    * **x** — Horizontal position.
    * **y** — Vertical position.
    * **mods** — Modifier key bitmask.

Called when a mouse button is released.

---

### onMouseMove

* `static FunctionSubscribe<void(float,float,int)> onMouseMove`
* Callback: `void(float x, float y, int mods)`
    * **x** — Horizontal position in canvas coordinates.
    * **y** — Vertical position in canvas coordinates.
    * **mods** — Modifier key bitmask.

Called when the mouse cursor moves. Also called outside the canvas when [allowEventsOutCanvas](#alloweventsoutcanvas) is `true`.

---

### onMouseScroll

* `static FunctionSubscribe<void(float,float,int)> onMouseScroll`
* Callback: `void(float xoffset, float yoffset, int mods)`
    * **xoffset** — Horizontal scroll amount.
    * **yoffset** — Vertical scroll amount (positive = scroll up).
    * **mods** — Modifier key bitmask.

Called when the mouse scroll wheel changes.

---

### onMouseEnter

* `static FunctionSubscribe<void()> onMouseEnter`
* Callback: `void()`

Called when the mouse cursor enters the canvas boundary.

---

### onMouseLeave

* `static FunctionSubscribe<void()> onMouseLeave`
* Callback: `void()`

Called when the mouse cursor leaves the canvas boundary.

---

### onKeyDown

* `static FunctionSubscribe<void(int,bool,int)> onKeyDown`
* Callback: `void(int key, bool repeat, int mods)`
    * **key** — Key code; see [Input](input.md#keys) constants (`D_KEY_*` in C++, `Input.KEY_*` in Lua).
    * **repeat** — `true` if the key is being held and this is a repeat event.
    * **mods** — Modifier key bitmask.

Called when any keyboard key is pressed.

---

### onKeyUp

* `static FunctionSubscribe<void(int,bool,int)> onKeyUp`
* Callback: `void(int key, bool repeat, int mods)`
    * **key** — Key code.
    * **repeat** — Always `false` on key-up.
    * **mods** — Modifier key bitmask.

Called when any keyboard key is released.

---

### onCharInput

* `static FunctionSubscribe<void(wchar_t)> onCharInput`
* Callback: `void(wchar_t codepoint)`
    * **codepoint** — Unicode code point of the typed character, including composed/accented characters.

Called for text input. Prefer this over [onKeyDown](#onkeydown) when implementing text fields.
