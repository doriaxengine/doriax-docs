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
| `Vector3.UNIT_SCALE` | (1, 1, 1) |
| `Vector3.UNIT_X` | (1, 0, 0) |
| `Vector3.UNIT_Y` | (0, 1, 0) |
| `Vector3.UNIT_Z` | (0, 0, 1) |

## Quaternion

[`Quaternion`](../reference/classes/quaternion.md) represents 3D rotation. Prefer
quaternions over Euler angles for rotation interpolation and composition.

```lua
-- Create from Euler angles (ZYX order; degrees if useDegrees is enabled)
local q = Quaternion(0, 90, 0)

-- Interpolate (interpolation factor comes first)
local result = Quaternion.slerp(0.5, q1, q2)

-- Rotate a direction (C++: q * v). In Lua, use an axis helper:
local rotated = q:xAxis()  -- local +X after applying q
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
-- Cast a ray through the cursor and test it against the scene's 3D physics bodies
local pos = Input.getMousePosition()
local ray = camera:screenToRay(pos.x, pos.y)
local result = ray:intersects(scene, RayFilter.BODY_3D)
if result.hit then
    print("Hit entity:", result.body, "at distance", result.distance)
end
```

`intersects` also accepts individual `AABB`, `OBB`, `Plane`, `Body2D`, and `Body3D`
targets. The returned `RayReturn` carries `hit`, `distance`, `point`, `normal`, `body`
(the entity), and `shapeIndex`.

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
conversions. Rendering expects linear color space internally.

```lua
-- Convert from sRGB to linear for the renderer
local linearRed = Color.sRGBToLinear(Vector3(1, 0, 0))

-- And back for display values
local srgb = Color.linearTosRGB(linearRed)
```

## Logging

[`Log`](../reference/classes/log.md) provides formatted console output at different
severity levels.

=== "Lua"

    ```lua
    -- The Lua functions take a single string; use .. for formatting
    Log.print("Scene loaded")
    Log.debug("Player position: " .. tostring(obj.position))
    Log.warn("Optional resource missing: " .. path)
    Log.error("Physics body creation failed")
    ```

=== "C++"

    ```cpp
    // The C++ functions accept printf-style format arguments
    Log::print("Scene loaded");
    Log::debug("Player position: %s", position.toString().c_str());
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
local Mover = {
    properties = {
        { name = "speed", displayName = "Speed", type = "float", default = 50.0 }
    }
}

function Mover:init()
    RegisterEngineEvent(self, "onUpdate")
end

function Mover:onUpdate()
    local obj = Object(self.scene, self.entity)
    local dt = Engine.deltatime
    obj.position = obj.position + Vector3(0, self.speed * dt, 0)
end

return Mover
```

## Base64

The [`Base64`](../reference/classes/base64.md) utility class encodes and decodes binary
data as base64 strings. Useful for embedding small binary data in JSON or YAML, or for
network/save serialization. **C++ only** — `encode` / `decode` are not exposed to Lua yet.

## See also

- [Vector2](../reference/classes/vector2.md), [Vector3](../reference/classes/vector3.md), [Vector4](../reference/classes/vector4.md)
- [Quaternion](../reference/classes/quaternion.md)
- [Rect](../reference/classes/rect.md)
- [AABB](../reference/classes/aabb.md), [OBB](../reference/classes/obb.md), [Ray](../reference/classes/ray.md)
- [Log](../reference/classes/log.md)
- [Color](../reference/classes/color.md), [Angle](../reference/classes/angle.md)
