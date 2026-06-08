---
description: Light API reference (C++ and Lua).
---

# Light

**Inherits:** [Object](object.md)  
**C++ type:** `Light`

## Description

Represents a light source in a 3D scene. Doriax supports three light types — directional, point, and spot — all sharing the same `Light` class. The light type determines which properties have effect: a directional light uses `direction` and an unlimited `range`, a point light radiates in all directions with a finite `range`, and a spot light uses both `direction` and cone angles.

Shadows are opt-in per-light and render via a shadow map. Cascaded shadow maps (CSM) are available for directional lights to spread shadow quality across a large view distance.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [LightType](#lighttype) | [type](#type) | `DIRECTIONAL` | C++ \| Lua |
| Vector3 | [direction](#direction) | `(0,-1,0)` | C++ \| Lua |
| Vector3 | [color](#color) | `(1,1,1)` | C++ \| Lua |
| float | [range](#range) | `10.0` | C++ \| Lua |
| float | [intensity](#intensity) | `1.0` | C++ \| Lua |
| float | [innerConeAngle](#innerconeangle-outerconeangle) | `10°` | C++ \| Lua |
| float | [outerConeAngle](#innerconeangle-outerconeangle) | `45°` | C++ \| Lua |
| bool | [shadows](#shadows) | `false` | C++ \| Lua |
| float | [bias](#bias) | `0.005` | C++ \| Lua |
| unsigned int | [shadowMapSize](#shadowmapsize) | `1024` | C++ \| Lua |
| float | [cameraNear](#cameranear-camerafar) | `0.1` | C++ \| Lua |
| float | [cameraFar](#cameranear-camerafar) | `100.0` | C++ \| Lua |
| bool | [automaticShadowCamera](#automaticshadowcamera) | `true` | C++ \| Lua |
| unsigned int | [numCascades](#numcascades) | `1` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setType](#type) | C++ \| Lua |
| LightType | [getType](#type) | C++ \| Lua |
| void | [setDirection](#direction) | C++ \| Lua |
| Vector3 | [getDirection](#direction) | C++ \| Lua |
| void | [setColor](#color) | C++ \| Lua |
| Vector3 | [getColor](#color) | C++ \| Lua |
| void | [setRange](#range) | C++ \| Lua |
| float | [getRange](#range) | C++ \| Lua |
| void | [setIntensity](#intensity) | C++ \| Lua |
| float | [getIntensity](#intensity) | C++ \| Lua |
| void | [setConeAngle](#innerconeangle-outerconeangle) | C++ \| Lua |
| void | [setInnerConeAngle](#innerconeangle-outerconeangle) | C++ \| Lua |
| float | [getInnerConeAngle](#innerconeangle-outerconeangle) | C++ \| Lua |
| void | [setOuterConeAngle](#innerconeangle-outerconeangle) | C++ \| Lua |
| float | [getOuterConeAngle](#innerconeangle-outerconeangle) | C++ \| Lua |
| void | [setShadows](#shadows) | C++ \| Lua |
| bool | [isShadows](#shadows) | C++ \| Lua |
| void | [setBias](#bias) | C++ \| Lua |
| float | [getBias](#bias) | C++ \| Lua |
| void | [setShadowMapSize](#shadowmapsize) | C++ \| Lua |
| unsigned int | [getShadowMapSize](#shadowmapsize) | C++ \| Lua |
| void | [setShadowCameraNearFar](#cameranear-camerafar) | C++ \| Lua |
| void | [setCameraNear](#cameranear-camerafar) | C++ \| Lua |
| float | [getCameraNear](#cameranear-camerafar) | C++ \| Lua |
| void | [setCameraFar](#cameranear-camerafar) | C++ \| Lua |
| float | [getCameraFar](#cameranear-camerafar) | C++ \| Lua |
| void | [setAutomaticShadowCamera](#automaticshadowcamera) | C++ \| Lua |
| bool | [isAutomaticShadowCamera](#automaticshadowcamera) | C++ \| Lua |
| void | [setNumCascades](#numcascades) | C++ \| Lua |
| float | [getNumCascades](#numcascades) | C++ \| Lua |

## Enumerations

### LightType

* **DIRECTIONAL** - A light that shines uniformly in one direction from infinitely far away, like the sun. Position is irrelevant; only `direction` matters.
* **POINT** - A light that radiates equally in all directions from its world-space position, like a light bulb. Use `range` and `intensity` to control reach.
* **SPOT** - A cone-shaped light emanating from its world-space position in the given `direction`. Use `innerConeAngle` and `outerConeAngle` to shape the cone.

---

## Property details

### type

* *Setter*: void **setType**([LightType](#lighttype) type)
* *Getter*: [LightType](#lighttype) **getType**() const

The light model to use. See [LightType](#lighttype) for the available values. Changing the type at run-time is supported.

=== "C++"
    ```cpp
    Light sun(&scene);
    sun.setType(LightType::DIRECTIONAL);
    sun.setDirection(Vector3(-0.5f, -1.0f, -0.5f));
    ```

=== "Lua"
    ```lua
    local sun = Light(scene)
    sun:setType(LightType.DIRECTIONAL)
    sun:setDirection(Vector3(-0.5, -1.0, -0.5))
    ```

---

### direction

* *Setter*: void **setDirection**(Vector3 direction)
* *Setter*: void **setDirection**(float x, float y, float z)
* *Getter*: Vector3 **getDirection**() const

The normalised direction vector the light shines *towards*. Used by `DIRECTIONAL` and `SPOT` lights.

---

### color

* *Setter*: void **setColor**(Vector3 color)
* *Setter*: void **setColor**(float r, float g, float b)
* *Getter*: Vector3 **getColor**() const

The linear-space RGB color of the emitted light. Each channel ranges from `0.0` to `1.0` for standard colours, though values above `1.0` are valid for HDR scenes.

---

### range

* *Setter*: void **setRange**(float range)
* *Getter*: float **getRange**() const

The maximum distance (in world units) at which the light has any effect. Relevant for `POINT` and `SPOT` lights. `DIRECTIONAL` lights have an infinite range and ignore this value.

---

### intensity

* *Setter*: void **setIntensity**(float intensity)
* *Getter*: float **getIntensity**() const

A multiplier applied to the light's [color](#color). `1.0` is the default. Higher values create a brighter light without altering the hue.

---

### innerConeAngle / outerConeAngle

* *Setter*: void **setConeAngle**(float inner, float outer)
* *Setter*: void **setInnerConeAngle**(float inner)
* *Getter*: float **getInnerConeAngle**() const
* *Setter*: void **setOuterConeAngle**(float outer)
* *Getter*: float **getOuterConeAngle**() const

Define the shape of a `SPOT` light. The angle is specified in degrees (or radians if `Engine::useDegrees` is `false`).

* **innerConeAngle** — the full-brightness cone. Everything inside this angle receives 100 % of the light.
* **outerConeAngle** — the penumbra edge. Light fades to zero between the inner and outer angle.

`setConeAngle()` sets both values at once.

=== "C++"
    ```cpp
    Light torch(&scene);
    torch.setType(LightType::SPOT);
    torch.setConeAngle(15.0f, 40.0f);
    ```

=== "Lua"
    ```lua
    local torch = Light(scene)
    torch:setType(LightType.SPOT)
    torch:setConeAngle(15.0, 40.0)
    ```

---

### shadows

* *Setter*: void **setShadows**(bool shadows)
* *Getter*: bool **isShadows**() const

Enables shadow map generation for this light. Shadow casting also requires the caster mesh to have `castShadows` enabled and the receiver mesh to have `receiveShadows` enabled. See the [Mesh](mesh.md) documentation.

---

### bias

* *Setter*: void **setBias**(float bias)
* *Getter*: float **getBias**() const

The shadow-map depth bias added to prevent self-shadowing artefacts (shadow acne). Increase this value if you see acne on surfaces; decrease it if you see shadows detaching from geometry (Peter-panning). A good starting value is `0.005`.

---

### shadowMapSize

* *Setter*: void **setShadowMapSize**(unsigned int size)
* *Getter*: unsigned int **getShadowMapSize**() const

The resolution of the shadow map texture in pixels (e.g. `512`, `1024`, `2048`). Higher values produce sharper shadows at the cost of GPU memory and fillrate. Must be a power of two.

---

### cameraNear / cameraFar

* *Setter*: void **setShadowCameraNearFar**(float nearValue, float farValue)
* *Setter*: void **setCameraNear**(float nearValue)
* *Getter*: float **getCameraNear**() const
* *Setter*: void **setCameraFar**(float farValue)
* *Getter*: float **getCameraFar**() const

The near and far clip planes of the shadow-map camera. Tighten these around the scene geometry to maximise shadow-map precision. `setShadowCameraNearFar()` sets both at once.

Has no effect when [automaticShadowCamera](#automaticshadowcamera) is `true`.

---

### automaticShadowCamera

* *Setter*: void **setAutomaticShadowCamera**(bool automatic)
* *Getter*: bool **isAutomaticShadowCamera**() const

When `true`, the engine automatically fits the shadow-map camera frustum around the visible scene each frame, optimising shadow quality. Disable this if you need manual control over [cameraNear / cameraFar](#cameranear-camerafar).

---

### numCascades

* *Setter*: void **setNumCascades**(unsigned int numCascades)
* *Getter*: float **getNumCascades**() const

Number of cascades for Cascaded Shadow Maps (CSM). Only relevant for `DIRECTIONAL` lights. More cascades distribute shadow-map resolution more evenly across the view frustum, reducing the "blurry distant shadows" artefact at the cost of additional render passes. Typical values are `1` (off) to `4`.
