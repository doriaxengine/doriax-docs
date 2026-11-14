---
description: PostProcessPass API reference — one fullscreen pass of a scene's post-process chain (C++ and Lua).
---

# PostProcessPass

**C++ type:** `PostProcessPass` (struct)

## Description

One entry of a scene's post-process chain: the shader file to run over the finished
image, whether it runs, and the values and textures of the parameters it declares. Passes
are plain values — build them, then hand the whole chain to
[Scene.postProcessPasses](scene.md#postprocesspasses). To change a value on a chain that
is already running, use [Scene.setPostProcessUniform](scene.md#setpostprocessuniform),
which does not rebuild the chain.

See [Shader Files — Post-process](../../manual/shader-files.md#post-process) for how to
write a pass, and [Custom Shaders — Post-process passes](../../editor/custom-shaders.md#post-process-passes)
for the chain in the editor.

### Constructors

* `PostProcessPass()` — the built-in passthrough, enabled, with no values.

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| string | [shader](#shader) | `""` | C++ \| Lua |
| bool | [enabled](#enabled) | `true` | C++ \| Lua |
| vector&lt;pair&lt;string, Vector4&gt;&gt; | [uniforms](#setuniform) | `{}` | C++ |
| vector&lt;pair&lt;string, Texture&gt;&gt; | [textures](#settexture) | `{}` | C++ |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [setUniform](#setuniform) | C++ \| Lua |
| Vector4 | [getUniform](#setuniform) | C++ \| Lua |
| bool | [removeUniform](#setuniform) | C++ \| Lua |
| void | [setTexture](#settexture) | C++ \| Lua |
| Texture | [getTexture](#settexture) | C++ \| Lua |

## Property details

### shader

Project-relative path of the `postprocess` [shader file](../../manual/shader-files.md#post-process)
(`.glsl`) or [shader graph](../../editor/shader-graphs.md) (`.shader`), such as
`"shaders/vignette.glsl"`. Its `getColor` hook runs over the finished image and receives
the previous pass at each pixel. Empty runs the built-in passthrough, which is also what a
shader that fails to build falls back to.

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

Values of the parameters the shader declares with `#pragma param`, keyed by name and stored
in `uniforms`. A name the shader does not declare is stored but unused, and a parameter
with no value reads its declared default. A narrower value leaves the remaining components at zero. These edit the pass
value only; the scene picks the change up when the chain is set again (a value-only change
keeps the compiled chain).

=== "C++"

    ```cpp
    PostProcessPass vignette;
    vignette.shader = "shaders/vignette.glsl";
    vignette.setUniform("strength", 0.6f);
    vignette.setUniform("color", Vector3(0.0f, 0.0f, 0.1f));

    scene.setPostProcessPasses({vignette});
    ```

=== "Lua"

    ```lua
    local vignette = PostProcessPass()
    vignette.shader = "shaders/vignette.glsl"
    vignette:setUniform("strength", 0.6)
    vignette:setUniform("color", Vector3(0, 0, 0.1))

    scene.postProcessPasses = {vignette}
    ```

---

### setTexture

* `void setTexture(const std::string& name, const Texture& texture)`
* `Texture getTexture(const std::string& name) const`

Texture parameters the shader declares with `#pragma param texture2D` or `textureCube`
(see [Textures](../../manual/shader-files.md#textures)), keyed by name and stored in
`textures`. An empty texture draws the declared default. Like the values, a texture
reaches the scene when the chain is set again, but a changed texture rebuilds the chain;
on a running chain, [Scene.setPostProcessTexture](scene.md#setpostprocesstexture) sets
one directly. `getTexture` returns the stored texture, empty when none.

=== "C++"

    ```cpp
    PostProcessPass grade;
    grade.shader = "shaders/grade.glsl";
    grade.setTexture("lut", Texture("textures/grade_lut.png"));

    scene.setPostProcessPasses({grade});
    ```

=== "Lua"

    ```lua
    local grade = PostProcessPass()
    grade.shader = "shaders/grade.glsl"
    grade:setTexture("lut", Texture("textures/grade_lut.png"))

    scene.postProcessPasses = {grade}
    ```
