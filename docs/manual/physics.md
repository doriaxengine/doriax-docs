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
