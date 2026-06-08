---
description: Body3D API reference — 3D physics body powered by Jolt Physics, shapes, forces, constraints, and contacts.
---

# Body3D

## Description

`Body3D` is the 3D rigid-body handle built on top of the **Jolt Physics** library. Obtain one by calling `object.getBody3D()`. Create one or more shapes, set the body type and material properties, then call `load()` to register with the physics world. The body transform is synchronized with the parent [Object](object.md) each physics step.

**Inherits:** [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    Mesh cube(&scene);
    cube.setTexture("textures/box.png");

    Body3D body = cube.getBody3D();
    body.createBoxShape(1.0f, 1.0f, 1.0f);
    body.setType(BodyType::DYNAMIC);
    body.load();
    ```

=== "Lua"

    ```lua
    local cube = Mesh(scene)
    cube:setTexture("textures/box.png")

    local body = cube:getBody3D()
    body:createBoxShape(1, 1, 1)
    body.type = BodyType.DYNAMIC
    body:load()
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| [BodyType](#bodytype) | [type](#type) | `STATIC` | C++ \| Lua |
| [Body3DMotionQuality](#body3dmotionquality) | [motionQuality](#motionquality) | `DISCRETE` | C++ \| Lua |
| float | [mass](#mass) | — | C++ \| Lua |
| float | [gravityFactor](#gravityfactor) | `1.0` | C++ \| Lua |
| float | [friction](#friction-restitution) | `0.2` | C++ \| Lua |
| float | [restitution](#friction-restitution) | `0.0` | C++ \| Lua |
| Vector3 | [linearVelocity](#linearvelocity-angularvelocity) | `(0,0,0)` | C++ \| Lua |
| Vector3 | [angularVelocity](#linearvelocity-angularvelocity) | `(0,0,0)` | C++ \| Lua |
| bool | allowSleeping | `true` | C++ \| Lua |
| bool | [isSensor](#issensor) | `false` | C++ \| Lua |
| bool | [collideKinematicVsNonDynamic](#collidekinematicvsnondynamic) | `false` | C++ \| Lua |
| uint16_t | [categoryBitsFilter](#categorybitsfilter-maskbitsfilter) | `0xFFFF` | C++ \| Lua |
| uint16_t | [maskBitsFilter](#categorybitsfilter-maskbitsfilter) | `0xFFFF` | C++ \| Lua |
| uint32_t | [collisionGroupID](#collisiongroupid) | `0` | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [load](#load) | C++ \| Lua |
| int | [createBoxShape](#createboxshape) | C++ \| Lua |
| int | [createSphereShape](#createsphereshape) | C++ \| Lua |
| int | [createCapsuleShape](#createcapsuleshape) | C++ \| Lua |
| int | [createTaperedCapsuleShape](#createtaperedcapsuleshape) | C++ \| Lua |
| int | [createCylinderShape](#createcylindershape) | C++ \| Lua |
| int | [createConvexHullShape](#createconvexhullshape) | C++ \| Lua |
| int | [createMeshShape](#createmeshshape) | C++ \| Lua |
| int | [createHeightFieldShape](#createheightfieldshape) | C++ \| Lua |
| size_t | getNumShapes | C++ \| Lua |
| [Shape3DType](#shape3dtype) | getShapeType | C++ \| Lua |
| void | [setShapeDensity](#setshapedensity) | C++ \| Lua |
| float | [getShapeDensity](#setshapedensity) | C++ \| Lua |
| void | [activate](#activate-deactivate) | C++ \| Lua |
| void | [deactivate](#activate-deactivate) | C++ \| Lua |
| bool | canBeKinematicOrDynamic | C++ \| Lua |
| void | [setAllowedDOFsAll](#setalloweddofsall-setalloweddofs2dplane-setalloweddofs) | C++ \| Lua |
| void | [setAllowedDOFs2DPlane](#setalloweddofsall-setalloweddofs2dplane-setalloweddofs) | C++ \| Lua |
| void | [setAllowedDOFs](#setalloweddofsall-setalloweddofs2dplane-setalloweddofs) | C++ \| Lua |
| void | [setMass](#setmass-setoverridemassandinertia) | C++ \| Lua |
| void | [setOverrideMassAndInertia](#setmass-setoverridemassandinertia) | C++ \| Lua |
| void | [setBitsFilter](#categorybitsfilter-maskbitsfilter) | C++ \| Lua |
| void | [setLinearVelocity](#linearvelocity-angularvelocity) | C++ \| Lua |
| void | [setLinearVelocityClamped](#setlinearvelocityclamped-setangularvelocityclamped) | C++ \| Lua |
| void | [setAngularVelocity](#linearvelocity-angularvelocity) | C++ \| Lua |
| void | [setAngularVelocityClamped](#setlinearvelocityclamped-setangularvelocityclamped) | C++ \| Lua |
| Vector3 | [getPointVelocity](#getpointvelocity) | C++ \| Lua |
| Vector3 | getAccumulatedForce | C++ \| Lua |
| Vector3 | getAccumulatedTorque | C++ \| Lua |
| void | [applyForce](#applyforce) | C++ \| Lua |
| void | [applyTorque](#applytorque) | C++ \| Lua |
| void | [applyImpulse](#applyimpulse) | C++ \| Lua |
| void | [applyAngularImpulse](#applyangularimpulse) | C++ \| Lua |
| bool | [applyBuoyancyImpulse](#applybuoyancyimpulse) | C++ \| Lua |
| Vector3 | [getCenterOfMassPosition](#getcenterofmassposition) | C++ \| Lua |
| Object | [getAttachedObject](#getattachedobject) | C++ \| Lua |

## Enumerations

### BodyType

* **STATIC** — Infinite mass; never moves. Walls, floors, and terrain.
* **KINEMATIC** — Controlled by velocity, not forces. Elevators and moving platforms.
* **DYNAMIC** — Fully simulated by Jolt; reacts to forces and gravity.

---

### Body3DMotionQuality

* **DISCRETE** — Standard collision detection per time step (default). Suitable for most objects.
* **LINEAR_CAST** — Continuous collision detection: sweeps the shape along its path each step. Use for fast-moving objects that may tunnel through thin geometry.

---

### Shape3DType

`BOX`, `SPHERE`, `CAPSULE`, `TAPERED_CAPSULE`, `CYLINDER`, `CONVEX_HULL`, `MESH`, `HEIGHT_FIELD`

## Property details

### type

* *Setter:* `void setType(BodyType type)`
* *Getter:* `BodyType getType() const`

Simulation mode. See [BodyType](#bodytype). Can be changed at runtime to switch between, e.g., KINEMATIC and DYNAMIC.

---

### motionQuality

* *Setter:* `void setMotionQuality(Body3DMotionQuality motionQuality)`
* *Getter:* `Body3DMotionQuality getMotionQuality() const`

Collision detection mode. See [Body3DMotionQuality](#body3dmotionquality).

---

### mass

* *Setter:* `void setMass(float mass)`
* *Getter:* `float getMass() const`

Manual mass override in kilograms. Applies to dynamic bodies. Set the mass after calling [load](#load), or use [setOverrideMassAndInertia](#setmass-setoverridemassandinertia) for combined mass + inertia control.

---

### gravityFactor

* *Setter:* `void setGravityFactor(float gravityFactor)`
* *Getter:* `float getGravityFactor() const`

Scales the global gravity for this body. `0` = gravity-free, `2` = double gravity.

---

### friction / restitution

* *Setters:* `void setFriction(float)` / `void setRestitution(float)`
* *Getters:* `float getFriction() const` / `float getRestitution() const`

Surface material properties shared across all shapes on this body. Friction `[0, ∞)` controls sliding resistance; restitution `[0, 1]` controls bounciness.

---

### linearVelocity / angularVelocity

* *Setters:* `void setLinearVelocity(Vector3)` / `void setAngularVelocity(Vector3)`
* *Getters:* `Vector3 getLinearVelocity() const` / `Vector3 getAngularVelocity() const`

Current velocity vectors. Linear velocity is in world units/second; angular velocity is in radians/second around each world axis.

---

### isSensor

* *Setter:* `void setIsSensor(bool sensor)`
* *Getter:* `bool isSensor() const`

When `true`, the body acts as a trigger volume: overlapping bodies generate events but no physical impulse is applied.

---

### collideKinematicVsNonDynamic

* *Setter:* `void setCollideKinematicVsNonDynamic(bool)`
* *Getter:* `bool isCollideKinematicVsNonDynamic() const`

When `true`, this kinematic body generates collision reports against static and other kinematic bodies (normally skipped for performance).

---

### categoryBitsFilter / maskBitsFilter

Collision layer filtering bitmasks. A collision occurs only when `(a.category & b.mask) != 0`.

---

### collisionGroupID

Group index for disabling self-collision within a group (e.g. ragdoll bones).

## Method details

### load

* `void load()`

Registers the body and all its shapes with the Jolt physics world. Must be called after defining shapes. Re-call if shapes change at runtime.

---

### createBoxShape

* `int createBoxShape(float width, float height, float depth)`
* `int createBoxShape(Vector3 position, Quaternion rotation, float width, float height, float depth)` *(with local offset)*

Creates a solid box collider. Returns the shape index. The offset overload positions the shape relative to the entity origin.

---

### createSphereShape

* `int createSphereShape(float radius)`
* `int createSphereShape(Vector3 position, Quaternion rotation, float radius)` *(with local offset)*

Creates a sphere collider. Spheres are the cheapest shape to simulate.

---

### createCapsuleShape

* `int createCapsuleShape(float halfHeight, float radius)`
* `int createCapsuleShape(Vector3 position, Quaternion rotation, float halfHeight, float radius)`

Creates a vertical capsule (hemisphere-capped cylinder). Standard character controller shape.

=== "C++"

    ```cpp
    Body3D body = player.getBody3D();
    body.createCapsuleShape(0.9f, 0.3f);   // 1.8 m tall, 0.3 m radius
    body.setType(BodyType::DYNAMIC);
    body.setAllowedDOFs2DPlane();           // constrain to XZ plane
    body.load();
    ```

=== "Lua"

    ```lua
    local body = player:getBody3D()
    body:createCapsuleShape(0.9, 0.3)
    body.type = BodyType.DYNAMIC
    body:setAllowedDOFs2DPlane()
    body:load()
    ```

---

### createTaperedCapsuleShape

* `int createTaperedCapsuleShape(float halfHeight, float topRadius, float bottomRadius)`
* `int createTaperedCapsuleShape(Vector3 position, Quaternion rotation, float halfHeight, float topRadius, float bottomRadius)`

Capsule with different radii at each end. Useful for cones, bullets, and stylised characters.

---

### createCylinderShape

* `int createCylinderShape(float halfHeight, float radius)`
* `int createCylinderShape(Vector3 position, Quaternion rotation, float halfHeight, float radius)`

Upright cylinder collider. Less stable than capsules on uneven ground; prefer capsules for characters.

---

### createConvexHullShape

* `int createConvexHullShape()`
* `int createConvexHullShape(std::vector<Vector3> vertices)`
* `int createConvexHullShape(Vector3 position, Quaternion rotation, std::vector<Vector3> vertices)`

Creates a convex hull from the mesh vertices (no-argument form) or from explicit vertices. Must be convex; Jolt computes the hull automatically.

---

### createMeshShape

* `int createMeshShape()`
* `int createMeshShape(std::vector<Vector3> vertices, std::vector<uint16_t> indices)`
* `int createMeshShape(Vector3 position, Quaternion rotation, std::vector<Vector3> vertices, std::vector<uint16_t> indices)`

Creates a static triangle-mesh collider. **Mesh shapes can only be STATIC.** Use convex hull for dynamic objects.

---

### createHeightFieldShape

* `int createHeightFieldShape()`
* `int createHeightFieldShape(unsigned int samplesSize)`

Creates a height-field collider sized to the terrain mesh in the entity. Used with the [Terrain](terrain.md) class. `samplesSize` controls the resolution grid.

---

### activate / deactivate

* `void activate()` — Wakes the body if it is sleeping.
* `void deactivate()` — Forces the body to sleep immediately.

---

### setAllowedDOFsAll / setAllowedDOFs2DPlane / setAllowedDOFs

Constrain which degrees of freedom the body can move in.

* **setAllowedDOFsAll** — All 6 DOF (default).
* **setAllowedDOFs2DPlane** — Restricts to translation on X/Z and rotation on Y. Use for top-down or side-view games.
* **setAllowedDOFs(translationX, translationY, translationZ, rotationX, rotationY, rotationZ)** — Fine-grained control per axis.

---

### setMass / setOverrideMassAndInertia

* `void setMass(float mass)` — Overrides the auto-computed mass.
* `void setOverrideMassAndInertia(Vector3 solidBoxSize, float solidBoxDensity)` — Computes mass and inertia for a solid box of the given size and density, then applies those values.

---

### setShapeDensity

* `void setShapeDensity(float density)` *(all shapes)*
* `void setShapeDensity(size_t index, float density)` *(specific shape)*

Sets the density (kg/m³) used to compute mass. Call after adding shapes and before [load](#load), or call [load](#load) again after runtime changes.

---

### setLinearVelocityClamped / setAngularVelocityClamped

Velocity setters that clamp the new value to the body's configured speed limits (set in Jolt body settings). Safer for kinematic controllers.

---

### getPointVelocity

* `Vector3 getPointVelocity(Vector3 point) const`

Returns the velocity of a world-space point on the body, including the contribution of angular velocity. Use for precise impact and dragging calculations.

---

### applyForce

* `void applyForce(const Vector3& force)`
* `void applyForce(const Vector3& force, const Vector3& point)`

Applies a force in Newtons each simulation step. The single-argument overload applies force at the center of mass (no torque). The two-argument overload applies force at a world-space point, potentially generating torque.

---

### applyTorque

* `void applyTorque(const Vector3& torque)`

Applies a torque (Nm) to rotate the body. The vector direction defines the rotation axis (right-hand rule).

---

### applyImpulse

* `void applyImpulse(const Vector3& impulse)`
* `void applyImpulse(const Vector3& impulse, const Vector3& point)`

Instantaneous velocity change. Prefer impulses over forces for one-shot events (jumps, explosions, hits).

---

### applyAngularImpulse

* `void applyAngularImpulse(const Vector3& angularImpulse)`

Instantaneous angular velocity change. Useful for spinning objects on impact.

---

### applyBuoyancyImpulse

* `bool applyBuoyancyImpulse(Vector3 surfacePosition, Vector3 surfaceNormal, float buoyancy, float linearDrag, float angularDrag, Vector3 fluidVelocity, Vector3 gravity, float deltaTime)`

Simulates buoyancy for a body partially submerged in a fluid. Returns `true` if the body intersects the water plane. Call once per physics step with the water plane data.

---

### getAttachedObject

* `Object getAttachedObject()`

Returns the [Object](object.md) that owns this body.

---

### getCenterOfMassPosition

* `Vector3 getCenterOfMassPosition()`

Returns the world-space position of the center of mass, which may differ from the entity origin if shapes are offset.
