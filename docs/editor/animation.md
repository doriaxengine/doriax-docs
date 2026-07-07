---
description: Using the animation timeline, sprite animation, skeletal animation, and keyframe tracks in the Doriax editor.
---

# Animation Timeline

The **Animation Timeline** edits time-based changes and previews them in the scene. It
works with entity transforms, sprite frame sequences, skeletal animation clips, morph
targets, and runtime action components — all driven by the `ActionSystem` at runtime.

![Animation timeline](../assets/screenshots/editor-animation.png)

## Timeline concepts

| Concept | Meaning |
| --- | --- |
| **Playhead** | Current time or frame being previewed |
| **Track** | A single animated property channel (e.g. position X, sprite frame, alpha) |
| **Keyframe** | A value recorded at a specific time on a track |
| **Clip** | A named time range containing one or more tracks |
| **Interpolation** | How values are calculated between keyframes (linear, step, ease, etc.) |
| **Snap** | Grid interval used when placing or moving keyframes |
| **Loop** | Whether the clip repeats when it reaches the end |

## Supported track types

| Track type | What it controls |
| --- | --- |
| **Transform** | Position, rotation, scale (translate, rotate, scale tracks) |
| **Color / Alpha** | Color tint and opacity |
| **Sprite frame** | Active frame index for a `Sprite` atlas |
| **Skeletal clip** | Bone transforms from an imported GLTF animation |
| **Morph weights** | Blend shape weights for facial or deformation animation |
| **Particle playback** | Play/stop state of a `Particles` action |

## Creating a clip

1. Select an entity in the **Structure panel** or **Scene view**.
2. Open the **Animation Timeline** panel.
3. Click **+ New Clip** and enter a name.
4. Click **+ Track** and select the property to animate.
5. Move the playhead to a time and set a keyframe value in the Properties window.
6. Move the playhead and set another keyframe.
7. Press **Play** in the timeline to preview the clip.

## Editing keyframes

| Operation | How |
| --- | --- |
| Select keyframe | Click the diamond marker on the track |
| Move keyframe | Drag the marker, or type a time in the selection panel |
| Change value | Edit the value in the Properties window or right-click the marker |
| Change interpolation | Right-click a keyframe and pick a curve type |
| Delete keyframe | Select and press **Delete** |

## Sprite animation

For 2D frame animation, add a **Sprite Frame** track and set keyframes to specific
frame names or indices from the sliced sprite sheet. Keep frame intervals consistent
for smooth playback.

The runtime equivalent is `SpriteAnimation`. See the
[Sprite Slicer](sprite-slicer.md) page for how to prepare a sprite sheet.

## Skeletal animation

GLTF models can include one or more named skeletal animation clips. The timeline editor
lets you preview and blend these clips on the **Model** entity. Use the **Bone** view
to inspect and edit individual joint transforms.

![Bone tools](../assets/screenshots/editor-bones.png)

At runtime, look up a clip by name on the `Model` object:

=== "Lua"

    ```lua
    model = Model(scene)
    model:loadGLTF("characters/hero.gltf")
    local walk = model:findAnimation("Walk")
    walk:start()
    ```

=== "C++"

    ```cpp
    Model hero(&scene);
    hero.loadGLTF("characters/hero.gltf");
    Animation walk = hero.findAnimation("Walk");
    walk.start();
    ```

### Previewing crossfades between clips

At runtime you usually switch clips with a **crossfade** so the character eases from one
motion into the next instead of snapping (see
[Smooth transitions](../manual/animation.md#smooth-transitions-crossfading)). You can
preview that blend directly in the timeline:

1. Select an animation clip and press **Play** to preview it.
2. In the toolbar, pick a clip in the **Blend to** dropdown.
3. Click the **⇄** button. The playing clip fades out while the chosen clip fades in,
   using the target clip's **Fade time**, and the viewport shows the blended result.

Each clip carries a **Fade time** (`defaultFadeTime`) — the default crossfade duration
used when [`Model:playAnimation`](../reference/classes/model.md#playanimation-stopanimations)
is called without an explicit time. Edit it in the **Properties** window under
**AnimationComponent → Fade time** (~0.2–0.3s reads well for locomotion, ~0.1s for a
quick hit or death). Scrubbing the playhead exits the transition and returns to the
single selected clip.

!!! tip "Use looping clips to see the blend"
    The blend reads best when you crossfade *from* a looping clip (idle, run). Blending
    from a one-shot clip that has already finished will snap, because a finished clip no
    longer contributes to the pose.

## Runtime action system

For scripted one-shot and looping motion that does not need a full authored timeline,
the runtime action system provides lightweight action types:

| Action | Purpose |
| --- | --- |
| `PositionAction` | Animate entity position |
| `RotationAction` | Animate entity rotation |
| `ScaleAction` | Animate entity scale |
| `ColorAction` | Animate material or UI color |
| `AlphaAction` | Animate opacity |
| `TimedAction` | Trigger a callback after a delay or on each loop iteration |
| `SpriteAnimation` | Cycle through sprite frames |
| `Animation` | Play a skeletal or keyframe clip |
| `Particles` | Drive particle playback |

All actions support easing curves. See [TimedAction](../reference/classes/timedaction.md)
for the full list of `EaseType` values.

## Easing curves

Apply easing in the timeline by right-clicking a keyframe, or set it on runtime actions
with `setFunctionType()`. Common choices:

| Curve | Best for |
| --- | --- |
| `LINEAR` | Constant-speed motion, debug |
| `QUAD_IN_OUT` | UI transitions and camera moves |
| `BOUNCE_OUT` | Playful jumps and pop-in effects |
| `BACK_IN` | Anticipation before a jump |
| `ELASTIC_OUT` | Springing UI elements |

## Best practices

- Name clips clearly and consistently (`idle`, `walk`, `run`, `jump`, `attack`).
- Keep looping and one-shot animations in separate clips.
- Use consistent frame intervals for sprite animations.
- Prefer skeletal animation for character movement; use keyframe tracks for camera
  and scene-wide effects.
- Use morph targets sparingly on performance-sensitive targets.
- Test in play mode after changing script-driven animation timing.
