---
description: Index of all Doriax API classes (C++ and Lua on each page).
---

# API Reference

Each class page documents the **C++ and Lua** API together, in the style of the
[Supernova Engine docs](https://github.com/supernovaengine/supernova-docs).

Pages with detailed method descriptions: **Engine**, **Scene**, **Object**, **Input**,
**Camera**, **Body2D**, **PhysicsSystem**, and related core types. Other classes list
the full API surface; expand descriptions over time by editing the markdown files
under `docs/reference/classes/`.

Use `doriax/generate_api_suggestions.py` in the engine repo to inventory bindings
when adding new APIs.

See also [Enumerations](enums.md) and [Build Options](build-options.md).

## Actions

- [Action](classes/action.md)
- [AlphaAction](classes/alphaaction.md)
- [Animation](classes/animation.md)
- [ColorAction](classes/coloraction.md)
- [MorphTracks](classes/morphtracks.md)
- [PositionAction](classes/positionaction.md)
- [RotateTracks](classes/rotatetracks.md)
- [RotationAction](classes/rotationaction.md)
- [ScaleAction](classes/scaleaction.md)
- [ScaleTracks](classes/scaletracks.md)
- [SpriteAnimation](classes/spriteanimation.md)
- [TimedAction](classes/timedaction.md)
- [TranslateTracks](classes/translatetracks.md)

## Components

- [ActionComponent](classes/actioncomponent.md)
- [AnimationComponent](classes/animationcomponent.md)
- [ButtonComponent](classes/buttoncomponent.md)
- [PanelComponent](classes/panelcomponent.md)
- [ParticlesComponent](classes/particlescomponent.md)
- [ProgressbarComponent](classes/progressbarcomponent.md)
- [ScrollbarComponent](classes/scrollbarcomponent.md)
- [SoundComponent](classes/soundcomponent.md)
- [SpriteAnimationComponent](classes/spriteanimationcomponent.md)
- [TextEditComponent](classes/texteditcomponent.md)
- [TilemapComponent](classes/tilemapcomponent.md)
- [TimedActionComponent](classes/timedactioncomponent.md)
- [UIComponent](classes/uicomponent.md)
- [UILayoutComponent](classes/uilayoutcomponent.md)

## Core

- [Engine](classes/engine.md)
- [EntityManager](classes/entitymanager.md)
- [EntityRegistry](classes/entityregistry.md)
- [Input](classes/input.md)
- [Log](classes/log.md)
- [Scene](classes/scene.md)
- [System](classes/system.md)

## I/O

- [Data](classes/data.md)
- [File](classes/file.md)
- [FileData](classes/filedata.md)
- [UserSettings](classes/usersettings.md)

## Managers

- [BundleManager](classes/bundlemanager.md)
- [SceneManager](classes/scenemanager.md)

## Math

- [AABB](classes/aabb.md)
- [Angle](classes/angle.md)
- [Matrix3](classes/matrix3.md)
- [Matrix4](classes/matrix4.md)
- [OBB](classes/obb.md)
- [Plane](classes/plane.md)
- [Quaternion](classes/quaternion.md)
- [Ray](classes/ray.md)
- [Rect](classes/rect.md)
- [Sphere](classes/sphere.md)
- [Vector2](classes/vector2.md)
- [Vector3](classes/vector3.md)
- [Vector4](classes/vector4.md)

## Objects

- [Bone](classes/bone.md)
- [Camera](classes/camera.md)
- [Fog](classes/fog.md)
- [Light](classes/light.md)
- [Light2D](classes/light2d.md)
- [Lines](classes/lines.md)
- [Mesh](classes/mesh.md)
- [Model](classes/model.md)
- [Object](classes/object.md)
- [Occluder2D](classes/occluder2d.md)
- [Points](classes/points.md)
- [ReflectionProbe](classes/reflectionprobe.md)
- [Shape](classes/shape.md)
- [SkyBox](classes/skybox.md)
- [Sound](classes/sound.md)
- [Sprite](classes/sprite.md)
- [Terrain](classes/terrain.md)
- [Tilemap](classes/tilemap.md)

### UI

- [Button](classes/button.md)
- [Container](classes/container.md)
- [Image](classes/image.md)
- [Panel](classes/panel.md)
- [Polygon](classes/polygon.md)
- [Progressbar](classes/progressbar.md)
- [Scrollbar](classes/scrollbar.md)
- [Text](classes/text.md)
- [TextEdit](classes/textedit.md)
- [UILayout](classes/uilayout.md)

## Other

- [ActionFrame](classes/actionframe.md)
- [Base64](classes/base64.md)
- [Color](classes/color.md)
- [EntityHandle](classes/entityhandle.md)
- [FramebufferRender](classes/framebufferrender.md)
- [InstanceData](classes/instancedata.md)
- [LineData](classes/linedata.md)
- [MeshPolygon](classes/meshpolygon.md)
- [OverallBuildProgress](classes/overallbuildprogress.md)
- [PointData](classes/pointdata.md)
- [RayReturn](classes/rayreturn.md)
- [ResourceBuildInfo](classes/resourcebuildinfo.md)
- [ResourceProgress](classes/resourceprogress.md)
- [TextureLoadResult](classes/textureloadresult.md)
- [TextureRender](classes/texturerender.md)
- [ThreadPoolManager](classes/threadpoolmanager.md)
- [TileData](classes/tiledata.md)
- [TileRectData](classes/tilerectdata.md)

## Particles

- [ParticleAccelerationInitializer](classes/particleaccelerationinitializer.md)
- [ParticleAccelerationModifier](classes/particleaccelerationmodifier.md)
- [ParticleAlphaInitializer](classes/particlealphainitializer.md)
- [ParticleAlphaModifier](classes/particlealphamodifier.md)
- [ParticleBurst](classes/particleburst.md)
- [ParticleColorGradient](classes/particlecolorgradient.md)
- [ParticleColorGradientStop](classes/particlecolorgradientstop.md)
- [ParticleColorInitializer](classes/particlecolorinitializer.md)
- [ParticleColorModifier](classes/particlecolormodifier.md)
- [ParticleLifeInitializer](classes/particlelifeinitializer.md)
- [ParticlePositionInitializer](classes/particlepositioninitializer.md)
- [ParticlePositionModifier](classes/particlepositionmodifier.md)
- [ParticleRotationInitializer](classes/particlerotationinitializer.md)
- [ParticleRotationModifier](classes/particlerotationmodifier.md)
- [Particles](classes/particles.md)
- [ParticleScaleInitializer](classes/particlescaleinitializer.md)
- [ParticleScaleModifier](classes/particlescalemodifier.md)
- [ParticleSizeInitializer](classes/particlesizeinitializer.md)
- [ParticleSizeModifier](classes/particlesizemodifier.md)
- [ParticleSpriteInitializer](classes/particlespriteinitializer.md)
- [ParticleSpriteModifier](classes/particlespritemodifier.md)
- [ParticleVelocityInitializer](classes/particlevelocityinitializer.md)
- [ParticleVelocityModifier](classes/particlevelocitymodifier.md)

## Physics

- [Body2D](classes/body2d.md)
- [Body3D](classes/body3d.md)
- [CollideShapeResult3D](classes/collideshaperesult3d.md)
- [Contact2D](classes/contact2d.md)
- [Contact3D](classes/contact3d.md)
- [Joint2D](classes/joint2d.md)
- [Joint3D](classes/joint3d.md)
- [Manifold2D](classes/manifold2d.md)
- [PhysicsSystem](classes/physicssystem.md)

## Scripting

- [ScriptBase](classes/scriptbase.md)

## Systems

- [ActionSystem](classes/actionsystem.md)
- [AudioSystem](classes/audiosystem.md)
- [MeshSystem](classes/meshsystem.md)
- [RenderSystem](classes/rendersystem.md)
- [UISystem](classes/uisystem.md)

## Textures

- [Framebuffer](classes/framebuffer.md)
- [Material](classes/material.md)
- [Texture](classes/texture.md)
- [TextureData](classes/texturedata.md)
