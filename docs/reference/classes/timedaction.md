---
description: TimedAction API reference (C++ and Lua).
---

# TimedAction

**Inherits:** [Action](action.md)  
**C++ type:** `TimedAction`

## Description

Base class for all fixed-duration tweens. `TimedAction` drives a single value from `0.0` to `1.0` over a specified number of seconds, optionally with an easing curve. Concrete subclasses ([AlphaAction](alphaaction.md), [ColorAction](coloraction.md), [PositionAction](positionaction.md), [RotationAction](rotationaction.md), [ScaleAction](scaleaction.md)) apply that interpolated value to a specific property of the target object.

You typically do not instantiate `TimedAction` directly.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| float | [duration](#duration) | `1.0` | C++ \| Lua |
| bool | [loop](#loop) | `false` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setFunctionType](#setfunctiontype) | C++ \| Lua |
| float | [getValue](#getvalue-gettime) | C++ \| Lua |
| float | [getTime](#getvalue-gettime) | C++ \| Lua |
| void | [setDuration](#duration) | C++ \| Lua |
| float | [getDuration](#duration) | C++ \| Lua |
| void | [setLoop](#loop) | C++ \| Lua |
| bool | [isLoop](#loop) | C++ \| Lua |

## Enumerations

### EaseType

Controls the interpolation curve applied to the tween.

* **LINEAR** — Constant speed from start to end.
* **QUAD_IN / QUAD_OUT / QUAD_IN_OUT** — Quadratic easing (gentle acceleration or deceleration).
* **CUBIC_IN / CUBIC_OUT / CUBIC_IN_OUT** — Cubic easing (stronger acceleration or deceleration).
* **QUART_IN / QUART_OUT / QUART_IN_OUT** — Quartic easing.
* **QUINT_IN / QUINT_OUT / QUINT_IN_OUT** — Quintic easing.
* **SINE_IN / SINE_OUT / SINE_IN_OUT** — Sinusoidal easing (smooth, natural motion).
* **EXPO_IN / EXPO_OUT / EXPO_IN_OUT** — Exponential easing (very sharp).
* **CIRC_IN / CIRC_OUT / CIRC_IN_OUT** — Circular easing.
* **ELASTIC_IN / ELASTIC_OUT / ELASTIC_IN_OUT** — Elastic spring overshoot.
* **BACK_IN / BACK_OUT / BACK_IN_OUT** — Slight overshoot (anticipation).
* **BOUNCE_IN / BOUNCE_OUT / BOUNCE_IN_OUT** — Bouncing ball effect.
* **STEP** — Hold the start value and jump at the end; on keyframe tracks, holds each
  key's value until the next key (how GLTF `STEP` clips import).
* **CUSTOM** — Provide your own ease function via the `Ease` overloads.

---

## Property details

### duration

* *Setter*: void **setDuration**(float duration)
* *Getter*: float **getDuration**() const

Length of the tween in **seconds**.

---

### loop

* *Setter*: void **setLoop**(bool loop)
* *Getter*: bool **isLoop**() const

When `true`, the tween restarts from the beginning after completing.

---

## Method details

### setFunctionType

* void **setFunctionType**([EaseType](#easetype) functionType)

Apply an easing curve to the tween. See [EaseType](#easetype) for available values.

---

### getValue / getTime

* float **getValue**() const
* float **getTime**() const

`getValue()` returns the current eased output value in `[0, 1]`. `getTime()` returns the current elapsed time in seconds.
