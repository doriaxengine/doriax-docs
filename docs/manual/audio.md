---
description: Sound playback, 3D audio, global volume, pooling, and audio workflow in Doriax.
---

# Audio

Doriax uses **SoLoud** for audio playback and exposes sound behavior through the
`Sound` object class, `SoundComponent`, `SoundPool`, and `AudioSystem`. Audio entities
are regular ECS entities — you position them in the world just like any other object,
and the audio system reads their Transform to compute spatial attenuation.

## Adding a sound to a scene

=== "Lua"

    ```lua
    sound = Sound(scene)
    sound:load("audio/jump.ogg")
    sound:setVolume(0.8)
    sound:play()
    ```

=== "C++"

    ```cpp
    Sound jump(&scene);
    jump.load("audio/jump.ogg");
    jump.setVolume(0.8f);
    jump.play();
    ```

## Core features

| Feature | API | Notes |
| --- | --- | --- |
| **Playback control** | `play()`, `pause()`, `stop()`, `resume()` | Standard transport controls |
| **Looping** | `setLoop(bool)` | Loop music or ambient sound |
| **Volume** | `setVolume(float)` | Per-sound level from 0.0 to 1.0+ |
| **Pitch / speed** | `setSpeed(float)` | 1.0 = normal, 2.0 = double speed |
| **Pan** | `setPan(float)` | –1.0 = full left, 0 = center, +1.0 = full right |
| **Seek** | `seek(seconds)` | Jump to a position in the audio |
| **3D position** | `setPosition()` or entity Transform | Spatial audio uses the entity's world position |
| **Attenuation** | `setSoundAttenuation()`, `setMinDistance()`, `setMaxDistance()` | Distance-based volume falloff |
| **Doppler effect** | `setDopplerFactor(float)` | Pitch shift from relative motion |

## 3D spatial audio

Attach a sound to a moving entity to get automatic position-based spatialization. The
audio system reads the entity's world transform every frame.

=== "Lua"

    ```lua
    -- 3D footstep sound attached to a character entity
    footstep = Sound(scene)
    footstep:setParent(characterEntity)
    footstep:load("audio/footstep.ogg")
    footstep:setSoundAttenuation(SoundAttenuation.INVERSE)
    footstep:setMinDistance(1.0)
    footstep:setMaxDistance(20.0)
    footstep:play()
    ```

=== "C++"

    ```cpp
    Sound footstep(&scene);
    footstep.setParent(character);
    footstep.load("audio/footstep.ogg");
    footstep.setSoundAttenuation(SoundAttenuation::INVERSE);
    footstep.setMinDistance(1.0f);
    footstep.setMaxDistance(20.0f);
    footstep.play();
    ```

### Attenuation models

| `SoundAttenuation` | Behavior |
| --- | --- |
| `NONE` | No distance attenuation — volume is constant regardless of distance |
| `INVERSE` | Volume decreases inversely with distance (realistic for point sources) |
| `LINEAR` | Volume falls off linearly between min and max distance |
| `EXPONENTIAL` | Exponential falloff, louder near the source |

## Global controls

`AudioSystem` provides scene-wide controls:

=== "Lua"

    ```lua
    AudioSystem.setGlobalVolume(0.5)   -- halve all audio
    AudioSystem.pauseAll()
    AudioSystem.resumeAll()
    AudioSystem.stopAll()
    ```

=== "C++"

    ```cpp
    AudioSystem::setGlobalVolume(0.5f);
    AudioSystem::pauseAll();
    AudioSystem::resumeAll();
    AudioSystem::stopAll();
    ```

## SoundPool

For sounds that play frequently (gunshots, footsteps, coins), use `SoundPool` to avoid
loading the same audio data multiple times. The pool caches loaded audio and reuses it
across multiple `Sound` instances.

```cpp
SoundPool::load("audio/coin.ogg");

// Later, play from any number of Sound objects without re-loading
Sound coin1(&scene);
coin1.load("audio/coin.ogg");  // served from pool
```

## Background music

Music typically loops, has no 3D attenuation, and plays at a lower priority than sound
effects:

=== "Lua"

    ```lua
    music = Sound(scene)
    music:load("audio/music_level1.ogg")
    music:setLoop(true)
    music:setVolume(0.4)
    music:play()
    ```

## Audio workflow checklist

1. Add audio files to the project resources folder (OGG or WAV recommended).
2. Create a `Sound` entity, set the resource path, and configure volume and loop.
3. For 3D audio: parent the sound to a spatial entity and configure attenuation.
4. For music: mark the sound as looping; keep it non-spatial.
5. Use `AudioSystem` for master volume and global pause.
6. Test on target hardware — mobile speakers and headphones differ significantly.

## Practical tips

- Keep sound effect files short and compressed; use OGG/Vorbis for best size-to-quality
  ratio.
- Use WAV for very short, frequently-triggered sounds where decoding latency matters.
- Non-spatial sounds (UI clicks, music) should not have a parent Transform entity — set
  attenuation to `NONE`.
- Tune attenuation `minDistance` and `maxDistance` in the actual scene scale so the
  falloff feels natural.
- Separate music, ambient, and SFX into named volume categories so players can control
  them independently in settings.

## See also

- [Sound](../reference/classes/sound.md) — full API reference
- [AudioSystem](../reference/classes/audiosystem.md) — global controls
