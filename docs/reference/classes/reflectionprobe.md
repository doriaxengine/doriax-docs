---
description: ReflectionProbe API reference (C++ and Lua).
---

# ReflectionProbe

**Inherits:** [Object](object.md)  
**C++ type:** `ReflectionProbe`

## Description

A local reflection environment. Meshes inside the probe's box-shaped influence volume
sample its cubemap (box-projected, so reflections stay anchored to the volume) instead of
the global sky environment. Meshes need **Receive IBL** and **Receive Lights** enabled to
pick probes up.

Meshes with `renderInReflectionProbes` disabled are skipped by captures, which keeps an
object that wraps around a probe out of its own reflection — see
[Mesh](mesh.md#renderinreflectionprobes).

Static probes use an authored cubemap — or capture the scene once at load when no cubemap
is set. Dynamic probes re-capture at runtime according to their update mode, budgeted at
one cubemap face per frame. See
[Rendering Pipeline — Reflection probes](../../manual/rendering-pipeline.md#reflection-probes)
for how probes are selected, blended, and captured.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| [ReflectionProbeMode](#reflectionprobemode) | [mode](#mode) | `STATIC` | C++ \| Lua |
| [ReflectionProbeUpdateMode](#reflectionprobeupdatemode) | [updateMode](#updatemode) | `ON_LOAD` | C++ \| Lua |
| Vector3 | [boxOffset](#boxoffset-boxsize) | `(0, 0, 0)` | C++ \| Lua |
| Vector3 | [boxSize](#boxoffset-boxsize) | `(10, 10, 10)` | C++ \| Lua |
| float | [blendDistance](#blenddistance) | `1.0` | C++ \| Lua |
| float | [intensity](#intensity) | `1.0` | C++ \| Lua |
| int | [priority](#priority) | `0` | C++ \| Lua |
| unsigned int | [resolution](#resolution) | `128` | C++ \| Lua |
| float | [nearClip](#nearclip-farclip) | `0.1` | C++ \| Lua |
| float | [farClip](#nearclip-farclip) | `100.0` | C++ \| Lua |
| float | [updateInterval](#updateinterval) | `1.0` | C++ \| Lua |
| bool | [includeSky](#includesky) | `true` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setBoxOffset](#boxoffset-boxsize) | C++ \| Lua |
| void | [setBoxSize](#boxoffset-boxsize) | C++ \| Lua |
| void | [setClipPlanes](#nearclip-farclip) | C++ \| Lua |
| void | [setTextures](#settextures-settexture) | C++ \| Lua |
| void | [setTexture](#settextures-settexture) | C++ \| Lua |
| void | [refresh](#refresh) | C++ \| Lua |

## Enumerations

### ReflectionProbeMode

* **STATIC** — Uses the authored cubemap ([setTextures](#settextures-settexture)); with no
  cubemap set, captures the scene once at load and keeps that result.
* **DYNAMIC** — Re-captures the scene at runtime according to
  [updateMode](#updatemode).

### ReflectionProbeUpdateMode

* **ON_LOAD** — Captures once when the scene starts.
* **ON_MOVE** — Re-captures whenever the probe entity moves.
* **INTERVAL** — Re-captures every [updateInterval](#updateinterval) seconds.
* **MANUAL** — Re-captures only when [refresh](#refresh) is called.

---

## Property details

### mode

* *Setter*: void **setMode**([ReflectionProbeMode](#reflectionprobemode) mode)
* *Getter*: [ReflectionProbeMode](#reflectionprobemode) **getMode**() const

Whether the probe is static or re-captures at runtime. Changing the mode restarts any
in-flight capture.

=== "C++"
    ```cpp
    ReflectionProbe probe(&scene);
    probe.setPosition(0.0f, 2.0f, 0.0f);
    probe.setBoxSize(12.0f, 6.0f, 12.0f);
    probe.setMode(ReflectionProbeMode::DYNAMIC);
    probe.setUpdateMode(ReflectionProbeUpdateMode::MANUAL);
    probe.refresh();   // capture now
    ```

=== "Lua"
    ```lua
    local probe = ReflectionProbe(scene)
    probe:setPosition(0, 2, 0)
    probe:setBoxSize(12, 6, 12)
    probe.mode = ReflectionProbeMode.DYNAMIC
    probe.updateMode = ReflectionProbeUpdateMode.MANUAL
    probe:refresh()   -- capture now
    ```

---

### updateMode

* *Setter*: void **setUpdateMode**([ReflectionProbeUpdateMode](#reflectionprobeupdatemode) updateMode)
* *Getter*: [ReflectionProbeUpdateMode](#reflectionprobeupdatemode) **getUpdateMode**() const

When a `DYNAMIC` probe re-captures. Ignored by static probes.

---

### boxOffset / boxSize

* *Setter*: void **setBoxOffset**(Vector3 boxOffset) / **setBoxOffset**(float x, float y, float z)
* *Setter*: void **setBoxSize**(Vector3 boxSize) / **setBoxSize**(float x, float y, float z)
* *Getter*: Vector3 **getBoxOffset**() / **getBoxSize**() const

The influence volume, in the entity's local space. The box is world-axis-aligned,
centred on the entity plus `boxOffset`, and scaled by the entity's world scale. The
cubemap is always captured at the entity origin, not the offset centre.

---

### blendDistance

* *Setter*: void **setBlendDistance**(float blendDistance)
* *Getter*: float **getBlendDistance**() const

Fade band inside the box edges where the probe blends into the sky IBL, hiding the seam
at the volume boundary. Runtime blending is limited to the box's smallest half-extent.

---

### intensity

* *Setter*: void **setIntensity**(float intensity)
* *Getter*: float **getIntensity**() const

Multiplier on the probe's reflection contribution.

---

### priority

* *Setter*: void **setPriority**(int priority)
* *Getter*: int **getPriority**() const

When influence boxes overlap, the higher-priority probe wins; on a tie, the probe whose
centre is nearest the mesh wins.

---

### resolution

* *Setter*: void **setResolution**(unsigned int resolution)
* *Getter*: unsigned int **getResolution**() const

Capture cubemap face size, clamped to 16–1024 at capture time. Changing it restarts any
in-flight capture.

---

### nearClip / farClip

* *Setter*: void **setNearClip**(float nearClip) / **setFarClip**(float farClip)
* *Setter*: void **setClipPlanes**(float nearClip, float farClip)
* *Getter*: float **getNearClip**() / **getFarClip**() const

Clip planes of the capture cameras.

---

### updateInterval

* *Setter*: void **setUpdateInterval**(float updateInterval)
* *Getter*: float **getUpdateInterval**() const

Seconds between captures for `INTERVAL` update mode.

---

### includeSky

* *Setter*: void **setIncludeSky**(bool includeSky)
* *Getter*: bool **isIncludeSky**() const

Whether the sky (and scene background colour) appears in runtime captures.

---

## Method details

### setTextures / setTexture

* void **setTextures**(const std::string& texturePositiveX, const std::string& textureNegativeX, const std::string& texturePositiveY, const std::string& textureNegativeY, const std::string& texturePositiveZ, const std::string& textureNegativeZ)
* void **setTexture**(const std::string& texture)

Assigns the authored cubemap used by `STATIC` probes — six face image paths, or a single
cross-layout image. Authored cubemaps are GGX-prefiltered like the sky environment, so
rough surfaces get correct blurry reflections.

---

### refresh

* void **refresh**()

Requests a new capture (or re-bake of the authored cubemap), regardless of mode and
update mode. This is what the editor's **Refresh Probe** button calls, and the way to
update a `MANUAL` probe from gameplay code.
