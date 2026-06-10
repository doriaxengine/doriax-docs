---
description: Scene API reference — camera, background, lighting, UI events, and subsystems.
---

# Scene

## Description

A `Scene` is the root container for all objects, systems, and resources in a project. It manages the active camera, background color, global illumination, shadow settings, and the update/draw lifecycle. You typically create one or more scenes at startup and set the active one with `Engine::setScene`.

**Inherits:** [EntityRegistry](entityregistry.md)

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Scene scene;

    void MySystem::onUpdate() {
        scene.setBackgroundColor(0.1f, 0.1f, 0.2f);
    }
    ```

=== "Lua"

    ```lua
    local scene = Scene()
    scene:setBackgroundColor(0.1, 0.1, 0.2)
    Engine.setScene(scene)
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| Vector4 | [backgroundColor](#backgroundcolor) | `(0,0,0,1)` | C++ \| Lua |
| bool | [shadowsPCF](#shadowspcf) | `true` | C++ \| Lua |
| [LightState](#lightstate) | [lightState](#lightstate_1) | `AUTO` | C++ \| Lua |
| float | [globalIlluminationIntensity](#globalilluminationintensity) | `1.0` | C++ \| Lua |
| Vector3 | [globalIlluminationColor](#globalilluminationcolor) | `(1,1,1)` | C++ \| Lua |
| [UIEventState](#uieventstate) | [enableUIEvents](#enableuievents) | `NOT_SET` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [load](#load) | C++ \| Lua |
| void | [destroy](#destroy) | C++ \| Lua |
| void | [draw](#draw) | C++ \| Lua |
| void | [update](#update) | C++ \| Lua |
| void | [fixedUpdate](#fixedupdate) | C++ \| Lua |
| void | [setCamera](#setcamera) | C++ \| Lua |
| Entity | [getCamera](#getcamera) | C++ \| Lua |
| void | [setBackgroundColor](#setbackgroundcolor) | C++ \| Lua |
| Vector4 | [getBackgroundColor](#setbackgroundcolor) | C++ \| Lua |
| void | [setShadowsPCF](#setshadowspcf) | C++ \| Lua |
| bool | [isShadowsPCF](#setshadowspcf) | C++ \| Lua |
| void | [setLightState](#setlightstate) | C++ \| Lua |
| LightState | [getLightState](#setlightstate) | C++ \| Lua |
| void | [setGlobalIllumination](#setglobalillumination) | C++ \| Lua |
| float | [getGlobalIlluminationIntensity](#setglobalillumination) | C++ \| Lua |
| Vector3 | [getGlobalIlluminationColor](#setglobalillumination) | C++ \| Lua |
| void | [enableUIEvents](#enableuievents_1) | C++ \| Lua |
| bool | [isEnableUIEvents](#isenableuievents) | C++ \| Lua |
| bool | [canReceiveUIEvents](#canreceiveuievents) | C++ \| Lua |
| void | [updateCameraSize](#updatecamerasize) | C++ \| Lua |
| void | [removeSubscriptionsByTag](#removesubscriptionsbytag) | C++ \| Lua |

Entity and hierarchy methods — `createEntity`, `destroyEntity`, `setEntityName` /
`getEntityName`, [`findEntity`](entityregistry.md#findentity), `addEntityChild`,
`getEntityList` — are inherited from [EntityRegistry](entityregistry.md).

## Enumerations

### LightState

* **OFF** — Disables all lights in the scene; objects are rendered with no dynamic lighting.
* **ON** — Forces dynamic lighting on regardless of light objects present.
* **AUTO** — Activates lighting automatically when at least one light entity exists in the scene (default).

---

### UIEventState

* **NOT_SET** — Inherits UI event behaviour from the engine default.
* **ENABLED** — This scene receives UI pointer events.
* **DISABLED** — This scene ignores UI pointer events.

## Property details

### backgroundColor

* *Setter:* `void setBackgroundColor(Vector4 color)`
* *Getter:* `Vector4 getBackgroundColor() const`

Background clear color for the scene, in RGBA [0, 1] range. Convenience overloads accept `(r, g, b)` or `(r, g, b, a)` floats directly.

---

### shadowsPCF

* *Setter:* `void setShadowsPCF(bool shadowsPCF)`
* *Getter:* `bool isShadowsPCF() const`

Enables Percentage Closer Filtering for shadow maps, producing softer shadow edges. Disable for hard-edged shadows or performance savings on mobile.

---

### lightState

* *Setter:* `void setLightState(LightState state)`
* *Getter:* `LightState getLightState() const`

Controls whether the render system activates the lighting pass. See [LightState](#lightstate).

---

### globalIlluminationIntensity

Part of [setGlobalIllumination](#setglobalillumination). Controls the brightness of the ambient light applied uniformly across the scene.

---

### globalIlluminationColor

Part of [setGlobalIllumination](#setglobalillumination). Controls the tint of the ambient light (linear color, [0,1] per channel).

---

### enableUIEvents

* *Setter:* `void setEnableUIEvents(UIEventState enableUIEvents)`
* *Getter:* `UIEventState getEnableUIEvents() const`

Per-scene override for UI event routing. See [UIEventState](#uieventstate).

## Method details

### load

* `void load()`

Initializes the scene subsystems. Called automatically by the engine when the scene is added via `Engine::setScene` or `Engine::addSceneLayer`. Only call manually when managing scenes outside the engine lifecycle.

---

### destroy

* `void destroy()`

Tears down all subsystems and destroys every entity in the scene. Called automatically by the engine when the scene is removed from the stack.

---

### draw

* `void draw()`

Triggers a render pass for this scene. Normally called by the engine each frame; use only for custom render pipelines.

---

### update

* `void update(double dt)`

Runs one variable-step update for all subscribed systems. `dt` is the frame delta in seconds. Normally called by the engine.

---

### fixedUpdate

* `void fixedUpdate(double dt)`

Runs one fixed-step update for physics and other time-sensitive systems. `dt` equals [Engine::updateTime](engine.md#updatetime). Normally called by the engine.

---

### setCamera

* `void setCamera(Camera* camera)`
* `void setCamera(Entity camera)`

Sets the active camera for this scene. Only one camera can be active at a time. Pass the `Camera` object or its underlying `Entity` handle.

=== "C++"

    ```cpp
    Camera cam(&scene);
    cam.activate();           // equivalent shortcut
    // or:
    scene.setCamera(&cam);
    ```

=== "Lua"

    ```lua
    local cam = Camera(scene)
    scene:setCamera(cam)
    ```

---

### getCamera

* `Entity getCamera() const`

Returns the entity handle of the currently active camera.

---

### setBackgroundColor

* `void setBackgroundColor(Vector4 color)`
* `void setBackgroundColor(float red, float green, float blue)`
* `void setBackgroundColor(float red, float green, float blue, float alpha)`

Sets the clear color used before rendering the scene each frame.

=== "C++"

    ```cpp
    scene.setBackgroundColor(0.05f, 0.05f, 0.1f, 1.0f);
    ```

=== "Lua"

    ```lua
    scene:setBackgroundColor(0.05, 0.05, 0.1, 1.0)
    ```

---

### setShadowsPCF

* `void setShadowsPCF(bool shadowsPCF)`
* `bool isShadowsPCF() const`

Enables or disables Percentage Closer Filtering for shadow rendering.

---

### setLightState

* `void setLightState(LightState state)`
* `LightState getLightState() const`

Overrides automatic lighting detection. See [LightState](#lightstate).

---

### setGlobalIllumination

* `void setGlobalIllumination(float intensity, Vector3 color)`
* `void setGlobalIllumination(float intensity)`
* `void setGlobalIllumination(Vector3 color)`

Sets the ambient (global illumination) light for the scene. Intensity scales brightness; color tints the light. Flat-shaded or unlit materials are not affected.

=== "C++"

    ```cpp
    scene.setGlobalIllumination(0.3f, Vector3(1.0f, 0.95f, 0.9f));
    ```

=== "Lua"

    ```lua
    scene:setGlobalIllumination(0.3, Vector3(1.0, 0.95, 0.9))
    ```

---

### enableUIEvents

* `void enableUIEvents()`

Shorthand for `setEnableUIEvents(UIEventState::ENABLED)`.

---

### isEnableUIEvents

* `bool isEnableUIEvents() const`

Returns `true` if UI events are enabled for this scene (either via explicit `ENABLED` state or engine default).

---

### canReceiveUIEvents

* `bool canReceiveUIEvents()`

Returns `true` if this scene is currently the topmost scene that is able to receive UI pointer events. The engine calls this internally to route events to the correct scene layer.

---

### updateCameraSize

* `void updateCameraSize()`

Recalculates the active camera's projection to match the current canvas size. Called automatically when the canvas changes; call manually after resizing the viewport from script.

---

### removeSubscriptionsByTag

* `void removeSubscriptionsByTag(const std::string& substring)`

Removes all event subscriptions whose tag string contains `substring`. Used to clean up callbacks belonging to a destroyed script or component.
