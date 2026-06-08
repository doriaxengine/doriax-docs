---
description: Color API reference (C++ and Lua).
---

# Color

**C++ type:** `Color` (static utility class)

## Description

A static utility class providing colour space conversion between **linear** (physically-based) and **sRGB** (perceptually uniform, display-encoded) colour spaces.

Doriax's rendering pipeline works in linear colour space. When you specify a colour constant (e.g. a material's `baseColorFactor`) it should typically be in linear space. If you are reading a colour from a design tool or HTML hex code, it is likely in sRGB space and needs conversion before use.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static Vector3 | [linearTosRGB](#lineartosrgb) | C++ \| Lua |
| static Vector4 | [linearTosRGB](#lineartosrgb) | C++ \| Lua |
| static Vector3 | [sRGBToLinear](#srgbtolinear) | C++ \| Lua |
| static Vector4 | [sRGBToLinear](#srgbtolinear) | C++ \| Lua |

## Method details

### linearTosRGB

* static Vector3 **linearTosRGB**(float r, float g, float b)
* static Vector3 **linearTosRGB**(Vector3 color)
* static Vector4 **linearTosRGB**(float r, float g, float b, float a)
* static Vector4 **linearTosRGB**(Vector4 color)

Converts a linear colour to sRGB display-encoded space. Use this when you need to display a physically-accurate linear value to the user as a readable colour (e.g. in a UI colour picker).

=== "C++"
    ```cpp
    // Convert the material base colour to sRGB for display
    Vector3 displayColor = Color::linearTosRGB(material.baseColorFactor);
    ```

=== "Lua"
    ```lua
    local displayColor = Color.linearTosRGB(material.baseColorFactor)
    ```

---

### sRGBToLinear

* static Vector3 **sRGBToLinear**(float r, float g, float b)
* static Vector3 **sRGBToLinear**(Vector3 srgbIn)
* static Vector4 **sRGBToLinear**(float r, float g, float b, float a)
* static Vector4 **sRGBToLinear**(Vector4 srgbIn)

Converts an sRGB colour to linear space. Use this before assigning a colour from a design tool or a hex code to a [Material](material.md) or light property.

=== "C++"
    ```cpp
    // Web colour #FF8040 converted to linear for PBR rendering
    Vector3 linearOrange = Color::sRGBToLinear(1.0f, 0.502f, 0.251f);
    mat.baseColorFactor = Vector4(linearOrange, 1.0f);
    ```

=== "Lua"
    ```lua
    local linearOrange = Color.sRGBToLinear(1.0, 0.502, 0.251)
    mat.baseColorFactor = Vector4(linearOrange, 1.0)
    ```
