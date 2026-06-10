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

Import a GLTF file as a `Model`. The model exposes its embedded animation clips by name
or index.

=== "Lua"

    ```lua
    model = Model(scene)
    model:loadGLTF("characters/hero.gltf")

    -- Find and play by name (loop is a property in Lua)
    local walk = model:findAnimation("Walk")
    walk.loop = true
    walk:start()

    -- Or blend between clips
    local idle = model:findAnimation("Idle")
    idle:start()
    ```

=== "C++"

    ```cpp
    Model hero(&scene);
    hero.loadGLTF("characters/hero.gltf");

    Animation walk = hero.findAnimation("Walk");
    walk.setLoop(true);
    walk.start();
    ```

GLTF can carry multiple named clips in a single file. You can play several clips
simultaneously for layered animation blending.

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
