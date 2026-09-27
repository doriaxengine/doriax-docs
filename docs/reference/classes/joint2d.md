---
description: Joint2D API reference (C++ and Lua).
---

# Joint2D

Box2D joint constraint.

## Methods

| Name | Languages |
| --- | --- |
| [`setDistanceJoint`](#setdistancejoint) | C++ \| Lua |
| `setRevoluteJoint` | C++ \| Lua |
| `setPrismaticJoint` | C++ \| Lua |
| `setMouseJoint` | C++ \| Lua |
| `setWheelJoint` | C++ \| Lua |
| `setWeldJoint` | C++ \| Lua |
| `setMotorJoint` | C++ \| Lua |
| `getType` | C++ \| Lua |

## Method details

### setDistanceJoint

* `void setDistanceJoint(Entity bodyA, Entity bodyB)`
* `void setDistanceJoint(Entity bodyA, Entity bodyB, Vector2 worldAnchorOnBodyA, Vector2 worldAnchorOnBodyB, bool rope)`

Keeps two bodies at the distance their anchors have when the joint is created. The first form anchors at each body's position, the second takes anchors in world space. With `rope` set to `true` the joint acts like a rope: the bodies can move closer, but never farther apart than that distance. This is the **Rope** option of a Distance joint in the editor.

=== "C++"

    ```cpp
    // the weight hangs at most 150 points below the hook
    Joint2D rope(&scene);
    rope.setDistanceJoint(hook.getEntity(), weight.getEntity(), Vector2(0, 200), Vector2(0, 50), true);
    ```

=== "Lua"

    ```lua
    -- the weight hangs at most 150 points below the hook
    local rope = Joint2D(scene)
    rope:setDistanceJoint(hook.entity, weight.entity, Vector2(0, 200), Vector2(0, 50), true)
    ```
