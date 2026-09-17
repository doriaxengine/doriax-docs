---
description: SoundComponent API reference (C++ and Lua).
---

# SoundComponent

`SoundComponent` API exposed to Lua and C++ gameplay code.

## Properties

!!! note "Writing a component field"
    Some fields take effect only once the matching `needUpdate…` flag is set too. See
    [Writing components directly](../../manual/entity-component-system.md#writing-components-directly).

| Name | Languages |
| --- | --- |
| `handle` | C++ \| Lua (read-only) |
| `state` | C++ \| Lua (read-only) |
| `filename` | C++ \| Lua |
| `loaded` | C++ \| Lua (read-only) |
| `enableClocked` | C++ \| Lua |
| `lastPosition` | C++ \| Lua (read-only) |
| `startTrigger` | C++ \| Lua |
| `stopTrigger` | C++ \| Lua |
| `pauseTrigger` | C++ \| Lua |
| `onStart` | C++ \| Lua |
| `onPause` | C++ \| Lua |
| `onStop` | C++ \| Lua |
| `volume` | C++ \| Lua |
| `pan` | C++ \| Lua |
| `speed` | C++ \| Lua |
| `looping` | C++ \| Lua |
| `loopingPoint` | C++ \| Lua |
| `protectVoice` | C++ \| Lua |
| `inaudibleBehaviorMustTick` | C++ \| Lua |
| `inaudibleBehaviorKill` | C++ \| Lua |
| `minDistance` | C++ \| Lua |
| `maxDistance` | C++ \| Lua |
| `attenuationModel` | C++ \| Lua |
| `attenuationRolloffFactor` | C++ \| Lua |
| `dopplerFactor` | C++ \| Lua |
| `length` | C++ \| Lua (read-only) |
| `playingTime` | C++ \| Lua (read-only) |
| `needUpdate` | C++ \| Lua |

`needUpdate` applies `volume`, `speed`, `pan`, `looping`, `loopingPoint`, `protectVoice`, the two
`inaudibleBehavior` fields and the 3D attenuation to the playing voice. It is not a load: a new `filename` needs
[Sound.loadSound](sound.md#loadsound).
