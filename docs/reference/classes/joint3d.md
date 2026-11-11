---
description: Joint3D API reference (C++ and Lua).
---

# Joint3D

Jolt 3D joint constraint.

## Methods

| Name | Languages |
| --- | --- |
| `setFixedJoint` | C++ \| Lua |
| `setDistanceJoint` | C++ \| Lua |
| `setPointJoint` | C++ \| Lua |
| `setHingeJoint` | C++ \| Lua |
| `setConeJoint` | C++ \| Lua |
| `setPrismaticJoint` | C++ \| Lua |
| `setSwingTwistJoint` | C++ \| Lua |
| `setSixDOFJoint` | C++ \| Lua |
| `setPathJoint` | C++ \| Lua |
| `setGearJoint` | C++ \| Lua |
| `setRackAndPinionJoint` | C++ \| Lua |
| `setPulleyJoint` | C++ \| Lua |
| `getType` | C++ \| Lua |
| [`setMotorState` / `getMotorState`](#motors) | C++ \| Lua (property `motorState`) |
| [`setMotorTargetVelocity` / `getMotorTargetVelocity`](#motors) | C++ \| Lua (property `motorTargetVelocity`) |
| [`setMotorTargetPosition` / `getMotorTargetPosition`](#motors) | C++ \| Lua (property `motorTargetPosition`) |
| [`setMotorFrequency` / `getMotorFrequency`](#motors) | C++ \| Lua (property `motorFrequency`) |
| [`setMotorDamping` / `getMotorDamping`](#motors) | C++ \| Lua (property `motorDamping`) |
| [`setMotorMaxForce` / `getMotorMaxForce`](#motors) | C++ \| Lua (property `motorMaxForce`) |
| [`getCurrentPosition`](#motors) | C++ \| Lua |
| `getJoint3DComponent` ([Joint3DComponent](joint3dcomponent.md)) | Lua |

## Enumerations

### Joint3DMotorState

* **OFF** — No motor (default). The joint moves freely within its limits. Turning a motor off
  wakes its bodies, so what it held falls or swings free.
* **VELOCITY** — Drives the joint at `motorTargetVelocity`, as hard as `motorMaxForce` allows.
* **POSITION** — Springs the joint to `motorTargetPosition`, with the spring set by
  `motorFrequency` and `motorDamping`.
* **POSITION_AND_VELOCITY** — Springs the joint to `motorTargetPosition` while it moves at
  `motorTargetVelocity`. Move the target a little each step at that velocity for a smooth
  path that does not lag behind.

## Motors

A **hinge** or **prismatic** joint can drive its bodies: a door that swings shut, a lift that
rises to a floor, a crank or a wheel that turns on its own. On other joint types the motor
values are kept but do nothing.

| Property | Default | Hinge | Prismatic |
| --- | --- | --- | --- |
| `motorState` | `OFF` | [Joint3DMotorState](#joint3dmotorstate) | same |
| `motorTargetVelocity` | `0` | angle per second | m/s along the axis |
| `motorTargetPosition` | `0` | angle | m along the axis |
| `motorFrequency` | `2` | Hz | Hz |
| `motorDamping` | `1` | ratio | ratio |
| `motorMaxForce` | `0` | torque limit, N·m | force limit, N |

* Angles are in degrees, or radians when `Engine::useDegrees` is `false`. A hinge's angle
  `0` is the pose its bodies have when the joint is made, and a body reload during play keeps
  it.
* A prismatic position is measured in the same frame as its `limitsMin` and `limitsMax`, and
  Jolt keeps the target inside them.
* `motorFrequency` is how fast a position motor springs back, and `motorDamping` how much it
  resists overshooting: `1` stops at the target without bouncing, less bounces. A frequency of
  `0` makes the spring as stiff as the solver allows.
* `motorMaxForce` `0` means no limit. With a limit, a heavy door or lift may stop short of
  its target or move slower than asked, which is often what a mechanism should do. A limited
  position motor can also swing past its target before it settles, whatever its damping.

The setters change the live joint at once and wake its bodies; one called from a 3D
callback takes effect before the next step. The values are also
stored on the [Joint3DComponent](joint3dcomponent.md), so they survive the joint being rebuilt
and are saved with the scene. In the editor they are the **Motor** section of a hinge or
prismatic joint, and changing them during Play moves the running joint without rebuilding it.

`getCurrentPosition()` returns the hinge angle or prismatic position now, in the same units,
and `0` while the joint is not built.

=== "C++"

    ```cpp
    // a door that swings open to 90 degrees
    Joint3D hinge(&scene);
    hinge.setHingeJoint(frame.getEntity(), door.getEntity(), hingePoint, Vector3(0, 1, 0), Vector3(1, 0, 0));
    hinge.setMotorState(Joint3DMotorState::POSITION);
    hinge.setMotorMaxForce(200.0f);  // N m: a player can still hold it
    hinge.setMotorTargetPosition(90.0f);

    // a lift that rises at 1 m/s
    Joint3D lift(&scene);
    lift.setPrismaticJoint(shaft.getEntity(), cabin.getEntity(), Vector3(0, 1, 0), 0.0f, 12.0f);
    lift.setMotorState(Joint3DMotorState::VELOCITY);
    lift.setMotorTargetVelocity(1.0f);

    // later, in onFixedUpdate: stop at the top
    if (lift.getCurrentPosition() >= 12.0f){
        lift.setMotorState(Joint3DMotorState::OFF);
    }
    ```

=== "Lua"

    ```lua
    local hinge = Joint3D(scene)
    hinge:setHingeJoint(frame.entity, door.entity, hingePoint, Vector3(0, 1, 0), Vector3(1, 0, 0))
    hinge.motorState = Joint3DMotorState.POSITION
    hinge.motorMaxForce = 200
    hinge.motorTargetPosition = 90

    local lift = Joint3D(scene)
    lift:setPrismaticJoint(shaft.entity, cabin.entity, Vector3(0, 1, 0), 0, 12)
    lift.motorState = Joint3DMotorState.VELOCITY
    lift.motorTargetVelocity = 1

    -- later, in onFixedUpdate: stop at the top
    if lift:getCurrentPosition() >= 12 then
        lift.motorState = Joint3DMotorState.OFF
    end
    ```
