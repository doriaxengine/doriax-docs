---
description: PostProcessPass API reference — one fullscreen pass of a scene's post-process chain (C++ and Lua).
---

# PostProcessPass

**C++ type:** `PostProcessPass` (struct)

## Description

One entry of a scene's post-process chain: the forked fullscreen shader to run, whether
it runs, and the values of its `u_fs_postParams` members. Passes are plain values —
build them, then hand the whole chain to
[Scene.postProcessPasses](scene.md#postprocesspasses). To change a value on a chain that
is already running, use [Scene.setPostProcessUniform](scene.md#setpostprocessuniform),
which does not rebuild the chain.

See [Custom Shaders — Post-process passes](../../editor/custom-shaders.md#post-process-passes)
for how to write a pass.

### Constructors

* `PostProcessPass()` — the built-in passthrough, enabled, with no values.

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| string | [shader](#shader) | `""` | C++ \| Lua |
| bool | [enabled](#enabled) | `true` | C++ \| Lua |
| vector&lt;pair&lt;string, Vector4&gt;&gt; | [uniforms](#setuniform) | `{}` | C++ |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [setUniform](#setuniform) | C++ \| Lua |
| Vector4 | [getUniform](#setuniform) | C++ \| Lua |
| bool | [removeUniform](#setuniform) | C++ \| Lua |

## Property details

### shader

Project-relative base path of the forked shader (`"shaders/sharpen"` resolves to
`shaders/sharpen.vert` and `shaders/sharpen.frag`, or `"a.vert|b.frag"` names the files
separately). Empty runs the built-in passthrough, which is also what a fork that fails to
compile falls back to.

---

### enabled

Whether the pass runs. A disabled pass keeps its shader and values, and is still exported,
so it can be turned back on at runtime with
[Scene.setPostProcessPassEnabled](scene.md#setpostprocesspassenabled).

## Method details

### setUniform

* `void setUniform(const std::string& name, const Vector4& value)`
* `void setUniform(const std::string& name, const Vector3& value)`
* `void setUniform(const std::string& name, const Vector2& value)`
* `void setUniform(const std::string& name, float value)`
* `Vector4 getUniform(const std::string& name) const`
* `bool removeUniform(const std::string& name)`

Values for the members of the shader's `u_fs_postParams` block, keyed by member name and
stored in `uniforms`. A name the shader does not declare is stored but unused, a member
with no value reads zero, matrix and array members take no value, and `time` and
`resolution` are written by the engine every frame — setting either logs an error and is
ignored. A narrower value leaves the remaining components at zero. These edit the pass
value only; the scene picks the change up when the chain is set again (a value-only change
keeps the compiled chain).

=== "C++"

    ```cpp
    PostProcessPass vignette;
    vignette.shader = "shaders/vignette";
    vignette.setUniform("strength", 0.6f);
    vignette.setUniform("color", Vector3(0.0f, 0.0f, 0.1f));

    scene.setPostProcessPasses({vignette});
    ```

=== "Lua"

    ```lua
    local vignette = PostProcessPass()
    vignette.shader = "shaders/vignette"
    vignette:setUniform("strength", 0.6)
    vignette:setUniform("color", Vector3(0, 0, 0.1))

    scene.postProcessPasses = {vignette}
    ```
