---
description: AudioSystem API reference (C++ and Lua).
---

# AudioSystem

**Inherits:** [SubSystem](subsystem.md)

SoLoud playback and 3D audio.

## Methods

| Name | Languages |
| --- | --- |
| `stopAll` | C++ \| Lua |
| `pauseAll` | C++ \| Lua |
| `resumeAll` | C++ \| Lua |
| `checkActive` | C++ \| Lua |
| `setMuted` | C++ |

## Constants

- `globalVolume`

## Platform mute

`AudioSystem::setMuted(bool muted)` silences all audio, whatever `globalVolume` is set
to, until it is called again with `false`. It is meant for mutes the platform imposes:
web exports for YouTube Playables call it when YouTube turns the game's audio off. See
[Monetization → Pauses and mute](../../manual/monetization.md#web-portal-pauses).
