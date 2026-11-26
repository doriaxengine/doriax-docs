---
description: Network API reference (C++ and Lua) — hosting a server, connecting clients and calling RPCs on other peers.
---

# Network

**C++ type:** `Network` (static) · **Header:** `Network.h`

## Description

A multiplayer session: one server and its clients, on UDP for desktop and mobile builds
and on WebSocket for web builds. Peers call functions on each other with RPCs. A client
only reaches the server. See [Multiplayer](../../manual/multiplayer.md) for the model
and how to use it.

=== "C++"

    ```cpp
    Network::registerRpc("say", [](int sender, std::string text){
        Log::print("peer %i: %s", sender, text.c_str());
    });

    if (hosting){
        Network::host(7777);
    }else{
        Network::connect("192.168.0.10", 7777);
    }

    Network::rpc(Network::ALL, "say", "hello");
    ```

=== "Lua"

    ```lua
    Network.registerRpc("say", function(sender, text)
        print("peer " .. sender .. ": " .. text)
    end)

    if hosting then
        Network.host(7777)
    else
        Network.connect("192.168.0.10", 7777)
    end

    Network.rpc(Network.ALL, "say", "hello")
    ```

### Constants

| Type | Name | Value | Langs |
| --- | --- | --- | --- |
| int | `ALL` | 0, every connected peer | C++ \| Lua |
| int | `SERVER` | 1, the server | C++ \| Lua |

### Properties

| Type | Name | Langs |
| --- | --- | --- |
| [NetworkState](#networkstate) | [state](#getstate) (read-only) | Lua |
| int | [id](#getid) (read-only) | Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| static bool | [host](#host) | C++ \| Lua |
| static bool | [hostOffline](#hostoffline) | C++ \| Lua |
| static bool | [connect](#connect) | C++ \| Lua |
| static void | [close](#close) | C++ \| Lua |
| static void | [disconnect](#disconnect) | C++ \| Lua |
| static [NetworkState](#networkstate) | [getState](#getstate) | C++ |
| static bool | [isServer](#isserver-isconnected) | C++ \| Lua |
| static bool | [isConnected](#isserver-isconnected) | C++ \| Lua |
| static int | [getId](#getid) | C++ |
| static std::vector&lt;int&gt; | [getPeers](#getpeers) | C++ \| Lua |
| static float | [getPing](#getping) | C++ \| Lua |
| static void | [setVersion](#setversion) | C++ \| Lua |
| static void | [setSimulation](#setsimulation) | C++ \| Lua |
| static void | [registerRpc](#registerrpc) | C++ \| Lua |
| static void | [unregisterRpc](#unregisterrpc) | C++ \| Lua |
| static bool | [rpc](#rpc-rpcunreliable) | C++ \| Lua |
| static bool | [rpcUnreliable](#rpc-rpcunreliable) | C++ \| Lua |
| static Entity | [spawn](#spawn) | C++ \| Lua |
| static int | [getOwner](#getowner-isowner) | C++ \| Lua |
| static bool | [isOwner](#getowner-isowner) | C++ \| Lua |
| static void | [sync](#sync) | C++ \| Lua |

### Callback events

| Callback | Name | Languages |
| --- | --- | --- |
| void(int) | [onPeerConnected](#events) | C++ \| Lua |
| void(int) | [onPeerDisconnected](#events) | C++ \| Lua |
| void() | [onConnected](#events) | C++ \| Lua |
| void(std::string) | [onConnectionFailed](#events) | C++ \| Lua |
| void() | [onDisconnected](#events) | C++ \| Lua |

## Method details

### host

* static bool **host**(uint16_t port, int maxPeers = 32)

Starts a server on the port: UDP, and TCP for the WebSocket connections of web builds.
False when a port can't be opened, or in a web build, which can't host. Any session
this peer was in is closed first.

---

### hostOffline

* static bool **hostOffline**()

A server that opens no port and accepts no client, so a single player runs the same
code as a multiplayer session. RPCs sent to `SERVER` are called here.

---

### connect

* static bool **connect**(const std::string& address, uint16_t port = 0)

Connects to a server by host name or IP address. False when the attempt can't start,
as with a name that does not resolve. Otherwise [`onConnected`](#events) or
[`onConnectionFailed`](#events) reports the result.

Desktop and mobile builds use UDP. Web builds use WebSocket, with `wss://` when the
page is served over HTTPS. An address that is a `ws://` or `wss://` URL uses WebSocket
on every platform and may hold the port and a path; outside the web only `ws://`
works. See [Web builds](../../manual/multiplayer.md#web).

---

### close

* static void **close**()

Leaves the session: a server disconnects its clients, a client leaves its server. No
event fires on this peer.

---

### disconnect

* static void **disconnect**(int peer)

On the server, removes a client. [`onPeerDisconnected`](#events) fires for it.

---

### getState

* static [NetworkState](#networkstate) **getState**()

Whether this peer is offline, connecting, connected to a server or hosting. `state` in
Lua.

---

### isServer / isConnected {#isserver-isconnected}

* static bool **isServer**()
* static bool **isConnected**()

`isServer()` is true while hosting, also offline. `isConnected()` is true on a client
once the server accepted it.

---

### getId

* static int **getId**()

The number of this peer: 1 on the server, 2 or more on a client, 0 while not connected.
`id` in Lua.

---

### getPeers

* static std::vector&lt;int&gt; **getPeers**()

The connected peers: the clients on the server, and only the server on a client.

---

### getPing

* static float **getPing**(int peer = SERVER)

The round trip to a peer in milliseconds, measured every second. 0 while unknown.

---

### setVersion

* static void **setVersion**(const std::string& version)

A server refuses clients whose version differs from its own, with the reason
`version`. Set it before hosting or connecting. See
[Versions](../../manual/multiplayer.md#versions).

---

### setSimulation

* static void **setSimulation**(float latency, float jitter, float loss)

Simulates a bad connection on what this peer sends: `latency` and `jitter` in
milliseconds, and `loss` from 0 to 1 for the share of unreliable RPCs dropped. Zeros
turn it off. See [Testing](../../manual/multiplayer.md#testing).

---

### registerRpc

* static void **registerRpc**(const std::string& name, Function function)

Registers the function a peer calls with this name. It receives the sender's number
and then the values. A name holds one function: registering it again replaces the
earlier one.

A script registers one of its methods, and the RPC is removed when the script is
destroyed. See [RPCs in a script](../../manual/multiplayer.md#rpc-scripts).

=== "C++"

    ```cpp
    REGISTER_RPC("hit", onHit);

    void Game::onHit(int sender, int target, float damage){
        applyDamage(target, damage);
    }
    ```

    An RPC whose values don't match the parameters after `int sender` is logged and
    not called.

=== "Lua"

    ```lua
    Network.registerRpc("hit", self, "onHit")

    function Game:onHit(sender, target, damage)
        applyDamage(target, damage)
    end
    ```

Outside a script the function is a lambda or a function pointer in C++ and a function
in Lua. It stays until [`unregisterRpc`](#unregisterrpc).

---

### unregisterRpc

* static void **unregisterRpc**(const std::string& name)

Removes a function. RPCs that arrive for an unknown name are logged and ignored.

---

### rpc / rpcUnreliable {#rpc-rpcunreliable}

* static bool **rpc**(int target, const std::string& name, values...)
* static bool **rpcUnreliable**(int target, const std::string& name, values...)

Calls the function registered as `name` on the target: a peer, `ALL`, or this peer's
own number to call it here on the next frame. False when the target is not connected
or there is no session.

The values are `nil`, booleans, integers, numbers, strings, `Vector2`, `Vector3`,
`Vector4` and `Quaternion`. `rpc` always arrives and keeps the order of the calls;
`rpcUnreliable` may be lost. See [RPCs](../../manual/multiplayer.md#rpcs).

---

### spawn

* static Entity **spawn**(const std::string& bundle, Scene* scene, int owner = SERVER)

On the server, creates an instance of a bundle in the scene and in the same scene of
every client. The root of the bundle needs a
[NetworkComponent](networkcomponent.md). Returns the root, or no entity when this peer
is not the server. Destroying the instance destroys it on the clients too. See
[Entities that follow the server](../../manual/multiplayer.md#entities).

---

### getOwner / isOwner {#getowner-isowner}

* static int **getOwner**(Scene* scene, Entity entity)
* static bool **isOwner**(Scene* scene, Entity entity)

The peer an entity was spawned for: 1, the server, for an entity of the scene, and 0
for an entity without a NetworkComponent. `isOwner` is true when it is this peer.

---

### sync

* static void **sync**(Scene* scene, Entity entity, const std::string& name, T* value, std::function&lt;void()&gt; changed = nullptr)

Makes a value of a script follow the server: the clients receive it when it changes on
the server and when they join, and `changed` is called on a client after the value was
replaced. The entity needs a [NetworkComponent](networkcomponent.md). In a C++ script
`REGISTER_SYNC(member)` registers a member and removes it with the script.

In Lua it is `Network.sync(self, "field", "methodName")`, where the optional method
receives the new and the old value. See
[Script values](../../manual/multiplayer.md#entity-values).

## Events

Each event is a static `FunctionSubscribe` member; subscribe with `REGISTER_EVENT` in C++
or `RegisterEvent` in Lua (see [Events](../../manual/events.md#service-events)).

| Event | Parameters | When |
| --- | --- | --- |
| `onPeerConnected` | `int peer` | On the server, a client joined |
| `onPeerDisconnected` | `int peer` | On the server, a client left, was lost or was disconnected |
| `onConnected` | — | On a client, the server accepted the connection |
| `onConnectionFailed` | `std::string reason` | On a client, no connection: `unreachable`, `timeout`, `version`, `full` or `protocol` |
| `onDisconnected` | — | On a client, the server closed or was lost |

## Enumerations

### NetworkState

* **OFFLINE** — No session.
* **CONNECTING** — A client waiting for its server.
* **CONNECTED** — A client of a server.
* **HOSTING** — A server.
