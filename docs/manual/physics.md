---
description: Integrated 2D and 3D physics in Doriax, powered by Box2D and Jolt Physics.
---

# Physics

Doriax includes integrated physics for both 2D and 3D games, so you can add realistic
movement, collisions, and interactions without external libraries.

![Physics in the editor](../assets/screenshots/editor-physics.png)

## Physics backends

| Dimension | Backend |
| --- | --- |
| 2D | [Box2D](https://box2d.org/) |
| 3D | [Jolt Physics](https://github.com/jrouwe/JoltPhysics) |

Both backends are integrated into the engine and exposed through the same ECS-based
workflow.

## Core concepts

- **Rigid bodies** — give entities physical behavior so they respond to forces and
  gravity. Bodies can be static, kinematic, or dynamic.
- **Colliders / shapes** — define the volume used for collision detection (boxes,
  spheres, capsules, polygons, and more).
- **Joints** — constrain bodies together to model hinges, sliders, and other
  mechanical connections.
- **Collision detection** — the physics system detects overlaps and contacts between
  bodies each step.

## Typical workflow

1. Add a physics body component to an entity.
2. Attach one or more collision shapes that match its geometry.
3. Configure mass, friction, restitution, and body type.
4. Let the physics system step the simulation each frame, updating transforms.

You can react to collisions in your game logic to trigger gameplay events such as
damage, pickups, or sounds.

## Gravity

Each scene has its own gravity, and the 2D and 3D worlds are independent: `gravity2D`
drives the Box2D world and `gravity3D` drives the Jolt world. Both default to
`(0, -9.81)` m/s².

In the editor, select the scene in the Properties window and set **Gravity** in the
**Physics** section — 2D scenes edit the 2D world, 3D scenes the 3D world. The value is
saved with the scene and applied in exported projects.

=== "C++"

    ```cpp
    scene.setGravity2D(Vector2(0, -20));       // snappier platformer fall
    scene.setGravity3D(Vector3(0, -3.7f, 0));  // Mars
    ```

=== "Lua"

    ```lua
    scene.gravity2D = Vector2(0, -20)
    scene.gravity3D = Vector3(0, -3.7, 0)
    ```

Scale the response per body with [Body2D — gravityScale](../reference/classes/body2d.md#gravityscale)
or [Body3D — gravityFactor](../reference/classes/body3d.md#gravityfactor). Changing
gravity at runtime does not wake sleeping bodies — they pick up the new value when
something wakes them.

## 2D physics

2D physics uses Box2D. A body can contain up to `MAX_SHAPES` shapes and each shape can
have density, friction, restitution, sensor state, and collision filtering.

| Shape | Use it for |
| --- | --- |
| Box/polygon | Platforms, crates, walls, characters with simple silhouettes |
| Circle | Balls, radial triggers, wheels |
| Capsule | Characters, rounded obstacles |
| Segment/chain | Terrain edges, one-way boundaries, outlines |

```cpp
Body2D body = object.getBody2D();
body.createBoxShape(64, 32);
body.setType(BodyType::DYNAMIC);
body.setLinearVelocity(Vector2(4, 0));
```

## 3D physics

3D physics uses Jolt Physics. Bodies can use primitives, compound shapes, mesh shapes,
or height fields. Use simple primitives for dynamic bodies whenever possible, and
reserve mesh shapes for static world geometry.

| Shape | Use it for |
| --- | --- |
| Box/sphere/capsule/cylinder | Dynamic props and characters |
| Convex hull | Medium-complexity dynamic objects |
| Mesh | Static level collision |
| Height field | Terrain collision |

```cpp
Body3D body = object.getBody3D();
body.createCapsuleShape(0.8f, 0.25f);
body.setType(BodyType::DYNAMIC);
body.setAllowedDOFs2DPlane();
```

### 3D sensors

A whole 3D body can be turned into a trigger volume with the **Sensor** flag: it still
reports contacts, but produces no collision response. Use it for checkpoints, pickup
volumes, damage zones, and detection areas.

In the editor, tick **Sensor** in the Body3D component of the Properties window. The flag
is stored on the component, so it is saved with the scene, applied in exported projects,
and kept when the body is rebuilt (for example after changing shapes). From code, set it
with [Body3D — sensor](../reference/classes/body3d.md#sensor) before or after `load()`:

=== "C++"

    ```cpp
    Body3D trigger = checkpoint.getBody3D();
    trigger.createBoxShape(2, 2, 2);
    trigger.setIsSensor(true);
    trigger.load();
    ```

=== "Lua"

    ```lua
    local trigger = checkpoint:getBody3D()
    trigger:createBoxShape(2, 2, 2)
    trigger.sensor = true
    trigger:load()
    ```

Sensor overlaps arrive through the regular 3D contact events below, and the
[Contact3D](../reference/classes/contact3d.md) passed to them carries a `sensor` flag so
trigger contacts can be told apart from solid ones. A static sensor only sees **awake**
dynamic and kinematic bodies; make the sensor itself dynamic or kinematic when it must
also detect sleeping bodies.

## Moving a body

A physics body owns its own pose. The engine syncs it with the entity's transform once
per fixed step: **transform → body** before the step, **body → transform** after it. Which
API you use depends on where your code runs.

| Where | Continuous movement | Teleport |
| --- | --- | --- |
| `onFixedUpdate` | `setLinearVelocity` / `applyForce` | `Body2D`/`Body3D` `setPosition` |
| `onUpdate` | not recommended for bodies | `Object::setPosition` also works |

!!! warning "Transform positions and rotations written in onFixedUpdate are discarded"

    `Engine::onFixedUpdate` runs **between** those two syncs. A position or rotation
    written to the transform there is read back over by the post-step sync before
    anything renders it, so the write silently does nothing — no error, no warning,
    unless you also call `Object::updateTransform()` to refresh the world transform the
    pre-step sync reads. Moving a **parent** of a body-carrying entity has the same
    effect on the body. The body pose API below avoids the whole ordering question.

    The exact scope is worth knowing:

    - **3D bodies** — always. The post-step sync writes back every body each step.
    - **2D bodies** — only when Box2D reports the body as moved. A sleeping or static
      `Body2D` produces no move event, so a transform write there survives and reaches
      the body on the next sync. Do not rely on it: whether a body sleeps is the
      simulation's decision, not yours.
    - **Scale** — not affected. Neither path writes scale back, so `Object::setScale`
      persists. Only its effect is delayed: the collider is resized once the world
      scale refreshes in the next variable-timestep pass.

Use the body's own pose API instead. It writes to the simulation directly and updates
the transform for you, so it works from any callback:

=== "C++"

    ```cpp
    void Player::onFixedUpdate() {
        // Continuous movement: let the solver do the work
        body.setLinearVelocity(Vector3(input.x * speed, body.getLinearVelocity().y, input.z * speed));

        // Teleport: write the body pose, never the transform
        if (fellOffTheMap) {
            body.setPosition(spawnPoint);
            body.setLinearVelocity(Vector3::ZERO);
        }
    }
    ```

=== "Lua"

    ```lua
    function Player:onFixedUpdate()
        body.linearVelocity = Vector3(input.x * speed, body.linearVelocity.y, input.z * speed)

        if fellOffTheMap then
            body.position = spawnPoint
            body.linearVelocity = Vector3(0, 0, 0)
        end
    end
    ```

Entities **without** a physics body have no such restriction — `Object::setPosition`
works from `onFixedUpdate` as usual.

Prefer velocities and forces over teleporting whenever the motion is continuous.
Teleporting skips collision detection between the old and new pose, so a body can pass
straight through walls. Do not scale forces or torques by `Engine::getDeltatime()`: the
solver already integrates them over the fixed step.

## Contacts and filtering

The physics system exposes contact subscriptions so you can react to collisions in game
logic. **2D bodies** use `beginContact2D`, `endContact2D`, hit, sensor, and `preSolve2D`
events — use begin/end for gameplay state, hit for impacts, and pre-solve when a contact
should be conditionally disabled. **3D bodies** instead use `onContactAdded3D`,
`onContactPersisted3D`, and `onContactRemoved3D` (plus `onBodyActivated3D` /
`onBodyDeactivated3D`); each added/persisted callback receives a
[Contact3D](../reference/classes/contact3d.md) carrying the contact normal and points.

Collision filters use category and mask bits. Put broad gameplay groups into category
bits, such as player, enemy, world, projectile, and trigger. Use masks to decide which
groups interact.

## Raycasts and ground checks

A common need for character controllers is knowing whether a body is **standing on the
ground**. Doriax has no built-in `isGrounded()` flag, but you can build a reliable check
two ways.

### Downward raycast (recommended)

Cast a short [Ray](../reference/classes/ray.md) straight down from the body's feet and
test it against the 3D physics world with `RayFilter::BODY_3D`. Checking `normal.y` lets
you reject steep walls so only near-horizontal surfaces count as ground.

```cpp
bool isGrounded(Body3D& body, Scene* scene, float feetOffset, float probe = 0.15f) {
    // feetOffset = distance from the center of mass down to the soles
    // (for a capsule: halfHeight + radius)
    Vector3 com = body.getCenterOfMassPosition();
    Vector3 origin = com - Vector3(0, feetOffset - 0.05f, 0); // start just above the soles
    Ray ray(origin, Vector3(0, -(probe + 0.05f), 0));         // direction also sets the length

    RayReturn result = ray.intersects(scene, RayFilter::BODY_3D);

    return result.hit
        && result.body != body.getEntity()  // ignore a self-hit
        && result.normal.y > 0.7f;           // ~45 degree slope limit
}
```

Pass `onlyStatic` or category/mask bits to restrict what counts as ground, for example
`ray.intersects(scene, RayFilter::BODY_3D, true, groundCategory, groundMask)`. The same
`Ray` API is available in Lua. The returned [RayReturn](../reference/classes/rayreturn.md)
also carries the hit `distance`, which is handy for step snapping or coyote-time.

### Contact normal (event-driven)

If you already subscribe to contact events, inspect the contact normal instead of
raycasting. Read [Contact3D](../reference/classes/contact3d.md)`::getWorldSpaceNormal()`
inside `onContactAdded3D` / `onContactPersisted3D`. Jolt's normal points **from body 1
toward body 2**, and Jolt — not your code — decides which body is which, so flip the sign
when your character is body 1:

```cpp
Vector3 n = contact.getWorldSpaceNormal();
Vector3 up = (bodyA.getEntity() == characterEntity) ? n * -1.0f : n;
bool grounded = up.y > 0.7f;
```

Track grounded state with a contact counter (increment on `onContactAdded3D`, decrement
on `onContactRemoved3D`) rather than a single bool, so multiple simultaneous contacts are
handled correctly.

## Joints

Doriax exposes 2D and 3D joint wrappers for constrained motion. 2D joint types include
revolute, prismatic, weld, distance, friction, and motor joints. In 3D, use constraints
and allowed degrees of freedom to lock or limit movement.

## Practical guidance

- Prefer primitive collision shapes for dynamic entities.
- Keep visual meshes and collision meshes separate.
- Use sensors for triggers, pickups, and detection volumes.
- Use fixed update logic for physics-driven gameplay.
- Tune gravity and meter scale before authoring a large scene.

## Next steps

Bring everything together and ship your game in [Export Window](../editor/export.md).
