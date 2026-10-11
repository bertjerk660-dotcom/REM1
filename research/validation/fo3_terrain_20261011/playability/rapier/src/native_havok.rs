use rapier3d::prelude::*;
use rapier3d::math::{Vector,Pose};
use rapier3d::control::{KinematicCharacterController,CharacterLength,CharacterAutostep};
use super::tests::sample_mesh;
fn u32_at(b:&[u8],p:usize)->usize{u32::from_le_bytes(b[p..p+4].try_into().unwrap()) as usize}
fn f32_at(b:&[u8],p:usize)->f32{f32::from_le_bytes(b[p..p+4].try_into().unwrap())}
fn native()->(Vec<Vector>,Vec<[u32;3]>) {
 let root=std::env::var("REM_TERRAIN_VALIDATION_DIR").unwrap();
 let b=std::fs::read(std::path::Path::new(&root).join("fo3_original_havok_static_collisions.bin")).unwrap();
 assert_eq!(&b[..8],b"FO3COL01");
 let nv=u32_at(&b,8);let ni=u32_at(&b,12);
 assert_eq!(nv,17214);assert_eq!(ni,24754);
 let start=16;
 let verts=(0..nv).map(|i|{
   let p=start+i*12;
   Vector::new(f32_at(&b,p),f32_at(&b,p+4),f32_at(&b,p+8))
 }).collect();
 let start=start+nv*12;
 let tris=(0..ni).map(|i|{
    let p=start+i*12;
    [u32_at(&b,p) as u32,u32_at(&b,p+4) as u32,u32_at(&b,p+8) as u32]
 }).collect();
 (verts,tris)
}
fn ray_ground(world:&PhysicsWorld,terrain:ColliderHandle,x:f32,z:f32)->f32{
 let filter=|h:ColliderHandle,_:&Collider|h==terrain;
 let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),&world.bodies,&world.colliders,QueryFilter::default().predicate(&filter));
 let ray=Ray::new(Vector::new(x,360.,z),Vector::new(0.,-1.,0.));
 let (_,t)=qp.cast_ray(&ray,250.,false).unwrap();
 360.-t
}
#[test]
fn native_havok_trimesh_is_accepted_by_rapier() {
 let (verts,tris)=native();
 assert_eq!((verts.len(),tris.len()),(17214,24754));
 assert!(verts.iter().all(|p|p.is_finite()));
 let mut world=PhysicsWorld::default();
 let (_,native_h)=world.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(verts.clone(),tris).expect("must accept original NIF Havok geometry"));
 world.step();
 let sample=verts[500];
 let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),&world.bodies,&world.colliders,QueryFilter::default());
 let ray=Ray::new(sample+Vector::new(0.,100.,0.),Vector::new(0.,-1.,0.));
 let (hit,_) = qp.cast_ray(&ray,200.,false).expect("native collider should be raycastable");
 assert_eq!(hit,native_h);
 println!("NATIVE_HAVOK_PROOF models=28 instances=149 verts={} triangles={} raycast=true",verts.len(),24754);
}
#[test]
fn walking_across_real_land_with_native_havok_objects() {
 let (v,t)=sample_mesh();
 let (nv,nt)=native();
 let mut world=PhysicsWorld::default();
 world.integration_parameters.dt=1.0/60.0;
 let (_,terrain)=world.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(v,t).unwrap());
 world.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(nv,nt).unwrap());
 let (player,_)=world.insert(RigidBodyBuilder::kinematic_position_based(),ColliderBuilder::capsule_y(0.55,0.35));
 world.step();
 let mut pos=Vector::new(416.0,ray_ground(&world,terrain,416.0,-506.0)+1.4,-506.0);
 let mut motor=KinematicCharacterController::default();
 motor.offset=CharacterLength::Absolute(0.02);
 motor.max_slope_climb_angle=50.0_f32.to_radians();
 motor.min_slope_slide_angle=35.0_f32.to_radians();
 motor.autostep=Some(CharacterAutostep{max_height:CharacterLength::Absolute(0.35),min_width:CharacterLength::Absolute(0.2),include_dynamic_bodies:false});
 motor.snap_to_ground=Some(CharacterLength::Absolute(0.3));
 let mut vy=0.0f32;let mut grounded=false;let mut frames=0;let mut sink=0.0_f32;
 for _ in 0..660 {
   let dt=1.0/60.0;
   if grounded{vy=-0.5;} else {vy-=9.81*dt;}
   let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),
           &world.bodies,&world.colliders,QueryFilter::exclude_dynamic().exclude_rigid_body(player));
   let movev=motor.move_shape(dt,&qp,&Capsule::new_y(0.55,0.35),
                   &Pose::from_translation(pos),Vector::new(4.2*dt,vy*dt,0.0),|_|{});
   pos+=movev.translation;
   grounded=movev.grounded;
   if grounded{frames+=1;if vy<0.0{vy=0.0;}}
   world.bodies.get_mut(player).unwrap().set_next_kinematic_translation(pos);
   world.step();
   let terr=ray_ground(&world,terrain,pos.x,pos.z);
   sink=sink.max((terr+0.90-pos.y).max(0.0));
   assert!(pos.is_finite());
 }
 println!("NATIVE_HAVOK_WALK x={} z={} grounded={} sink={} native_instances=149",pos.x,pos.z,frames,sink);
 assert!(pos.x>455.0,"native colliders blocked test path");
 assert!(frames>=560,"missing terrain grounding");
 assert!(sink<0.18,"fell below original terrain");
}
