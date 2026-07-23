---
description: SpriteAnimation API reference (C++ and Lua).
---

# SpriteAnimation

**Inherits:** [Action](action.md)  
**C++ type:** `SpriteAnimation`

## Description

Cycles through a sequence of texture atlas frames on its target [Sprite](sprite.md), creating flip-book-style 2D animation. This is distinct from skeletal animation ([Animation](animation.md)); `SpriteAnimation` only advances the active frame of a sprite sheet.

### Properties

| Type | Name | Default | Langs |
| --- | --- | --- | --- |
| std::string | [name](#name) | `""` | C++ \| Lua |

### Methods

| Type | Name | Langs |
| --- | --- | --- |
| void | [setAnimation](#setanimation) | C++ \| Lua |

## Property details

### name

*Inherited from:* [EntityHandle](entityhandle.md#name)

* *Setter*: void **setName**(const std::string& name)
* *Getter*: std::string **getName**() const

The sprite animation entity's human-readable name. The editor shows this name in the
Structure panel. There is no separate name stored in
[`SpriteAnimationComponent`](spriteanimationcomponent.md) — rename the entity (or call
`setName`) when you need a label for lookup with
[`Scene::findEntity`](entityregistry.md#findentity).

## Method details

### setAnimation

* void **setAnimation**(std::vector\<int\> frames, std::vector\<int\> framesTime, bool loop)
* void **setAnimation**(int startFrame, int endFrame, int interval, bool loop)

Configure the frame sequence.

**First overload** — explicit frame list with per-frame durations in milliseconds:

=== "C++"
    ```cpp
    SpriteAnimation anim(&scene);
    anim.setTarget(&hero);
    // Show frames 0, 1, 2, 1 with 100 ms each
    anim.setAnimation({0, 1, 2, 1}, {100, 100, 100, 100}, true);
    anim.start();
    ```

=== "Lua"
    ```lua
    local anim = SpriteAnimation(scene)
    anim:setTarget(hero)
    anim:setAnimation({0, 1, 2, 1}, {100, 100, 100, 100}, true)
    anim:start()
    ```

**Second overload** — range-based with a fixed interval (milliseconds per frame):

=== "C++"
    ```cpp
    SpriteAnimation walk(&scene);
    walk.setTarget(&hero);
    walk.setAnimation(4, 7, 120, true);  // frames 4-7, 120 ms each
    walk.start();
    ```

=== "Lua"
    ```lua
    local walk = SpriteAnimation(scene)
    walk:setTarget(hero)
    walk:setAnimation(4, 7, 120, true)
    walk:start()
    ```

## See also

- [SpriteAnimationComponent](spriteanimationcomponent.md)
- [Sprite](sprite.md)
- [Action](action.md)