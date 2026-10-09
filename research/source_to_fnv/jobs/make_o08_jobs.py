"""Generate the O08a/b/c weapon job files from the staged packages, checking every
input against the 2026-10-07 packet hashes. Files the packets do not list are
pinned (hash recorded at first use) and named in `pinned_inputs`.

Usage: python make_o08_jobs.py --root <workspace> --repo <repo>
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path

H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
PKG = "build/prepared/gmod_hl_weapon_models/packages"

COMMON = {
    "scale": 1.7777778,
    "cubemap": "textures\\effects\\shinybright_e.dds",
    "vtfcmd": "third_party/tools/VTFEdit_Reloaded/VTFCmd.exe",
    "templates": {
        "metal": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handpistol\\10mmpistol.nif"],
        "glow": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handgrenadethrow\\plasmagrenade.nif"],
        "glow_no_env": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handgrenadethrow\\stungrenade.nif"],
    },
}

WEAPONS = {
    "a": {
        "name": "crowbar", "packet": "opus_o08a_crowbar_presentation_20261007.json",
        "job": "O08a GMod/HL Crowbar presentation - models/weapons/w_crowbar.mdl + c_crowbar.mdl",
        "grip": {"nif": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handmelee\\leadpipe.nif"], "mode": "shaft",
                 "note": "DLL melee animation donor WeapLeadPipe (00004337). Shaft centred on the lead pipe at hand height; Source grip position along the shaft kept."},
        "world": {"smd": "w_crowbar/decompiled/w_Crowbar_reference.smd", "phy": "w_crowbar/decompiled/w_crowbar_physics.smd",
                  "qc": "w_crowbar/decompiled/w_crowbar.qc", "mdl": "w_crowbar/src/models/weapons/w_crowbar.mdl",
                  "havok": "MAT_METAL", "havok_note": "w_crowbar.qc $surfaceprop crowbar (metal bar)."},
        "view": {"smd": "c_crowbar/decompiled/crowbar_reference.smd", "qc": "c_crowbar/decompiled/c_crowbar.qc",
                 "mdl": "c_crowbar/src/models/weapons/c_crowbar.mdl", "mode": "icp_to_world", "bone": "ValveBiped.Bip01_R_Hand", "max_median": 0.5, "fixed_scale": 1.0},
        "materials": {
            "crowbar_cyl": {"vmt": "w_crowbar/materials/materials/models/weapons/v_crowbar/crowbar_cyl.vmt",
                            "base": "w_crowbar/materials/materials/models/weapons/v_crowbar/crowbar_cyl.vtf",
                            "bump": "w_crowbar/materials/materials/models/weapons/v_crowbar/crowbar_normal.vtf"},
            "head_uvw": {"vmt": "w_crowbar/materials/materials/models/weapons/v_crowbar/head_uvw.vmt",
                         "base": "w_crowbar/materials/materials/models/weapons/v_crowbar/head.vtf",
                         "bump": "w_crowbar/materials/materials/models/weapons/v_crowbar/head_normal.vtf"}},
        "muzzle": None,
    },
    "b": {
        "name": "pistol", "packet": "opus_o08b_pistol_presentation_20261007.json",
        "job": "O08b GMod/HL Pistol presentation - models/weapons/w_pistol.mdl + c_pistol.mdl",
        "grip": {"nif": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handpistol\\9mm.nif"], "mode": "bottom", "shape": "*", "window": {"donor_x": [-6, 6], "source_x": [-2, 14]},
                 "note": "DLL pistol animation donor WeapNV9mmPistol (000E3778). Grip bottom registered onto the 9mm grip bottom."},
        "world": {"smd": "w_pistol/decompiled/w_pistol_ref.smd", "phy": "w_pistol/decompiled/w_pistol_physics.smd",
                  "qc": "w_pistol/decompiled/w_pistol.qc", "mdl": "w_pistol/src/models/weapons/w_pistol.mdl",
                  "havok": "MAT_METAL", "havok_note": "w_pistol.qc $surfaceprop weapon."},
        "view": {"smd": "c_pistol/decompiled/v_pistol_reference.smd", "qc": "c_pistol/decompiled/c_pistol.qc",
                 "mdl": "c_pistol/src/models/weapons/c_pistol.mdl", "mode": "icp_to_world", "bone": "ValveBiped.Bip01_R_Hand", "max_median": 0.5, "fixed_scale": 1.0},
        "materials": {
            "pistol": {"vmt": "w_pistol/materials/materials/models/weapons/w_pistol/pistol.vmt",
                       "base": "w_pistol/materials/materials/models/weapons/w_pistol/pistol.vtf"},
            "v_pistol_sheet": {"vmt": "c_pistol/materials/materials/models/weapons/v_pistol/v_pistol_sheet.vmt",
                               "base": "c_pistol/materials/materials/models/weapons/v_pistol/v_pistol_sheet.vtf",
                               "bump": "c_pistol/materials/materials/models/weapons/v_pistol/v_pistol_sheet_normal.vtf"}},
        "muzzle": "muzzle",
    },
    "c": {
        "name": "smg1", "packet": "opus_o08c_smg1_presentation_20261007.json",
        "job": "O08c GMod/HL SMG1 presentation - models/weapons/w_smg1.mdl + c_smg1.mdl",
        "grip": {"nif": ["Fallout - Meshes.bsa", "meshes\\weapons\\1handpistol\\10mmsubmachinegun.nif"], "mode": "bottom", "shape": "*", "window": {"donor_x": [-6, 6], "source_x": [-2, 14]},
                 "note": "SMG1 is outside the DLL's 14 handled GMod weapons; its ESP animation type is one-hand pistol (3), so the vanilla 10mm SMG (same type) is the grip reference."},
        "world": {"smd": "w_smg1/decompiled/smg1_reference.smd", "phy": "w_smg1/decompiled/w_smg1_physics.smd",
                  "qc": "w_smg1/decompiled/w_smg1.qc", "mdl": "w_smg1/src/models/weapons/w_smg1.mdl",
                  "havok": "MAT_METAL", "havok_note": "w_smg1.qc $surfaceprop weapon."},
        "view": {"smd": "c_smg1/decompiled/Smg1_ref.smd", "qc": "c_smg1/decompiled/c_smg1.qc",
                 "mdl": "c_smg1/src/models/weapons/c_smg1.mdl", "mode": "icp_to_world", "bone": "ValveBiped.base", "max_median": 0.5, "scale_range": [0.8, 1.25]},
        "materials": {
            "w_smg2": {"vmt": "w_smg1/materials/materials/models/weapons/w_smg1/w_smg2.vmt",
                       "base": "w_smg1/materials/materials/models/weapons/w_smg1/w_smg2.vtf",
                       "envmapmask": "w_smg1/materials/materials/models/weapons/w_smg1/w_smg2specularmask.vtf"},
            "smg_crosshair": {"vmt": "w_smg1/materials/materials/models/weapons/w_smg1/smg_crosshair.vmt",
                              "base": "w_smg1/materials/materials/models/weapons/w_smg1/smg_crosshair.vtf"},
            "v_smg1_sheet": {"vmt": "c_smg1/materials/materials/models/weapons/v_smg1/v_smg1_sheet.vmt",
                             "base": "c_smg1/materials/materials/models/weapons/v_smg1/v_smg1_sheet.vtf",
                             "bump": "c_smg1/materials/materials/models/weapons/v_smg1/smg1_normal.vtf"},
            "texture4": {"vmt": "c_smg1/materials/materials/models/weapons/v_smg1/texture4.vmt",
                         "base": "c_smg1/materials/materials/models/weapons/v_smg2/texture4.vtf"}},
        "muzzle": "muzzle",
    },
}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    root, repo = Path(a.root), Path(a.repo)
    for key, w in WEAPONS.items():
        pkt = json.loads(subprocess.run(["git", "-C", str(repo), "show",
                                         f"HEAD:build/prepared/{w['packet']}"], capture_output=True, text=True).stdout)
        want = {k.lower(): v.upper() for k, v in pkt["verified_inputs"].items()}
        if key == "c":
            want["texture4.vtf"] = want.get("v_smg2_texture4.vtf")
        inputs, pinned, mismatch = {}, [], []

        def add(k, rel):
            p = f"{PKG}/models__weapons__{rel}"
            h = H(root / p)
            nm = Path(rel).name.lower()
            exp = want.get(nm)
            if exp is None:
                pinned.append(k)
            elif exp != h:
                mismatch.append((k, nm, exp, h))
            inputs[k] = {"path": p, "sha256": h}
        add("w_ref_smd", w["world"]["smd"]); add("w_phy_smd", w["world"]["phy"]); add("w_qc", w["world"]["qc"]); add("w_mdl", w["world"]["mdl"])
        add("c_ref_smd", w["view"]["smd"]); add("c_qc", w["view"]["qc"]); add("c_mdl", w["view"]["mdl"])
        mats = {}
        for m, spec in w["materials"].items():
            mats[m] = {}
            for role, rel in spec.items():
                k = f"{role}_{m}"; add(k, rel); mats[m][role] = k
        if mismatch:
            raise SystemExit(f"O08{key} packet hash mismatch: {mismatch}")
        qc = (root / inputs["w_qc"]["path"]).read_text(encoding="utf-8", errors="ignore")
        mass = float((re.search(r"\$mass\s+([\d.]+)", qc) or [None, "2"])[1])
        n = w["name"]
        job = {"job": w["job"], **COMMON,
               "grip_reference": w["grip"],
               "world": {"nif_name": f"w_{n}", "output": f"meshes/rem/gmod/weapons/{n}/w_{n}.nif",
                         "hand_bone": "ValveBiped.Bip01_R_Hand", "havok_material": w["world"]["havok"],
                         "havok_material_note": w["world"]["havok_note"], "mass": mass, "bsx": 67},
               "view": {"nif_name": f"c_{n}", "output": f"meshes/rem/gmod/weapons/{n}/c_{n}.nif",
                        "bone": w["view"]["bone"], "mode": w["view"]["mode"], "bsx": 65},
               "materials": mats,
               "flat_normal": f"{n}_flat_n.dds",
               "report_name": f"o08{key}_conversion_report.json",
               "inputs": inputs,
               "pinned_inputs": pinned,
               "pinned_inputs_note": "Not in the 2026-10-07 packet hash list (decompiled/derived files); hashes pinned at first O08 use.",
               "output": {"texture_dir": f"textures/rem/gmod/weapons/{n}"}}
        job["view"]["icp_cell"] = 2.0  # wider correspondence search for different c_/w_ meshes
        for k in ("max_median", "fixed_scale", "scale_range"):
            if k in w["view"]:
                job["view"][k] = w["view"][k]
        if w["muzzle"]:
            job["world"]["muzzle_attachment"] = {"qc": "w_qc", "name": w["muzzle"]}
        out = repo / "research/source_to_fnv/jobs" / f"o08{key}_{n}.json"
        out.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
        print(f"O08{key}: {out.name} inputs={len(inputs)} packet-verified={len(inputs) - len(pinned)} pinned={pinned} mass={mass}")


if __name__ == "__main__":
    main()
