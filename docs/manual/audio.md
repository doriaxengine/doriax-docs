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
    sound:loadSound("audio/jump.ogg")
    sound.volume = 0.8
    sound:play()
    ```

=== "C++"

    ```cpp
    Sound jump(&scene);
    jump.loadSound("audio/jump.ogg");
    jump.setVolume(0.8f);
    jump.play();
    ```

!!! note "Lua uses properties, C++ uses setters"
    Most sound parameters are exposed to Lua as **properties** (`sound.volume = 0.8`),
    while C++ uses setter methods (`sound.setVolume(0.8f)`). The property/method names
    below list both forms.

## Core features

| Feature | Lua property | C++ method | Notes |
| --- | --- | --- | --- |
| **Playback control** | `play()`, `pause()`, `stop()` | same | Transport controls (call `play()` again to resume a paused sound) |
| **Looping** | `sound.looping` | `setLooping(bool)` | Loop music or ambient sound |
| **Volume** | `sound.volume` | `setVolume(float)` | Per-sound level from 0.0 to 1.0+ |
| **Pitch / speed** | `sound.speed` | `setSpeed(float)` | 1.0 = normal, 2.0 = double speed |
| **Pan** | `sound.pan` | `setPan(float)` | –1.0 = full left, 0 = center, +1.0 = full right |
| **Seek** | `seek(seconds)` | same | Jump to a position in the audio |
| **3D mode** | `sound.sound3D` | `setSound3D(bool)` | Enable spatialization (or pass `true` to the constructor) |
| **Attenuation** | `sound.attenuationModel`, `sound.minDistance`, `sound.maxDistance` | `setAttenuationModel()`, `setMinDistance()`, `setMaxDistance()` | Distance-based volume falloff |
| **Doppler effect** | `sound.dopplerFactor` | `setDopplerFactor(float)` | Pitch shift from relative motion |

## 3D spatial audio

Attach a sound to a moving entity to get automatic position-based spatialization. The
audio system reads the entity's world transform every frame.

Pass `true` to the `Sound` constructor (or set `sound.sound3D = true`) to make a sound
spatial. A 3D sound is positioned by its entity's Transform, so parent it under the
moving entity in the editor's Structure panel (or in the scene hierarchy).

=== "Lua"

    ```lua
    -- 3D footstep sound (the `true` enables spatialization)
    footstep = Sound(scene, true)
    footstep:loadSound("audio/footstep.ogg")
    footstep.attenuationModel = SoundAttenuation.INVERSE_DISTANCE
    footstep.minDistance = 1.0
    footstep.maxDistance = 20.0
    footstep:play()
    ```

=== "C++"

    ```cpp
    Sound footstep(&scene, true);
    footstep.loadSound("audio/footstep.ogg");
    footstep.setAttenuationModel(SoundAttenuation::INVERSE_DISTANCE);
    footstep.setMinDistance(1.0f);
    footstep.setMaxDistance(20.0f);
    footstep.play();
    ```

### Attenuation models

| `SoundAttenuation` | Behavior |
| --- | --- |
| `NO_ATTENUATION` | No distance attenuation — volume is constant regardless of distance |
| `INVERSE_DISTANCE` | Volume decreases inversely with distance (realistic for point sources) |
| `LINEAR_DISTANCE` | Volume falls off linearly between min and max distance |
| `EXPONENTIAL_DISTANCE` | Exponential falloff, louder near the source |

## Global controls

`AudioSystem` provides scene-wide controls:

=== "Lua"

    ```lua
    AudioSystem.globalVolume = 0.5     -- halve all audio (property, not a setter)
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

For sounds that play frequently (gunshots, footsteps, coins), the engine caches decoded
audio data in an internal `SoundPool` so the same file is not loaded multiple times.
Loading the same path from several `Sound` instances reuses the cached data
automatically — you do not need to manage the pool yourself.

```cpp
// Each Sound that loads the same path shares the cached audio data.
Sound coin1(&scene);
coin1.loadSound("audio/coin.ogg");

Sound coin2(&scene);
coin2.loadSound("audio/coin.ogg");  // served from the shared cache
```

## Background music

Music typically loops, has no 3D attenuation, and plays at a lower priority than sound
effects:

=== "Lua"

    ```lua
    music = Sound(scene)
    music:loadSound("audio/music_level1.ogg")
    music.looping = true
    music.volume = 0.4
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
- Non-spatial sounds (UI clicks, music) should not be 3D — leave `sound3D` off (the
  default) so they play at full volume regardless of listener position.
- Tune attenuation `minDistance` and `maxDistance` in the actual scene scale so the
  falloff feels natural.
- Separate music, ambient, and SFX into named volume categories so players can control
  them independently in settings.

## See also

- [Sound](../reference/classes/sound.md) — full API reference
- [AudioSystem](../reference/classes/audiosystem.md) — global controls
