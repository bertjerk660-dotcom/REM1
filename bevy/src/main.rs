//! REM1 Bevy â€” standalone Fallout x Garry's Mod x THUG2 crossover (primary track, D-012).
//!
//! Vertical slice v0.1: window, authored collision scene, player + camera, shared
//! keyboard/Xbox input, interaction, inventory, save/load. `--autotest` runs a scripted
//! end-to-end gameplay check through the real input path and exits with 0 (pass) / 1.

mod gameplay;
mod input;
mod physics;
mod systems;

use bevy::prelude::*;
use bevy::render::view::screenshot::{save_to_disk, Screenshot};
use bevy::window::{CursorGrabMode, CursorOptions, PrimaryWindow, WindowResolution};
use gameplay::{Item, Player, PlayerState, PLAYER_HALF_HEIGHT, PLAYER_RADIUS};
use input::{Action, ActionState, InjectedInput};
use physics::Physics;
use serde::Serialize;
use std::path::PathBuf;
use systems::{Inventory, SavePath};

#[derive(Resource, Clone, Default)]
struct Cli {
    autotest: bool,
    out_dir: PathBuf,
}

fn parse_cli() -> Cli {
    let args: Vec<String> = std::env::args().collect();
    let mut cli = Cli { autotest: false, out_dir: PathBuf::from("rem1_output") };
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--autotest" => cli.autotest = true,
            "--out" if i + 1 < args.len() => {
                cli.out_dir = PathBuf::from(&args[i + 1]);
                i += 1;
            }
            _ => {}
        }
        i += 1;
    }
    cli
}

fn main() -> AppExit {
    let cli = parse_cli();
    let _ = std::fs::create_dir_all(&cli.out_dir);
    let mut app = App::new();
    app.add_plugins(DefaultPlugins.set(WindowPlugin {
        primary_window: Some(Window {
            title: format!("REM1 Bevy v{} - vertical slice", env!("CARGO_PKG_VERSION")),
            resolution: WindowResolution::new(1600, 900),
            ..default()
        }),
        ..default()
    }))
    .insert_resource(SavePath(cli.out_dir.join("saves").join("quicksave.json")))
    .insert_resource(cli.clone())
    .add_plugins((input::InputPlugin, physics::PhysicsPlugin, gameplay::GameplayPlugin, systems::SystemsPlugin))
    .add_systems(Update, cursor_control);
    if cli.autotest {
        app.init_resource::<AutoTest>().add_systems(PreUpdate, autotest.before(input::gather_actions_label()).after(bevy::input::InputSystems));
    }
    app.run()
}

/// Lock the cursor for mouse-look while playing; Esc releases it, clicking re-locks.
fn cursor_control(cli: Res<Cli>, actions: Res<ActionState>, mouse: Res<ButtonInput<MouseButton>>, mut cursors: Query<&mut CursorOptions, With<PrimaryWindow>>) {
    if cli.autotest {
        return; // never grab the user's mouse during scripted tests
    }
    let Ok(mut c) = cursors.single_mut() else { return };
    if actions.just_pressed(Action::Pause) {
        c.grab_mode = CursorGrabMode::None;
        c.visible = true;
    } else if mouse.just_pressed(MouseButton::Left) && c.grab_mode == CursorGrabMode::None {
        c.grab_mode = CursorGrabMode::Locked;
        c.visible = false;
    }
}

// ------------------------------------------------------------------ autotest

#[derive(Serialize, Default, Clone)]
struct Check {
    name: String,
    pass: bool,
    detail: String,
}

#[derive(Resource, Default)]
struct AutoTest {
    step: usize,
    t: f32,
    total: f32,
    checks: Vec<Check>,
    mark: Vec3,
    max_y: f32,
    saved_pos: Vec3,
    saved_items: usize,
    items_before_drop: usize,
    screenshots: Vec<String>,
    done: bool,
}

impl AutoTest {
    fn check(&mut self, name: &str, pass: bool, detail: String) {
        info!("[AUTOTEST] {} {}: {}", if pass { "PASS" } else { "FAIL" }, name, detail);
        self.checks.push(Check { name: name.into(), pass, detail });
    }
    fn next(&mut self) {
        self.step += 1;
        self.t = 0.0;
    }
}

#[derive(Serialize)]
struct Report {
    rem1_version: String,
    bevy: String,
    rapier3d: String,
    all_pass: bool,
    checks: Vec<Check>,
    physics_steps: u64,
    gamepads_detected: usize,
    screenshots: Vec<String>,
    duration_s: f32,
}

fn shot(commands: &mut Commands, at: &mut AutoTest, cli: &Cli, name: &str) {
    let p = cli.out_dir.join(format!("{name}.png"));
    commands.spawn(Screenshot::primary_window()).observe(save_to_disk(p.clone()));
    at.screenshots.push(p.display().to_string());
}

#[allow(clippy::too_many_arguments)]
fn autotest(
    mut commands: Commands,
    time: Res<Time>,
    cli: Res<Cli>,
    phys: Res<Physics>,
    inv: Res<Inventory>,
    save: Res<SavePath>,
    gamepads: Query<&Gamepad>,
    mut at: ResMut<AutoTest>,
    mut inj: ResMut<InjectedInput>,
    mut players: Query<(&Transform, &mut PlayerState), With<Player>>,
    items: Query<(&Item, &Transform)>,
    mut exit: MessageWriter<AppExit>,
) {
    if at.done {
        return;
    }
    let dt = time.delta_secs();
    at.t += dt;
    at.total += dt;
    let Ok((ptf, mut st)) = players.single_mut() else { return };
    let pos = ptf.translation;
    let stand_y = PLAYER_HALF_HEIGHT + PLAYER_RADIUS; // capsule centre when standing on y=0
    inj.move_axis = Vec2::ZERO;
    inj.look_delta = Vec2::ZERO;
    inj.hold.clear();

    match at.step {
        0 => {
            if at.t > 2.0 {
                let ok = st.grounded && (pos.y - stand_y).abs() < 0.15;
                at.check("boot_and_ground", ok && phys.steps > 60, format!("grounded={} y={:.3} expected~{:.2} physics_steps={}", st.grounded, pos.y, stand_y, phys.steps));
                shot(&mut commands, &mut at, &cli, "01_boot");
                at.mark = pos;
                at.next();
            }
        }
        1 => {
            inj.move_axis = Vec2::new(0.0, 1.0);
            if at.t > 1.5 {
                let d = Vec2::new(pos.x - at.mark.x, pos.z - at.mark.z).length();
                at.check("walk_forward", d > 3.5, format!("moved {d:.2} m in 1.5 s (walk {:.1} m/s)", gameplay::WALK_SPEED));
                at.mark = pos;
                at.max_y = pos.y;
                at.next();
            }
        }
        2 => {
            if at.t < 0.15 {
                inj.hold.push(Action::Jump);
            }
            at.max_y = at.max_y.max(pos.y);
            if at.t > 1.6 {
                let rise = at.max_y - at.mark.y;
                at.check("jump_and_land", rise > 0.8 && st.grounded, format!("peak rise {rise:.2} m, landed={}", st.grounded));
                st.teleport = Some(Vec3::new(-4.0, stand_y + 0.05, 6.0));
                st.yaw = std::f32::consts::FRAC_PI_2; // face -X, toward the test wall at x=-7
                at.next();
            }
        }
        3 => {
            if at.t > 0.3 {
                inj.move_axis = Vec2::new(0.0, 1.0);
            }
            if at.t > 2.5 {
                let wall_face = -6.5;
                let ok = pos.x > wall_face + PLAYER_RADIUS - 0.08 && pos.x < -5.0;
                at.check("wall_collision", ok, format!("player x={:.3} (wall face x={wall_face}, radius {PLAYER_RADIUS})", pos.x));
                // stand in front of crate_3 at (-3, 0.3, 0), first person, looking at it
                st.teleport = Some(Vec3::new(-3.0, stand_y + 0.05, 1.8));
                st.yaw = 0.0;
                st.pitch = -0.62;
                st.first_person = true;
                at.next();
            }
        }
        4 => {
            if (0.6..0.6 + dt * 1.5).contains(&at.t) {
                shot(&mut commands, &mut at, &cli, "02_look_at_crate");
            }
            if at.t > 0.9 && at.t < 0.9 + dt * 1.5 {
                inj.tap.push(Action::Interact);
            }
            if at.t > 1.4 {
                let has = inv.items.iter().any(|i| i.id == "crate_3");
                let gone = !items.iter().any(|(i, _)| i.id == "crate_3");
                at.check("pickup", has && gone, format!("inventory={:?} crate_3 removed from world={gone}", inv.items.iter().map(|i| &i.id).collect::<Vec<_>>()));
                inj.tap.push(Action::QuickSave);
                at.saved_pos = pos;
                at.saved_items = items.iter().count();
                at.next();
            }
        }
        5 => {
            if at.t > 0.5 {
                let exists = save.0.exists();
                at.check("quicksave_written", exists, format!("{} exists={exists}", save.0.display()));
                st.teleport = Some(Vec3::new(5.0, stand_y + 0.05, 5.0));
                at.next();
            }
        }
        6 => {
            if at.t > 0.6 && at.t < 0.6 + dt * 1.5 {
                inj.tap.push(Action::QuickLoad);
            }
            if at.t > 1.5 {
                let d = pos.distance(at.saved_pos);
                let n = items.iter().count();
                let ok = d < 0.3 && inv.items.iter().any(|i| i.id == "crate_3") && n == at.saved_items;
                let saved_items = at.saved_items;
                at.check("quickload_restores", ok, format!("pos error {d:.3} m, inventory={}, world items {n} (saved {saved_items})", inv.items.len()));
                at.items_before_drop = n;
                st.first_person = false;
                st.pitch = -0.2;
                at.next();
            }
        }
        7 => {
            if at.t > 0.3 && at.t < 0.3 + dt * 1.5 {
                inj.tap.push(Action::Drop);
            }
            if at.t > 2.3 {
                let n = items.iter().count();
                let dropped = items.iter().find(|(i, _)| i.id == "crate_3").map(|(_, t)| t.translation);
                let rest_ok = dropped.map(|p| p.y < 0.7 && p.y > 0.1).unwrap_or(false);
                let expected = at.items_before_drop + 1;
                at.check("drop_and_physics", n == expected && inv.items.is_empty() && rest_ok, format!("world items {n}, dropped crate at {dropped:?}, inventory {}", inv.items.len()));
                shot(&mut commands, &mut at, &cli, "03_after_drop");
                at.next();
            }
        }
        8 => {
            if at.t > 1.0 {
                let all = at.checks.iter().all(|c| c.pass);
                let rep = Report {
                    rem1_version: env!("CARGO_PKG_VERSION").into(),
                    bevy: "0.20.0".into(),
                    rapier3d: "0.36.0".into(),
                    all_pass: all,
                    checks: at.checks.clone(),
                    physics_steps: phys.steps,
                    gamepads_detected: gamepads.iter().count(),
                    screenshots: at.screenshots.clone(),
                    duration_s: at.total,
                };
                let path = cli.out_dir.join("autotest_report.json");
                let _ = std::fs::write(&path, serde_json::to_string_pretty(&rep).unwrap_or_default());
                info!("[AUTOTEST] {} -> {}", if all { "ALL PASS" } else { "FAILURES" }, path.display());
                at.done = true;
                exit.write(if all { AppExit::Success } else { AppExit::from_code(1) });
            }
        }
        _ => {}
    }
}
