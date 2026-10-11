use rapier3d::prelude::*;
use rapier3d::math::{Vector,Pose};
use rapier3d::control::{KinematicCharacterController, CharacterLength, CharacterAutostep};
use serde_json::Value;
use std::collections::HashMap;

use super::tests::sample_mesh;

fn input_json(file:&str)->Value {
 let binding=std::env::var("REM_TERRAIN_VALIDATION_DIR").unwrap();
 let root=std::path::Path::new(&binding);
 serde_json::from_slice(&std::fs::read(root.join(file)).unwrap()).unwrap()
}

fn fixture()->(PhysicsWorld,ColliderHandle,RigidBodyHandle,Vec<(String,ColliderHandle)>) {
 let (vertices,triangles)=sample_mesh();
 let mut world=PhysicsWorld::default();
 world.integration_parameters.dt=1.0/60.0;
 let (_,terrain)=world.insert(
    RigidBodyBuilder::fixed(),
    ColliderBuilder::trimesh(vertices,triangles).expect("original FO3 terrain must be valid"));
 let objs=input_json("fo3_placed_objects_two_cells.json");
 let bases=input_json("fo3_two_cell_base_models.json");
 let mut registrations=Vec::new();
 let refs=objs["all_placed"].as_array().unwrap();
 assert_eq!(refs.len(),252);
 let mut unique=HashMap::new();
 for o in refs {
   let id=o["id"].as_str().unwrap().to_owned();
   if o["kind"]=="ACRE" {continue;}
   let base=o["base"].as_str().unwrap();
   let model=&bases["base_records"][base];
   let bbox=model["obnd"].as_array().unwrap();
   if bbox.len()!=6 {continue;}
   let local:Vec<f32>=bbox.iter().map(|v|v.as_f64().unwrap() as f32).collect();
   let scale=o["scale"].as_f64().unwrap() as f32;
   let pos=o["position"].as_array().unwrap();
   let px=pos[0].as_f64().unwrap() as f32/64.0;
   let pz=-(pos[1].as_f64().unwrap() as f32/64.0);
   let py=pos[2].as_f64().unwrap() as f32/64.0;
   // Proxies: original OBND only. Rotation/real NIF collision NOT represented.
   let center=Vector::new(px+(local[0]+local[3])*0.5*scale/64.0,
                         py+(local[2]+local[5])*0.5*scale/64.0,
                         pz-(local[1]+local[4])*0.5*scale/64.0);
   let half=Vector::new((local[3]-local[0]).abs()*0.5*scale/64.0,
                         (local[5]-local[2]).abs()*0.5*scale/64.0,
                         (local[4]-local[1]).abs()*0.5*scale/64.0)
       .max(Vector::splat(0.025));
   let (_,h)=world.insert(RigidBodyBuilder::fixed().translation(center),
                          ColliderBuilder::cuboid(half.x,half.y,half.z));
   assert!(unique.insert(id.clone(),h).is_none());
   registrations.push((id,h));
 }
 let (player,_) = world.insert(RigidBodyBuilder::kinematic_position_based(),
                                ColliderBuilder::capsule_y(0.55,0.35));
 world.step();
 (world,terrain,player,registrations)
}

fn ground_at(world:&PhysicsWorld, x:f32,z:f32, terrain:ColliderHandle)->f32 {
  let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),
                     &world.bodies,&world.colliders,QueryFilter::default());
  let binding=|handle: ColliderHandle, _: &Collider|handle==terrain;
  let filter=QueryFilter::default().predicate(&binding);
  let qp2=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),
                     &world.bodies,&world.colliders,filter);
  let ray=Ray::new(Vector::new(x,360.0,z),Vector::new(0.0,-1.0,0.0));
  let (_,t)=qp2.cast_ray(&ray,250.0,false).expect("must raycast original FO3 LAND");
  let _=qp;
  360.0-t
}

#[test]
fn original_world_object_placements_register_251_proxy_colliders() {
 let (world,terrain,_player,refs)=fixture();
 assert_eq!(refs.len(),251);
 assert!(world.colliders.contains(terrain));
 for (_,h) in refs.iter().take(251) {assert!(world.colliders.contains(*h));}
 let obj=input_json("fo3_placed_objects_two_cells.json");
 let bases=input_json("fo3_two_cell_base_models.json");
 assert_eq!(obj["object_count"],252);
 assert_eq!(bases["resolved"],37);
 println!("WORLD_OBJECT_PROXY_REGISTRATIONS={} BASE_FORMS=37; original NIF/collision NOT loaded",refs.len());
}

#[test]
fn raycast_surface_continuity_across_exact_cell_boundary() {
 let (world,terrain,_player,_refs)=fixture();
 let z=-506.0;
 let left=ground_at(&world,447.98,z,terrain);
 let right=ground_at(&world,448.02,z,terrain);
 println!("SEAM_HEIGHT left={} right={} difference={}",left,right,(left-right).abs());
 assert!((left-right).abs()<0.05,"actual LAND seam discontinuity");
}

#[test]
fn full_controller_walks_across_wasteland_cell_boundary_on_real_collision() {
 let (mut world,terrain,player,refs)=fixture();
 let dt=1.0_f32/60.0;
 let z=-506.0;
 let ground=ground_at(&world,416.0,z,terrain);
 let mut pos=Vector::new(416.0,ground+1.4,z);
 let mut controller=KinematicCharacterController::default();
 controller.offset=CharacterLength::Absolute(0.02);
 controller.max_slope_climb_angle=50.0_f32.to_radians();
 controller.min_slope_slide_angle=35.0_f32.to_radians();
 controller.autostep=Some(CharacterAutostep {max_height:CharacterLength::Absolute(0.35),
                  min_width:CharacterLength::Absolute(0.2),include_dynamic_bodies:false});
 controller.snap_to_ground=Some(CharacterLength::Absolute(0.3));
 let mut vel_y=0.0f32;
 let mut was_grounded=false;
 let mut grounded_frames=0;
 let mut max_lift=0.0f32;
 let mut max_sink=0.0f32;
 for frame in 0..660 {
   if was_grounded {vel_y=-0.5;}else{vel_y-=9.81*dt;}
   let filter=QueryFilter::exclude_dynamic().exclude_rigid_body(player);
   let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),
                               &world.bodies,&world.colliders,filter);
   let requested=Vector::new(4.2*dt,vel_y*dt,0.0);
   let out=controller.move_shape(dt,&qp,&Capsule::new_y(0.55,0.35),
                  &Pose::from_translation(pos),requested,|_|{});
   pos+=out.translation;
   was_grounded=out.grounded;
   if out.grounded {grounded_frames+=1;if vel_y<0.0{vel_y=0.0;}}
   if let Some(rb)=world.bodies.get_mut(player) {rb.set_next_kinematic_translation(pos);}
   world.step();
   let expected=ground_at(&world,pos.x,pos.z,terrain)+0.90;
   max_lift=max_lift.max((pos.y-expected).max(0.0));
   max_sink=max_sink.max((expected-pos.y).max(0.0));
   if frame%120==0 {println!("TRAVERSE t={:.1}s x={:.3} height={:.3} ground={} placed={}",frame as f32*dt,pos.x,pos.y,out.grounded,refs.len());}
   assert!(pos.is_finite(),"non-finite traversal result");
 }
 println!("TRAVERSE_RESULT x={:.4} z={:.4} landed_frames={} max_lift={} max_sink={} static_proxies={}",
         pos.x,pos.z,grounded_frames,max_lift,max_sink,refs.len());
 assert!(pos.x>448.0,"player did not cross the original Fallout cell boundary");
 assert!(pos.x>455.0,"insufficient actual traversed distance");
 assert!((pos.z-z).abs()<1.0,"lateral ground-contact deflection exceeds 1 metre");
 assert!(grounded_frames>=560,"ground contact fraction too low");
 assert!(max_sink<0.18,"character sinks significantly below LAND contact");
 assert!(max_lift<1.5,"character floats relative to LAND");
}
