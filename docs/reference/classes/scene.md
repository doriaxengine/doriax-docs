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
| [ShadowQuality](#shadowquality) | [shadowQuality](#shadowquality_1) | `LOW` | C++ \| Lua |
| [LightState](#lightstate) | [lightState](#lightstate_1) | `AUTO` | C++ \| Lua |
| float | [globalIlluminationIntensity](#globalilluminationintensity) | `1.0` | C++ \| Lua |
| Vector3 | [globalIlluminationColor](#globalilluminationcolor) | `(1,1,1)` | C++ \| Lua |
| float | [ambientLight2DIntensity](#ambientlight2dintensity) | `1.0` | C++ \| Lua |
| Vector3 | [ambientLight2DColor](#ambientlight2dcolor) | `(1,1,1)` | C++ \| Lua |
| [ShadowQuality](#shadowquality) | [shadow2DQuality](#shadow2dquality) | `LOW` | C++ \| Lua |
| bool | [ssaoEnabled](#ssaoenabled) | `false` | C++ \| Lua |
| float | [ssaoRadius](#ssaoradius) | `0.5` | C++ \| Lua |
| float | [ssaoIntensity](#ssaointensity) | `1.0` | C++ \| Lua |
| float | [ssaoBias](#ssaobias) | `0.025` | C++ \| Lua |
| bool | [ssaoDebug](#ssaodebug) | `false` | C++ \| Lua |
| bool | [ssrEnabled](#ssrenabled) | `false` | C++ \| Lua |
| float | [ssrMaxDistance](#ssrmaxdistance) | `8.0` | C++ \| Lua |
| float | [ssrThickness](#ssrthickness) | `0.5` | C++ \| Lua |
| int | [ssrMaxSteps](#ssrmaxsteps) | `48` | C++ \| Lua |
| float | [ssrIntensity](#ssrintensity) | `1.0` | C++ \| Lua |
| float | [ssrBlur](#ssrblur) | `0.0` | C++ \| Lua |
| int | [ssrDebugMode](#ssrdebugmode) | `0` | C++ \| Lua |
| bool | [fixedResolutionEnabled](#fixedresolutionenabled) | `false` | C++ \| Lua |
| unsigned int | [fixedResolutionWidth](#fixedresolutionwidth-fixedresolutionheight) | `640` | C++ \| Lua |
| unsigned int | [fixedResolutionHeight](#fixedresolutionwidth-fixedresolutionheight) | `360` | C++ \| Lua |
| TextureFilter | [fixedResolutionFilter](#fixedresolutionfilter) | `NEAREST` | C++ \| Lua |
| string | [defaultMeshShader](#defaultmeshshader) | `""` | C++ \| Lua |
| string | [defaultUIShader](#defaultuishader) | `""` | C++ \| Lua |
| string | [defaultSkyShader](#defaultskyshader) | `""` | C++ \| Lua |
| string | [defaultPointsShader](#defaultpointsshader) | `""` | C++ \| Lua |
| string | [defaultLinesShader](#defaultlinesshader) | `""` | C++ \| Lua |
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
| void | [setShadowQuality](#shadowquality_1) | C++ |
| ShadowQuality | [getShadowQuality](#shadowquality_1) | C++ |
| void | [setLightState](#setlightstate) | C++ \| Lua |
| LightState | [getLightState](#setlightstate) | C++ \| Lua |
| void | [setGlobalIllumination](#setglobalillumination) | C++ \| Lua |
| float | [getGlobalIlluminationIntensity](#setglobalillumination) | C++ \| Lua |
| Vector3 | [getGlobalIlluminationColor](#setglobalillumination) | C++ \| Lua |
| void | [setAmbientLight2D](#setambientlight2d) | C++ \| Lua |
| float | [getAmbientLight2DIntensity](#setambientlight2d) | C++ \| Lua |
| Vector3 | [getAmbientLight2DColor](#setambientlight2d) | C++ \| Lua |
| void | [setShadow2DQuality](#shadow2dquality) | C++ |
| ShadowQuality | [getShadow2DQuality](#shadow2dquality) | C++ |
| void | [setSSAOEnabled](#ssaoenabled) | C++ \| Lua |
| bool | [isSSAOEnabled](#ssaoenabled) | C++ \| Lua |
| void | [setSSAORadius](#ssaoradius) | C++ \| Lua |
| float | [getSSAORadius](#ssaoradius) | C++ \| Lua |
| void | [setSSAOIntensity](#ssaointensity) | C++ \| Lua |
| float | [getSSAOIntensity](#ssaointensity) | C++ \| Lua |
| void | [setSSAOBias](#ssaobias) | C++ \| Lua |
| float | [getSSAOBias](#ssaobias) | C++ \| Lua |
| void | [setSSAODebug](#ssaodebug) | C++ \| Lua |
| bool | [isSSAODebug](#ssaodebug) | C++ \| Lua |
| void | [setSSREnabled](#ssrenabled) | C++ \| Lua |
| bool | [isSSREnabled](#ssrenabled) | C++ \| Lua |
| void | [setSSRMaxDistance](#ssrmaxdistance) | C++ \| Lua |
| float | [getSSRMaxDistance](#ssrmaxdistance) | C++ \| Lua |
| void | [setSSRThickness](#ssrthickness) | C++ \| Lua |
| float | [getSSRThickness](#ssrthickness) | C++ \| Lua |
| void | [setSSRMaxSteps](#ssrmaxsteps) | C++ \| Lua |
| int | [getSSRMaxSteps](#ssrmaxsteps) | C++ \| Lua |
| void | [setSSRIntensity](#ssrintensity) | C++ \| Lua |
| float | [getSSRIntensity](#ssrintensity) | C++ \| Lua |
| void | [setSSRBlur](#ssrblur) | C++ \| Lua |
| float | [getSSRBlur](#ssrblur) | C++ \| Lua |
| void | [setSSRDebugMode](#ssrdebugmode) | C++ \| Lua |
| int | [getSSRDebugMode](#ssrdebugmode) | C++ \| Lua |
| void | [setFixedResolutionEnabled](#fixedresolutionenabled) | C++ \| Lua |
| bool | [isFixedResolutionEnabled](#fixedresolutionenabled) | C++ \| Lua |
| void | [setFixedResolutionWidth](#fixedresolutionwidth-fixedresolutionheight) | C++ \| Lua |
| unsigned int | [getFixedResolutionWidth](#fixedresolutionwidth-fixedresolutionheight) | C++ \| Lua |
| void | [setFixedResolutionHeight](#fixedresolutionwidth-fixedresolutionheight) | C++ \| Lua |
| unsigned int | [getFixedResolutionHeight](#fixedresolutionwidth-fixedresolutionheight) | C++ \| Lua |
| void | [setFixedResolutionSize](#fixedresolutionwidth-fixedresolutionheight) | C++ \| Lua |
| void | [setFixedResolutionFilter](#fixedresolutionfilter) | C++ \| Lua |
| TextureFilter | [getFixedResolutionFilter](#fixedresolutionfilter) | C++ \| Lua |
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

---

### ShadowQuality

PCF filter quality of shadow edges, shared by [shadowQuality](#shadowquality) (3D shadow maps) and [shadow2DQuality](#shadow2dquality) (2D lights).

* **NONE** — 1 tap, no filtering (hard edges)
* **LOW** — 3×3 taps in 3D / 5 taps in 2D (default)
* **MEDIUM** — 5×5 taps in 3D / 9 taps in 2D
* **HIGH** — 7×7 taps in 3D / 13 taps in 2D

## Property details

### backgroundColor

* *Setter:* `void setBackgroundColor(Vector4 color)`
* *Getter:* `Vector4 getBackgroundColor() const`

Background clear color for the scene, in RGBA [0, 1] range. Convenience overloads accept `(r, g, b)` or `(r, g, b, a)` floats directly.

---

### shadowQuality

* *Setter:* `void setShadowQuality(ShadowQuality quality)`
* *Getter:* `ShadowQuality getShadowQuality() const`

Filter quality of 3D shadow map edges (PCF kernel size, applied instantly with no shader rebuild):

* **NONE** — 1 tap, hard edges (or performance savings on mobile)
* **LOW** — 3×3 taps (default)
* **MEDIUM** — 5×5 taps
* **HIGH** — 7×7 taps

The same [ShadowQuality](#shadowquality) enum also drives [shadow2DQuality](#shadow2dquality) for 2D lights.

Lua exposes this setting as the `shadowQuality` property:

```lua
scene.shadowQuality = ShadowQuality.MEDIUM
```

There is no separate `shadow3DQuality` Lua property; `shadowQuality` is the 3D shadow quality setting.

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

### ambientLight2DIntensity

Part of [setAmbientLight2D](#setambientlight2d). Controls the brightness of the 2D ambient light applied to 2D-lit objects. Defaults to `1.0` (fully lit), so a scene looks unchanged until you dim it.

---

### ambientLight2DColor

Part of [setAmbientLight2D](#setambientlight2d). Controls the tint of the 2D ambient light.

---

### shadow2DQuality

* *Setter:* `void setShadow2DQuality(ShadowQuality quality)`
* *Getter:* `ShadowQuality getShadow2DQuality() const`

Filter quality of 2D light shadows (PCF taps along the 1D polar shadow map). More taps smooth the **same** penumbra width (set per light by [Light2D — shadowSoftness](light2d.md#shadowsoftness)), removing banding on wide penumbras. Changing it takes effect immediately (no shader rebuild).

* **NONE** — 1 tap, no filtering (hard edges regardless of softness)
* **LOW** — 5 taps (default)
* **MEDIUM** — 9 taps
* **HIGH** — 13 taps

=== "C++"

    ```cpp
    scene.setShadow2DQuality(ShadowQuality::MEDIUM);
    ```

=== "Lua"

    ```lua
    scene.shadow2DQuality = ShadowQuality.MEDIUM
    ```

---

### ssaoEnabled

* *Setter:* `void setSSAOEnabled(bool enabled)`
* *Getter:* `bool isSSAOEnabled() const`

Enables screen-space ambient occlusion. SSAO darkens the ambient/indirect lighting (IBL or global illumination) in creases and contact areas; it does not affect direct light. Toggling it recompiles lit mesh shaders. Applies to the main camera; terrain is currently excluded.

---

### ssaoRadius

* *Setter:* `void setSSAORadius(float radius)`
* *Getter:* `float getSSAORadius() const`

View-space sampling radius (world units). Larger values gather occlusion from farther surfaces (broader, softer AO); smaller values keep it to tight contact creases.

---

### ssaoIntensity

* *Setter:* `void setSSAOIntensity(float intensity)`
* *Getter:* `float getSSAOIntensity() const`

Strength of the effect, applied as an exponent on the occlusion factor — higher values darken occluded areas more.

---

### ssaoBias

* *Setter:* `void setSSAOBias(float bias)`
* *Getter:* `float getSSAOBias() const`

View-space depth bias that prevents self-occlusion artifacts (acne) on flat surfaces. Increase slightly if flat areas appear dirty; keep small to preserve fine contact detail.

---

### ssaoDebug

* *Setter:* `void setSSAODebug(bool debug)`
* *Getter:* `bool isSSAODebug() const`

Debug aid: when enabled, lit meshes output the raw screen-space AO buffer as grayscale instead of their shaded color, so you can inspect and tune the occlusion directly. Not serialized.

---

### ssrEnabled

* *Setter:* `void setSSREnabled(bool ssrEnabled)`
* *Getter:* `bool isSSREnabled() const`

Enables screen-space reflections. SSR reflects on-screen geometry by marching the camera depth/G-buffer, and where it finds a hit it *replaces* the surface's IBL environment reflection rather than adding to it (falling back to IBL where the ray misses). Requires a framebuffer destination (editor viewport, render-to-texture camera, or engine framebuffer) and applies to the main camera. Toggling it reloads meshes to build the G-buffer shaders.

---

### ssrMaxDistance

* *Setter:* `void setSSRMaxDistance(float maxDistance)`
* *Getter:* `float getSSRMaxDistance() const`

Maximum reflection ray length in view-space units. Longer rays catch more distant reflections at higher cost. Default `8.0`.

---

### ssrThickness

* *Setter:* `void setSSRThickness(float thickness)`
* *Getter:* `float getSSRThickness() const`

Depth-compare tolerance (view-space units) for accepting a ray hit. Smaller is stricter; larger fills gaps but can smear at object contacts. Default `0.5`.

---

### ssrMaxSteps

* *Setter:* `void setSSRMaxSteps(int maxSteps)`
* *Getter:* `int getSSRMaxSteps() const`

Linear march sample count. Higher gives sharper, longer reflections (and helps thin contacts register) at more cost. Default `48`.

---

### ssrIntensity

* *Setter:* `void setSSRIntensity(float intensity)`
* *Getter:* `float getSSRIntensity() const`

Overall reflection strength multiplier applied in the composite. Default `1.0`.

---

### ssrBlur

* *Setter:* `void setSSRBlur(float blur)`
* *Getter:* `float getSSRBlur() const`

Glossy blur amount in `[0..1]`. `0` keeps mirror-sharp reflections; higher values blur the reflection in proportion to each surface's roughness. Default `0.0`.

---

### ssrDebugMode

* *Setter:* `void setSSRDebugMode(int mode)`
* *Getter:* `int getSSRDebugMode() const`

Debug visualization of the SSR G-buffer, rendered full-screen: `0` off, `1` reflection buffer, `2` normal, `3` roughness, `4` metallic, `5` albedo, `6` IBL specular. Not serialized.

---

### fixedResolutionEnabled

* *Setter:* `void setFixedResolutionEnabled(bool fixedResolutionEnabled)`
* *Getter:* `bool isFixedResolutionEnabled() const`

Renders the main camera into an internal buffer of [fixedResolutionWidth × fixedResolutionHeight](#fixedresolutionwidth-fixedresolutionheight) and upscales the result to the view rect, instead of rendering at the window's native resolution. Takes effect only when this scene is the Engine main scene; scenes added as layers always render at native resolution. Letterboxing, input mapping, and object coordinates keep following the canvas and scaling mode. In the editor, the fixed resolution is applied during play mode only. Toggling at runtime rebuilds the scene's render pipelines, which may cause a brief hitch — prefer changing the size instead. See [Multiple Resolutions](../../manual/multiple-resolutions.md#fixed-resolution).

=== "C++"

    ```cpp
    scene.setFixedResolutionSize(320, 180);
    scene.setFixedResolutionFilter(TextureFilter::NEAREST);
    scene.setFixedResolutionEnabled(true);
    ```

=== "Lua"

    ```lua
    scene:setFixedResolutionSize(320, 180)
    scene.fixedResolutionFilter = TextureFilter.NEAREST
    scene.fixedResolutionEnabled = true
    ```

---

### fixedResolutionWidth, fixedResolutionHeight

* *Setters:* `void setFixedResolutionWidth(unsigned int width)`, `void setFixedResolutionHeight(unsigned int height)`, `void setFixedResolutionSize(unsigned int width, unsigned int height)`
* *Getters:* `unsigned int getFixedResolutionWidth() const`, `unsigned int getFixedResolutionHeight() const`

The internal render resolution in pixels used when [fixedResolutionEnabled](#fixedresolutionenabled) is on. Can be changed at any time — the internal buffer is recreated on the next frame with no interruption, which makes render-scale options and dynamic resolution scaling cheap. Keep the aspect ratio equal to the canvas aspect ratio to avoid non-square pixels. Defaults `640 × 360`.

---

### fixedResolutionFilter

* *Setter:* `void setFixedResolutionFilter(TextureFilter filter)`
* *Getter:* `TextureFilter getFixedResolutionFilter() const`

Sampling filter used when the fixed-resolution image is upscaled to the view rect: `TextureFilter::NEAREST` (default) keeps hard pixel edges for a pixel-art look; `TextureFilter::LINEAR` interpolates smoothly, which suits fixed resolution used purely as a performance measure.

---

### defaultMeshShader

* *Setter:* `void setDefaultMeshShader(const std::string& path)`
* *Getter:* `const std::string& getDefaultMeshShader() const`

Scene-wide custom shader for Mesh components. The value is a project-relative base path to a forked shader (for example `"shaders/myMesh"`, resolving to `.vert`/`.frag`), or `"a.vert|b.frag"` for separately named files. Every Mesh whose own custom shader is empty uses it; an empty string (default) means the engine built-in. A shader assigned on the component always takes priority. Changing the value reloads the affected meshes. See [Custom Shaders — Scene default shaders](../../editor/custom-shaders.md#scene-default-shaders).

=== "C++"

    ```cpp
    scene.setDefaultMeshShader("shaders/toon");
    ```

=== "Lua"

    ```lua
    scene.defaultMeshShader = "shaders/toon"
    ```

---

### defaultUIShader

* *Setter:* `void setDefaultUIShader(const std::string& path)`
* *Getter:* `const std::string& getDefaultUIShader() const`

Scene-wide custom shader for UI components. Same semantics as [defaultMeshShader](#defaultmeshshader).

---

### defaultSkyShader

* *Setter:* `void setDefaultSkyShader(const std::string& path)`
* *Getter:* `const std::string& getDefaultSkyShader() const`

Scene-wide custom shader for the Sky component. Same semantics as [defaultMeshShader](#defaultmeshshader).

---

### defaultPointsShader

* *Setter:* `void setDefaultPointsShader(const std::string& path)`
* *Getter:* `const std::string& getDefaultPointsShader() const`

Scene-wide custom shader for Points components. Same semantics as [defaultMeshShader](#defaultmeshshader).

---

### defaultLinesShader

* *Setter:* `void setDefaultLinesShader(const std::string& path)`
* *Getter:* `const std::string& getDefaultLinesShader() const`

Scene-wide custom shader for Lines components. Same semantics as [defaultMeshShader](#defaultmeshshader).

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

### setAmbientLight2D

* `void setAmbientLight2D(float intensity, Vector3 color)`
* `void setAmbientLight2D(float intensity)`
* `void setAmbientLight2D(Vector3 color)`

Sets the ambient light for the **2D lighting path** (see [Light2D](light2d.md)). Every [Light2D](light2d.md) adds on top of this base level, so dim the ambient to make 2D lights visible. Separate from [setGlobalIllumination](#setglobalillumination), which drives the 3D PBR ambient.

=== "C++"

    ```cpp
    scene.setAmbientLight2D(0.15f, Vector3(0.9f, 0.9f, 1.0f)); // dark, blueish night
    ```

=== "Lua"

    ```lua
    scene:setAmbientLight2D(0.15, Vector3(0.9, 0.9, 1.0)) -- dark, blueish night
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
