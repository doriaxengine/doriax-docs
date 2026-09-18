---
description: PhysicsSystem API reference — Box2D and Jolt (C++ and Lua).
---

# PhysicsSystem

2D (Box2D) and 3D (Jolt) simulation. `scene:getPhysicsSystem()`.

## Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| Vector2 | gravity2D | `(0,-9.81)` | C++ \| Lua |
| Vector3 | gravity3D | `(0,-9.81,0)` | C++ \| Lua |
| Vector3 | gravity | `(0,-9.81,0)` | C++ \| Lua |
| float | pointsToMeterScale2D | `64.0` | C++ \| Lua |
| bool | lock3DBodies | `true` | C++ \| Lua |
| bool | steppingWorld3D | `false` | C++ \| Lua *(read-only)* |

`gravity2D` and `gravity3D` set each world's gravity independently (m/s²); the legacy `gravity` / `setGravity(...)` sets both worlds at once and reads back the 3D value. The same values are exposed directly on [Scene](scene.md#gravity2d) — `scene.gravity2D` / `scene.gravity3D` — which is what the editor's scene **Physics** section edits and saves.

=== "Lua"

    ```lua
    local physics = scene:getPhysicsSystem()
    physics.gravity2D = Vector2(0, -20)
    physics.gravity3D = Vector3(0, -3.7, 0)
    ```

`lock3DBodies` decides whether 3D body access takes Jolt's body locks. Leave it on unless
you drive the world from a worker thread. It is ignored while `steppingWorld3D` is true,
since the step already holds those locks.

`steppingWorld3D` is true while the 3D world simulates, which is exactly when the 3D
callbacks below run.

## Events

**2D:** `beginContact2D`, `endContact2D`, `hitContact2D`, sensor contacts, `preSolve2D`, `shouldCollide2D`

**3D:** `onContactAdded3D`, `onContactPersisted3D`, `onContactRemoved3D`, `onBodyActivated3D`, `onBodyDeactivated3D`, `shouldCollide3D`

=== "Lua"

    ```lua
    RegisterEvent(self, physics.beginContact2D, "onHit")
    ```

See [Events](../../manual/events.md). Use `onFixedUpdate` for forces.

!!! warning "A filter callback must return a value"
    `shouldCollide2D` and `shouldCollide3D` are the two events whose return value is
    read. A Lua handler that falls off the end returns `nil`, which is read as `false`
    and **rejects the contact**. The `true` default only applies when nothing is
    subscribed at all, so always end the handler with an explicit `return`.

    ```lua
    function Trap:shouldCollide(bodyA, bodyB, offset, result)
        if bodyA.entity == self.ghostEntity then
            return false
        end
        return true          -- without this, nothing collides
    end
    ```

### Inside a 3D callback

3D events fire while Jolt is stepping, on a thread that already holds the body locks:

* Reading and moving bodies is fine — velocity, position, ray casts. The engine uses
  Jolt's lock-free interfaces for the whole step.
* Creating a body or joint is **refused** and logged; the next update retries it.
* Destroying one is **queued** and applied when the step ends, so removing a
  `Body3DComponent` from a callback tears its body down properly.

Anything else belongs in `onUpdate` or `onFixedUpdate`. Check `steppingWorld3D` when a
helper can be called from both places.
