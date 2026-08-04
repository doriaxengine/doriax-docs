---
description: Body2D API reference — 2D physics body powered by Box2D, shapes, forces, filters, and contacts.
---

# Body2D

## Description

`Body2D` is the 2D rigid-body handle built on top of the **Box2D v3** physics library. Obtain one by calling `object.getBody2D()`. After creating shapes and setting properties, call `load()` to register the body with the physics world. The body position is synchronized with the parent [Object](object.md) transform automatically each physics step.

**Inherits:** [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    Sprite ball(&scene);
    ball.setTexture("ball.png");
    ball.setSize(32, 32);
    ball.createSprite();

    Body2D body = ball.getBody2D();
    body.createCircleShape(Vector2(16, 16), 16.0f);
    body.setType(BodyType::DYNAMIC);
    body.load();
    ```

=== "Lua"

    ```lua
    local ball = Sprite(scene)
    ball:setTexture("ball.png")
    ball:setSize(32, 32)
    ball:createSprite()

    local body = ball:getBody2D()
    body:createCircleShape(Vector2(16, 16), 16)
    body.type = BodyType.DYNAMIC
    body:load()
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| [BodyType](#bodytype) | [type](#type) | `STATIC` | C++ \| Lua |
| Vector2 | [position](#position-angle) | — | C++ \| Lua |
| float | [angle](#position-angle) | — | C++ \| Lua |
| Vector2 | [linearVelocity](#linearvelocity) | `(0,0)` | C++ \| Lua |
| float | [angularVelocity](#angularvelocity) | `0` | C++ \| Lua |
| float | [linearDamping](#lineardamping-angulardamping) | `0` | C++ \| Lua |
| float | [angularDamping](#lineardamping-angulardamping) | `0` | C++ \| Lua |
| bool | enableSleep | `true` | C++ \| Lua |
| bool | awake | `true` | C++ \| Lua |
| bool | [fixedRotation](#fixedrotation) | `false` | C++ \| Lua |
| bool | [bullet](#bullet) | `false` | C++ \| Lua |
| bool | enabled | `true` | C++ \| Lua |
| float | [gravityScale](#gravityscale) | `1.0` | C++ \| Lua |
| float | [mass](#mass-rotationalinertia) | — | C++ \| Lua |
| float | [rotationalInertia](#mass-rotationalinertia) | — | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [load](#load) | C++ \| Lua |
| int | [createBoxShape](#createboxshape) | C++ \| Lua |
| int | [createCenteredBoxShape](#createcenteredboxshape) | C++ \| Lua |
| int | [createRoundedBoxShape](#createroundedboxshape) | C++ \| Lua |
| int | [createPolygonShape](#createpolygonshape) | C++ \| Lua |
| int | [createCircleShape](#createcircleshape) | C++ \| Lua |
| int | [createCapsuleShape](#createcapsuleshape) | C++ \| Lua |
| int | [createSegmentShape](#createsegmentshape) | C++ \| Lua |
| int | [createChainShape](#createchainshape) | C++ \| Lua |
| void | [removeAllShapes](#removeallshapes) | C++ \| Lua |
| size_t | getNumShapes | C++ \| Lua |
| [Shape2DType](#shape2dtype) | getShapeType | C++ \| Lua |
| void | [setShapeDensity](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| float | [getShapeDensity](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| void | [setShapeFriction](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| float | [getShapeFriction](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| void | [setShapeRestitution](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| float | [getShapeRestitution](#setshapedensity-setshapefriction-setshaperestitution) | C++ \| Lua |
| void | [setShapeEnableHitEvents](#setshapeenablehitevents-setshapecontactevents-setshapepresolveevents-setshapesensorevents) | C++ \| Lua |
| void | [setShapeContactEvents](#setshapeenablehitevents-setshapecontactevents-setshapepresolveevents-setshapesensorevents) | C++ \| Lua |
| void | [setShapePreSolveEvents](#setshapeenablehitevents-setshapecontactevents-setshapepresolveevents-setshapesensorevents) | C++ \| Lua |
| void | [setShapeSensorEvents](#setshapeenablehitevents-setshapecontactevents-setshapepresolveevents-setshapesensorevents) | C++ \| Lua |
| void | [setBitsFilter](#setbitsfilter) | C++ \| Lua |
| void | [setCategoryBitsFilter](#setbitsfilter) | C++ \| Lua |
| void | [setMaskBitsFilter](#setbitsfilter) | C++ \| Lua |
| void | [setGroupIndexFilter](#setbitsfilter) | C++ \| Lua |
| void | [applyMassFromShapes](#applymassfromshapes) | C++ \| Lua |
| void | [applyForce](#applyforce) | C++ \| Lua |
| void | [applyForceToCenter](#applyforcetocenter) | C++ \| Lua |
| void | [applyTorque](#applytorque) | C++ \| Lua |
| void | [applyLinearImpulse](#applylinearimpulse-applylinearimpulsetocenter) | C++ \| Lua |
| void | [applyLinearImpulseToCenter](#applylinearimpulse-applylinearimpulsetocenter) | C++ \| Lua |
| void | [applyAngularImpulse](#applyangularimpulse) | C++ \| Lua |
| std::vector\<Contact2D\> | [getBodyContacts](#getbodycontacts-getshapecontacts) | C++ \| Lua |
| std::vector\<Contact2D\> | [getShapeContacts](#getbodycontacts-getshapecontacts) | C++ \| Lua |
| Object | [getAttachedObject](#getattachedobject) | C++ \| Lua |
| float | [getPointsToMeterScale](#getpointstometerscale) | C++ \| Lua |

## Enumerations

### BodyType

* **STATIC** — Does not move; infinite mass. Used for ground, walls, and platforms.
* **KINEMATIC** — Moved by setting velocity directly, not by forces. Collides with dynamic bodies.
* **DYNAMIC** — Fully simulated; responds to forces, torques, and gravity.

---

### Shape2DType

* **BOX** — Rectangular polygon shape.
* **CIRCLE** — Circle shape defined by center and radius.
* **CAPSULE** — Two circles connected by a rectangle.
* **POLYGON** — Arbitrary convex polygon.
* **SEGMENT** — Line segment (edge shape, no volume).
* **CHAIN** — Connected chain of line segments; can be open or closed.

## Property details

### type

* *Setter:* `void setType(BodyType type)`
* *Getter:* `BodyType getType() const`

Sets the body simulation mode. See [BodyType](#bodytype). Must be set before calling [load](#load) or changed at runtime by re-loading the body.

---

### position / angle

* *Setters:* `void setPosition(Vector2)` / `void setAngle(float angle)`
* *Getters:* `Vector2 getPosition() const` / `float getAngle() const`

The body's own pose in **world space**, read from and written straight to the simulation, and the only way to place a body from `onFixedUpdate`. Setting either also updates the entity [Object](object.md) transform so rendering follows and the next step does not undo the move. Both wake the body. Box2D owns only X and Y, so the Transform's Z is left untouched.

Use these for teleports — respawns, checkpoints, portals. For continuous movement prefer [linearVelocity](#linearvelocity) or [applyForce](#applyforce), which let the solver resolve collisions instead of pushing bodies through walls.

!!! note "Parented bodies"

    The world pose is converted to the entity's local space using the parent's transform as
    of the last variable-timestep sync. Moving a body's **parent** and teleporting the body
    in the same callback therefore places it relative to the parent's *previous* pose — do
    one or the other per frame. Bodies with no parent, the common case, are exact.

=== "C++"

    ```cpp
    Body2D body = object.getBody2D();

    body.setPosition(Vector2(0, 240));     // respawn
    body.setLinearVelocity(Vector2::ZERO); // stop residual motion
    ```

=== "Lua"

    ```lua
    local body = object:getBody2D()

    body.position = Vector2(0, 240)
    body.linearVelocity = Vector2(0, 0)
    ```

!!! warning "Do not use Object::setPosition from onFixedUpdate"

    Writing an entity's [Object](object.md) transform only reaches the body between fixed
    steps. Inside `onFixedUpdate` the physics system syncs the body from the transform
    *before* stepping and writes the stepped pose back *after*, so a transform written
    there is discarded unless you also call [updateTransform](object.md#updatetransform)
    to refresh the world transform the sync reads. Prefer `Body2D::setPosition` /
    `setAngle`: one call, and it writes the simulation directly.
    `Object::setPosition` is fine from `onUpdate` and outside the update callbacks.

---

### linearVelocity

* *Setter:* `void setLinearVelocity(Vector2 linearVelocity)`
* *Getter:* `Vector2 getLinearVelocity() const`

Current velocity of the center of mass in world units per second.

---

### angularVelocity

* *Setter:* `void setAngularVelocity(float angularVelocity)`
* *Getter:* `float getAngularVelocity() const`

Current angular velocity in radians per second (regardless of `Engine::useDegrees`).

---

### linearDamping / angularDamping

* *Setters:* `void setLinearDamping(float)` / `void setAngularDamping(float)`
* *Getters:* `float getLinearDamping() const` / `float getAngularDamping() const`

Drag coefficients that slow down translation and rotation over time. Values in `[0, ∞)`. Zero means no damping.

---

### fixedRotation

* *Setter:* `void setFixedRotation(bool fixedRotation)`
* *Getter:* `bool isFixedRotation() const`

When `true`, the body cannot rotate. Useful for top-down characters that should always stay upright.

---

### bullet

* *Setter:* `void setBullet(bool bullet)`
* *Getter:* `bool isBullet() const`

Enables continuous collision detection (CCD) for fast-moving objects that might tunnel through thin geometry in a single time step.

---

### gravityScale

* *Setter:* `void setGravityScale(float gravityScale)`
* *Getter:* `float getGravityScale() const`

Multiplier applied to global gravity for this body. `0` means the body is unaffected by gravity; negative values invert gravity.

---

### mass / rotationalInertia

* *Getter:* `float getMass() const` / `float getRotationalInertia() const`

Computed mass and moment of inertia. Updated automatically when [applyMassFromShapes](#applymassfromshapes) is called.

## Method details

### load

* `void load()`

Registers all shapes with the Box2D world and activates the body. Must be called after creating shapes. Call again to rebuild the body after runtime shape changes.

---

### createBoxShape

* `int createBoxShape(float width, float height)`

Creates a rectangular polygon shape with corner at the entity's local origin. Returns the shape index (0-based).

---

### createCenteredBoxShape

* `int createCenteredBoxShape(float width, float height)`
* `int createCenteredBoxShape(float width, float height, Vector2 center, float angle)`

Creates a rectangular polygon centered at `(width/2, height/2)` relative to the entity origin. The second overload allows an explicit center offset and pre-rotation.

=== "C++"

    ```cpp
    body.createCenteredBoxShape(64.0f, 64.0f);
    ```

=== "Lua"

    ```lua
    body:createCenteredBoxShape(64, 64)
    ```

---

### createRoundedBoxShape

* `int createRoundedBoxShape(float width, float height, float radius)`

Creates a rounded rectangle (box with chamfered corners). `radius` specifies the corner rounding amount.

---

### createPolygonShape

* `int createPolygonShape(std::vector<Vector2> vertices)`

Creates a convex hull from the given vertices. Box2D requires the shape to be convex; provide vertices in counter-clockwise order.

---

### createCircleShape

* `int createCircleShape(Vector2 center, float radius)`

Creates a circle shape at `center` (in local space) with the given `radius`.

---

### createCapsuleShape

* `int createCapsuleShape(Vector2 center1, Vector2 center2, float radius)`

Creates a capsule defined by two center points and a radius. Good for characters and rounded projectiles.

---

### createSegmentShape

* `int createSegmentShape(Vector2 point1, Vector2 point2)`

Creates a one-sided edge segment. Only dynamic bodies moving from `point1` to `point2` (based on normal direction) are blocked. Useful for platforms.

---

### createChainShape

* `int createChainShape(std::vector<Vector2> vertices, bool loop)`

Creates a chain of connected edge segments. When `loop` is `true`, the last point connects back to the first forming a closed boundary.

---

### removeAllShapes

* `void removeAllShapes()`

Removes all shapes from the body. Call [load](#load) again after adding new shapes.

---

### setShapeDensity / setShapeFriction / setShapeRestitution

Per-shape or all-shapes material properties:

* **density** — Mass per unit area (affects computed mass).
* **friction** — Coulomb friction coefficient `[0, ∞)`. `0` = frictionless, `1` = high friction.
* **restitution** — Bounciness `[0, 1]`. `0` = no bounce, `1` = perfectly elastic.

All three come in two overloads: `setXxx(value)` applies to all shapes; `setXxx(index, value)` applies to a single shape.

---

### setShapeEnableHitEvents / setShapeContactEvents / setShapePreSolveEvents / setShapeSensorEvents

Enable specific collision event callbacks for a shape. See [PhysicsSystem events](physicssystem.md) and [Events manual](../../manual/events.md#physics-events).

* **HitEvents** — Fired when two shapes collide (one-shot, not sustained).
* **ContactEvents** — Fired while shapes are in contact.
* **PreSolveEvents** — Fired before the physics impulse is resolved; allows modifying or cancelling the collision.
* **SensorEvents** — Marks the shape as a sensor (no physical response) but still fires overlap events.

---

### setBitsFilter

* `void setBitsFilter(uint16_t categoryBits, uint16_t maskBits)`
* `void setBitsFilter(size_t shapeIndex, uint16_t categoryBits, uint16_t maskBits)`

Configures collision filtering using bitmasks. A body collides with another only if `(a.category & b.mask) != 0` and `(b.category & a.mask) != 0`.

=== "C++"

    ```cpp
    const uint16_t LAYER_PLAYER   = 0x0001;
    const uint16_t LAYER_ENEMY    = 0x0002;
    const uint16_t LAYER_WALL     = 0x0004;

    // Player collides with enemies and walls
    playerBody.setBitsFilter(LAYER_PLAYER, LAYER_ENEMY | LAYER_WALL);
    // Enemy collides with player and walls
    enemyBody.setBitsFilter(LAYER_ENEMY, LAYER_PLAYER | LAYER_WALL);
    ```

---

### applyMassFromShapes

* `void applyMassFromShapes()`

Recomputes mass and inertia from the attached shapes' density values. Call after changing `setShapeDensity` at runtime.

---

### applyForce

* `void applyForce(const Vector2& force, const Vector2& point, bool wake)`

Applies a force (in Newtons) at a given world-space `point`. Pass `wake = true` to activate a sleeping body.

---

### applyForceToCenter

* `void applyForceToCenter(const Vector2& force, bool wake)`

Applies a force at the body's center of mass; produces linear acceleration but no torque.

---

### applyTorque

* `void applyTorque(float torque, bool wake)`

Applies a rotational force. Positive values spin counter-clockwise.

---

### applyLinearImpulse / applyLinearImpulseToCenter

Instantaneous velocity changes (Δv = impulse / mass). Prefer impulses over forces for one-shot events like jumps.

---

### applyAngularImpulse

* `void applyAngularImpulse(float impulse, bool wake)`

Instantaneous angular velocity change.

---

### getBodyContacts / getShapeContacts

* `std::vector<Contact2D> getBodyContacts()`
* `std::vector<Contact2D> getShapeContacts(size_t index)`

Returns currently active contact manifolds for the entire body or for a specific shape. Useful for manual overlap queries without subscribing to per-frame events.

---

### getAttachedObject

* `Object getAttachedObject()`

Returns the [Object](object.md) whose entity owns this body.

---

### getPointsToMeterScale

* `float getPointsToMeterScale() const`

Returns the pixels-to-meters conversion scale used by Box2D. The physics simulation uses SI units (meters/kg/seconds); divide pixel distances by this value before passing them to physics methods, or use the engine's automatic scaling.
