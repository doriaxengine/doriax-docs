---
description: Fog API reference (C++ and Lua).
---

# Fog

**Inherits:** [EntityHandle](entityhandle.md)  
**C++ type:** `Fog`

## Description

Applies atmospheric fog to a scene. Fog blends the scene's rendered colour towards a fog colour based on the depth of each fragment from the camera, simulating haze, mist, or distance-based visibility falloff.

Three fog models are supported: linear, exponential, and squared-exponential.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [FogType](#fogtype) | [type](#type) | `LINEAR` | C++ \| Lua |
| Vector3 | [color](#color) | `(0.8, 0.8, 0.8)` | C++ \| Lua |
| float | [density](#density) | `0.01` | C++ \| Lua |
| float | [linearStart](#linearstart-linearend) | `10.0` | C++ \| Lua |
| float | [linearEnd](#linearstart-linearend) | `100.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setType](#type) | C++ \| Lua |
| void | [setColor](#color) | C++ \| Lua |
| void | [setDensity](#density) | C++ \| Lua |
| void | [setLinearStart](#linearstart-linearend) | C++ \| Lua |
| void | [setLinearEnd](#linearstart-linearend) | C++ \| Lua |
| void | [setLinearStartEnd](#linearstart-linearend) | C++ \| Lua |

## Enumerations

### FogType

* **LINEAR** — Fog increases linearly between `linearStart` and `linearEnd` distances. Full opacity at `linearEnd`.
* **EXPONENTIAL** — Fog uses the formula `exp(-density * d)`. Grows gradually regardless of distance bounds.
* **EXPONENTIALSQUARED** — Fog uses `exp(-(density * d)²)`. More concentrated near objects, faster roll-off.

---

## Property details

### type

* *Setter*: void **setType**([FogType](#fogtype) type)
* *Getter*: [FogType](#fogtype) **getType**() const

The fog calculation model.

=== "C++"
    ```cpp
    Fog fog(&scene);
    fog.setType(FogType::LINEAR);
    fog.setColor(Vector3(0.7f, 0.8f, 0.9f));
    fog.setLinearStartEnd(50.0f, 200.0f);
    ```

=== "Lua"
    ```lua
    local fog = Fog(scene)
    fog.type = FogType.LINEAR
    fog.color = Vector3(0.7, 0.8, 0.9)
    fog:setLinearStartEnd(50, 200)
    ```

---

### color

* *Setter*: void **setColor**(Vector3 color)
* *Setter*: void **setColor**(float red, float green, float blue)
* *Getter*: Vector3 **getColor**() const

The fog colour in linear space. Match this to your sky colour for a natural-looking effect.

---

### density

* *Setter*: void **setDensity**(float density)
* *Getter*: float **getDensity**() const

The density coefficient for `EXPONENTIAL` and `EXPONENTIALSQUARED` modes. Larger values produce thicker fog.

---

### linearStart / linearEnd

* *Setter*: void **setLinearStart**(float start) / **setLinearEnd**(float end)
* *Setter*: void **setLinearStartEnd**(float start, float end)
* *Getter*: float **getLinearStart**() / **getLinearEnd**() const

The near and far clip distances for `LINEAR` fog. Objects closer than `linearStart` are unaffected; objects beyond `linearEnd` are fully in the fog colour.
