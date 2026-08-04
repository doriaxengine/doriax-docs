---
description: Object API reference — transform, hierarchy, visibility, billboards, and physics bodies.
---

# Object

## Description

`Object` is the base class for all scene objects. It wraps an ECS entity and exposes the transform (position, rotation, scale), parent–child hierarchy, visibility, billboard orientation, and shortcuts to the physics body attachments.

**Inherits:** [EntityHandle](entityhandle.md)

=== "C++"

    ```cpp
    #include "Doriax.h"
    using namespace doriax;

    Sprite sprite(&scene);
    sprite.setPosition(100.0f, 200.0f, 0.0f);
    sprite.setVisible(true);
    ```

=== "Lua"

    ```lua
    local sprite = Sprite(scene)
    sprite.position = Vector3(100, 200, 0)
    sprite.visible = true
    ```

### Properties

| Type | Name | Default | Languages |
| --- | --- | --- | --- |
| Vector3 | [position](#position) | `(0,0,0)` | C++ \| Lua |
| Quaternion | [rotation](#rotation) | identity | C++ \| Lua |
| Vector3 | [scale](#scale) | `(1,1,1)` | C++ \| Lua |
| bool | [visible](#visible) | `true` | C++ \| Lua |
| bool | [billboard](#billboard) | `false` | C++ \| Lua |
| bool | [fakeBillboard](#fakebillboard) | `false` | C++ \| Lua |
| bool | [cylindricalBillboard](#cylindricalbillboard) | `false` | C++ \| Lua |
| Quaternion | [billboardRotation](#billboardrotation) | identity | C++ \| Lua |
| Matrix4 | [localMatrix](#localmatrix) | identity | C++ \| Lua |
| Matrix4 | [modelMatrix](#modelmatrix) | — | C++ \| Lua |
| Matrix4 | [normalMatrix](#normalmatrix) | — | C++ \| Lua |

### Methods

| Returns | Name | Languages |
| --- | --- | --- |
| void | [addChild](#addchild) | C++ \| Lua |
| void | [removeChild](#removechild) | C++ \| Lua |
| void | [removeParent](#removeparent) | C++ \| Lua |
| void | [moveToTop](#movetotop-moveup-movedown-movetobottom) | C++ \| Lua |
| void | [moveUp](#movetotop-moveup-movedown-movetobottom) | C++ \| Lua |
| void | [moveDown](#movetotop-moveup-movedown-movetobottom) | C++ \| Lua |
| void | [moveToBottom](#movetotop-moveup-movedown-movetobottom) | C++ \| Lua |
| void | [setPosition](#setposition) | C++ \| Lua |
| Vector3 | [getPosition](#setposition) | C++ \| Lua |
| Vector3 | [getWorldPosition](#getworldposition) | C++ \| Lua |
| void | [setRotation](#setrotation) | C++ \| Lua |
| Quaternion | [getRotation](#setrotation) | C++ \| Lua |
| Quaternion | [getWorldRotation](#setrotation) | C++ \| Lua |
| void | [setScale](#setscale) | C++ \| Lua |
| Vector3 | [getScale](#setscale) | C++ \| Lua |
| Vector3 | [getWorldScale](#setscale) | C++ \| Lua |
| void | [setVisible](#setvisible) | C++ \| Lua |
| bool | [isVisible](#setvisible) | C++ \| Lua |
| void | [setVisibleOnly](#setvisibleonly) | C++ \| Lua |
| void | [setBillboard](#setbillboard) | C++ \| Lua |
| bool | [isBillboard](#billboard) | C++ \| Lua |
| void | [setFakeBillboard](#fakebillboard) | C++ \| Lua |
| bool | [isFakeBillboard](#fakebillboard) | C++ \| Lua |
| void | [setCylindricalBillboard](#cylindricalbillboard) | C++ \| Lua |
| bool | [isCylindricalBillboard](#cylindricalbillboard) | C++ \| Lua |
| void | [setBillboardRotation](#billboardrotation) | C++ \| Lua |
| Quaternion | [getBillboardRotation](#billboardrotation) | C++ \| Lua |
| void | [setLocalMatrix](#localmatrix) | C++ \| Lua |
| Matrix4 | [getLocalMatrix](#localmatrix) | C++ \| Lua |
| Matrix4 | [getModelMatrix](#modelmatrix) | C++ \| Lua |
| Matrix4 | [getNormalMatrix](#normalmatrix) | C++ \| Lua |
| void | [updateTransform](#updatetransform) | C++ \| Lua |
| [Body2D](body2d.md) | [getBody2D](#getbody2d) | C++ \| Lua |
| void | [removeBody2D](#removebody2d) | C++ \| Lua |
| [Body3D](body3d.md) | [getBody3D](#getbody3d) | C++ \| Lua |
| void | [removeBody3D](#removebody3d) | C++ \| Lua |
| [Ray](ray.md) | [getRay](#getray) | C++ \| Lua |

## Property details

### position

* *Setter:* `void setPosition(Vector3 position)`
* *Setter:* `void setPosition(float x, float y, float z)`
* *Setter:* `void setPosition(float x, float y)` *(2D shorthand, z = 0)*
* *Getter:* `Vector3 getPosition() const`

Local position relative to the parent object (or world origin if no parent). Changing position does not automatically update children — that is handled by the scene's transform system each frame.

On an entity with a physics body this is not the way to move it from `onFixedUpdate` — see [Body2D](body2d.md#position-angle) / [Body3D](body3d.md#position-rotation) `position`.

=== "C++"

    ```cpp
    obj.setPosition(100.0f, 0.0f, -50.0f);
    Vector3 pos = obj.getPosition();
    ```

=== "Lua"

    ```lua
    obj.position = Vector3(100, 0, -50)
    local pos = obj.position
    ```

---

### rotation

* *Setter:* `void setRotation(Quaternion rotation)`
* *Setter:* `void setRotation(float xAngle, float yAngle, float zAngle)` *(Euler angles in degrees when `Engine::useDegrees` is true)*
* *Getter:* `Quaternion getRotation() const`

Local rotation relative to the parent. The Euler overload applies rotations in X → Y → Z order.

=== "C++"

    ```cpp
    obj.setRotation(0.0f, 45.0f, 0.0f);  // 45° around Y
    ```

=== "Lua"

    ```lua
    obj.rotation = Quaternion.fromEuler(0, 45, 0)
    ```

---

### scale

* *Setter:* `void setScale(Vector3 scale)`
* *Setter:* `void setScale(float factor)` *(uniform scale)*
* *Getter:* `Vector3 getScale() const`

Local scale relative to the parent.

---

### visible

* *Setter:* `void setVisible(bool visible)`
* *Getter:* `bool isVisible() const`

Hides or shows the object **and all of its children**. To hide only this object without affecting children, use [setVisibleOnly](#setvisibleonly).

---

### billboard

* *Setter:* `void setBillboard(bool billboard)`
* *Getter:* `bool isBillboard() const`

When `true`, the object's orientation is overridden each frame so it always faces the active camera. Position and scale are unaffected.

---

### fakeBillboard

* *Setter:* `void setFakeBillboard(bool fakeBillboard)`
* *Getter:* `bool isFakeBillboard() const`

Fake billboard rotates the object to face the camera while keeping the local `position` offset in world space. Unlike a true billboard, the object moves as its parent moves but stays facing the camera.

---

### cylindricalBillboard

* *Setter:* `void setCylindricalBillboard(bool cylindricalBillboard)`
* *Getter:* `bool isCylindricalBillboard() const`

Constrains billboard rotation to the Y axis only (vertical axis). The object faces the camera horizontally but does not tilt up or down.

---

### billboardRotation

* *Setter:* `void setBillboardRotation(Quaternion rotation)`
* *Setter:* `void setBillboardRotation(float xAngle, float yAngle, float zAngle)`
* *Getter:* `Quaternion getBillboardRotation() const`

An additional rotation applied on top of the billboard face-camera rotation. Use to offset or spin billboard sprites.

---

### localMatrix

* *Setter:* `void setLocalMatrix(Matrix4 localMatrix)`
* *Getter:* `Matrix4 getLocalMatrix() const`

Provides direct access to the local-space transform matrix. Setting this overrides position/rotation/scale decomposed values. Useful for loading pre-computed transforms from GLTF animations or procedural geometry.

---

### modelMatrix

* *Getter:* `Matrix4 getModelMatrix() const`

Read-only world-space transform matrix, computed from the full parent chain. Updated by the transform system every frame.

---

### normalMatrix

* *Getter:* `Matrix4 getNormalMatrix() const`

Inverse transpose of the model matrix. Used in shaders to correctly transform surface normals when non-uniform scale is applied.

## Method details

### addChild

* `void addChild(Object* child)`
* `void addChild(Entity child)`

Attaches `child` to this object's transform hierarchy. The child's `position`, `rotation`, and `scale` become relative to this object.

=== "C++"

    ```cpp
    Sprite parent(&scene);
    Sprite child(&scene);
    parent.addChild(&child);
    ```

=== "Lua"

    ```lua
    local parent = Sprite(scene)
    local child  = Sprite(scene)
    parent:addChild(child)
    ```

---

### removeChild

* `void removeChild(Object* child)`
* `void removeChild(Entity child)`

Detaches `child` from this hierarchy. The child's world transform is preserved by converting it back to world-space values.

---

### removeParent

* `void removeParent()`

Detaches this object from its parent and re-parents it to the scene root. The world transform is preserved.

---

### moveToTop / moveUp / moveDown / moveToBottom

Control the draw/update order of this object among its siblings.

* **moveToTop** — Drawn last (on top of siblings).
* **moveUp** — Moves one position toward the top.
* **moveDown** — Moves one position toward the bottom.
* **moveToBottom** — Drawn first (behind siblings).

=== "C++"

    ```cpp
    sprite.moveToTop();
    ```

=== "Lua"

    ```lua
    sprite:moveToTop()
    ```

---

### setPosition

* `void setPosition(Vector3 position)`
* `void setPosition(float x, float y, float z)`
* `void setPosition(float x, float y)`

Sets local position. See [position](#position) property.

---

### getWorldPosition

* `Vector3 getWorldPosition() const`

Returns the position of this object in world space, taking the full parent chain into account.

---

### setRotation

* `void setRotation(Quaternion rotation)`
* `void setRotation(float xAngle, float yAngle, float zAngle)`

Sets local rotation. See [rotation](#rotation) property.

---

### getWorldRotation

* `Quaternion getWorldRotation() const`

Returns the combined world-space rotation after applying all parent rotations.

---

### setScale

* `void setScale(Vector3 scale)`
* `void setScale(float factor)`

Sets local scale. The single-float overload applies uniform scale on all axes.

---

### getWorldScale

* `Vector3 getWorldScale() const`

Returns the effective world-space scale, multiplied through the parent chain.

---

### setVisible

* `void setVisible(bool visible)`
* `bool isVisible() const`

Shows or hides this object and all its descendants.

---

### setVisibleOnly

* `void setVisibleOnly(bool visible)`

Shows or hides only this object without propagating the change to children.

---

### setBillboard

* `void setBillboard(bool billboard, bool fake, bool cylindrical)`
* `void setBillboard(bool billboard)`

Enables billboard mode. The three-argument overload allows setting `fake` and `cylindrical` flags in a single call. See [billboard](#billboard), [fakeBillboard](#fakebillboard), and [cylindricalBillboard](#cylindricalbillboard).

---

### updateTransform

* `void updateTransform()`

Forces an immediate recalculation of the world transform. The engine handles this automatically each frame; call only when you need an up-to-date transform outside the normal update order. Writing a transform from `onFixedUpdate` is one such case: the physics step reads the world transform, which is otherwise only refreshed once per frame.

---

### getBody2D

* `Body2D getBody2D()`

Returns the [Body2D](body2d.md) physics handle for this object. Creates the body component if it does not already exist.

=== "C++"

    ```cpp
    Body2D body = sprite.getBody2D();
    body.createBoxShape(64.0f, 64.0f);
    body.setType(BodyType::DYNAMIC);
    body.load();
    ```

=== "Lua"

    ```lua
    local body = sprite:getBody2D()
    body:createBoxShape(64, 64)
    body.type = BodyType.DYNAMIC
    body:load()
    ```

---

### removeBody2D

* `void removeBody2D()`

Destroys the 2D physics body attached to this object.

---

### getBody3D

* `Body3D getBody3D()`

Returns the [Body3D](body3d.md) physics handle for this object. Creates the body component if it does not already exist.

---

### removeBody3D

* `void removeBody3D()`

Destroys the 3D physics body attached to this object.

---

### getRay

* `Ray getRay(Vector3 direction)`

Constructs a [Ray](ray.md) originating from this object's world position in the given world-space direction. Useful for raycasting from an object's location.

=== "C++"

    ```cpp
    Ray ray = obj.getRay(Vector3(0, -1, 0));  // ray pointing down
    ```

=== "Lua"

    ```lua
    local ray = obj:getRay(Vector3(0, -1, 0))
    ```
