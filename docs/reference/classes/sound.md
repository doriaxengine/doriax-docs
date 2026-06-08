---
description: Sound API reference (C++ and Lua).
---

# Sound

**Inherits:** [EntityHandle](entityhandle.md)  
**C++ type:** `Sound`

## Description

Plays audio clips in a scene, supporting both 2D and 3D positional audio. `Sound` wraps the [SoLoud](https://solhsa.com/soloud/) audio engine, giving you precise control over playback state, volume, pitch, panning, looping, 3D attenuation and Doppler effect.

A 2D sound is heard at the same volume and position regardless of where in the scene the listener or source is placed; a 3D sound is automatically attenuated based on the distance between the sound entity and the active camera.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| bool | [sound3D](#sound3d) | `false` | C++ \| Lua |
| bool | [clockedSound](#clockedsound) | `false` | C++ \| Lua |
| double | [volume](#volume) | `1.0` | C++ \| Lua |
| float | [speed](#speed) | `1.0` | C++ \| Lua |
| float | [pan](#pan) | `0.0` | C++ \| Lua |
| bool | [lopping](#lopping) | `false` | C++ \| Lua |
| double | [loopingPoint](#loopingpoint) | `0.0` | C++ \| Lua |
| bool | [protectVoice](#protectvoice) | `false` | C++ \| Lua |
| float | [minDistance](#mindistance-maxdistance) | `1.0` | C++ \| Lua |
| float | [maxDistance](#mindistance-maxdistance) | `1000.0` | C++ \| Lua |
| [SoundAttenuation](#soundattenuation) | [attenuationModel](#attenuationmodel) | `NO_ATTENUATION` | C++ \| Lua |
| float | [attenuationRolloffFactor](#attenuationrollofffactor) | `1.0` | C++ \| Lua |
| float | [dopplerFactor](#dopplerfactor) | `1.0` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| int | [loadSound](#loadsound) | C++ \| Lua |
| void | [destroySound](#destroysound) | C++ \| Lua |
| [Object](object.md) | [getObject](#getobject) | C++ \| Lua |
| void | [play](#play-pause-stop) | C++ \| Lua |
| void | [pause](#play-pause-stop) | C++ \| Lua |
| void | [stop](#play-pause-stop) | C++ \| Lua |
| void | [seek](#seek) | C++ \| Lua |
| double | [getLength](#getlength-getplayingtime) | C++ \| Lua |
| double | [getPlayingTime](#getlength-getplayingtime) | C++ \| Lua |
| bool | [isPlaying](#isplaying-ispaused-isstopped) | C++ \| Lua |
| bool | [isPaused](#isplaying-ispaused-isstopped) | C++ \| Lua |
| bool | [isStopped](#isplaying-ispaused-isstopped) | C++ \| Lua |
| void | [setInaudibleBehavior](#setinaudiblebehavior) | C++ \| Lua |
| void | [setMinMaxDistance](#mindistance-maxdistance) | C++ \| Lua |

## Enumerations

### SoundAttenuation

Controls how volume falls off with distance in 3D audio.

* **NO_ATTENUATION** - No distance attenuation; the sound is heard at full volume everywhere
* **INVERSE_DISTANCE** - Classic `1 / distance` model, similar to the OpenAL default
* **LINEAR_DISTANCE** - Linear ramp from `minDistance` to `maxDistance`
* **EXPONENTIAL_DISTANCE** - Exponential roll-off; volume drops quickly after `minDistance`

---

## Property details

### sound3D

* *Setter*: void **setSound3D**(bool sound3D)
* *Getter*: bool **isSound3D**() const

When `true`, the sound is rendered in 3D space relative to the active camera. The entity's world position is used as the source position. When `false`, the sound is a standard stereo/mono clip with no positional information.

---

### clockedSound

* *Setter*: void **setClockedSound**(bool enableClocked)
* *Getter*: bool **isClockedSound**() const

When enabled, SoLoud plays the sound in *clocked* mode. This keeps multiple streamed sounds synchronised to the engine's update tick, which is important when mixing music with synchronised sound effects. Has no effect on loaded WAV/OGG samples (`Wav`).

---

### volume

* *Setter*: void **setVolume**(double volume)
* *Getter*: double **getVolume**() const

Master volume for this source. A value of `1.0` is full-volume, `0.0` is silent. Values above `1.0` are allowed but may clip the audio output.

---

### speed

* *Setter*: void **setSpeed**(float speed)
* *Getter*: float **getSpeed**() const

Playback speed (pitch) multiplier. `1.0` is normal, `2.0` plays at double speed (one octave up), `0.5` plays at half speed (one octave down).

---

### pan

* *Setter*: void **setPan**(float pan)
* *Getter*: float **getPan**() const

Stereo pan. `-1.0` is fully left, `0.0` is centre, `1.0` is fully right. Panning has no effect when `sound3D` is `true`.

---

### lopping

* *Setter*: void **setLopping**(bool lopping)
* *Getter*: bool **isLopping**() const

When `true`, the clip restarts from [loopingPoint](#loopingpoint) after it finishes.

---

### loopingPoint

* *Setter*: void **setLoopingPoint**(double loopingPoint)
* *Getter*: double **getLoopingPoint**() const

Position in **seconds** at which the clip restarts when [lopping](#lopping) is `true`. Defaults to `0.0` (beginning of the clip).

---

### protectVoice

* *Setter*: void **setProtectVoice**(bool protectVoice)
* *Getter*: bool **isProtectVoice**() const

If `true`, SoLoud will never steal this voice when all voice slots are occupied. Use for critical audio (e.g. player death sounds) that must always play.

---

### minDistance / maxDistance

* *Setter*: void **setMinDistance**(float minDistance)
* *Getter*: float **getMinDistance**() const
* *Setter*: void **setMaxDistance**(float maxDistance)
* *Getter*: float **getMaxDistance**() const
* *Combined setter*: void **setMinMaxDistance**(float minDistance, float maxDistance)

Distance thresholds used by the [attenuationModel](#attenuationmodel) when `sound3D` is `true`.

* Inside `minDistance` the sound plays at full volume.
* Beyond `maxDistance` the sound is inaudible (for `LINEAR_DISTANCE`) or effectively silent.

---

### attenuationModel

* *Setter*: void **setAttenuationModel**([SoundAttenuation](#soundattenuation) attenuationModel)
* *Getter*: [SoundAttenuation](#soundattenuation) **getAttenuationModel**() const

Select the distance-attenuation algorithm for this 3D source. See [SoundAttenuation](#soundattenuation) for the available values.

---

### attenuationRolloffFactor

* *Setter*: void **setAttenuationRolloffFactor**(float attenuationRolloffFactor)
* *Getter*: float **getAttenuationRolloffFactor**() const

Scales how aggressively the attenuation model reduces volume with distance. Higher values mean faster roll-off. The exact meaning depends on the [attenuationModel](#attenuationmodel) in use.

---

### dopplerFactor

* *Setter*: void **setDopplerFactor**(float dopplerFactor)
* *Getter*: float **getDopplerFactor**() const

Controls the intensity of the Doppler pitch shift for this 3D source. `0.0` disables Doppler; `1.0` is physically accurate; values above `1.0` exaggerate the effect. Requires `sound3D` to be `true`.

---

## Method details

### loadSound

* int **loadSound**(const std::string& filename)

Loads an audio file from disk. Supported formats depend on the SoLoud build bundled with Doriax (WAV, OGG, FLAC, MP3, and others). Returns `0` on success or a non-zero SoLoud error code on failure.

=== "C++"
    ```cpp
    Sound bgm(&scene);
    bgm.loadSound("sounds/music.ogg");
    bgm.setLopping(true);
    bgm.play();
    ```

=== "Lua"
    ```lua
    local bgm = Sound(scene)
    bgm:loadSound("sounds/music.ogg")
    bgm:setLopping(true)
    bgm:play()
    ```

---

### destroySound

* void **destroySound**()

Unloads the audio data and frees the SoLoud voice slot. Call this when the sound is no longer needed to free memory immediately without destroying the entity.

---

### getObject

* [Object](object.md) **getObject**() const

Returns the `Object` component of this sound entity. Use this to set the world-space position for 3D audio or to attach the sound to a parent entity.

=== "C++"
    ```cpp
    Sound footstep(&scene, true);  // 3D sound
    footstep.loadSound("sounds/step.wav");
    footstep.getObject().setPosition(playerPos);
    ```

=== "Lua"
    ```lua
    local footstep = Sound(scene, true)
    footstep:loadSound("sounds/step.wav")
    footstep:getObject():setPosition(playerPos)
    ```

---

### play / pause / stop

* void **play**()
* void **pause**()
* void **stop**()

Control the playback state of the sound. `play()` starts or resumes from the current position, `pause()` freezes playback at the current position, and `stop()` resets the position to the beginning.

---

### seek

* void **seek**(double time)

Jump to a specific position in **seconds** within the audio clip. Has no effect if no clip is loaded.

---

### getLength / getPlayingTime

* double **getLength**()
* double **getPlayingTime**()

`getLength()` returns the total duration of the loaded clip in **seconds**. `getPlayingTime()` returns the current playback cursor position in **seconds**.

---

### isPlaying / isPaused / isStopped

* bool **isPlaying**()
* bool **isPaused**()
* bool **isStopped**()

Query the current playback state.

---

### setInaudibleBehavior

* void **setInaudibleBehavior**(bool mustTick, bool kill)

Controls what SoLoud does when this voice becomes inaudible (volume reaches zero or the source is out of range).

* **mustTick** — when `true`, the voice continues to advance its playback position even while inaudible, so it stays in sync with other sources.
* **kill** — when `true`, the voice is automatically removed once it becomes inaudible, freeing a voice slot.

If both are `false`, the voice is simply paused while inaudible and resumes when it becomes audible again.
