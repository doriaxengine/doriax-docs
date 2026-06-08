---
description: UI components, layout, anchors, events, text, buttons, panels, and UI scenes in Doriax.
---

# User Interface

Doriax includes a complete runtime UI system for menus, HUDs, overlays, and in-game
controls. UI entities are regular ECS entities with UI-specific components and layout
state. Because the UI system is built on the same ECS foundation as the rest of the
engine, you can combine UI with 3D, 2D, and scripting seamlessly.

![Doriax UI tools](../assets/screenshots/editor-ui.png)

## UI scenes

For anything beyond a single HUD element, put UI into its own **UI scene** and add it
as a scene layer on top of your gameplay scene.

```lua
-- Startup: run gameplay and HUD simultaneously
Engine.setScene(gameplayScene)
Engine.addSceneLayer(hudScene)
```

This approach keeps gameplay entities separate from screen-space widgets, makes it easy
to swap menus without touching gameplay data, and lets you load/unload UI independently
(for example, showing a pause menu without reloading the game level).

Typical UI scene examples:

| UI Scene | Content |
| --- | --- |
| HUD | Health bar, ammo counter, minimap overlay |
| Main menu | Title, Play/Settings/Quit buttons |
| Pause menu | Resume, Options, Quit to menu |
| Settings screen | Sliders, dropdowns, back button |
| Dialog / modal | Confirmation popup, item description panel |
| Loading screen | Progress bar and spinner |

## UI widget classes

| Class | Purpose |
| --- | --- |
| [`UILayout`](../reference/classes/uilayout.md) | Base for all UI elements — anchors, size, and margin |
| [`Image`](../reference/classes/image.md) | Textured or solid-color rectangular region, 9-patch scaling |
| [`Text`](../reference/classes/text.md) | Unicode text with font, size, color, and multiline support |
| [`Button`](../reference/classes/button.md) | Interactive button with normal/over/pressed state textures and label |
| [`Panel`](../reference/classes/panel.md) | Framed or colored container with optional 9-patch background |
| [`TextEdit`](../reference/classes/textedit.md) | Single-line text input with placeholder and password mode |
| [`Scrollbar`](../reference/classes/scrollbar.md) | Horizontal or vertical scroll control with step and onChange callback |
| [`Progressbar`](../reference/classes/progressbar.md) | Horizontal or vertical fill display |
| [`Container`](../reference/classes/container.md) | Automatic layout for vertical, horizontal, or wrapped children |
| [`Polygon`](../reference/classes/polygon.md) | Simple polygon drawing, usable in 2D and UI scenes |

## Anchors and layout

Every UI element inherits from `UILayout` which exposes an anchor system for
resolution-independent placement. Anchors define how an element is positioned and sized
relative to its parent.

### Anchor presets

Use anchor presets for the most common layouts:

```cpp
Image logo(&scene);
logo.setAnchorPreset(AnchorPreset::CENTER);
logo.setTexture("ui/logo.png");

Image header(&scene);
header.setAnchorPreset(AnchorPreset::TOP_WIDE);  // stretches full width at the top
```

Available presets include `TOP_LEFT`, `TOP_CENTER`, `TOP_RIGHT`, `CENTER_LEFT`,
`CENTER`, `CENTER_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_CENTER`, `BOTTOM_RIGHT`, `LEFT_WIDE`,
`RIGHT_WIDE`, `TOP_WIDE`, `BOTTOM_WIDE`, and `FULL_RECT` (stretch to fill parent).

### Manual anchors

For precise control, set the four anchor values directly. Anchor values range from 0
(left/top of parent) to 1 (right/bottom of parent):

```lua
widget.anchorLeft   = 0.25
widget.anchorRight  = 0.75
widget.anchorTop    = 0.0
widget.anchorBottom = 0.5
```

## Building UI in code

=== "Lua"

    ```lua
    scene = Scene()

    -- Background panel
    panel = Panel(scene)
    panel:setAnchorPreset(AnchorPreset.CENTER)
    panel:setSize(400, 300)
    panel:setTexture("ui/panel_bg.png")

    -- Label
    title = Text(scene)
    title:setParent(panel)
    title:setAnchorPreset(AnchorPreset.TOP_CENTER)
    title:setText("Game Over")
    title:setFontSize(36)

    -- Button
    btn = Button(scene)
    btn:setParent(panel)
    btn:setAnchorPreset(AnchorPreset.BOTTOM_CENTER)
    btn:setLabel("Restart")
    btn.onPress = function()
        SceneManager.loadScene("Game")
    end

    Engine.setScene(scene)
    ```

=== "C++"

    ```cpp
    Scene uiScene;

    Panel panel(&uiScene);
    panel.setAnchorPreset(AnchorPreset::CENTER);
    panel.setSize(400, 300);
    panel.setTexture("ui/panel_bg.png");

    Text title(&uiScene);
    title.setParent(panel);
    title.setAnchorPreset(AnchorPreset::TOP_CENTER);
    title.setText("Game Over");
    title.setFontSize(36);

    Button btn(&uiScene);
    btn.setParent(panel);
    btn.setAnchorPreset(AnchorPreset::BOTTOM_CENTER);
    btn.setLabel("Restart");
    btn.onPress = []() {
        SceneManager::loadScene("Game");
    };
    ```

## UI events and input

UI widgets receive pointer and touch events automatically. The `Button` fires `onPress`
and `onRelease`; `TextEdit` fires `onChange` when the text changes; `Scrollbar` fires
`onChange` with the new scroll value.

To prevent UI clicks from also triggering gameplay input (such as shooting when the
player taps a UI button), call:

=== "Lua"

    ```lua
    Engine.setIgnoreEventsHandledByUI(true)
    ```

=== "C++"

    ```cpp
    Engine::setIgnoreEventsHandledByUI(true);
    ```

## 9-patch scaling

`Image` and `Panel` support 9-patch (nine-slice) scaling so borders remain sharp as
the widget resizes. Set the border insets to define the corner and edge regions that
should not be stretched:

```cpp
Image frame(&scene);
frame.setTexture("ui/frame.png");
frame.setPatchMargin(12, 12, 12, 12);  // left, right, top, bottom pixel margins
frame.setSize(300, 200);
```

## Containers

`Container` arranges its children automatically in a vertical stack, horizontal row, or
wrapped grid. This is useful for inventory grids, option lists, and toolbars where the
number of items changes at runtime.

```lua
list = Container(scene)
list:setContainerType(ContainerType.VERTICAL)
list:setSpacing(8)

for i = 1, 5 do
    local item = Button(scene)
    item:setParent(list)
    item:setLabel("Item " .. i)
end
```

## Canvas size and scaling

The UI canvas size defines the logical coordinate space. Set a fixed canvas size that
matches your design resolution and choose a scaling mode:

| Scaling mode | Behavior |
| --- | --- |
| `FITWIDTH` | Scale to fit the horizontal axis; may letterbox vertically |
| `FITHEIGHT` | Scale to fit the vertical axis; may letterbox horizontally |
| `LETTERBOX` | Fit inside the screen maintaining aspect ratio |
| `CROP` | Fill the screen, cropping edges |
| `STRETCH` | Stretch to fill (may distort) |
| `NATIVE` | Use actual screen pixel resolution |

Set the canvas size on the scene before adding UI:

```cpp
scene.setCanvasSize(1920, 1080);
scene.setScalingMode(ScalingMode::LETTERBOX);
```

## Practical guidance

- Design against a fixed canvas size (e.g. 1920×1080 or 1280×720) for predictable
  layouts across screen sizes.
- Use anchor presets wherever possible; reserve manual anchor values for non-standard
  layouts.
- Separate HUD, pause menu, and modal dialogs into different root containers or
  separate UI scenes.
- Keep UI textures and fonts organized in a dedicated asset folder.
- Use `Container` for lists and grids so the layout adjusts automatically when items
  are added or removed.
- Test UI scaling on the target aspect ratios early in development.
