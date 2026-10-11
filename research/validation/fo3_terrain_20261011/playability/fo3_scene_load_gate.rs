//! Local-only scene-load verification for original Fallout 3 two-cell glTF.
use bevy::prelude::*;
use bevy::asset::LoadState;
use bevy::window::{Window, WindowPlugin};
use bevy::world_serialization::prelude::{WorldAsset,WorldAssetRoot};
#[derive(Resource)]
struct TestScene {
    handle: Handle<WorldAsset>,
    frames: u32,
}
fn bootstrap(mut commands: Commands, assets: Res<AssetServer>) {
    let scene:Handle<WorldAsset>=assets.load("fo3_wasteland.glb#Scene0");
    commands.spawn((WorldAssetRoot(scene.clone()),Transform::default()));
    commands.insert_resource(TestScene{handle:scene,frames:0});
    commands.spawn((Camera3d::default(),Transform::from_xyz(445.0,255.0,-525.0).looking_at(Vec3::new(448.0,233.0,-485.0),Vec3::Y)));
    commands.spawn((DirectionalLight{illuminance:12500.0,shadow_maps_enabled:true,..default()},
        Transform::from_xyz(438.0,300.0,-505.0).looking_at(Vec3::new(448.0,230.0,-480.0),Vec3::Y)));
    println!("REM_TERRAIN_SCENE_LOAD_REQUESTED");
}
fn verify(mut state: ResMut<TestScene>, assets: Res<AssetServer>, mut exit: MessageWriter<AppExit>, scenes: Res<Assets<WorldAsset>>) {
    state.frames+=1;
    let load=assets.load_state(&state.handle);
    match load {
        LoadState::Loaded => {
            let loaded=scenes.get(&state.handle).is_some();
            println!("REM_TERRAIN_SCENE_LOADED={} FRAME={} handle_loaded={}",loaded,state.frames,loaded);
            exit.write(if loaded{AppExit::Success}else{AppExit::error()});
        }
        LoadState::Failed(ref e) =>{
            eprintln!("REM_TERRAIN_SCENE_FAILED={e:?}");
            exit.write(AppExit::error());
        }
        _ if state.frames>900=>{
            eprintln!("REM_TERRAIN_SCENE_TIMEOUT last_state={load:?}");
            exit.write(AppExit::error());
        }
        _=>{}
    }
}
fn main(){
    let mut app=App::new();
    app.add_plugins(DefaultPlugins.set(WindowPlugin{
        primary_window:Some(Window{visible:false,title:"REM Dream original FO3 terrain isolated load check".into(),
             resolution:(960,540).into(),..default()}),..default()
    }));
    app.add_systems(Startup,bootstrap);
    app.add_systems(Update,verify);
    app.run();
}
