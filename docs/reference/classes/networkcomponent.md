---
description: NetworkComponent API reference (C++).
---

# NetworkComponent

Makes an entity follow the server on every client. Add it in the editor with
**Add Component → Network**. See
[Entities that follow the server](../../manual/multiplayer.md#entities).

## Properties

| Name | Languages |
| --- | --- |
| `owner` | C++ |
| `syncPosition` | C++ |
| `syncRotation` | C++ |
| `syncScale` | C++ |

`owner` is the peer given to [`Network::spawn`](network.md#spawn), 1 otherwise. Lua
reads it with [`Network.getOwner`](network.md#getowner-isowner).

`syncPosition`, `syncRotation` and `syncScale` choose what the server sends. Position
and rotation are on by default.
