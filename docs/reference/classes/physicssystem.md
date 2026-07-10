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

`gravity2D` and `gravity3D` set each world's gravity independently (m/s²); the legacy `gravity` / `setGravity(...)` sets both worlds at once and reads back the 3D value. The same values are exposed directly on [Scene](scene.md#gravity2d) — `scene.gravity2D` / `scene.gravity3D` — which is what the editor's scene **Physics** section edits and saves.

=== "Lua"

    ```lua
    local physics = scene:getPhysicsSystem()
    physics.gravity2D = Vector2(0, -20)
    physics.gravity3D = Vector3(0, -3.7, 0)
    ```

## Events

**2D:** `beginContact2D`, `endContact2D`, `hitContact2D`, sensor contacts, `preSolve2D`, `shouldCollide2D`

**3D:** `onContactAdded3D`, `onContactRemoved3D`, `onBodyActivated3D`, `shouldCollide3D`

=== "Lua"

    ```lua
    RegisterEvent(self, physics.beginContact2D, "onHit")
    ```

See [Events](../../manual/events.md). Use `onFixedUpdate` for forces.
