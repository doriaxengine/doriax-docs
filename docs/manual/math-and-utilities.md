---
description: Math types, geometry helpers, logging, angle/color utilities, and utility classes in Doriax.
---

# Math & Utilities

Doriax includes a complete set of math and utility types that are shared across
rendering, physics, animation, input, and gameplay code. Understanding these types helps
you write efficient, readable Doriax scripts.

## Vector types

| Type | Dimensions | Typical uses |
| --- | --- | --- |
| [`Vector2`](../reference/classes/vector2.md) | 2D (x, y) | Positions, sizes, velocities, UV coordinates |
| [`Vector3`](../reference/classes/vector3.md) | 3D (x, y, z) | Positions, directions, scales, normals |
| [`Vector4`](../reference/classes/vector4.md) | 4D (x, y, z, w) | Colors (RGBA), homogeneous coordinates, packed data |

```lua
-- Create vectors
local pos = Vector3(10, 5, 0)
local dir = Vector3(0, 1, 0)

-- Arithmetic
local newPos = pos + dir * 3.0
local dist   = pos:length()
local unit   = dir:normalized()
local dot    = pos:dotProduct(dir)
```

### Common static constants

| Constant | Value |
| --- | --- |
| `Vector3.ZERO` | (0, 0, 0) |
| `Vector3.ONE` | (1, 1, 1) |
| `Vector3.UNIT_X` | (1, 0, 0) |
| `Vector3.UNIT_Y` | (0, 1, 0) |
| `Vector3.UNIT_Z` | (0, 0, 1) |

## Quaternion

[`Quaternion`](../reference/classes/quaternion.md) represents 3D rotation. Prefer
quaternions over Euler angles for rotation interpolation and composition.

```lua
-- Create from Euler angles (in degrees if useDegrees is enabled)
local q = Quaternion.fromEulerAngles(0, 90, 0)

-- Interpolate
local result = Quaternion.slerp(q1, q2, 0.5)

-- Apply to a vector
local rotated = q * Vector3(1, 0, 0)
```

## Matrix types

| Type | Use |
| --- | --- |
| [`Matrix3`](../reference/classes/matrix3.md) | 3×3 transforms, normal matrix |
| [`Matrix4`](../reference/classes/matrix4.md) | 4×4 transforms, projection, view matrix |

Matrices are used internally by the renderer and physics, but you can construct them
for custom transforms or pass them to shader uniforms.

## Rect

[`Rect`](../reference/classes/rect.md) stores a 2D rectangle as (x, y, width, height).
Use it for UI bounds, sprite atlas frames, and screen-space regions.

```lua
local frame = Rect(64, 0, 32, 32)   -- x=64, y=0, w=32, h=32
local center = frame:center()
local contains = frame:contains(Vector2(70, 10))
```

## Bounds and spatial queries

| Class | Use |
| --- | --- |
| [`AABB`](../reference/classes/aabb.md) | Axis-aligned bounding box — fast broad-phase tests, frustum culling |
| [`OBB`](../reference/classes/obb.md) | Oriented bounding box — rotated objects that AABB over-approximates |
| [`Sphere`](../reference/classes/sphere.md) | Sphere bounds — broad-phase tests, shadow radius, audio range |
| [`Ray`](../reference/classes/ray.md) | Ray from origin in a direction — picking, raycasts, line-of-sight |
| [`Plane`](../reference/classes/plane.md) | Infinite plane defined by normal and distance — frustum planes, clip tests |

```lua
-- Cast a ray from a camera position
local ray = camera:screenToRay(Input.getMousePosition())
local result = ray:testScene(scene)
if result.hasHit then
    print("Hit entity:", result.entity)
end
```

## Angles

The [`Angle`](../reference/classes/angle.md) utility class provides explicit
degree/radian conversions. The engine can be configured to use degrees everywhere with
`Engine::setUseDegrees(true)`.

```lua
-- Convert explicitly regardless of engine setting
local rad = Angle.degToRad(90)
local deg = Angle.radToDeg(math.pi / 2)
```

## Color utilities

The static [`Color`](../reference/classes/color.md) class provides sRGB ↔ linear
conversions and a set of named color constants. Rendering expects linear color space
internally.

```lua
-- Convert from sRGB to linear for the renderer
local linearRed = Color.sRGBToLinear(Vector3(1, 0, 0))

-- Named constants
local white = Color.WHITE   -- Vector4(1, 1, 1, 1)
local black = Color.BLACK
```

## Logging

[`Log`](../reference/classes/log.md) provides formatted console output at different
severity levels.

=== "Lua"

    ```lua
    Log.print("Scene loaded")
    Log.debug("Entity count: " .. scene:getEntityCount())
    Log.warn("Optional resource missing: %s", path)
    Log.error("Physics body creation failed")
    ```

=== "C++"

    ```cpp
    Log::print("Scene loaded");
    Log::debug("Entity count: %u", scene.getEntityCount());
    Log::warn("Optional resource missing: %s", path.c_str());
    Log::error("Physics body creation failed");
    ```

Use `Log::debug` for development-only output. Release builds can strip debug logs by
setting the appropriate log level.

## Object utility

The [`Object`](../reference/classes/object.md) class wraps an entity handle and
provides transform, visibility, parenting, and basic physics convenience APIs. Use it
when you need to access transform data from a script without knowing the specific
object type.

```lua
function onUpdate()
    local obj = Object(self.scene, self.entity)
    obj.position = obj.position + Vector3(0, speed * dt, 0)
end
```

## Base64

The [`Base64`](../reference/classes/base64.md) utility class encodes and decodes binary
data as base64 strings. Useful for embedding small binary data in JSON or YAML, or for
network/save serialization.

## See also

- [Vector2](../reference/classes/vector2.md), [Vector3](../reference/classes/vector3.md), [Vector4](../reference/classes/vector4.md)
- [Quaternion](../reference/classes/quaternion.md)
- [Rect](../reference/classes/rect.md)
- [AABB](../reference/classes/aabb.md), [OBB](../reference/classes/obb.md), [Ray](../reference/classes/ray.md)
- [Log](../reference/classes/log.md)
- [Color](../reference/classes/color.md), [Angle](../reference/classes/angle.md)
