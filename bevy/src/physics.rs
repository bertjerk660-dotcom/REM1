//! Physics: rapier3d 0.36 owned directly by REM1 (decision D-B001).
//!
//! No Bevy physics plugin supports Bevy 0.20 yet, so this module is the integration
//! layer: one `PhysicsWorld` resource stepped on a fixed 60 Hz timestep, dynamic bodies
//! synced back to Bevy transforms, and every collider tagged with its Bevy entity
//! (`user_data`) so raycasts (interaction, later the Physics Gun) resolve to entities.
//! Units: 1 unit = 1 metre, Y up (Bevy convention). Legacy FNV/Source units are
//! converted by the content importers, never here.

use bevy::prelude::*;
use rapier3d::control::KinematicCharacterController;
use rapier3d::prelude::{
    ColliderBuilder, ColliderHandle, PhysicsWorld, QueryFilter, Ray, RigidBodyBuilder, RigidBodyHandle,
};

pub const FIXED_HZ: f64 = 60.0;

#[inline]
pub fn to_r(v: Vec3) -> rapier3d::math::Vector {
    rapier3d::math::Vector::new(v.x, v.y, v.z)
}
#[inline]
pub fn from_r(v: rapier3d::math::Vector) -> Vec3 {
    Vec3::new(v.x, v.y, v.z)
}
#[inline]
pub fn from_rq(q: rapier3d::math::Rotation) -> Quat {
    let a: [f32; 4] = [q.x, q.y, q.z, q.w];
    Quat::from_array(a)
}
#[inline]
pub fn to_rq(q: Quat) -> rapier3d::math::Rotation {
    rapier3d::math::Rotation::from_xyzw(q.x, q.y, q.z, q.w)
}

#[derive(Resource)]
pub struct Physics {
    pub world: PhysicsWorld,
    pub controller: KinematicCharacterController,
    pub steps: u64,
}

impl Default for Physics {
    fn default() -> Self {
        let mut world = PhysicsWorld::default();
        world.integration_parameters.dt = (1.0 / FIXED_HZ) as f32;
        let mut controller = KinematicCharacterController::default();
        controller.offset = rapier3d::control::CharacterLength::Absolute(0.02);
        controller.max_slope_climb_angle = 50f32.to_radians();
        controller.min_slope_slide_angle = 35f32.to_radians();
        controller.autostep = Some(rapier3d::control::CharacterAutostep {
            max_height: rapier3d::control::CharacterLength::Absolute(0.35),
            min_width: rapier3d::control::CharacterLength::Absolute(0.2),
            include_dynamic_bodies: false,
        });
        controller.snap_to_ground = Some(rapier3d::control::CharacterLength::Absolute(0.3));
        Self { world, controller, steps: 0 }
    }
}

/// A rapier body mirrored onto this entity's Transform each fixed step.
#[derive(Component, Clone, Copy, Debug)]
pub struct Body {
    pub handle: RigidBodyHandle,
    pub collider: ColliderHandle,
}

pub struct PhysicsPlugin;

impl Plugin for PhysicsPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<Physics>()
            .insert_resource(Time::<Fixed>::from_hz(FIXED_HZ))
            .add_systems(FixedUpdate, (step_world, sync_dynamic_bodies).chain().in_set(PhysicsStep));
    }
}

/// Systems that must run before (player move) or after (sync) the physics step use this set.
#[derive(SystemSet, Debug, Clone, PartialEq, Eq, Hash)]
pub struct PhysicsStep;

fn step_world(mut phys: ResMut<Physics>) {
    phys.world.step();
    phys.steps += 1;
}

fn sync_dynamic_bodies(phys: Res<Physics>, mut q: Query<(&Body, &mut Transform)>) {
    for (b, mut t) in &mut q {
        if let Some(rb) = phys.world.bodies.get(b.handle) {
            if rb.is_dynamic() || rb.is_kinematic() {
                t.translation = from_r(rb.translation());
                t.rotation = from_rq(*rb.rotation());
            }
        }
    }
}

fn tag(c: ColliderBuilder, e: Entity) -> ColliderBuilder {
    c.user_data(e.to_bits() as u128)
}

/// Fixed box collider (static world geometry). `half` = half extents.
pub fn add_static_box(phys: &mut Physics, e: Entity, center: Vec3, half: Vec3, rot: Quat) -> Body {
    let rb = RigidBodyBuilder::fixed().translation(to_r(center)).rotation(to_rq(rot).to_scaled_axis());
    let (handle, collider) = phys.world.insert(rb, tag(ColliderBuilder::cuboid(half.x, half.y, half.z).friction(0.8), e));
    Body { handle, collider }
}

/// Dynamic box (crates, props).
pub fn add_dynamic_box(phys: &mut Physics, e: Entity, center: Vec3, half: Vec3, density: f32) -> Body {
    let rb = RigidBodyBuilder::dynamic().translation(to_r(center)).ccd_enabled(true);
    let (handle, collider) = phys
        .world
        .insert(rb, tag(ColliderBuilder::cuboid(half.x, half.y, half.z).density(density).friction(0.7), e));
    Body { handle, collider }
}

/// Kinematic capsule for the player (pushes dynamic props, moved by the character controller).
pub fn add_player_capsule(phys: &mut Physics, e: Entity, center: Vec3, half_height: f32, radius: f32) -> Body {
    let rb = RigidBodyBuilder::kinematic_position_based().translation(to_r(center));
    let (handle, collider) = phys.world.insert(rb, tag(ColliderBuilder::capsule_y(half_height, radius), e));
    Body { handle, collider }
}

pub fn entity_of(phys: &Physics, c: ColliderHandle) -> Option<Entity> {
    phys.world.colliders.get(c).and_then(|col| Entity::try_from_bits(col.user_data as u64))
}

/// Ray cast against everything except `exclude`. Returns (entity, distance, point).
pub fn raycast(phys: &Physics, origin: Vec3, dir: Vec3, max: f32, exclude: Option<RigidBodyHandle>) -> Option<(Entity, f32, Vec3)> {
    let w = &phys.world;
    let mut filter = QueryFilter::default();
    if let Some(h) = exclude {
        filter = filter.exclude_rigid_body(h);
    }
    let qp = w.broad_phase.as_query_pipeline(w.narrow_phase.query_dispatcher(), &w.bodies, &w.colliders, filter);
    let ray = Ray::new(to_r(origin), to_r(dir.normalize_or_zero()));
    qp.cast_ray(&ray, max, true)
        .and_then(|(c, toi)| entity_of(phys, c).map(|e| (e, toi, origin + dir.normalize_or_zero() * toi)))
}
