---
description: Particles API reference (C++ and Lua).
---

# Particles

**Inherits:** [Action](action.md)  
**C++ type:** `Particles`

## Description

A GPU-accelerated particle emitter driven by the [Action](action.md) system. `Particles` handles birth, lifetime, movement, colour, and death for large numbers of small quads (sprites) to create effects such as fire, smoke, sparks, rain, and explosions.

The emitter has two layers of per-particle customisation:

* **Initializers** — applied once at birth to set the particle's starting value.
* **Modifiers** — applied over the particle's lifetime to interpolate a value from one state to another, with optional easing.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| unsigned int | [maxParticles](#maxparticles) | `100` | C++ \| Lua |
| int | [rate](#rate) | `10` | C++ \| Lua |
| int | [maxPerUpdate](#maxperupdate) | `10` | C++ \| Lua |
| bool | [emitter](#emitter) | `true` | C++ \| Lua |
| bool | [loop](#loop) | `true` | C++ \| Lua |
| bool | [localSpace](#localspace) | `false` | C++ \| Lua |
| [ParticleEmitterShape](#particleemittershape) | [emitterShape](#emittershape) | `Box` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [reset](#reset) | C++ \| Lua |
| void | [setLifeInitializer](#setlifeinitializer) | C++ \| Lua |
| void | [setPositionInitializer](#setpositioninitializer) | C++ \| Lua |
| void | [setSpherePositionInitializer](#setspherepositioninitializer) | C++ \| Lua |
| void | [setHemispherePositionInitializer](#sethemispherepositioninitializer) | C++ \| Lua |
| void | [setCirclePositionInitializer](#setcirclepositioninitializer) | C++ \| Lua |
| void | [setConePositionInitializer](#setconepositioninitializer) | C++ \| Lua |
| void | [setPositionModifier](#setpositionmodifier) | C++ \| Lua |
| void | [addBurst](#addburst-setbursts-clearbursts) | C++ \| Lua |
| void | [setBursts](#addburst-setbursts-clearbursts) | C++ \| Lua |
| void | [clearBursts](#addburst-setbursts-clearbursts) | C++ \| Lua |
| void | [setVelocityInitializer](#setvelocityinitializer) | C++ \| Lua |
| void | [setVelocityModifier](#setvelocitymodifier) | C++ \| Lua |
| void | [setAccelerationInitializer](#setaccelerationinitializer) | C++ \| Lua |
| void | [setAccelerationModifier](#setaccelerationmodifier) | C++ \| Lua |
| void | [setColorInitializer](#setcolorinitializer) | C++ \| Lua |
| void | [setColorModifier](#setcolormodifier) | C++ \| Lua |
| void | [addColorGradientStop](#addcolorgradientstop-setcolorgradient-clearcolorgradient-setcolorgradientusesrgb) | C++ \| Lua |
| void | [setColorGradient](#addcolorgradientstop-setcolorgradient-clearcolorgradient-setcolorgradientusesrgb) | C++ \| Lua |
| void | [clearColorGradient](#addcolorgradientstop-setcolorgradient-clearcolorgradient-setcolorgradientusesrgb) | C++ \| Lua |
| void | [setColorGradientUseSRGB](#addcolorgradientstop-setcolorgradient-clearcolorgradient-setcolorgradientusesrgb) | C++ \| Lua |
| void | [setAlphaInitializer](#setalphainitializer) | C++ \| Lua |
| void | [setAlphaModifier](#setalphamodifier) | C++ \| Lua |
| void | [setSizeInitializer](#setsizeinitializer) | C++ \| Lua |
| void | [setSizeModifier](#setsizemodifier) | C++ \| Lua |
| void | [setSpriteIntializer](#setspriteinitializer) | C++ \| Lua |
| void | [setSpriteModifier](#setspritemodifier) | C++ \| Lua |
| void | [setRotationInitializer](#setrotationinitializer) | C++ \| Lua |
| void | [setRotationModifier](#setrotationmodifier) | C++ \| Lua |
| void | [setScaleInitializer](#setscaleinitializer) | C++ \| Lua |
| void | [setScaleModifier](#setscalemodifier) | C++ \| Lua |

## Enumerations

### ParticleEmitterShape

The volume from which new particles are spawned.

* **Box** — Particles spawn within a box region defined by [setPositionInitializer](#setpositioninitializer).
* **Sphere** — Particles spawn within a sphere. Configure with [setSpherePositionInitializer](#setspherepositioninitializer).
* **Hemisphere** — Particles spawn within the upper hemisphere. Configure with [setHemispherePositionInitializer](#sethemispherepositioninitializer).
* **Circle** — Particles spawn on a flat circle. Configure with [setCirclePositionInitializer](#setcirclepositioninitializer).
* **Cone** — Particles spawn inside a cone pointing upward. Configure with [setConePositionInitializer](#setconepositioninitializer).

---

## Property details

### maxParticles

* *Setter*: void **setMaxParticles**(unsigned int maxParticles)
* *Getter*: unsigned int **getMaxParticles**() const

The maximum number of particles alive at any time. Increase this for denser effects; be mindful of GPU/CPU budget.

---

### rate

* *Setter*: void **setRate**(int rate)
* *Getter*: int **getRate**() const

Number of new particles spawned per second while the emitter is active.

---

### maxPerUpdate

* *Setter*: void **setMaxPerUpdate**(int maxPerUpdate)
* *Getter*: int **getMaxPerUpdate**() const

Caps the number of new particles spawned in a single update tick. Prevents a very long delta time (e.g. after a frame spike) from spawning hundreds of particles in one frame.

---

### emitter

* *Setter*: void **setEmitter**(bool emitter)
* *Getter*: bool **isEmitter**() const

When `true`, the particle system actively spawns new particles at the configured [rate](#rate). Set to `false` to stop new emissions while allowing existing particles to finish their lifetime.

---

### loop

* *Setter*: void **setLoop**(bool loop)
* *Getter*: bool **isLoop**() const

When `true`, the particle system restarts automatically after all particles have died. When `false`, the system stops after the first complete emission cycle.

---

### localSpace

* *Setter*: void **setLocalSpace**(bool localSpace)
* *Getter*: bool **isLocalSpace**() const

When `true`, particle positions are in local object space — they move with the emitter entity. When `false` (default), positions are in world space — particles continue along their trajectories even after the emitter moves.

---

### emitterShape

* *Setter*: void **setPositionInitializerShape**([ParticleEmitterShape](#particleemittershape) shape)
* *Getter*: [ParticleEmitterShape](#particleemittershape) **getPositionInitializerShape**() const

The spawn volume for new particles. See [ParticleEmitterShape](#particleemittershape).

---

## Method details

### reset

* void **reset**()

Immediately destroys all live particles and resets the emitter to its initial state.

---

### setLifeInitializer

* void **setLifeInitializer**(float life)
* void **setLifeInitializer**(float minLife, float maxLife)

Set how long (in seconds) each particle lives. The two-argument form randomises lifetime between `minLife` and `maxLife`.

---

### setPositionInitializer

* void **setPositionInitializer**(Vector3 position)
* void **setPositionInitializer**(Vector3 minPosition, Vector3 maxPosition)

Sets the spawn position (or random range) relative to the emitter. For Box shape, `minPosition` and `maxPosition` define the box corners.

=== "C++"
    ```cpp
    Particles fire(&scene);
    fire.setLifeInitializer(1.5f, 2.5f);
    fire.setPositionInitializer(Vector3(-0.5f, 0, -0.5f), Vector3(0.5f, 0, 0.5f));
    fire.setVelocityInitializer(Vector3(-0.2f, 1.0f, -0.2f), Vector3(0.2f, 2.0f, 0.2f));
    fire.start();
    ```

=== "Lua"
    ```lua
    local fire = Particles(scene)
    fire:setLifeInitializer(1.5, 2.5)
    fire:setPositionInitializer(Vector3(-0.5, 0, -0.5), Vector3(0.5, 0, 0.5))
    fire:setVelocityInitializer(Vector3(-0.2, 1.0, -0.2), Vector3(0.2, 2.0, 0.2))
    fire:start()
    ```

---

### setSpherePositionInitializer

* void **setSpherePositionInitializer**(float radius)
* void **setSpherePositionInitializer**(float radius, float innerRadius)

Spawns particles within a sphere of the given radius. `innerRadius` creates a hollow sphere (donut shape) — particles only spawn in the shell between `innerRadius` and `radius`.

---

### setHemispherePositionInitializer

* void **setHemispherePositionInitializer**(float radius)
* void **setHemispherePositionInitializer**(float radius, float innerRadius)

Spawns particles within the upper hemisphere (Y ≥ 0). Useful for upward explosions or fountain effects.

---

### setCirclePositionInitializer

* void **setCirclePositionInitializer**(float radius)
* void **setCirclePositionInitializer**(float radius, float innerRadius)

Spawns particles on a flat circle in the XZ plane. `innerRadius` creates a ring.

---

### setConePositionInitializer

* void **setConePositionInitializer**(float angle, float height)

Spawns particles inside a cone. `angle` is the half-angle of the cone (in degrees or radians depending on `Engine::useDegrees`), and `height` is its vertical extent.

---

### setPositionModifier

* void **setPositionModifier**(float fromTime, float toTime, Vector3 fromPosition, Vector3 toPosition)
* void **setPositionModifier**(float fromTime, float toTime, Vector3 fromPosition, Vector3 toPosition, EaseType functionType)

Adds a position offset over the particle's normalised lifetime (0 = birth, 1 = death). The `fromTime` and `toTime` values are in the `[0, 1]` range. An optional [EaseType](timedaction.md#easetype) controls interpolation.

---

### addBurst / setBursts / clearBursts

* void **addBurst**(float time, int count)
* void **addBurst**(float time, int minCount, int maxCount)
* void **setBursts**(std::vector\<ParticleBurst\> bursts)
* void **clearBursts**()

Bursts spawn a fixed number of particles at a specific time (in seconds) during the emitter's cycle, independent of [rate](#rate). Useful for explosions.

=== "C++"
    ```cpp
    Particles explosion(&scene);
    explosion.setEmitter(false);
    explosion.addBurst(0.0f, 50, 80);  // spawn 50–80 particles at t=0
    explosion.setLoop(false);
    explosion.start();
    ```

=== "Lua"
    ```lua
    local explosion = Particles(scene)
    explosion.emitter = false
    explosion:addBurst(0.0, 50, 80)
    explosion.loop = false
    explosion:start()
    ```

---

### setVelocityInitializer

* void **setVelocityInitializer**(Vector3 velocity)
* void **setVelocityInitializer**(Vector3 minVelocity, Vector3 maxVelocity)

Sets the initial velocity (units per second) at birth. The range form picks a random velocity for each particle between `minVelocity` and `maxVelocity`.

---

### setVelocityModifier

* void **setVelocityModifier**(float fromTime, float toTime, Vector3 fromVelocity, Vector3 toVelocity)
* void **setVelocityModifier**(float fromTime, float toTime, Vector3 fromVelocity, Vector3 toVelocity, EaseType functionType)

Interpolates the particle's velocity offset over its normalised lifetime. Times are in the `[0, 1]` range.

---

### setAccelerationInitializer

* void **setAccelerationInitializer**(Vector3 acceleration)
* void **setAccelerationInitializer**(Vector3 minAcceleration, Vector3 maxAcceleration)

Sets a constant per-particle acceleration (like gravity) applied from birth. Use `Vector3(0, -9.81f, 0)` to simulate gravity.

---

### setAccelerationModifier

* void **setAccelerationModifier**(float fromTime, float toTime, Vector3 fromAcceleration, Vector3 toAcceleration)
* void **setAccelerationModifier**(float fromTime, float toTime, Vector3 fromAcceleration, Vector3 toAcceleration, EaseType functionType)

Animates the per-particle acceleration offset over its normalised lifetime.

---

### setColorInitializer

* void **setColorInitializer**(Vector3 color)
* void **setColorInitializer**(Vector3 minColor, Vector3 maxColor)

Sets the particle's initial linear-space RGB colour. The range form randomises colour per particle.

---

### setColorModifier

* void **setColorModifier**(float fromTime, float toTime, Vector3 fromColor, Vector3 toColor)
* void **setColorModifier**(float fromTime, float toTime, Vector3 fromColor, Vector3 toColor, EaseType functionType)

Lerps colour over the particle's normalised lifetime. Times are in `[0, 1]`.

---

### addColorGradientStop / setColorGradient / clearColorGradient / setColorGradientUseSRGB

* void **addColorGradientStop**(float time, Vector3 color)
* void **setColorGradient**(std::vector\<ParticleColorGradientStop\> stops)
* void **clearColorGradient**()
* void **setColorGradientUseSRGB**(bool useSRGB)

Defines a multi-stop colour gradient applied over the particle's lifetime instead of a simple two-point modifier. `addColorGradientStop()` adds one stop at `time` (0–1). `setColorGradientUseSRGB()` enables perceptually-linear interpolation through sRGB colour space.

=== "C++"
    ```cpp
    fire.addColorGradientStop(0.0f, Vector3(1.0f, 0.6f, 0.0f));  // orange
    fire.addColorGradientStop(0.5f, Vector3(1.0f, 0.1f, 0.0f));  // red
    fire.addColorGradientStop(1.0f, Vector3(0.2f, 0.2f, 0.2f));  // smoke grey
    ```

=== "Lua"
    ```lua
    fire:addColorGradientStop(0.0, Vector3(1.0, 0.6, 0.0))
    fire:addColorGradientStop(0.5, Vector3(1.0, 0.1, 0.0))
    fire:addColorGradientStop(1.0, Vector3(0.2, 0.2, 0.2))
    ```

---

### setAlphaInitializer

* void **setAlphaInitializer**(float alpha)
* void **setAlphaInitializer**(float minAlpha, float maxAlpha)

Sets the initial opacity for each particle. `1.0` = fully opaque, `0.0` = invisible.

---

### setAlphaModifier

* void **setAlphaModifier**(float fromTime, float toTime, float fromAlpha, float toAlpha)
* void **setAlphaModifier**(float fromTime, float toTime, float fromAlpha, float toAlpha, EaseType functionType)

Animates opacity over the particle's normalised lifetime. For a fade-out effect, use `fromTime=0, toTime=1, fromAlpha=1, toAlpha=0`.

---

### setSizeInitializer

* void **setSizeInitializer**(float size)
* void **setSizeInitializer**(float minSize, float maxSize)

Sets the initial uniform size of each particle in world units.

---

### setSizeModifier

* void **setSizeModifier**(float fromTime, float toTime, float fromSize, float toSize)
* void **setSizeModifier**(float fromTime, float toTime, float fromSize, float toSize, EaseType functionType)

Animates particle size over its normalised lifetime.

---

### setSpriteInitializer

* void **setSpriteIntializer**(std::vector\<int\> frames)
* void **setSpriteIntializer**(int minFrame, int maxFrame)

Sets which sprite atlas frame each particle shows at birth. The vector form provides an explicit list to pick from randomly; the two-integer form picks a random frame in the range.

Requires the emitter mesh to have an atlas configured (see [Sprite](sprite.md) frame definitions).

---

### setSpriteModifier

* void **setSpriteModifier**(float fromTime, float toTime, std::vector\<int\> frames)
* void **setSpriteModifier**(float fromTime, float toTime, std::vector\<int\> frames, EaseType functionType)

Cycles through a list of sprite frames during the particle's lifetime, enabling flip-book animation.

---

### setRotationInitializer

* void **setRotationInitializer**(Quaternion rotation)
* void **setRotationInitializer**(float rotation)
* void **setRotationInitializer**(Quaternion minRotation, Quaternion maxRotation)
* void **setRotationInitializer**(float minRotation, float maxRotation)

Sets the initial rotation of each particle. The scalar overload takes an angle (degrees or radians per `Engine::useDegrees`) around the Z axis for 2D-style billboard rotation.

---

### setRotationModifier

* void **setRotationModifier**(float fromTime, float toTime, float fromRotation, float toRotation)
* void **setRotationModifier**(float fromTime, float toTime, Quaternion fromRotation, Quaternion toRotation)
* void **setRotationModifier**(float fromTime, float toTime, float fromRotation, float toRotation, EaseType functionType)

Animates rotation over the particle's normalised lifetime.

---

### setScaleInitializer

* void **setScaleInitializer**(float scale)
* void **setScaleInitializer**(Vector3 scale)
* void **setScaleInitializer**(float minScale, float maxScale)
* void **setScaleInitializer**(Vector3 minScale, Vector3 maxScale)

Sets the initial scale at birth. Use the `Vector3` overload for non-uniform scale.

---

### setScaleModifier

* void **setScaleModifier**(float fromTime, float toTime, float fromScale, float toScale)
* void **setScaleModifier**(float fromTime, float toTime, Vector3 fromScale, Vector3 toScale)
* void **setScaleModifier**(float fromTime, float toTime, Vector3 fromScale, Vector3 toScale, EaseType functionType)

Animates the particle's scale over its normalised lifetime. Useful for particles that shrink as they die.
