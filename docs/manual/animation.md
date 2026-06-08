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

=== "Lua"

    ```lua
    -- Move an entity from its current position to (100, 200, 0) over 1.5 seconds
    move = PositionAction(scene)
    move:setTarget(entity)
    move:setAction(Vector3(100, 200, 0), 1.5, EaseType.EASE_OUT_QUAD)
    move:start()
    ```

=== "C++"

    ```cpp
    PositionAction move(&scene);
    move.setTarget(entity);
    move.setAction(Vector3(100, 200, 0), 1.5f, EaseType::EASE_OUT_QUAD);
    move.start();
    ```

### Chaining actions with callbacks

Use `TimedAction` to sequence multiple actions:

=== "Lua"

    ```lua
    seq = TimedAction(scene)
    seq:setTarget(entity)
    seq:setDuration(0.5)
    seq:setCallback(function()
        -- start the next action when this one ends
        nextAction:start()
    end)
    seq:start()
    ```

## Easing curves

All `TimedAction` subclasses accept an `EaseType` that shapes the interpolation curve.
Common choices:

| EaseType | Best for |
| --- | --- |
| `LINEAR` | Constant-speed motion, debug |
| `EASE_IN_OUT_QUAD` | UI transitions and camera moves |
| `EASE_OUT_BOUNCE` | Playful jumps and pop-in effects |
| `EASE_IN_BACK` | Anticipation before a jump |
| `EASE_OUT_ELASTIC` | Springing UI elements |
| `EASE_OUT_CUBIC` | Smooth deceleration into a stop |

See [TimedAction](../reference/classes/timedaction.md) for the full `EaseType`
enumeration.

## Sprite animation

`SpriteAnimation` cycles through a sequence of atlas frames at a fixed interval. Use
the [Sprite Slicer](../editor/sprite-slicer.md) to cut a sprite sheet into named frames
first.

=== "Lua"

    ```lua
    sprite = Sprite(scene)
    sprite:setTexture("characters/hero.png")

    anim = SpriteAnimation(scene)
    anim:setTarget(sprite)
    anim:setAnimation("walk_00", "walk_07", 0.08)  -- from frame, to frame, interval (seconds)
    anim:setLoop(true)
    anim:start()
    ```

=== "C++"

    ```cpp
    Sprite hero(&scene);
    hero.setTexture("characters/hero.png");

    SpriteAnimation anim(&scene);
    anim.setTarget(hero);
    anim.setAnimation("walk_00", "walk_07", 0.08f);
    anim.setLoop(true);
    anim.start();
    ```

## Skeletal animation from GLTF

Import a GLTF file as a `Model`. The model exposes its embedded animation clips by name
or index.

=== "Lua"

    ```lua
    model = Model(scene)
    model:loadGLTF("characters/hero.gltf")

    -- Find and play by name
    local walk = model:findAnimation("Walk")
    walk:setLoop(true)
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
