---
description: Runtime animation, actions, sprite animation, keyframe tracks, skeletal animation, and morph targets in Doriax.
---

# Animation

Doriax supports two complementary animation approaches: **editor-authored keyframe
animation** built in the Animation Timeline, and **runtime action playback** written
in code. Both are updated each frame by `ActionSystem`. You can mix them freely —
author the idle loop in the timeline and drive attacks and UI effects with runtime
actions.

## Animation families

| Family | Best for | System |
| --- | --- | --- |
| **Actions** | Scripted one-shot or looping motion — position, rotation, scale, color, alpha | `ActionSystem`, `TimedAction` subclasses |
| **Sprite animation** | 2D frame cycling through an atlas | `SpriteAnimation` |
| **Skeletal / keyframe** | Imported GLTF character clips | `Animation`, `Model` |
| **Keyframe tracks** | Authored transform and property curves on the timeline | `TranslateTracks`, `RotateTracks`, `ScaleTracks`, `MorphTracks` |
| **Morph targets** | Blend shape deformation for facial animation | `MorphTracks` |
| **Particles** | Time-based particle playback | `Particles` |

## Runtime actions

Actions target an entity and update one property over time. They are lightweight,
code-friendly, and do not require the timeline editor.

### Available action types

| Class | Property controlled |
| --- | --- |
| [`PositionAction`](../reference/classes/positionaction.md) | Entity position |
| [`RotationAction`](../reference/classes/rotationaction.md) | Entity rotation |
| [`ScaleAction`](../reference/classes/scaleaction.md) | Entity scale |
| [`ColorAction`](../reference/classes/coloraction.md) | Material or UI element color |
| [`AlphaAction`](../reference/classes/alphaaction.md) | Opacity / alpha |
| [`TimedAction`](../reference/classes/timedaction.md) | Callback after a duration or on each loop |
| [`SpriteAnimation`](../reference/classes/spriteanimation.md) | Sprite atlas frame sequence |
| [`Animation`](../reference/classes/animation.md) | Skeletal or keyframe clip |
| [`Particles`](../reference/classes/particles.md) | Particle system playback |

### Basic action example

`setAction` takes the start value, end value, duration in seconds, and an optional loop
flag. The easing curve is set separately with `setFunctionType`:

=== "Lua"

    ```lua
    -- Move an entity from (0, 0, 0) to (100, 200, 0) over 1.5 seconds
    move = PositionAction(scene)
    move:setTarget(entity)
    move:setAction(Vector3(0, 0, 0), Vector3(100, 200, 0), 1.5, false)
    move:setFunctionType(EaseType.QUAD_OUT)
    move:start()
    ```

=== "C++"

    ```cpp
    PositionAction move(&scene);
    move.setTarget(entity);
    move.setAction(Vector3(0, 0, 0), Vector3(100, 200, 0), 1.5f, false);
    move.setFunctionType(EaseType::QUAD_OUT);
    move.start();
    ```

### Chaining actions with events

Every action's `ActionComponent` exposes `onStart`, `onPause`, `onStop`, and `onStep`
events. Subscribe to `onStop` to start the next action when one finishes:

=== "Lua"

    ```lua
    move:getActionComponent().onStop = function()
        -- start the next action when this one ends
        nextAction:start()
    end
    move:start()
    ```

=== "C++"

    ```cpp
    move.getComponent<ActionComponent>().onStop = []() {
        nextAction.start();
    };
    move.start();
    ```

## Easing curves

All `TimedAction` subclasses accept an `EaseType` (via `setFunctionType`) that shapes
the interpolation curve. Names follow the `<CURVE>_<IN/OUT/IN_OUT>` pattern. Common
choices:

| EaseType | Best for |
| --- | --- |
| `LINEAR` | Constant-speed motion, debug |
| `QUAD_IN_OUT` | UI transitions and camera moves |
| `BOUNCE_OUT` | Playful jumps and pop-in effects |
| `BACK_IN` | Anticipation before a jump |
| `ELASTIC_OUT` | Springing UI elements |
| `CUBIC_OUT` | Smooth deceleration into a stop |

The full set covers `QUAD`, `CUBIC`, `QUART`, `QUINT`, `SINE`, `EXPO`, `CIRC`,
`ELASTIC`, `BACK`, and `BOUNCE`, each with `_IN`, `_OUT`, and `_IN_OUT` variants, plus
`CUSTOM` for supplying your own curve function.

## Sprite animation

`SpriteAnimation` cycles through a sequence of atlas frames by **frame index**. Frames
must be registered on the sprite first — with `addFrame` in code or via the
[Sprite Slicer](../editor/sprite-slicer.md). The interval is in **milliseconds**, and
looping is the last argument of `setAnimation`.

=== "Lua"

    ```lua
    sprite = Sprite(scene)
    sprite:setTexture("characters/hero.png")
    -- frames 0..7 previously registered with addFrame or the Sprite Slicer

    anim = SpriteAnimation(scene)
    anim:setTarget(sprite)
    anim:setAnimation(0, 7, 80, true)  -- startFrame, endFrame, interval (ms), loop
    anim:start()
    ```

=== "C++"

    ```cpp
    Sprite hero(&scene);
    hero.setTexture("characters/hero.png");

    SpriteAnimation anim(&scene);
    anim.setTarget(&hero);
    anim.setAnimation(0, 7, 80, true);
    anim.start();
    ```

For per-frame timing, pass explicit frame and time lists:
`setAnimation({0, 1, 2, 5}, {100, 80, 80, 200}, true)`.

As a shortcut, `Sprite` can drive its own animation without a separate action object:

```lua
sprite:startAnimation(0, 7, 80, true)
-- ...
sprite:stopAnimation()
```

## Skeletal animation from GLTF

A `Model` exposes the animation clips embedded in its GLTF file, addressable by name or
index. How you obtain the `Model` depends on whether the model is **already in your
scene** or is being **created at runtime** — these are two different things, and mixing
them up is the most common animation mistake.

### Playing a clip on a model already in the scene

This is the usual case: you imported the GLTF in the editor (so it appears as an entity
in the Structure panel), and you want a script on that entity — or on a parent — to start
its idle clip. **Do not reload the file.** The mesh, skeleton, and clips are already
loaded; the script only needs to *reference* the existing entity and start the clip.

The cleanest way to reach another entity is an [entity reference property](script-properties.md):
expose a `Model` property, then drag the model entity onto it in the Properties window.

=== "Lua"

    ```lua
    -- player.lua — attached to a parent entity that has a child model
    local player = {}

    -- 'model' is filled in by dragging the child model onto the property
    player.properties = {
        { name = "model", type = "Model" },
    }

    function player:init()
        if self.model then
            local idle = self.model:findAnimation("idle")
            idle.loop = true
            idle:start()
        end
    end

    return player
    ```

Don't have a property wired up? Look the child up by name instead. `Scene:findEntity`
returns the first entity with that name (use the two-argument form to scope the search to
children of a given parent), and the **two-argument** `Model(scene, entity)` constructor
*wraps that existing entity* without creating or destroying anything:

=== "Lua"

    ```lua
    function player:init()
        -- find the child named "model" under this script's entity
        local modelEntity = self.scene:findEntity("model", self.entity)
        if modelEntity ~= NULL_ENTITY then
            local model = Model(self.scene, modelEntity)
            model:getAnimation(0):start()   -- first clip, by index
        end
    end
    ```

### Creating a model at runtime

When you genuinely want to spawn a brand-new model from code (an enemy, a pickup), use
the **single-argument** constructor and then `loadGLTF`. This *creates a new entity*.

=== "Lua"

    ```lua
    -- store the handle so it lives as long as you need the entity
    self.enemy = Model(self.scene)
    self.enemy:loadGLTF("characters/hero.gltf")

    local walk = self.enemy:findAnimation("Walk")
    walk.loop = true
    walk:start()
    ```

=== "C++"

    ```cpp
    Model hero(&scene);
    hero.loadGLTF("characters/hero.gltf");

    Animation walk = hero.findAnimation("Walk");
    walk.setLoop(true);
    walk.start();
    ```

!!! warning "`Model(scene)` creates a new entity — it does not find an existing one"
    `Model(self.scene)` (one argument) **always creates a new entity** and that handle
    *owns* it. `Model(self.scene, entity)` (two arguments) **wraps an existing entity**
    and does not own it. So:

    - Never put `Model(...)` + `loadGLTF` inside `onUpdate` — that reloads the file and
      churns entities every frame. Load once in `init`.
    - To touch a model placed in the editor, reference it (property or `findEntity`) and
      use the two-argument constructor. Reloading the GLTF in code is **not** required.
    - When you do create a model at runtime, keep the handle in `self` (or another
      long-lived reference). A one-argument handle stored only in a local can have its
      entity destroyed when the local is garbage-collected.

GLTF can carry multiple named clips in a single file. You can play several clips
simultaneously for layered animation blending.

!!! note "Clip names come from the GLTF, not the Structure panel"
    `findAnimation` matches the clip's name as authored in the GLTF (often Mixamo-style,
    e.g. `mixamo.com`), which is independent of the entity name you see in the editor. If
    a name lookup fails, check the clip's **AnimationComponent → Name** field in the
    Properties window, or address the clip by index with `getAnimation(0)`. Requesting a
    name or index that doesn't exist raises an error, so guard lookups you're unsure of.

### Smooth transitions (crossfading)

Starting a clip with `start()` snaps the skeleton straight into that clip's pose. For
character motion you almost always want a **crossfade** instead — when the player stops
running, the skeleton should ease from the run cycle into idle over a fraction of a
second rather than pop. Doriax blends this for you: while a transition is in progress
both clips play and each bone's pose is a weight-normalized average of them.

The simplest entry point is [`Model:playAnimation`](../reference/classes/model.md#playanimation-stopanimations),
which fades out whatever is currently playing on the model and fades the requested clip
in:

=== "Lua"

    ```lua
    -- Hold looping clips; playAnimation manages the transition
    self.model:findAnimation("Idle").loop = true
    self.model:findAnimation("Run").loop = true
    self.model:playAnimation("Idle")        -- uses each clip's Fade time

    -- on input, later:
    self.model:playAnimation("Run", 0.2)    -- crossfade over 0.2s
    self.model:playAnimation("Die", 0.1)    -- quick blend into a one-shot
    ```

=== "C++"

    ```cpp
    model.findAnimation("Idle").setLoop(true);
    model.findAnimation("Run").setLoop(true);
    model.playAnimation("Idle");

    model.playAnimation("Run", 0.2f);
    model.playAnimation("Die", 0.1f);
    ```

When the fade time is omitted, each clip's authored **Fade time**
([`defaultFadeTime`](../reference/classes/animation.md#defaultfadetime), set in the
Properties window or in code) is used. Tune it per clip: ~0.2–0.3s for locomotion,
shorter (~0.1s) for a snappy hit or death reaction. `playAnimation` works on clips of a
single model; to crossfade arbitrary clips by hand, ramp their weights directly with
[`Animation:fadeIn`](../reference/classes/animation.md#fadein-fadeout) and `fadeOut`, or
set [`blendWeight`](../reference/classes/animation.md#blendweight) yourself for layered
blending.

You can preview a transition without running the game — see
[Blending clips in the editor](../editor/animation.md#skeletal-animation).

## Keyframe tracks (timeline-authored)

In the editor, the Animation Timeline writes keyframe data into component tracks. These
are stored in the scene file and played back at runtime through the action system. The
track types available are:

| Track class | Property animated |
| --- | --- |
| `TranslateTracks` | Entity position over time |
| `RotateTracks` | Entity rotation over time |
| `ScaleTracks` | Entity scale over time |
| `MorphTracks` | Morph target weights for shape blending |

## Morph targets

Morph targets (blend shapes) are authored in a 3D tool such as Blender and exported
through GLTF. Use `MorphTracks` on a Model entity to blend between shape keys at
runtime.

```cpp
model.setMorphWeight("smile", 0.8f);
model.setMorphWeight("blink", 1.0f);
```

## Best practices

- Name animation clips consistently (`idle`, `walk`, `run`, `jump`, `attack`).
- Keep looping clips separate from one-shot clips.
- Use runtime actions for UI and gameplay feedback; use the timeline for complex
  authored motion.
- Avoid driving physics-controlled entities through animation — let physics simulate
  them and use animation only for visual overlays.
- Test frame intervals in play mode; what looks good in the editor may feel wrong at
  the actual game frame rate.

## See also

- [Action](../reference/classes/action.md) — base action class
- [TimedAction](../reference/classes/timedaction.md) — duration-based base
- [SpriteAnimation](../reference/classes/spriteanimation.md)
- [Animation](../reference/classes/animation.md)
- [Particles](../reference/classes/particles.md)
- [Animation Timeline](../editor/animation.md) — editor authoring
