---
description: PhysicsSystem API reference — Box2D and Jolt (C++ and Lua).
---

# PhysicsSystem

2D (Box2D) and 3D (Jolt) simulation. `scene:getPhysicsSystem()`.

## Events

**2D:** `beginContact2D`, `endContact2D`, `hitContact2D`, sensor contacts, `preSolve2D`, `shouldCollide2D`

**3D:** `onContactAdded3D`, `onContactRemoved3D`, `onBodyActivated3D`, `shouldCollide3D`

=== "Lua"

    ```lua
    RegisterEvent(self, physics.beginContact2D, "onHit")
    ```

See [Events](../../manual/events.md). Use `onFixedUpdate` for forces.
