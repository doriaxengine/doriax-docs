---
description: Particle systems in Doriax — emitters, initializers, modifiers, bursts, and rendering through points or instanced meshes.
---

# Particles

Doriax includes a CPU-simulated particle system for effects such as fire, smoke, sparks,
rain, explosions, and magic. A particle system has two parts:

| Part | Role |
| --- | --- |
| **`Particles` action** | Drives the simulation — emission rate, lifetime, initializers, modifiers, bursts. Configuration lives in `ParticlesComponent`. |
| **Render target entity** | Displays the particles — a `Points` entity (textured point sprites) or a `Mesh` with instancing (each particle is a mesh instance). |

`Particles` derives from [`Action`](../reference/classes/action.md): create it, point it
at the render target with `setTarget`, configure, and `start()`.

## Creating particles in the editor

In the **Structure panel**, right-click a render-target entity (such as a Points entity)
and choose **Create → Particles**. The editor creates an entity with `ActionComponent` +
`ParticlesComponent` and wires its action target to the parent. Tune emission settings in
the **Properties window**.

## Creating particles in code

=== "Lua"

    ```lua
    -- 1. A Points entity renders the particles as textured point sprites
    points = Points(scene)
    points:setTexture("effects/spark.png")

    -- 2. The Particles action simulates and emits into the target
    particles = Particles(scene)
    particles:setTarget(points)

    particles.rate = 50          -- particles emitted per second (property in Lua)
    particles.loop = true

    particles:setLifeInitializer(1.0, 2.0)                      -- min, max seconds
    particles:setSpherePositionInitializer(0.5)                 -- emit within a sphere
    particles:setVelocityInitializer(Vector3(-1, 2, -1), Vector3(1, 4, 1))
    particles:setAccelerationInitializer(Vector3(0, -9.8, 0))   -- gravity
    particles:setSizeInitializer(10, 30)

    -- Fade out between 1s and 2s of each particle's life
    particles:setAlphaModifier(1.0, 2.0, 1.0, 0.0)

    particles:start()
    ```

=== "C++"

    ```cpp
    Points points(&scene);
    points.setTexture("effects/spark.png");

    Particles particles(&scene);
    particles.setTarget(&points);

    particles.setRate(50);
    particles.setLoop(true);

    particles.setLifeInitializer(1.0f, 2.0f);
    particles.setSpherePositionInitializer(0.5f);
    particles.setVelocityInitializer(Vector3(-1, 2, -1), Vector3(1, 4, 1));
    particles.setAccelerationInitializer(Vector3(0, -9.8f, 0));
    particles.setSizeInitializer(10.0f, 30.0f);
    particles.setAlphaModifier(1.0f, 2.0f, 1.0f, 0.0f);

    particles.start();
    ```

!!! note "Lua properties vs. C++ setters"
    Emitter settings (`rate`, `loop`, `emitter`, `localSpace`, `maxPerUpdate`,
    `emitterShape`) are **properties** in Lua and `set…()` methods in C++. The
    initializer/modifier calls use the same `set…` form in both languages.

## Initializers and modifiers

Every particle property follows the same pattern:

- An **initializer** sets the value when the particle spawns. Passing two values picks a
  random value in that range per particle.
- A **modifier** interpolates the value between two points of the particle's lifetime
  (`fromTime` and `toTime`, in **seconds** of the particle's life), optionally shaped by
  an [`EaseType`](animation.md#easing-curves).

| Property | Initializer | Modifier |
| --- | --- | --- |
| Lifetime | `setLifeInitializer(min, max)` | — |
| Position | `setPositionInitializer(...)` + shape helpers | `setPositionModifier(...)` |
| Velocity | `setVelocityInitializer(...)` | `setVelocityModifier(...)` |
| Acceleration | `setAccelerationInitializer(...)` | `setAccelerationModifier(...)` |
| Color | `setColorInitializer(...)` | `setColorModifier(...)` or color gradient |
| Alpha | `setAlphaInitializer(...)` | `setAlphaModifier(...)` |
| Size | `setSizeInitializer(...)` | `setSizeModifier(...)` |
| Rotation | `setRotationInitializer(...)` | `setRotationModifier(...)` |
| Scale | `setScaleInitializer(...)` | `setScaleModifier(...)` (instanced mesh targets) |
| Sprite frame | `setSpriteIntializer(...)` | `setSpriteModifier(...)` |

## Emitter shapes

Position initializers can emit from a volume or surface:

| Shape | Helper |
| --- | --- |
| Box (min/max corners) | `setPositionInitializer(minPosition, maxPosition)` |
| Sphere | `setSpherePositionInitializer(radius [, innerRadius])` |
| Hemisphere | `setHemispherePositionInitializer(radius [, innerRadius])` |
| Circle | `setCirclePositionInitializer(radius [, innerRadius])` |
| Cone | `setConePositionInitializer(angle, height)` |

## Bursts

Bursts emit a batch of particles at a specific time, on top of (or instead of) the
continuous `rate`:

```lua
particles:addBurst(0.0, 100)        -- 100 particles immediately
particles:addBurst(1.5, 20, 40)     -- 20–40 particles at 1.5 s
```

For a one-shot explosion, set `rate` to `0`, add a burst at time `0`, and disable
looping.

## Color gradients

Instead of a single color modifier, define a gradient over the particle's normalized
lifetime (0 = spawn, 1 = death):

```lua
particles:addColorGradientStop(0.0, Vector3(1.0, 0.9, 0.3))  -- bright yellow at spawn
particles:addColorGradientStop(0.5, Vector3(1.0, 0.3, 0.1))  -- orange mid-life
particles:addColorGradientStop(1.0, Vector3(0.2, 0.2, 0.2))  -- dark smoke at death
```

## Animated particle sprites

When the target texture is a sprite sheet (sliced with the
[Sprite Slicer](../editor/sprite-slicer.md)), particles can spawn with random frames and
animate through frames over their lifetime:

```lua
particles:setSpriteIntializer(0, 3)              -- random start frame 0–3
particles:setSpriteModifier(0.0, 2.0, {0, 1, 2, 3})
```

## Local vs. world space

By default particles simulate in **world space** — they stay behind when the emitter
moves (right for smoke trails and exhaust). Set `localSpace = true` to make particles
follow the emitter's transform (right for auras and shields attached to a character).

## Performance tips

- Prefer `Points` targets for small, camera-facing particles — they are the cheapest
  to render. Use instanced-mesh targets only when particles need real geometry.
- Keep `maxParticles` as low as the effect allows; the simulation is CPU-side.
- Use `maxPerUpdate` to cap spawn spikes after frame hitches.
- Reuse one emitter with bursts rather than creating emitters per explosion.

## See also

- [Particles](../reference/classes/particles.md) — full API reference
- [Animation](animation.md) — the action system and easing curves
- [2D Graphics](2d-graphics.md), [3D Graphics](3d-graphics.md)
