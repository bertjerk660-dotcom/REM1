//! Vertical-slice gameplay: authored test scene, player character controller, camera.
//! All geometry here is authored primitives (no third-party assets), so it can be
//! committed and redistributed. Real Fallout regions arrive via the Phase C importer.

use crate::input::{Action, ActionState};
use crate::physics::{self, Body, Physics, PhysicsStep};
use bevy::prelude::*;

pub const PLAYER_RADIUS: f32 = 0.35;
pub const PLAYER_HALF_HEIGHT: f32 = 0.55; // capsule total height = 2*(0.55+0.35) = 1.8 m
pub const EYE_HEIGHT: f32 = 0.7; // above capsule centre
pub const WALK_SPEED: f32 = 4.2;
pub const SPRINT_SPEED: f32 = 7.0;
pub const JUMP_SPEED: f32 = 5.2;
pub const GRAVITY: f32 = 9.81;
pub const SPAWN: Vec3 = Vec3::new(0.0, 1.0, 6.0);

#[derive(Component)]
pub struct Player;

#[derive(Component, Debug, Clone)]
pub struct PlayerState {
    pub velocity: Vec3,
    pub grounded: bool,
    pub yaw: f32,
    pub pitch: f32,
    pub first_person: bool,
    /// Set by save/load or the autotest; applied at the next fixed step.
    pub teleport: Option<Vec3>,
}

#[derive(Component)]
pub struct MainCamera;

#[derive(Component, Debug, Clone)]
pub struct Item {
    pub id: String,
    pub name: String,
    pub half: Vec3,
}

#[derive(Resource, Clone)]
pub struct SceneAssets {
    pub crate_mesh: Handle<Mesh>,
    pub crate_mat: Handle<StandardMaterial>,
}

pub struct GameplayPlugin;

impl Plugin for GameplayPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, (spawn_scene, spawn_player).chain())
            .add_systems(FixedUpdate, move_player.before(PhysicsStep))
            .add_systems(Update, (update_look, toggle_pov, place_camera).chain());
    }
}

fn mat(materials: &mut Assets<StandardMaterial>, r: f32, g: f32, b: f32, rough: f32) -> Handle<StandardMaterial> {
    materials.add(StandardMaterial { base_color: Color::srgb(r, g, b), perceptual_roughness: rough, ..default() })
}

fn spawn_scene(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut phys: ResMut<Physics>,
) {
    commands.insert_resource(ClearColor(Color::srgb(0.62, 0.72, 0.82)));
    commands.insert_resource(GlobalAmbientLight { color: Color::srgb(1.0, 0.95, 0.85), brightness: 350.0, ..default() });
    commands.spawn((
        DirectionalLight { illuminance: 12_000.0, shadow_maps_enabled: true, ..default() },
        Transform::from_xyz(20.0, 40.0, 15.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));

    let sand = mat(&mut materials, 0.78, 0.66, 0.48, 0.95);
    let concrete = mat(&mut materials, 0.55, 0.55, 0.52, 0.9);
    let rust = mat(&mut materials, 0.45, 0.27, 0.16, 0.8);
    let wood = mat(&mut materials, 0.52, 0.36, 0.2, 0.85);

    // (center, half extents, rotation, material)
    let statics: Vec<(Vec3, Vec3, Quat, Handle<StandardMaterial>)> = vec![
        (Vec3::new(0.0, -0.5, 0.0), Vec3::new(40.0, 0.5, 40.0), Quat::IDENTITY, sand.clone()),
        // perimeter walls
        (Vec3::new(0.0, 1.5, -40.0), Vec3::new(40.0, 1.5, 0.5), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(0.0, 1.5, 40.0), Vec3::new(40.0, 1.5, 0.5), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(-40.0, 1.5, 0.0), Vec3::new(0.5, 1.5, 40.0), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(40.0, 1.5, 0.0), Vec3::new(0.5, 1.5, 40.0), Quat::IDENTITY, concrete.clone()),
        // test wall for collision checks (player must stop before x = -6.5)
        (Vec3::new(-7.0, 1.5, 6.0), Vec3::new(0.5, 1.5, 4.0), Quat::IDENTITY, concrete.clone()),
        // ramp (skate/traversal), stairs, a ledge and a rail-like bar for later skating work
        (Vec3::new(8.0, 0.6, -4.0), Vec3::new(2.0, 0.15, 4.0), Quat::from_rotation_x(-0.28), concrete.clone()),
        (Vec3::new(8.0, 1.2, -9.5), Vec3::new(2.0, 1.2, 2.0), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(-6.0, 0.25, -6.0), Vec3::new(1.5, 0.25, 0.5), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(-6.0, 0.5, -7.0), Vec3::new(1.5, 0.5, 0.5), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(-6.0, 0.75, -8.0), Vec3::new(1.5, 0.75, 0.5), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(0.0, 0.3, -12.0), Vec3::new(6.0, 0.3, 0.6), Quat::IDENTITY, concrete.clone()),
        (Vec3::new(0.0, 0.55, -16.0), Vec3::new(5.0, 0.04, 0.04), Quat::IDENTITY, rust.clone()),
        // shack
        (Vec3::new(14.0, 1.5, 10.0), Vec3::new(3.0, 1.5, 0.2), Quat::IDENTITY, rust.clone()),
        (Vec3::new(17.0, 1.5, 12.5), Vec3::new(0.2, 1.5, 2.5), Quat::IDENTITY, rust.clone()),
        (Vec3::new(11.0, 1.5, 12.5), Vec3::new(0.2, 1.5, 2.5), Quat::IDENTITY, rust.clone()),
    ];
    for (c, h, r, m) in statics {
        let e = commands
            .spawn((Mesh3d(meshes.add(Cuboid::new(h.x * 2.0, h.y * 2.0, h.z * 2.0))), MeshMaterial3d(m), Transform::from_translation(c).with_rotation(r)))
            .id();
        let b = physics::add_static_box(&mut phys, e, c, h, r);
        commands.entity(e).insert(b);
    }

    let crate_mesh = meshes.add(Cuboid::new(0.6, 0.6, 0.6));
    commands.insert_resource(SceneAssets { crate_mesh: crate_mesh.clone(), crate_mat: wood.clone() });
    for (i, p) in [Vec3::new(2.0, 0.4, 2.0), Vec3::new(3.0, 0.4, 2.5), Vec3::new(2.5, 1.1, 2.2), Vec3::new(-3.0, 0.4, 0.0)].iter().enumerate() {
        spawn_item(&mut commands, &mut phys, &crate_mesh, &wood, &format!("crate_{i}"), "Supply crate", *p, Quat::IDENTITY);
    }
}

pub fn spawn_item(
    commands: &mut Commands,
    phys: &mut Physics,
    mesh: &Handle<Mesh>,
    material: &Handle<StandardMaterial>,
    id: &str,
    name: &str,
    pos: Vec3,
    rot: Quat,
) -> Entity {
    let half = Vec3::splat(0.3);
    let e = commands
        .spawn((
            Mesh3d(mesh.clone()),
            MeshMaterial3d(material.clone()),
            Transform::from_translation(pos).with_rotation(rot),
            Item { id: id.to_string(), name: name.to_string(), half },
        ))
        .id();
    let b = physics::add_dynamic_box(phys, e, pos, half, 300.0);
    if let Some(rb) = phys.world.bodies.get_mut(b.handle) {
        rb.set_rotation(physics::to_rq(rot), true);
    }
    commands.entity(e).insert(b);
    e
}

fn spawn_player(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
    mut phys: ResMut<Physics>,
) {
    let e = commands
        .spawn((
            Player,
            PlayerState { velocity: Vec3::ZERO, grounded: false, yaw: 0.0, pitch: -0.15, first_person: false, teleport: None },
            Transform::from_translation(SPAWN),
            Visibility::default(),
        ))
        .with_children(|p| {
            p.spawn((
                Mesh3d(meshes.add(Capsule3d::new(PLAYER_RADIUS, PLAYER_HALF_HEIGHT * 2.0))),
                MeshMaterial3d(materials.add(StandardMaterial { base_color: Color::srgb(0.25, 0.35, 0.55), ..default() })),
                Transform::default(),
                PlayerBodyMesh,
            ));
        })
        .id();
    let b = physics::add_player_capsule(&mut phys, e, SPAWN, PLAYER_HALF_HEIGHT, PLAYER_RADIUS);
    commands.entity(e).insert(b);
    commands.spawn((Camera3d::default(), Transform::from_translation(SPAWN + Vec3::new(0.0, 2.0, 4.0)), MainCamera));
}

#[derive(Component)]
pub struct PlayerBodyMesh;

/// Fixed-step character movement through rapier's kinematic character controller.
fn move_player(actions: Res<ActionState>, time: Res<Time>, mut phys: ResMut<Physics>, mut q: Query<(&Body, &mut PlayerState, &mut Transform), With<Player>>) {
    let dt = time.delta_secs();
    let Ok((body, mut st, mut tf)) = q.single_mut() else { return };

    if let Some(p) = st.teleport.take() {
        if let Some(rb) = phys.world.bodies.get_mut(body.handle) {
            rb.set_translation(physics::to_r(p), true);
            rb.set_next_kinematic_translation(physics::to_r(p));
        }
        st.velocity = Vec3::ZERO;
        tf.translation = p;
        return;
    }

    let speed = if actions.pressed(Action::Sprint) { SPRINT_SPEED } else { WALK_SPEED };
    let fwd = Vec3::new(-st.yaw.sin(), 0.0, -st.yaw.cos());
    let right = Vec3::new(fwd.z * -1.0, 0.0, fwd.x);
    let wish = (fwd * actions.move_axis.y + right * actions.move_axis.x) * speed;
    st.velocity.x = wish.x;
    st.velocity.z = wish.z;
    if st.grounded {
        st.velocity.y = -0.5;
        if actions.pressed(Action::Jump) {
            st.velocity.y = JUMP_SPEED;
            st.grounded = false;
        }
    } else {
        st.velocity.y -= GRAVITY * dt;
    }

    let Some(rb) = phys.world.bodies.get(body.handle) else { return };
    let pos = rb.translation();
    let shape = rapier3d::prelude::Capsule::new_y(PLAYER_HALF_HEIGHT, PLAYER_RADIUS);
    let pose = rapier3d::math::Pose::from_translation(pos);
    let desired = physics::to_r(st.velocity * dt);
    let w = &phys.world;
    let filter = rapier3d::prelude::QueryFilter::exclude_dynamic().exclude_rigid_body(body.handle);
    let qp = w.broad_phase.as_query_pipeline(w.narrow_phase.query_dispatcher(), &w.bodies, &w.colliders, filter);
    let mv = phys.controller.move_shape(dt, &qp, &shape, &pose, desired, |_| {});
    let grounded = mv.grounded;
    let new_pos = pos + mv.translation;
    if let Some(rb) = phys.world.bodies.get_mut(body.handle) {
        rb.set_next_kinematic_translation(new_pos);
    }
    if grounded && st.velocity.y < 0.0 {
        st.velocity.y = 0.0;
    }
    if mv.translation.y.abs() < 1e-5 && st.velocity.y > 0.0 && !grounded {
        st.velocity.y = 0.0; // bumped head
    }
    st.grounded = grounded;
    tf.translation = physics::from_r(new_pos);
}

fn update_look(actions: Res<ActionState>, mut q: Query<&mut PlayerState, With<Player>>) {
    let Ok(mut st) = q.single_mut() else { return };
    st.yaw += actions.look_delta.x;
    st.pitch = (st.pitch + actions.look_delta.y).clamp(-1.35, 1.2);
}

fn toggle_pov(actions: Res<ActionState>, mut q: Query<&mut PlayerState, With<Player>>, mut vis: Query<&mut Visibility, With<PlayerBodyMesh>>) {
    let Ok(mut st) = q.single_mut() else { return };
    if actions.just_pressed(Action::TogglePov) {
        st.first_person = !st.first_person;
    }
    for mut v in &mut vis {
        *v = if st.first_person { Visibility::Hidden } else { Visibility::Inherited };
    }
}

/// Third-person boom with collision (ray cast back from the head) or first-person eye.
fn place_camera(phys: Res<Physics>, players: Query<(&Transform, &PlayerState, &Body), (With<Player>, Without<MainCamera>)>, mut cams: Query<&mut Transform, With<MainCamera>>) {
    let (Ok((ptf, st, body)), Ok(mut ctf)) = (players.single(), cams.single_mut()) else { return };
    let head = ptf.translation + Vec3::Y * EYE_HEIGHT;
    let rot = Quat::from_euler(EulerRot::YXZ, st.yaw, st.pitch, 0.0);
    if st.first_person {
        ctf.translation = head;
        ctf.rotation = rot;
        return;
    }
    // Over-the-shoulder boom: the player sits left of and below the screen centre so the
    // crosshair line (and interaction ray) is never blocked by the player's own body.
    let back = rot * Vec3::new(0.85, 0.55, 4.2);
    let dist = back.length();
    let dir = back / dist;
    let d = physics::raycast(&phys, head, dir, dist, Some(body.handle)).map(|(_, t, _)| (t - 0.2).max(0.3)).unwrap_or(dist);
    ctf.translation = head + dir * d;
    ctf.rotation = rot;
}
