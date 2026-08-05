---
description: Camera API reference — orthographic and perspective projection, target, navigation, render-to-texture.
---

# Camera

## Description

`Camera` defines the viewpoint from which the scene is rendered. It supports both orthographic (2D) and perspective (3D) projection, a look-at target, manual navigation helpers (walk, slide, orbit), and render-to-texture via an internal `Framebuffer`.

**Inherits:** [Object](object.md) → [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Camera cam(&scene);
    cam.setPerspective(60.0f, 1.333f, 0.1f, 1000.0f);
    cam.setPosition(0.0f, 2.0f, 10.0f);
    cam.setTarget(Vector3(0.0f, 0.0f, 0.0f));
    cam.activate();
    ```

=== "Lua"

    ```lua
    local cam = Camera(scene)
    cam:setPerspective(60, 1.333, 0.1, 1000)
    cam.position = Vector3(0, 2, 10)
    cam.target = Vector3(0, 0, 0)
    cam:activate()
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| [CameraType](#cameratype) | [type](#type) | `ORTHOGRAPHIC` | C++ \| Lua |
| bool | [autoResize](#autoresize) | `true` | C++ \| Lua |
| float | [nearClip](#nearclip-farclip) | `0.1` | C++ \| Lua |
| float | [farClip](#nearclip-farclip) | `1000.0` | C++ \| Lua |
| float | [leftClip](#leftclip-rightclip-bottomclip-topclip) | — | C++ \| Lua |
| float | [rightClip](#leftclip-rightclip-bottomclip-topclip) | — | C++ \| Lua |
| float | [bottomClip](#leftclip-rightclip-bottomclip-topclip) | — | C++ \| Lua |
| float | [topClip](#leftclip-rightclip-bottomclip-topclip) | — | C++ \| Lua |
| float | [aspect](#aspect) | — | C++ \| Lua |
| float | [yfov](#yfov) | `60.0°` | C++ \| Lua |
| Vector3 | [target](#target) | `(0,0,0)` | C++ \| Lua |
| Vector3 | [up](#up) | `(0,1,0)` | C++ \| Lua |
| bool | [renderToTexture](#rendertotexture) | `false` | C++ \| Lua |
| bool | [transparentSort](#transparentsort) | `true` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [activate](#activate) | C++ \| Lua |
| void | [setOrtho](#setortho) | C++ \| Lua |
| void | [setPerspective](#setperspective) | C++ \| Lua |
| void | [setAutoResize](#autoresize) | C++ \| Lua |
| bool | [isAutoResize](#autoresize) | C++ \| Lua |
| void | [setNearClip](#nearclip-farclip) | C++ \| Lua |
| float | [getNearClip](#nearclip-farclip) | C++ \| Lua |
| void | [setFarClip](#nearclip-farclip) | C++ \| Lua |
| float | [getFarClip](#nearclip-farclip) | C++ \| Lua |
| void | [setLeftClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| float | [getLeftClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| void | [setRightClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| float | [getRightClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| void | [setBottomClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| float | [getBottomClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| void | [setTopClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| float | [getTopClip](#leftclip-rightclip-bottomclip-topclip) | C++ \| Lua |
| void | [setAspect](#aspect) | C++ \| Lua |
| float | [getAspect](#aspect) | C++ \| Lua |
| void | [setYFov](#yfov) | C++ \| Lua |
| float | [getYFov](#yfov) | C++ \| Lua |
| void | [setType](#type) | C++ \| Lua |
| CameraType | [getType](#type) | C++ \| Lua |
| void | [setTarget](#settarget-disabletarget-isusingtarget) | C++ \| Lua |
| Vector3 | [getTarget](#target) | C++ \| Lua |
| void | [disableTarget](#settarget-disabletarget-isusingtarget) | C++ \| Lua |
| bool | [isUsingTarget](#settarget-disabletarget-isusingtarget) | C++ \| Lua |
| void | [setUp](#up) | C++ \| Lua |
| Vector3 | [getUp](#up) | C++ \| Lua |
| Vector3 | [getDirection](#getdirection-getright) | C++ \| Lua |
| Vector3 | [getRight](#getdirection-getright) | C++ \| Lua |
| Vector3 | [getWorldTarget](#target) | C++ \| Lua |
| Vector3 | [getWorldDirection](#getdirection-getright) | C++ \| Lua |
| Vector3 | [getWorldUp](#getdirection-getright) | C++ \| Lua |
| Vector3 | [getWorldRight](#getdirection-getright) | C++ \| Lua |
| Matrix4 | [getViewMatrix](#getviewmatrix-getprojectionmatrix-getviewprojectionmatrix) | C++ \| Lua |
| Matrix4 | [getProjectionMatrix](#getviewmatrix-getprojectionmatrix-getviewprojectionmatrix) | C++ \| Lua |
| Matrix4 | [getViewProjectionMatrix](#getviewmatrix-getprojectionmatrix-getviewprojectionmatrix) | C++ \| Lua |
| void | [rotateView](#rotateview) | C++ \| Lua |
| void | [rotatePosition](#rotateposition) | C++ \| Lua |
| void | [elevateView](#elevateview) | C++ \| Lua |
| void | [elevatePosition](#elevateposition) | C++ \| Lua |
| void | [walkForward](#walkforward) | C++ \| Lua |
| void | [zoom](#zoom) | C++ \| Lua |
| void | [slide](#slide-slideforward-slideup) | C++ \| Lua |
| void | [slideForward](#slide-slideforward-slideup) | C++ \| Lua |
| void | [slideUp](#slide-slideforward-slideup) | C++ \| Lua |
| void | [setRenderToTexture](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) | C++ \| Lua |
| bool | [isRenderToTexture](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) | C++ \| Lua |
| Framebuffer* | [getFramebuffer](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) | C++ \| Lua |
| void | [setFramebufferSize](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) | C++ \| Lua |
| void | [setFramebufferFilter](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) | C++ \| Lua |
| void | [setTransparentSort](#transparentsort) | C++ \| Lua |
| bool | [isTransparentSort](#transparentsort) | C++ \| Lua |
| Ray | [screenToRay](#screentoray) | C++ \| Lua |
| float | [getDistanceFromTarget](#getdistancefromtarget) | C++ \| Lua |
| void | [updateCamera](#updatecamera) | C++ \| Lua |

## Enumerations

### CameraType

* **ORTHOGRAPHIC** — Parallel projection; objects do not shrink with distance. Used for 2D games and UI.
* **PERSPECTIVE** — Frustum projection; objects appear smaller with distance. Used for 3D scenes.

## Property details

### type

* *Setter:* `void setType(CameraType type)`
* *Getter:* `CameraType getType() const`

Switches between orthographic and perspective projection. Setting the type does not automatically recalculate clip planes; use [setOrtho](#setortho) or [setPerspective](#setperspective) for that.

---

### autoResize

* *Setter:* `void setAutoResize(bool autoResize)`
* *Getter:* `bool isAutoResize() const`

When `true` (default), the projection is automatically recalculated when the canvas size changes. Disable if you manage the projection matrix manually.

---

### nearClip / farClip

* *Setters:* `void setNearClip(float nearValue)` / `void setFarClip(float farValue)`
* *Getters:* `float getNearClip() const` / `float getFarClip() const`

Near and far clip plane distances. Objects closer than `nearClip` or further than `farClip` are not rendered. Tighten these bounds to maximise depth-buffer precision.

---

### leftClip / rightClip / bottomClip / topClip

Orthographic frustum extents. Set via [setOrtho](#setortho) or individually. In auto-resize mode the engine keeps these aligned to the canvas.

---

### aspect

* *Setter:* `void setAspect(float aspect)`
* *Getter:* `float getAspect() const`

Width-to-height ratio for perspective projection. In auto-resize mode the engine updates this automatically.

---

### yfov

* *Setter:* `void setYFov(float yfov)`
* *Getter:* `float getYFov() const`

Vertical field-of-view in degrees (when `Engine::useDegrees` is `true`). Affects how wide the perspective frustum opens.

---

### target

* *Setter:* `void setTarget(Vector3 target)` / `void setTarget(float x, float y, float z)`
* *Getter:* `Vector3 getTarget() const`

Look-at point in local space. When set, the camera orientation is computed each frame so the camera always faces this point. Disable with [disableTarget](#settarget-disabletarget-isusingtarget).

---

### up

* *Setter:* `void setUp(Vector3 up)` / `void setUp(float x, float y, float z)`
* *Getter:* `Vector3 getUp() const`

Local up vector used when computing the view matrix from a target. Defaults to `(0, 1, 0)`.

---

### renderToTexture

* *Setter:* `void setRenderToTexture(bool renderToTexture)`
* *Getter:* `bool isRenderToTexture() const`

When `true`, the camera renders to an internal [Framebuffer](#setrendertotexture-getframebuffer-setframebuffersize-setframebufferfilter) instead of the main window surface. Retrieve the framebuffer with `getFramebuffer()` and pass it to a `Mesh::setTexture` call to create render-to-texture effects.

---

### transparentSort

* *Setter:* `void setTransparentSort(bool transparentSort)`
* *Getter:* `bool isTransparentSort() const`

Enables back-to-front depth sorting for transparent objects from this camera's viewpoint. Disable for orthographic UI cameras where order is determined by hierarchy.

## Method details

### activate

* `void activate()`

Makes this camera the active camera in its scene. Equivalent to calling `scene.setCamera(this)`.

---

### setOrtho

* `void setOrtho(float left, float right, float bottom, float top, float nearValue, float farValue)`

Configures the camera for orthographic projection with explicit clip planes. All objects within the box `(left, right, bottom, top, near, far)` are rendered.

=== "C++"

    ```cpp
    cam.setOrtho(0.0f, 800.0f, 0.0f, 600.0f, -100.0f, 100.0f);
    ```

=== "Lua"

    ```lua
    cam:setOrtho(0, 800, 0, 600, -100, 100)
    ```

---

### setPerspective

* `void setPerspective(float yfov, float aspect, float nearValue, float farValue)`

Configures the camera for perspective (3D) projection.

* **yfov** — Vertical field-of-view in degrees.
* **aspect** — Width ÷ height ratio.
* **nearValue** — Near clip plane distance (keep as large as possible).
* **farValue** — Far clip plane distance.

=== "C++"

    ```cpp
    cam.setPerspective(60.0f, (float)Engine::getCanvasWidth() / Engine::getCanvasHeight(), 0.1f, 500.0f);
    ```

=== "Lua"

    ```lua
    cam:setPerspective(60, Engine.canvasWidth / Engine.canvasHeight, 0.1, 500)
    ```

---

### setTarget / disableTarget / isUsingTarget

* `void setTarget(Vector3 target)` — Sets the look-at point. Activates target mode.
* `void disableTarget()` — Removes the look-at constraint and allows free rotation.
* `bool isUsingTarget() const` — Returns `true` while target mode is active.

---

### getDirection / getRight

* `Vector3 getDirection() const` — Local forward vector in camera space.
* `Vector3 getRight() const` — Local right vector in camera space.

Use `getWorldDirection()`, `getWorldUp()`, `getWorldRight()` for world-space equivalents.

---

### getViewMatrix / getProjectionMatrix / getViewProjectionMatrix

Computed matrices ready to pass to shaders or custom render pipelines.

---

### rotateView

* `void rotateView(float angle)`

Rotates the camera's *look direction* around the up axis by `angle` degrees (yaw). The camera position stays fixed.

---

### rotatePosition

* `void rotatePosition(float angle)`

Orbits the camera's *position* around the current [target](#target) by `angle` degrees. Useful for orbit camera controllers.

=== "C++"

    ```cpp
    // Orbit controller driven by mouse delta
    cam.rotatePosition(mouseDelta.x * 0.3f);
    cam.elevatePosition(-mouseDelta.y * 0.3f);
    ```

---

### elevateView

* `void elevateView(float angle)`

Tilts the camera's look direction up or down (pitch) by `angle` degrees. Position stays fixed.

---

### elevatePosition

* `void elevatePosition(float angle)`

Moves the camera position up or down along a sphere centered at [target](#target). Useful for orbit elevation.

---

### walkForward

* `void walkForward(float distance)`

Moves the camera forward along its look direction by `distance` units.

---

### zoom

* `void zoom(float distance)`

Moves the camera position along the direction toward [target](#target) by `distance` units. A positive value zooms in; negative zooms out.

---

### slide / slideForward / slideUp

* `void slide(float distance)` — Strafes along the local right vector.
* `void slideForward(float distance)` — Moves along the local forward vector.
* `void slideUp(float distance)` — Moves along the local up vector.

---

### screenToRay

* `Ray screenToRay(float x, float y)`

Converts a screen-space position (in canvas pixels) to a world-space [Ray](ray.md) for mouse picking.

=== "C++"

    ```cpp
    // Pick on mouse click
    Engine::onMouseDown.add("pick", [&](int btn, float x, float y, int mods) {
        Ray ray = cam.screenToRay(x, y);
        // test ray against physics or scene objects
    });
    ```

=== "Lua"

    ```lua
    Engine.onMouseDown = function(btn, x, y, mods)
        local ray = cam:screenToRay(x, y)
    end
    ```

---

### getDistanceFromTarget

* `float getDistanceFromTarget() const`

Returns the distance between the camera position and the current [target](#target) point. Useful for zoom limits in orbit controllers.

---

### setRenderToTexture / getFramebuffer / setFramebufferSize / setFramebufferFilter

Configure render-to-texture mode.

* `void setRenderToTexture(bool renderToTexture)` — Enable/disable off-screen rendering.
* `Framebuffer* getFramebuffer()` — Returns the internal framebuffer; valid only after `setRenderToTexture(true)`.
* `void setFramebufferSize(int width, int height)` — Overrides the framebuffer resolution (defaults to 512×512).
* `void setFramebufferFilter(TextureFilter filter)` — Sets the sampling filter for the output texture.

The size and filter are also editable in the editor's **Render Target** section on a render-to-texture camera and are saved with the scene.

=== "C++"

    ```cpp
    Camera rtCam(&scene);
    rtCam.setPerspective(60.0f, 1.0f, 0.1f, 100.0f);
    rtCam.setRenderToTexture(true);
    rtCam.setFramebufferSize(512, 512);

    Sprite screen(&scene);
    screen.setTexture(rtCam.getFramebuffer());
    screen.setSize(512, 512);
    screen.createSprite();
    ```

---

### updateCamera

* `void updateCamera()`

Forces an immediate recalculation of view and projection matrices. Called automatically each frame; call manually only when you need a fresh matrix outside the normal update cycle.
