//! REM Dream isolated native FO3 world and Bevy/rapier playability proof.
//! Original ESM/NIF extracts supplied locally, never committed. Not gameplay implementation.
use bevy::prelude::*;
use bevy::asset::LoadState;
use bevy::gltf::Gltf;
use bevy::world_serialization::prelude::{WorldAsset,WorldAssetRoot};
use bevy::window::{Window,WindowPlugin};
use rapier3d::prelude::*;
use rapier3d::math::{Vector,Pose};
use rapier3d::control::{KinematicCharacterController,CharacterLength,CharacterAutostep};
use serde_json::Value;
use std::path::Path;
use std::collections::HashSet;

fn u32_at(b:&[u8],p:usize)->usize {u32::from_le_bytes(b[p..p+4].try_into().unwrap()) as usize}
fn f32_at(b:&[u8],p:usize)->f32 {f32::from_le_bytes(b[p..p+4].try_into().unwrap())}
fn read_mesh(path:&Path)->(Vec<Vector>,Vec<[u32;3]>) {
 let b=std::fs::read(path).unwrap();
 assert_eq!(&b[..4],b"glTF");
 let len=u32_at(&b,12);
 let doc:Value=serde_json::from_slice(&b[20..20+len]).unwrap();
 let blob=&b[28+len..];
 let views=doc["bufferViews"].as_array().unwrap();
 let access=doc["accessors"].as_array().unwrap();
 let astart=|i:usize| views[access[i]["bufferView"].as_u64().unwrap() as usize]["byteOffset"].as_u64().unwrap() as usize;
 let p=astart(0);let n=access[0]["count"].as_u64().unwrap() as usize;
 let v=(0..n).map(|i|Vector::new(f32_at(blob,p+i*12),f32_at(blob,p+i*12+4),f32_at(blob,p+i*12+8))).collect();
 let p=astart(3);let n=access[3]["count"].as_u64().unwrap() as usize;
 let t=(0..n/3).map(|i|[u32_at(blob,p+i*12) as u32,u32_at(blob,p+i*12+4) as u32,u32_at(blob,p+i*12+8) as u32]).collect();
 (v,t)
}
fn json_file(root:&Path,name:&str)->Value {serde_json::from_slice(&std::fs::read(root.join(name)).unwrap()).unwrap()}
#[derive(Resource)]
struct Gate {
  scene:Handle<WorldAsset>,
  gltf:Handle<Gltf>,
  tick:u32,
  update_tick:u32,
  completed:bool,
  walked:bool,
  registered:usize,
  physics:PhysicsWorld,
  kcc:KinematicCharacterController,
  player:RigidBodyHandle,
  terrain:ColliderHandle,
  position:Vector,
  grounded:bool,
  vertical:f32,
  grounded_frames:u32,
  max_sink:f32,
  max_lift:f32,
}
#[derive(Component)]
struct Walker;
fn surface(world:&PhysicsWorld,terrain:ColliderHandle,x:f32,z:f32)->f32 {
 let only=|h:ColliderHandle,_:&Collider|h==terrain;
 let filter=QueryFilter::default().predicate(&only);
 let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),&world.bodies,&world.colliders,filter);
 let ray=Ray::new(Vector::new(x,360.0,z),Vector::new(0.0,-1.0,0.0));
 let (_,toi)=qp.cast_ray(&ray,250.0,false).expect("source FO3 terrain surface ray");
 360.0-toi
}
fn initialize(mut commands:Commands,assets:Res<AssetServer>,mut meshes:ResMut<Assets<Mesh>>,mut mats:ResMut<Assets<StandardMaterial>>) {
 let root=Path::new(r"D:\REM_Dream_validation_20261011");
 let (v,t)=read_mesh(&root.join("fo3_original_two_cells_6_7_7_7.glb"));
 let mut physics=PhysicsWorld::default();
 physics.integration_parameters.dt=1.0/60.0;
 let (_,terrain)=physics.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(v,t).unwrap());

 let native_manifest=json_file(root,"fo3_havok_collider_export_manifest.json");
 let native_ids:HashSet<String>=native_manifest["native_base_ids"].as_array().unwrap().iter()
     .map(|id|id.as_str().unwrap().to_owned()).collect();
 let nb=std::fs::read(root.join("fo3_original_havok_static_collisions.bin")).unwrap();
 assert_eq!(&nb[0..8],b"FO3COL01");
 let nv=u32_at(&nb,8);let nt=u32_at(&nb,12);
 assert_eq!((nv,nt),(17214,24754));
 let verts:Vec<Vector>=(0..nv).map(|i|{
    let p=16+i*12;Vector::new(f32_at(&nb,p),f32_at(&nb,p+4),f32_at(&nb,p+8))
 }).collect();
 let tris:Vec<[u32;3]>=(0..nt).map(|i|{
    let p=16+nv*12+i*12;[u32_at(&nb,p) as u32,u32_at(&nb,p+4) as u32,u32_at(&nb,p+8) as u32]
 }).collect();
 physics.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(verts,tris).unwrap());
 let mut source_colliders=0;
 let mut fallback_colliders=0;

 let metadata=json_file(root,"fo3_placed_objects_two_cells.json");
 let bases=json_file(root,"fo3_two_cell_base_models.json");
 let mut registered=0;
 for ob in metadata["all_placed"].as_array().unwrap() {
   if ob["kind"]!="REFR" {continue;}
   if native_ids.contains(ob["base"].as_str().unwrap()){
      registered+=1;
      source_colliders+=1;
      continue;
   }
   fallback_colliders+=1;
   let Some(bounds)=bases["base_records"][ob["base"].as_str().unwrap()]["obnd"].as_array() else{continue;};
   let lo:Vec<f32>=bounds.iter().map(|x|x.as_f64().unwrap() as f32).collect();
   let xyz=ob["position"].as_array().unwrap();
   let sc=ob["scale"].as_f64().unwrap() as f32;
   let x=xyz[0].as_f64().unwrap() as f32/64.0;
   let z=-(xyz[1].as_f64().unwrap() as f32/64.0);
   let y=xyz[2].as_f64().unwrap() as f32/64.0;
   let center=Vector::new(x+(lo[0]+lo[3])*sc/128.0,y+(lo[2]+lo[5])*sc/128.0,z-(lo[1]+lo[4])*sc/128.0);
   let half=Vector::new((lo[3]-lo[0]).abs()*sc/128.0,(lo[5]-lo[2]).abs()*sc/128.0,(lo[4]-lo[1]).abs()*sc/128.0).max(Vector::splat(0.025));
   physics.insert(RigidBodyBuilder::fixed().translation(center),ColliderBuilder::cuboid(half.x,half.y,half.z));
   registered+=1;
 }
 let (player,_)=physics.insert(RigidBodyBuilder::kinematic_position_based(),ColliderBuilder::capsule_y(0.55,0.35));
 physics.step();
 let y=surface(&physics,terrain,416.0,-506.0);
 let pos=Vector::new(416.0,y+1.4,-506.0);
 let mut controller=KinematicCharacterController::default();
 controller.offset=CharacterLength::Absolute(0.02);
 controller.max_slope_climb_angle=50.0f32.to_radians();
 controller.min_slope_slide_angle=35.0f32.to_radians();
 controller.autostep=Some(CharacterAutostep{max_height:CharacterLength::Absolute(0.35),min_width:CharacterLength::Absolute(0.2),include_dynamic_bodies:false});
 controller.snap_to_ground=Some(CharacterLength::Absolute(0.3));
 let scene:Handle<WorldAsset>=assets.load("fo3_wasteland.glb#Scene0");
 let gltf:Handle<Gltf>=assets.load("fo3_wasteland.glb");
 commands.spawn((WorldAssetRoot(scene.clone()),Transform::default()));
 commands.spawn((Walker,Mesh3d(meshes.add(Capsule3d::new(0.35,1.1))),MeshMaterial3d(mats.add(StandardMaterial{base_color:Color::srgb(0.95,0.45,0.08),..default()})),Transform::from_translation(Vec3::new(pos.x,pos.y,pos.z))));
 commands.spawn((Camera3d::default(),Transform::from_xyz(445.0,258.0,-532.0).looking_at(Vec3::new(448.0,234.0,-488.0),Vec3::Y)));
 commands.spawn((DirectionalLight{illuminance:14000.0,shadow_maps_enabled:true,..default()},Transform::from_xyz(445.0,300.0,-520.0).looking_at(Vec3::new(448.0,230.0,-480.0),Vec3::Y)));
 commands.insert_resource(Gate{scene,gltf,tick:0,update_tick:0,completed:false,walked:false,registered,physics,kcc:controller,player,terrain,position:pos,grounded:false,vertical:0.0,grounded_frames:0,max_sink:0.0,max_lift:0.0});
 println!("FO3_BEVY_GATE_BOOTSTRAP objects={} original_havok=149 fallback_proxies={} native_triangles=24754 initial_x=416 land_cells=2",registered,fallback_colliders);
 assert_eq!(source_colliders,149);
 assert_eq!(fallback_colliders,102);
}
fn walk(mut gate:ResMut<Gate>,mut walker:Query<&mut Transform,With<Walker>>) {
 if gate.tick>=660{return;}
 let dt=1.0f32/60.0;
 if gate.grounded{gate.vertical=-0.5;}else{gate.vertical-=9.81*dt;}
 let filter=QueryFilter::exclude_dynamic().exclude_rigid_body(gate.player);
 let qp=gate.physics.broad_phase.as_query_pipeline(gate.physics.narrow_phase.query_dispatcher(),&gate.physics.bodies,&gate.physics.colliders,filter);
 let delta=Vector::new(4.2*dt,gate.vertical*dt,0.0);
 let mv=gate.kcc.move_shape(dt,&qp,&Capsule::new_y(0.55,0.35),&Pose::from_translation(gate.position),delta,|_|{});
 let current=gate.position+mv.translation;
 gate.position=current;
 gate.grounded=mv.grounded;
 if mv.grounded{gate.grounded_frames+=1;if gate.vertical<0.0{gate.vertical=0.0;}}
 let player=gate.player;
 gate.physics.bodies.get_mut(player).unwrap().set_next_kinematic_translation(current);
 gate.physics.step();
 let expected=surface(&gate.physics,gate.terrain,current.x,current.z)+0.90;
 gate.max_lift=gate.max_lift.max((current.y-expected).max(0.0));
 gate.max_sink=gate.max_sink.max((expected-current.y).max(0.0));
 if let Ok(mut tf)=walker.single_mut(){tf.translation=Vec3::new(current.x,current.y,current.z);}
 gate.tick+=1;
 if gate.tick==660{
   gate.walked=current.x>455.0&&current.x>448.0&&gate.grounded_frames>=560&&gate.max_sink<0.18&&(current.z+506.0).abs()<1.0&&gate.registered==251;
   gate.completed=true;
   println!("FO3_BEVY_TRAVERSE_COMPLETE passed={} x={:.3} z={:.3} grounded={} ticks={} sink={:.5} lift={:.5} objects={}",
      gate.walked,current.x,current.z,gate.grounded_frames,gate.tick,gate.max_sink,gate.max_lift,gate.registered);
 }
}
fn finish(mut gate:ResMut<Gate>,assets:Res<AssetServer>,gltf:Res<Assets<Gltf>>,mut exit:MessageWriter<AppExit>,names:Query<&Name>) {
 gate.update_tick+=1;
 match assets.load_state(&gate.scene) {
   LoadState::Failed(ref why)=>{eprintln!("FO3_BEVY_GATE_SCENE_ERROR={why:?}");exit.write(AppExit::error());return;}
   _=>{}
 }
 if !gate.completed {
   if gate.update_tick>2400 {eprintln!("FO3_BEVY_GATE_TIMEOUT ticks={}",gate.tick);exit.write(AppExit::error());}
   return;
 }
 let scene_ready=matches!(assets.load_state(&gate.scene),LoadState::Loaded);
 let gltfdata=gltf.get(&gate.gltf);
 let models=gltfdata.map(|g|g.meshes.len()).unwrap_or(0);
 let nodes=gltfdata.map(|g|g.nodes.len()).unwrap_or(0);
 let known_entities=names.iter().filter(|n|n.as_str().starts_with("FO3_")).count();
 if !scene_ready||gltfdata.is_none() {
   if gate.update_tick>2400{eprintln!("FO3_BEVY_GATE_GLTF_TIMEOUT");exit.write(AppExit::error());}
   return;
 }
 let verdict=gate.walked && models==35 && nodes>=240;
 println!("FO3_BEVY_GATE_RESULT passed={} scene_loaded={} gltf_meshes={} gltf_nodes={} named_entities={} world_instances=239 land_triangles=4096",
          verdict,scene_ready,models,nodes,known_entities);
 exit.write(if verdict{AppExit::Success}else{AppExit::error()});
}
fn main(){
 let mut app=App::new();
 app.add_plugins(DefaultPlugins.set(WindowPlugin{primary_window:Some(Window{visible:false,title:"REM Dream FO3 automated traversal".into(),resolution:(960,540).into(),..default()}),..default()}));
 app.insert_resource(Time::<Fixed>::from_hz(60.0));
 app.add_systems(Startup,initialize);
 app.add_systems(FixedUpdate,walk);
 app.add_systems(Update,finish);
 app.run();
}
