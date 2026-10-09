"""Dump the structure of a Fallout NV NIF: block tree, shader/texture set,
BSX flags and Havok collision fields. Read-only.

Usage: python nif_dump.py <file.nif>
"""
import sys, time
if not hasattr(time, "clock"):  # pyffi 2.2.3 predates Python 3.8
    time.clock = time.perf_counter
from pyffi.formats.nif import NifFormat


def fmt(v):
    try:
        return v.decode("cp1252") if isinstance(v, bytes) else v
    except Exception:
        return v


def dump(path):
    data = NifFormat.Data()
    with open(path, "rb") as f:
        data.read(f)
    print("version", hex(data.version), "user", data.user_version, "user2", data.user_version_2)
    for root in data.roots:
        walk(root, 0, set())


def walk(b, d, seen):
    if b is None or id(b) in seen:
        return
    seen.add(id(b))
    ind = "  " * d
    name = fmt(getattr(b, "name", b""))
    print(f"{ind}{type(b).__name__} '{name}'")
    t = type(b).__name__
    if t == "BSXFlags":
        print(f"{ind}  integer_data={b.integer_data}")
    if t in ("NiNode", "BSFadeNode"):
        print(f"{ind}  flags={b.flags} scale={b.scale}")
    if t in ("NiTriShape", "NiTriStrips"):
        print(f"{ind}  flags={b.flags} scale={b.scale} trans=({b.translation.x:.2f},{b.translation.y:.2f},{b.translation.z:.2f})")
    if t == "NiTriShapeData":
        print(f"{ind}  verts={b.num_vertices} tris={b.num_triangles} has_normals={b.has_normals} uv_sets={b.num_uv_sets} vcol={b.has_vertex_colors}")
    if t == "BSShaderPPLightingProperty":
        print(f"{ind}  shader_type={b.shader_type} flags={b.shader_flags} env_scale={getattr(b,'environment_map_scale',None)} texclamp={b.texture_clamp_mode}")
    if t == "BSShaderTextureSet":
        for i, tx in enumerate(b.textures):
            print(f"{ind}  tex[{i}]={fmt(tx)}")
    if t == "NiMaterialProperty":
        print(f"{ind}  glossiness={b.glossiness} alpha={b.alpha} spec=({b.specular_color.r},{b.specular_color.g},{b.specular_color.b})")
    if t == "NiBinaryExtraData":
        print(f"{ind}  bytes={len(b.binary_data)}")
    if t == "bhkCollisionObject":
        print(f"{ind}  flags={b.flags}")
    if t in ("bhkRigidBody", "bhkRigidBodyT"):
        for f in ("layer", "col_filter", "mass", "friction", "restitution", "linear_damping", "angular_damping",
                  "max_linear_velocity", "max_angular_velocity", "penetration_depth", "motion_system",
                  "deactivator_type", "solver_deactivation", "quality_type"):
            if hasattr(b, f):
                print(f"{ind}  {f}={getattr(b, f)}")
    if t in ("bhkMoppBvTreeShape",):
        print(f"{ind}  material={getattr(b,'material',None)} mopp_bytes={len(b.mopp_data)}")
    if t in ("bhkPackedNiTriStripsShape", "bhkConvexVerticesShape", "bhkListShape", "bhkBoxShape", "bhkConvexTransformShape"):
        for f in ("material", "radius", "num_vertices", "num_normals", "num_sub_shapes", "scale"):
            if hasattr(b, f):
                v = getattr(b, f)
                print(f"{ind}  {f}={v}")
    if t == "hkPackedNiTriStripsData":
        print(f"{ind}  verts={b.num_vertices} tris={b.num_triangles}")
        if b.num_vertices:
            xs = [v.x for v in b.vertices]; ys = [v.y for v in b.vertices]; zs = [v.z for v in b.vertices]
            print(f"{ind}  havok_bounds x[{min(xs):.3f},{max(xs):.3f}] y[{min(ys):.3f},{max(ys):.3f}] z[{min(zs):.3f},{max(zs):.3f}]")
    for child in b.get_refs():
        walk(child, d + 1, seen)


if __name__ == "__main__":
    dump(sys.argv[1])
