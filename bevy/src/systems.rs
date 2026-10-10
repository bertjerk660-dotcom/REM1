//! Interaction, inventory, save/load and HUD for the vertical slice.

use crate::gameplay::{spawn_item, Item, MainCamera, Player, PlayerState, SceneAssets};
use crate::input::{Action, ActionState};
use crate::physics::{self, Body, Physics};
use bevy::prelude::*;
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

pub const INTERACT_RANGE: f32 = 3.0;
pub const SAVE_VERSION: u32 = 1;

#[derive(Resource, Default, Debug, Clone, Serialize, Deserialize)]
pub struct Inventory {
    pub items: Vec<InvItem>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct InvItem {
    pub id: String,
    pub name: String,
}

#[derive(Resource, Clone)]
pub struct SavePath(pub PathBuf);

#[derive(Resource, Default)]
pub struct Hud {
    pub prompt: String,
    pub message: String,
    pub message_timer: f32,
    pub looking_at: Option<Entity>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct SaveGame {
    pub version: u32,
    pub player_pos: [f32; 3],
    pub yaw: f32,
    pub pitch: f32,
    pub inventory: Vec<InvItem>,
    pub world_items: Vec<SavedItem>,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct SavedItem {
    pub id: String,
    pub name: String,
    pub pos: [f32; 3],
    pub rot: [f32; 4],
}

#[derive(Component)]
pub struct HudText;

pub struct SystemsPlugin;

impl Plugin for SystemsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<Inventory>()
            .init_resource::<Hud>()
            .add_systems(Startup, spawn_hud)
            .add_systems(Update, (look_target, interact, drop_item, save_load, update_hud).chain());
    }
}

fn spawn_hud(mut commands: Commands) {
    commands.spawn((
        Text::new(""),
        TextFont { font_size: FontSize::Px(18.0), ..default() },
        TextColor(Color::srgb(1.0, 0.85, 0.45)),
        Node { position_type: PositionType::Absolute, left: Val::Px(14.0), top: Val::Px(12.0), padding: UiRect::all(Val::Px(8.0)), ..default() },
        // Dark backing panel: yellow text was unreadable against the sand floor (playtest of run1).
        BackgroundColor(Color::srgba(0.05, 0.05, 0.07, 0.62)),
        HudText,
    ));
    // Centre crosshair: the interaction ray is cast through the screen centre.
    commands.spawn((
        Node {
            position_type: PositionType::Absolute,
            left: Val::Percent(50.0),
            top: Val::Percent(50.0),
            width: Val::Px(6.0),
            height: Val::Px(6.0),
            margin: UiRect { left: Val::Px(-3.0), top: Val::Px(-3.0), ..default() },
            ..default()
        },
        BackgroundColor(Color::srgba(1.0, 1.0, 1.0, 0.85)),
    ));
}

fn camera_ray(cam: &Transform) -> (Vec3, Vec3) {
    (cam.translation, cam.rotation * Vec3::NEG_Z)
}

fn look_target(
    phys: Res<Physics>,
    cams: Query<&Transform, With<MainCamera>>,
    players: Query<(&Transform, &Body), With<Player>>,
    items: Query<&Item>,
    mut hud: ResMut<Hud>,
) {
    hud.looking_at = None;
    hud.prompt.clear();
    let (Ok(cam), Ok((ptf, pbody))) = (cams.single(), players.single()) else { return };
    let (o, d) = camera_ray(cam);
    // reach is measured from the player, so third-person camera distance does not extend it
    let extra = (cam.translation - ptf.translation).length();
    if let Some((e, _t, p)) = physics::raycast(&phys, o, d, INTERACT_RANGE + extra, Some(pbody.handle)) {
        if p.distance(ptf.translation) <= INTERACT_RANGE + 0.6 {
            if let Ok(item) = items.get(e) {
                hud.looking_at = Some(e);
                hud.prompt = format!("[E / X] Take {}", item.name);
            }
        }
    }
}

pub fn pick_up(commands: &mut Commands, phys: &mut Physics, inv: &mut Inventory, e: Entity, item: &Item, body: &Body) {
    let w = &mut phys.world;
    w.remove_body_with_colliders(body.handle, true);
    commands.entity(e).despawn();
    inv.items.push(InvItem { id: item.id.clone(), name: item.name.clone() });
}

fn interact(
    mut commands: Commands,
    actions: Res<ActionState>,
    mut phys: ResMut<Physics>,
    mut inv: ResMut<Inventory>,
    mut hud: ResMut<Hud>,
    items: Query<(&Item, &Body)>,
) {
    if !actions.just_pressed(Action::Interact) {
        return;
    }
    let Some(e) = hud.looking_at else { return };
    if let Ok((item, body)) = items.get(e) {
        let name = item.name.clone();
        pick_up(&mut commands, &mut phys, &mut inv, e, item, body);
        hud.message = format!("{name} added");
        hud.message_timer = 2.5;
    }
}

fn drop_item(
    mut commands: Commands,
    actions: Res<ActionState>,
    mut phys: ResMut<Physics>,
    mut inv: ResMut<Inventory>,
    mut hud: ResMut<Hud>,
    assets: Res<SceneAssets>,
    players: Query<(&Transform, &PlayerState), With<Player>>,
) {
    if !actions.just_pressed(Action::Drop) {
        return;
    }
    let Ok((ptf, st)) = players.single() else { return };
    let Some(it) = inv.items.pop() else {
        hud.message = "Nothing to drop".into();
        hud.message_timer = 1.5;
        return;
    };
    let fwd = Vec3::new(-st.yaw.sin(), 0.0, -st.yaw.cos());
    let pos = ptf.translation + fwd * 1.1 + Vec3::Y * 0.6;
    spawn_item(&mut commands, &mut phys, &assets.crate_mesh, &assets.crate_mat, &it.id, &it.name, pos, Quat::IDENTITY);
    hud.message = format!("{} dropped", it.name);
    hud.message_timer = 2.0;
}

pub fn build_save(players: &Query<(&Transform, &PlayerState), With<Player>>, items: &Query<(&Item, &Transform)>, inv: &Inventory) -> Option<SaveGame> {
    let (ptf, st) = players.single().ok()?;
    let mut world_items: Vec<SavedItem> = items
        .iter()
        .map(|(i, t)| SavedItem { id: i.id.clone(), name: i.name.clone(), pos: t.translation.to_array(), rot: t.rotation.to_array() })
        .collect();
    world_items.sort_by(|a, b| a.id.cmp(&b.id));
    Some(SaveGame { version: SAVE_VERSION, player_pos: ptf.translation.to_array(), yaw: st.yaw, pitch: st.pitch, inventory: inv.items.clone(), world_items })
}

fn save_load(
    mut commands: Commands,
    actions: Res<ActionState>,
    path: Res<SavePath>,
    mut phys: ResMut<Physics>,
    mut inv: ResMut<Inventory>,
    mut hud: ResMut<Hud>,
    assets: Res<SceneAssets>,
    mut players: Query<(&Transform, &mut PlayerState), With<Player>>,
    items: Query<(Entity, &Item, &Transform, &Body)>,
) {
    if actions.just_pressed(Action::QuickSave) {
        let Ok((ptf, st)) = players.single() else { return };
        let mut world_items: Vec<SavedItem> = items
            .iter()
            .map(|(_, i, t, _)| SavedItem { id: i.id.clone(), name: i.name.clone(), pos: t.translation.to_array(), rot: t.rotation.to_array() })
            .collect();
        world_items.sort_by(|a, b| a.id.cmp(&b.id));
        let save = SaveGame { version: SAVE_VERSION, player_pos: ptf.translation.to_array(), yaw: st.yaw, pitch: st.pitch, inventory: inv.items.clone(), world_items };
        if let Some(dir) = path.0.parent() {
            let _ = std::fs::create_dir_all(dir);
        }
        match serde_json::to_string_pretty(&save).map(|s| std::fs::write(&path.0, s)) {
            Ok(Ok(())) => {
                hud.message = "Quicksaved".into();
                info!("[SAVE] wrote {}", path.0.display());
            }
            e => {
                hud.message = "Quicksave FAILED".into();
                error!("[SAVE] failed: {e:?}");
            }
        }
        hud.message_timer = 2.0;
    }
    if actions.just_pressed(Action::QuickLoad) {
        let save: SaveGame = match std::fs::read_to_string(&path.0).ok().and_then(|s| serde_json::from_str(&s).ok()) {
            Some(s) => s,
            None => {
                hud.message = "No quicksave".into();
                hud.message_timer = 2.0;
                return;
            }
        };
        if save.version != SAVE_VERSION {
            hud.message = format!("Save version {} not supported", save.version);
            hud.message_timer = 3.0;
            return;
        }
        for (e, _, _, b) in &items {
            phys.world.remove_body_with_colliders(b.handle, true);
            commands.entity(e).despawn();
        }
        for it in &save.world_items {
            spawn_item(&mut commands, &mut phys, &assets.crate_mesh, &assets.crate_mat, &it.id, &it.name, Vec3::from_array(it.pos), Quat::from_array(it.rot));
        }
        inv.items = save.inventory.clone();
        if let Ok((_, mut st)) = players.single_mut() {
            st.teleport = Some(Vec3::from_array(save.player_pos));
            st.yaw = save.yaw;
            st.pitch = save.pitch;
        }
        hud.message = "Quickloaded".into();
        hud.message_timer = 2.0;
        info!("[SAVE] loaded {}", path.0.display());
    }
}

fn update_hud(time: Res<Time>, actions: Res<ActionState>, inv: Res<Inventory>, mut hud: ResMut<Hud>, players: Query<&PlayerState, With<Player>>, mut text: Query<&mut Text, With<HudText>>) {
    hud.message_timer = (hud.message_timer - time.delta_secs()).max(0.0);
    let Ok(mut t) = text.single_mut() else { return };
    let st = players.single().ok();
    let device = if actions.using_gamepad { "Xbox controller" } else { "Keyboard/mouse" };
    let pov = st.map(|s| if s.first_person { "1st person" } else { "3rd person" }).unwrap_or("-");
    let ground = st.map(|s| if s.grounded { "grounded" } else { "airborne" }).unwrap_or("-");
    let mut s = format!(
        "REM1 Bevy vertical slice  |  {device}  |  {pov}  |  {ground}\nInventory: {} item(s){}\nWASD/LS move  Mouse/RS look  Space/A jump  E/X take  G/B drop  V/RS-click view  F5 save  F9 load\n",
        inv.items.len(),
        if inv.items.is_empty() { String::new() } else { format!(" ({})", inv.items.iter().map(|i| i.name.as_str()).collect::<Vec<_>>().join(", ")) },
    );
    if !hud.prompt.is_empty() {
        s.push_str(&format!("\n{}", hud.prompt));
    }
    if hud.message_timer > 0.0 {
        s.push_str(&format!("\n{}", hud.message));
    }
    **t = s;
}
