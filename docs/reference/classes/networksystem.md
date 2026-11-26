---
description: NetworkSystem API reference (C++).
---

# NetworkSystem

**Inherits:** [SubSystem](subsystem.md)

Sends the entities with a [NetworkComponent](networkcomponent.md) of a server's scene to
the clients that loaded the same scene, and moves them there between the states that
arrive. See [Entities that follow the server](../../manual/multiplayer.md#entities).

## Methods

| Name | Languages |
| --- | --- |
| `setSendRate` / `getSendRate` | C++ |
| `setInterpolationDelay` / `getInterpolationDelay` | C++ |
| `setSceneId` | C++ |

`setSendRate(float)` is how many states per second the server sends, 20 by default.

`setInterpolationDelay(float)` is how many seconds in the past a client shows the
scene, 0.1 by default. See [Tuning](../../manual/multiplayer.md#entity-tuning).

`setSceneId(uint32_t)` names a scene that the project creates by itself, with the same
number on every peer. Scenes of the editor are already told apart.
