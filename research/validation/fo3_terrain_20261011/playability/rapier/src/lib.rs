// Independent, test-only physics proof on an extracted original FO3 heightfield GLB.
// The input must come from an owner-held local Fallout3.esm; it must never be committed.
#[cfg(test)]
mod tests {
    use rapier3d::prelude::*;
    use rapier3d::math::{Vector, Pose};
    use rapier3d::control::KinematicCharacterController;
    use serde_json::Value;
    use std::path::PathBuf;

    fn read_u32(bytes: &[u8], at: usize)->usize {
        u32::from_le_bytes(bytes[at..at+4].try_into().unwrap()) as usize
    }
    fn read_f32(bytes: &[u8], at: usize)->f32 {
        f32::from_le_bytes(bytes[at..at+4].try_into().unwrap())
    }
    pub(super) fn sample_mesh()->(Vec<Vector>,Vec<[u32;3]>) {
        let p=std::env::var("REM_FO3_TERRAIN_GLB").map(PathBuf::from)
            .expect("set REM_FO3_TERRAIN_GLB to locally extracted Fallout3.esm terrain GLB");
        let b=std::fs::read(p).unwrap();
        assert_eq!(&b[0..4], b"glTF");
        assert_eq!(read_u32(&b,4),2);
        assert_eq!(read_u32(&b,8),b.len());
        let js=read_u32(&b,12);
        assert_eq!(&b[16..20],b"JSON");
        let doc: Value=serde_json::from_slice(&b[20..20+js]).unwrap();
        let bin_hdr=20+js;
        assert_eq!(&b[bin_hdr+4..bin_hdr+8],b"BIN\0");
        let payload=&b[bin_hdr+8..];
        let views=doc["bufferViews"].as_array().unwrap();
        let access=doc["accessors"].as_array().unwrap();
        let acc_offset=|idx:usize|{
            let viewidx=access[idx]["bufferView"].as_u64().unwrap() as usize;
            views[viewidx]["byteOffset"].as_u64().unwrap() as usize
        };
        let base=acc_offset(0);
        let total=access[0]["count"].as_u64().unwrap() as usize;
        let mut vertices=Vec::with_capacity(total);
        for i in 0..total {
            let o=base+i*12;
            vertices.push(Vector::new(read_f32(payload,o),read_f32(payload,o+4),read_f32(payload,o+8)));
        }
        let ioff=acc_offset(3);
        let ni=access[3]["count"].as_u64().unwrap() as usize;
        assert_eq!(ni%3,0);
        let mut triangles=Vec::with_capacity(ni/3);
        for i in 0..ni/3 {
            let o=ioff+i*12;
            triangles.push([read_u32(payload,o) as u32,read_u32(payload,o+4) as u32,read_u32(payload,o+8) as u32]);
        }
        (vertices,triangles)
    }
    #[test]
    fn real_land_mesh_accepts_rapier_and_surface_raycast() {
        let (verts,tris)=sample_mesh();
        assert_eq!(verts.len(),2178);
        assert_eq!(tris.len(),4096);
        assert!(verts.iter().all(|p|p.is_finite()));
        let mut world=PhysicsWorld::default();
        let tri=ColliderBuilder::trimesh(verts.clone(),tris).expect("real terrain must be a valid triangle mesh");
        let (_,handle)=world.insert(RigidBodyBuilder::fixed(),tri);
        world.step();
        for (ci,cx) in [(0_usize,416.0_f32),(1_usize,480.0_f32)] {
            let vidx=ci*1089+16*33+16;
            let target=verts[vidx];
            let q=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),&world.bodies,&world.colliders,QueryFilter::default());
            let ray=Ray::new(Vector::new(cx,target.y+20.0,-480.0),Vector::new(0.0,-1.0,0.0));
            let (found,toi)=q.cast_ray(&ray,40.0,true).expect("Ray must strike imported FO3 terrain");
            assert_eq!(handle,found);
            let observed=target.y+20.0-toi;
            assert!((observed-target.y).abs()<0.075,"cell {} expected {} got {}",ci,target.y,observed);
        }
    }

    #[test]
    fn kinematic_capsule_grounded_on_imported_land() {
        let (verts,tris)=sample_mesh();
        let mut world=PhysicsWorld::default();
        let (_,c)=world.insert(RigidBodyBuilder::fixed(),ColliderBuilder::trimesh(verts.clone(),tris).unwrap());
        world.step();
        let v=verts[16*33+16]; // cell (6,7), centre
        let shape=Capsule::new_y(0.55,0.35);
        let mut controller=KinematicCharacterController::default();
        controller.offset=rapier3d::control::CharacterLength::Absolute(0.02);
        let mut pos=Vector::new(v.x,v.y+5.0,v.z);
        let mut ever_ground=false;
        for _ in 0..180 {
            let qp=world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(),&world.bodies,&world.colliders,QueryFilter::default());
            let out=controller.move_shape(1.0/60.0,&qp,&shape,&Pose::from_translation(pos),Vector::new(0.0,-0.15,0.0),|_|{});
            pos+=out.translation;
            if out.grounded {ever_ground=true;break;}
        }
        assert!(ever_ground,"capsule never settled on FO3 LAND");
        assert!(pos.y>v.y + 0.65 && pos.y < v.y+1.3, "unexpected capsule terrain contact height {}",pos.y);
        let _=c;
    }
}

#[cfg(test)]
mod playability;

#[cfg(test)]
mod native_havok;
