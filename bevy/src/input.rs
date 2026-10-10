//! Shared action-input adapter (keyboard/mouse + Xbox controller).
//!
//! Gameplay code never reads raw devices. Each frame the adapter folds every device
//! into one `ActionState`, gated by `ControlOwner` so a menu (later: GMod Q-menu,
//! skate HUD) can take input without the world also reacting (the legacy F019 lesson:
//! the NVSE build read keys globally while the console/menus were open).
//! The autotest drives the same `ActionState` through `InjectedInput`, so scripted
//! tests exercise the real gameplay path.

use bevy::input::mouse::AccumulatedMouseMotion;
use bevy::prelude::*;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Action {
    Jump,
    Sprint,
    Interact,
    Drop,
    TogglePov,
    QuickSave,
    QuickLoad,
    Pause,
}

/// Who currently owns player input. Only `Gameplay` lets movement/look reach the world.
#[derive(Resource, Clone, Copy, Debug, PartialEq, Eq, Default)]
pub enum ControlOwner {
    #[default]
    Gameplay,
    Menu,
}

#[derive(Resource, Default, Debug, Clone)]
pub struct ActionState {
    /// x = strafe right, y = forward, each -1..1.
    pub move_axis: Vec2,
    /// Look delta this frame in radians (yaw, pitch).
    pub look_delta: Vec2,
    pressed: Vec<Action>,
    just_pressed: Vec<Action>,
    pub using_gamepad: bool,
}

impl ActionState {
    pub fn pressed(&self, a: Action) -> bool {
        self.pressed.contains(&a)
    }
    pub fn just_pressed(&self, a: Action) -> bool {
        self.just_pressed.contains(&a)
    }
}

/// Scripted input used by the autotest; merged after device input.
#[derive(Resource, Default, Debug, Clone)]
pub struct InjectedInput {
    pub move_axis: Vec2,
    pub look_delta: Vec2,
    pub hold: Vec<Action>,
    pub tap: Vec<Action>,
}

#[derive(Resource, Clone, Debug)]
pub struct InputSettings {
    pub mouse_sensitivity: f32,
    pub stick_look_speed: f32,
    pub stick_deadzone: f32,
}

impl Default for InputSettings {
    fn default() -> Self {
        Self { mouse_sensitivity: 0.0025, stick_look_speed: 2.6, stick_deadzone: 0.15 }
    }
}

pub struct InputPlugin;

/// Label so scripted input (autotest) can be ordered relative to action gathering.
#[derive(SystemSet, Debug, Clone, PartialEq, Eq, Hash)]
pub struct GatherActions;

pub fn gather_actions_label() -> GatherActions {
    GatherActions
}

impl Plugin for InputPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<ActionState>()
            .init_resource::<InjectedInput>()
            .init_resource::<InputSettings>()
            .init_resource::<ControlOwner>()
            .add_systems(PreUpdate, gather_actions.in_set(GatherActions).after(bevy::input::InputSystems));
    }
}

fn key_binding(a: Action) -> &'static [KeyCode] {
    match a {
        Action::Jump => &[KeyCode::Space],
        Action::Sprint => &[KeyCode::ShiftLeft],
        Action::Interact => &[KeyCode::KeyE],
        Action::Drop => &[KeyCode::KeyG],
        Action::TogglePov => &[KeyCode::KeyV],
        Action::QuickSave => &[KeyCode::F5],
        Action::QuickLoad => &[KeyCode::F9],
        Action::Pause => &[KeyCode::Escape],
    }
}

fn pad_binding(a: Action) -> &'static [GamepadButton] {
    match a {
        Action::Jump => &[GamepadButton::South],
        Action::Sprint => &[GamepadButton::LeftThumb],
        Action::Interact => &[GamepadButton::West],
        Action::Drop => &[GamepadButton::East],
        Action::TogglePov => &[GamepadButton::RightThumb],
        Action::QuickSave => &[GamepadButton::Select],
        Action::QuickLoad => &[],
        Action::Pause => &[GamepadButton::Start],
    }
}

const ALL: [Action; 8] = [
    Action::Jump,
    Action::Sprint,
    Action::Interact,
    Action::Drop,
    Action::TogglePov,
    Action::QuickSave,
    Action::QuickLoad,
    Action::Pause,
];

fn deadzone(v: Vec2, dz: f32) -> Vec2 {
    let len = v.length();
    if len < dz { Vec2::ZERO } else { v * ((len - dz) / (1.0 - dz)).min(1.0) / len }
}

fn gather_actions(
    keys: Res<ButtonInput<KeyCode>>,
    mouse_motion: Res<AccumulatedMouseMotion>,
    gamepads: Query<&Gamepad>,
    settings: Res<InputSettings>,
    owner: Res<ControlOwner>,
    time: Res<Time>,
    mut injected: ResMut<InjectedInput>,
    mut state: ResMut<ActionState>,
) {
    let prev = std::mem::take(&mut state.pressed);
    let mut move_axis = Vec2::ZERO;
    let mut look = Vec2::ZERO;
    let mut pressed: Vec<Action> = Vec::new();
    let mut using_pad = state.using_gamepad;

    // keyboard + mouse
    if keys.pressed(KeyCode::KeyW) { move_axis.y += 1.0; }
    if keys.pressed(KeyCode::KeyS) { move_axis.y -= 1.0; }
    if keys.pressed(KeyCode::KeyD) { move_axis.x += 1.0; }
    if keys.pressed(KeyCode::KeyA) { move_axis.x -= 1.0; }
    look += -mouse_motion.delta * settings.mouse_sensitivity;
    for a in ALL {
        if key_binding(a).iter().any(|k| keys.pressed(*k)) {
            pressed.push(a);
        }
    }
    if move_axis != Vec2::ZERO || mouse_motion.delta != Vec2::ZERO || keys.get_pressed().next().is_some() {
        using_pad = false;
    }

    // Xbox controller(s)
    for pad in &gamepads {
        let ls = deadzone(pad.left_stick(), settings.stick_deadzone);
        let rs = deadzone(pad.right_stick(), settings.stick_deadzone);
        if ls != Vec2::ZERO || rs != Vec2::ZERO {
            using_pad = true;
        }
        move_axis += ls;
        look += Vec2::new(-rs.x, rs.y) * settings.stick_look_speed * time.delta_secs();
        for a in ALL {
            if pad_binding(a).iter().any(|b| pad.pressed(*b)) {
                pressed.push(a);
                using_pad = true;
            }
        }
    }

    // scripted input (autotest)
    move_axis += injected.move_axis;
    look += injected.look_delta;
    pressed.extend(injected.hold.iter().copied());
    let taps: Vec<Action> = injected.tap.drain(..).collect();

    if move_axis.length() > 1.0 {
        move_axis = move_axis.normalize();
    }
    pressed.sort_by_key(|a| *a as u8);
    pressed.dedup();
    let mut just: Vec<Action> = pressed.iter().copied().filter(|a| !prev.contains(a)).collect();
    just.extend(taps.iter().copied());

    // control ownership: menus swallow movement/look; system actions still pass
    if *owner != ControlOwner::Gameplay {
        move_axis = Vec2::ZERO;
        look = Vec2::ZERO;
        pressed.retain(|a| matches!(a, Action::Pause | Action::QuickSave | Action::QuickLoad));
        just.retain(|a| matches!(a, Action::Pause | Action::QuickSave | Action::QuickLoad));
    }

    state.move_axis = move_axis;
    state.look_delta = look;
    state.pressed = pressed;
    state.just_pressed = just;
    state.using_gamepad = using_pad;
}
