---
description: Multiplayer in Doriax — hosting a server, connecting clients from desktop, mobile and web builds, and calling functions on other peers with RPCs.
---

# Multiplayer

[`Network`](../reference/classes/network.md) connects running copies of a project: one
**server** and its **clients**. They talk through **RPCs**, functions that one side
registers by name and the other side calls with values.

The model is server-authoritative. A client only reaches the server, never another
client, so the server decides what every player sees. The server can also be a player
(a *listen server*): the same code runs on it and on the clients.

Entities with a **Network** component [follow the server](#entities) on every client.
Everything else is sent with RPCs.

## Hosting and connecting {#hosting-and-connecting}

=== "Lua"

    ```lua
    -- on the server
    Network.host(7777)

    -- on a client
    Network.onConnected = function()
        print("connected as peer " .. Network.id)
    end
    Network.onConnectionFailed = function(reason)
        print("no connection: " .. reason)
    end
    Network.connect("192.168.0.10", 7777)
    ```

=== "C++"

    ```cpp
    #include "Network.h"

    // on the server
    Network::host(7777);

    // on a client
    REGISTER_EVENT(Network::onConnected, onConnected);
    REGISTER_EVENT(Network::onConnectionFailed, onConnectionFailed);
    Network::connect("192.168.0.10", 7777);
    ```

`host` opens the port twice: on **UDP** for desktop and mobile clients, and on **TCP**
for the **WebSocket** connections of web builds. Clients of every platform join the
same server. Open both in the firewall of the machine that hosts.

`connect` returns at once. `onConnected` or `onConnectionFailed` tells how it went, with
one of these reasons:

| Reason | Meaning |
| --- | --- |
| `unreachable` | Nothing answered at that address and port |
| `timeout` | Something answered, but no server accepted in 10 seconds |
| `version` | The server runs another [version](#versions) of the project |
| `full` | The server already has its `maxPeers` clients |
| `protocol` | It is not a Doriax server, or it runs another engine version |

Every peer has a number. The server is always `Network.SERVER` (1), and each client
gets its own from 2 on, never reused while the server runs. `Network.id` is the number
of this peer.

| Event | Where | When |
| --- | --- | --- |
| `onPeerConnected(peer)` | Server | A client joined |
| `onPeerDisconnected(peer)` | Server | A client left, was lost or was disconnected |
| `onConnected()` | Client | The server accepted the connection |
| `onConnectionFailed(reason)` | Client | The connection could not be made |
| `onDisconnected()` | Client | The server closed or was lost |

`Network.close()` ends the session on either side. On the server,
`Network.disconnect(peer)` removes one client. The editor closes the session when Play
stops.

## RPCs {#rpcs}

The receiving side registers a function under a name. The first argument is always the
peer that called it, followed by the values it sent.

=== "Lua"

    ```lua
    -- on the server
    Network.registerRpc("move", function(sender, position)
        players[sender].position = position
    end)

    -- on a client
    Network.rpc(Network.SERVER, "move", Vector3(1, 0, 4))
    ```

=== "C++"

    ```cpp
    // on the server
    Network::registerRpc("move", [this](int sender, Vector3 position){
        players[sender].setPosition(position);
    });

    // on a client
    Network::rpc(Network::SERVER, "move", Vector3(1, 0, 4));
    ```

The target of an RPC is:

- a **peer**: `Network.SERVER` from a client, or a client's number from the server;
- **`Network.ALL`**: every connected peer, which on a client is only the server;
- **this peer's own number**, which calls the function here. A listen server uses it to
  treat its own player like the others.

Handlers run at the start of a frame, and the RPCs of a frame leave when it ends. A
handler can call RPCs, disconnect a peer or close the session.

### In a script {#rpc-scripts}

A script registers one of its methods, and the RPC is removed when the script is
destroyed with its entity:

=== "Lua"

    ```lua
    function Player:init()
        Network.registerRpc("move", self, "onMove")
    end

    function Player:onMove(sender, position)
        self.target = position
    end
    ```

=== "C++"

    ```cpp
    Player::Player(Scene* scene, Entity entity): ScriptBase(scene, entity){
        REGISTER_RPC("move", onMove);
    }

    void Player::onMove(int sender, Vector3 position){
        target = position;
    }
    ```

A name holds one function: registering it again replaces the earlier one. An RPC
registered with a plain function stays until `unregisterRpc`, so it must not use a
script that may be destroyed.

### Values {#rpc-values}

An RPC carries `nil`, booleans, integers, numbers, strings, `Vector2`, `Vector3`,
`Vector4` and `Quaternion`. Lua tables are not sent.

Each value travels with its type. Integers and numbers convert to each other, so a Lua
`2` reaches a C++ `float`. In C++ a call with other types, or with another number of
values, is refused and logged, and the function is not called. A Lua function gets what
was sent, as any Lua function does.

Lua and C++ call each other: the name and the values are all they share.

### Reliable and unreliable {#rpc-delivery}

`rpc` is **reliable**: the call arrives, and calls arrive in the order they were made.
Use it for what must not be missed, like a shot, a score or a chat line.

`rpcUnreliable` sends once and never waits. A call can be lost, and one that arrives
late is dropped when a newer one already arrived. Use it for values sent again every
tick, like a position, where the next one replaces a lost one.

=== "Lua"

    ```lua
    Engine.onFixedUpdate = function()
        if Network.isConnected() then
            Network.rpcUnreliable(Network.SERVER, "move", player.position)
        end
    end
    ```

=== "C++"

    ```cpp
    void Player::onFixedUpdate(){
        if (Network::isConnected()){
            Network::rpcUnreliable(Network::SERVER, "move", getPosition());
        }
    }
    ```

A WebSocket has no unreliable delivery, so with web clients `rpcUnreliable` is as
reliable as `rpc`, and a bad connection delays it instead of dropping it.

### Never trust a client {#security}

Anyone can send any RPC with any values to a server. `sender` is safe, the server sets
it from the connection, but everything after it is a request: check that the peer may
do it and that the values make sense before acting. Keep on the server what decides the
game, such as health, scores and who hit whom.

## The server as a player {#listen-server}

Write the game once by sending requests to `Network.SERVER` and results to peers, and
by letting the server target itself:

=== "Lua"

    ```lua
    Network.registerRpc("fire", function(sender, direction)
        -- runs on the server, for clients and for its own player
        if canFire(sender) then
            Network.rpc(Network.ALL, "fired", sender, direction)
            showShot(sender, direction) -- ALL does not include this peer
        end
    end)

    Network.registerRpc("fired", function(sender, shooter, direction)
        showShot(shooter, direction)
    end)

    -- the same line on the server and on a client
    Network.rpc(Network.SERVER, "fire", aim)
    ```

=== "C++"

    ```cpp
    Network::registerRpc("fire", [this](int sender, Vector3 direction){
        // runs on the server, for clients and for its own player
        if (canFire(sender)){
            Network::rpc(Network::ALL, "fired", sender, direction);
            showShot(sender, direction); // ALL does not include this peer
        }
    });

    Network::registerRpc("fired", [this](int sender, int shooter, Vector3 direction){
        showShot(shooter, direction);
    });

    // the same line on the server and on a client
    Network::rpc(Network::SERVER, "fire", aim);
    ```

`Network.hostOffline()` is a server that opens no port. A single-player session then
runs the same code, and it is the only way to host in a web build, since a browser
can't accept connections.

## Entities that follow the server {#entities}

Add a **Network** component to an entity (**Add Component → Network**) and the clients
show it where the server has it. The server sends its position and rotation, and scale
when **Sync Scale** is on, and each client moves the entity smoothly between the states
it receives. Only the server moves such an entity: a client that moves it is overwritten
by the next state.

Two kinds of entity follow the server:

- **Entities saved in a scene**, which every peer already has when it loads the scene. A
  door or a platform only needs the component.
- **Bundles created with `Network.spawn`**, for what appears during the game: players,
  bullets, pickups. The root of the bundle has the component, and the server creates the
  instance in its scene and in the same scene of every client.

=== "Lua"

    ```lua
    -- on the server, one player for each client that joins
    Network.onPeerConnected = function(peer)
        players[peer] = Network.spawn("player", self.scene, peer)
    end

    Network.onPeerDisconnected = function(peer)
        BundleManager.destroyBundle(self.scene, players[peer])
        players[peer] = nil
    end
    ```

=== "C++"

    ```cpp
    // on the server, one player for each client that joins
    void Game::onPeerConnected(int peer){
        players[peer] = Network::spawn("player", getScene(), peer);
    }

    void Game::onPeerDisconnected(int peer){
        BundleManager::destroyBundle(getScene(), players[peer]);
        players.erase(peer);
    }
    ```

Destroying the instance on the server destroys it on the clients. A bundle created with
`BundleManager.createBundle` stays local, as before.

### Owners {#owners}

The last argument of `spawn` is the **owner**: the peer the entity belongs to, the
server when left out. The owner changes nothing by itself. It is there for the project
to ask whose entity this is, and it is already set when the scripts of the bundle start:

=== "Lua"

    ```lua
    function Player:init()
        if Network.isOwner(self.scene, self.entity) then
            -- this peer's own player: it gets the camera and reads the input
            RegisterEngineEvent(self, "onFixedUpdate")
        end
    end

    function Player:onFixedUpdate()
        Network.rpcUnreliable(Network.SERVER, "input", self.direction)
    end
    ```

=== "C++"

    ```cpp
    Player::Player(Scene* scene, Entity entity): ScriptBase(scene, entity){
        if (Network::isOwner(scene, entity)){
            // this peer's own player: it gets the camera and reads the input
            REGISTER_ENGINE_EVENT(onFixedUpdate);
        }
    }
    ```

The client sends what the player wants with an RPC, the server checks it and moves the
entity, and every client sees the result. A player's own entity is therefore shown a
little late, by the trip to the server and the [delay](#entity-tuning) below.

### Joining and leaving {#entity-join}

A client receives the entities of a scene when it has that scene loaded and is
connected, in either order: the spawned bundles as they are at that moment, and the
scene entities that moved. Clients in another scene receive nothing of this one.

When a client disconnects, the bundles the server spawned are destroyed in its scenes
and the scene entities stay where they were.

### Tuning {#entity-tuning}

The server sends states 20 times per second, and only for the entities that moved. A
client shows the scene 0.1 seconds in the past, so it has two states to move between
even when one is lost. `NetworkSystem` changes both for a scene:

```cpp
auto network = scene->getSystem<NetworkSystem>();
network->setSendRate(30);
network->setInterpolationDelay(0.07f);
```

A shorter delay shows the server sooner and stutters more on a bad connection. Keep it
above two send intervals.

### Physics {#entity-physics}

Physics runs on the server. While a client is connected, the copies it has of the
entities that follow the server are not simulated:

- A **dynamic body**, 2D or 3D, becomes **kinematic**. It moves to each state with a
  velocity, so it pushes the bodies that only this client has, like debris, and nothing
  on the client pushes it back.
- A **3D character** becomes [kinematic](../reference/classes/character3d.md#kinematic):
  it has no gravity and ignores `moveVelocity` and `jump`.

Apply forces, impulses and character movement on the server. A client asks for them
with an RPC:

=== "Lua"

    ```lua
    -- on the client that owns the player
    Network.rpc(Network.SERVER, "jump")

    -- on the server
    Network.registerRpc("jump", function(sender)
        Character3D(self.scene, players[sender]):jump(5)
    end)
    ```

=== "C++"

    ```cpp
    // on the client that owns the player
    Network::rpc(Network::SERVER, "jump");

    // on the server
    Network::registerRpc("jump", [this](int sender){
        Character3D(getScene(), players[sender]).jump(5);
    });
    ```

When the client disconnects, the bodies and characters of its scene entities are
simulated again, so the scene keeps working offline.

### What does not follow yet {#entity-limits}

- Only the transform is sent. Animations, colors and script values go through RPCs.
- In a bundle only the root follows; its children move with it.
- A spawned bundle is created at the root of the scene, not under a parent.
- A body on a child of a bundle is still simulated on the client. Keep the body on the
  root.
- A client does not predict its own player: it sees it after the trip to the server.

## Web builds {#web}

A web build connects with the browser's WebSocket:

- A page served over **HTTPS**, as on game portals and most hosts, may only open secure
  sockets. `connect("play.example.com", 7777)` then uses `wss://`, and the server must
  answer with TLS.
- The server itself has no TLS. Put a reverse proxy in front of it, which holds the
  certificate and forwards to the port. With [Caddy](https://caddyserver.com), which
  gets the certificate on its own:

    ```text
    play.example.com {
        reverse_proxy localhost:7777
    }
    ```

    Clients then call `Network.connect("wss://play.example.com")`.

An address that is a `ws://` or `wss://` URL connects with WebSocket on every platform.
Outside the web only `ws://` works.

A browser stops running a page in a hidden tab. The connection stays open and what the
server sent meanwhile arrives when the player comes back.

## Versions {#versions}

Builds that can't play together should refuse each other instead of failing later. Set
the same text on both sides before hosting or connecting, and change it whenever the
RPCs change:

```lua
Network.setVersion("1.4")
```

A client with another version gets `onConnectionFailed("version")`.

## Testing {#testing}

Run the project twice on one machine and connect to `127.0.0.1`, or export it and run
the copies side by side.

A game that works on one machine can fail on a real connection. `setSimulation` delays
and drops what this side sends, so set it on both sides to affect both directions:

```lua
-- 80 ms each way, 20 ms of jitter, 5% of the unreliable calls lost
Network.setSimulation(80, 20, 0.05)
```

Reliable calls are never dropped, as a lost one is sent again: they only arrive late.
`Network.getPing()` is the measured round trip to the server in milliseconds, updated
every second, and on the server `Network.getPing(peer)` is that of a client. Messages are
read once per frame, so it includes up to a frame of waiting on each side.

## Limits {#limits}

- The server must be reachable from its clients: a public address, or a forwarded
  port. There is no relay and no matchmaking; services like
  [Nakama](https://heroiclabs.com/nakama/) or the platform's own (Steam, Epic) provide
  them.
- UDP traffic is not encrypted. WebSocket traffic is when it goes through a TLS proxy.
- One RPC carries up to about 1 MB, and a Lua function receives up to 64 values.
- A client that does not finish connecting within 5 seconds is dropped by the server.

## Reference

- [Network](../reference/classes/network.md)
- [Events](events.md)
