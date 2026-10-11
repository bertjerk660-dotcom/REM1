// Offline source-level validation of an upstream open-source detector.
// Copy the pinned upstream crates/render_anim/src/skate/rails.rs into
// src/rails_external.rs before testing. DO NOT edit or commit that file.
// This alias lets its original `use bevy::math::Vec3;` resolve to
// the target Bevy 0.20 maths crate without compiling the entire IW4L runtime.
extern crate self as bevy;
pub mod math { pub use bevy_math::Vec3; }

#[path = "rails_external.rs"]
mod rails;

#[cfg(test)]
mod validation {
    use super::math::Vec3;
    use super::rails;

    fn v(x:f32,y:f32,z:f32)->Vec3 {Vec3::new(x,y,z)}
    fn quad(size:f32, z:f32) -> Vec<[Vec3;3]> {
        vec![
          [v(0.,0.,z),v(size,0.,z),v(size,size,z)],
          [v(0.,0.,z),v(size,size,z),v(0.,size,z)]
        ]
    }

    #[test]
    fn empty_world_never_produces_a_rail() {
        let (found, census) = rails::find(&[]);
        assert!(found.is_empty());
        assert_eq!(census.rails, 0);
    }

    #[test]
    fn vertical_wall_not_a_walkable_lip() {
        let triangles = [[v(0.,0.,0.),v(0.,128.,0.),v(0.,128.,64.)],
                         [v(0.,0.,0.),v(0.,128.,64.),v(0.,0.,64.)]];
        let (found,census)=rails::find(&triangles);
        assert!(found.is_empty(), "wall produces {} rails", census.rails);
    }

    #[test]
    fn small_platform_does_not_make_full_grind_rail() {
        let t=quad(8.,16.);
        let (found,census)=rails::find(&t);
        assert!(found.is_empty(), "tiny platform yields {} rails", census.rails);
    }

    #[test]
    fn platform_edges_detected_and_interior_diagonal_excluded() {
        let t=quad(128.,16.);
        let (found,census)=rails::find(&t);
        assert!(census.rails>0,"large platform produced no edges");
        assert!(census.candidates>=5,"unexpected candidate edge count");
        assert!(found.iter().all(|r| r.len()>=2));
        assert!(!found.iter().any(|p| p.windows(2).any(|w|
            ((w[0]-v(0.,0.,16.)).length()<0.1&&(w[1]-v(128.,128.,16.)).length()<0.1) ||
            ((w[1]-v(0.,0.,16.)).length()<0.1&&(w[0]-v(128.,128.,16.)).length()<0.1)
        )),"interior diagonal falsely grindable");
    }

    #[test]
    fn reversed_face_winding_not_walkable() {
        let triangles=quad(128.,16.).into_iter().map(|[a,b,c]| [a,c,b]).collect::<Vec<_>>();
        let (found,census)=rails::find(&triangles);
        assert!(found.is_empty(),"downward winding yields {} rails",census.rails);
    }

    #[test]
    fn rail_endpoints_are_finite() {
        let (found,_)=rails::find(&quad(128.,16.));
        assert!(found.iter().flat_map(|r|r.iter()).all(|p|p.is_finite()));
    }
}
