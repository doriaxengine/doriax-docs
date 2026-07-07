---
description: Model API reference (C++ and Lua).
---

# Model

**Inherits:** [Mesh](mesh.md)  
**C++ type:** `Model`

## Description

Loads and displays 3D model files in a scene. `Model` extends [Mesh](mesh.md) and adds support for loading OBJ and GLTF files (including binary GLB), including skeletal animation (via `Animation` / `Bone`), blend-shape morph targets, and PBR materials.

A single GLTF file can contain multiple meshes, materials, textures, skeletons, and animations; Doriax imports all of them into the scene hierarchy and makes each accessible through the API. Use [getAnimation()](#getanimation-findanimation) and [getBone()](#getbone) to drive skeletal playback, and [setMorphWeight()](#getmorphweight-setmorphweight) to control blend shapes.

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| bool | [loadModel](#loadmodel) | C++ \| Lua |
| bool | [loadOBJ](#loadobj-loadgltf) | C++ \| Lua |
| bool | [loadGLTF](#loadobj-loadgltf) | C++ \| Lua |
| [Animation](animation.md) | [getAnimation](#getanimation-findanimation) | C++ \| Lua |
| [Animation](animation.md) | [findAnimation](#getanimation-findanimation) | C++ \| Lua |
| void | [playAnimation](#playanimation-stopanimations) | C++ \| Lua |
| void | [stopAnimations](#playanimation-stopanimations) | C++ \| Lua |
| [Bone](bone.md) | [getBone](#getbone) | C++ \| Lua |
| float | [getMorphWeight](#getmorphweight-setmorphweight) | C++ \| Lua |
| void | [setMorphWeight](#getmorphweight-setmorphweight) | C++ \| Lua |
| void | [resetToBindPose](#resettobindpose) | C++ \| Lua |

## Method details

### loadModel

* bool **loadModel**(const std::string& filename)

Loads a 3D model file from disk. Doriax automatically detects the format based on file extension:

* `.obj` — Wavefront OBJ
* `.gltf` / `.glb` — GL Transmission Format (GLTF 2.0 / binary GLB)

Returns `true` on success. On failure, check the log for details.

=== "C++"
    ```cpp
    Model character(&scene);
    if (!character.loadModel("characters/hero.glb")) {
        Log::error("Failed to load hero model");
    }
    ```

=== "Lua"
    ```lua
    local character = Model(scene)
    if not character:loadModel("characters/hero.glb") then
        Log.error("Failed to load hero model")
    end
    ```

---

### loadOBJ / loadGLTF

* bool **loadOBJ**(const std::string& filename)
* bool **loadGLTF**(const std::string& filename)

Format-specific loaders. Use these when you want to be explicit about the format, or when the file extension is non-standard. `loadGLTF()` accepts both text `.gltf` and binary `.glb` files.

---

### getAnimation / findAnimation

* [Animation](animation.md) **getAnimation**(int index)
* [Animation](animation.md) **findAnimation**(const std::string& name)

Retrieve a skeletal or morph-target animation embedded in the loaded model. `getAnimation()` accesses by zero-based index; `findAnimation()` searches by name as exported from the DCC tool. Both return an [Animation](animation.md) object that can be started, stopped, and configured for looping.

=== "C++"
    ```cpp
    Model soldier(&scene);
    soldier.loadModel("soldiers/rifleman.glb");

    Animation walkAnim = soldier.findAnimation("Walk");
    walkAnim.setLoop(true);
    walkAnim.start();
    ```

=== "Lua"
    ```lua
    local soldier = Model(scene)
    soldier:loadModel("soldiers/rifleman.glb")

    local walkAnim = soldier:findAnimation("Walk")
    walkAnim:setLoop(true)
    walkAnim:start()
    ```

---

### playAnimation / stopAnimations

* void **playAnimation**(int index)
* void **playAnimation**(int index, float fadeTime)
* void **playAnimation**(const std::string& name)
* void **playAnimation**(const std::string& name, float fadeTime)
* void **stopAnimations**(float fadeTime)

Switch the model's active clip with a **smooth crossfade** instead of an instant pose snap. `playAnimation()` fades out every other running clip on this model and fades the requested one in over `fadeTime` seconds; `stopAnimations()` fades all running clips out.

This is the recommended way to change animation state at runtime (idle → run → jump → die). During the fade both clips play and their poses are blended by weight, so the character eases between motions rather than popping. When `fadeTime` is omitted, the target clip's authored [defaultFadeTime](animation.md#defaultfadetime) is used (set per-clip as **AnimationComponent → Fade time**). A `fadeTime` of `0` switches instantly.

Unlike [getAnimation()](#getanimation-findanimation), which returns a handle you start yourself, `playAnimation()` manages the transition for you. Set looping on the clips you intend to hold (idle, run) via [Animation::loop](animation.md#loop).

=== "C++"
    ```cpp
    Model hero(&scene);
    hero.loadModel("characters/hero.glb");

    // Make locomotion clips loop, then start on idle
    hero.findAnimation("Idle").setLoop(true);
    hero.findAnimation("Run").setLoop(true);
    hero.playAnimation("Idle");          // uses each clip's Fade time

    // Later, on input:
    hero.playAnimation("Run", 0.2f);     // crossfade to run over 0.2s
    hero.playAnimation("Die", 0.1f);     // snappy transition into a one-shot
    ```

=== "Lua"
    ```lua
    local hero = Model(scene)
    hero:loadModel("characters/hero.glb")

    hero:findAnimation("Idle").loop = true
    hero:findAnimation("Run").loop = true
    hero:playAnimation("Idle")           -- uses each clip's Fade time

    -- Later, on input:
    hero:playAnimation("Run", 0.2)       -- crossfade to run over 0.2s
    hero:playAnimation("Die", 0.1)       -- snappy transition into a one-shot
    ```

!!! note "Crossfades assume full-skeleton clips"
    The blend is a weight-normalized average per bone, so it looks best when both clips animate the whole skeleton (the usual case for GLTF character clips). A bone animated by only the outgoing clip holds its pose until that clip finishes fading rather than easing.

---

### getBone

* [Bone](bone.md) **getBone**(const std::string& name)
* [Bone](bone.md) **getBone**(int id)

Returns a [Bone](bone.md) handle by name or by index. A `Bone` inherits [Object](object.md) so you can read and write its local transform to override the skeleton. For example, you can aim a character's head bone toward a target while the rest of the body plays a walk cycle.

=== "C++"
    ```cpp
    Bone head = soldier.getBone("Head");
    head.setRotation(targetRotation);
    ```

=== "Lua"
    ```lua
    local head = soldier:getBone("Head")
    head:setRotation(targetRotation)
    ```

---

### getMorphWeight / setMorphWeight

* float **getMorphWeight**(const std::string& name)
* float **getMorphWeight**(int id)
* void **setMorphWeight**(const std::string& name, float value)
* void **setMorphWeight**(int id, float value)

Read or write the weight of a blend-shape morph target. Weights range from `0.0` (no influence) to `1.0` (full influence). Multiple morphs can be active simultaneously. Access by exported name or by zero-based index.

=== "C++"
    ```cpp
    Model face(&scene);
    face.loadModel("characters/face.glb");
    face.setMorphWeight("Smile", 0.8f);
    face.setMorphWeight("Blink_L", 1.0f);
    ```

=== "Lua"
    ```lua
    local face = Model(scene)
    face:loadModel("characters/face.glb")
    face:setMorphWeight("Smile", 0.8)
    face:setMorphWeight("Blink_L", 1.0)
    ```

---

### resetToBindPose

* void **resetToBindPose**()

Resets all bones back to the bind pose defined in the model file, clearing any programmatic or animation-driven overrides. Useful when switching between animations or when stopping all playback.
