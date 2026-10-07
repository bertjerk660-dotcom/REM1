#!/usr/bin/env python3
"""Synthetic extractor safety checks. Every fixture byte is project-authored.

Run: python research/test_gmod_dependency_inventory.py
No game installation, native-code analysis, deployment, or network is required.
"""
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zlib

SCRIPT = Path(__file__).with_name("gmod_dependency_inventory.py")
spec = importlib.util.spec_from_file_location("gmod_inventory", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def main():
    with tempfile.TemporaryDirectory(prefix="gmod_inventory_test_") as temporary:
        root = Path(temporary)
        game = root / "game"
        gmod = game / "garrysmod"
        project = root / "project"
        out = project / "build/prepared/gmod_dependency_20261007"
        (gmod / "lua/includes/modules").mkdir(parents=True)
        (gmod / "lua/vgui").mkdir(parents=True)
        source = b'vgui.Create("DPanel")\nMaterial("fixture/mat")\nMaterial("priority/mat")\nsurface.CreateFont("ToolFont", {font="Verified Fixture Family", size=12})\nsurface.CreateFont("HostFont", {font="Absent Fixture System Font", size=12})\n'
        (gmod / "lua/includes/modules/spawnmenu.lua").write_bytes(source)
        (gmod / "lua/vgui/dpanel.lua").write_text('vgui.Register("DPanel", PANEL, "Panel")\n')
        (gmod / "resource/fonts").mkdir(parents=True)
        font_name = "Verified Fixture Family".encode("utf-16-be")
        name_table = struct.pack(">3H", 0, 1, 18) + struct.pack(">6H", 3, 1, 0x409, 1, len(font_name), 0) + font_name
        sfnt = struct.pack(">I4H", 0x10000, 1, 16, 0, 0) + struct.pack(">4sIII", b"name", 0, 28, len(name_table)) + name_table
        (gmod / "resource/fonts/unrelated-filename.ttf").write_bytes(sfnt)
        reuse = project / "build/gmod_spawnmenu_original/lua/includes/modules/spawnmenu.lua"
        reuse.parent.mkdir(parents=True)
        reuse.write_bytes(source)
        material = b'// Original shader fixture\n"UnlitGeneric"\n{\n"$basetexture" "fixture/tex"\n}\n'
        texture = b"VTF_fixture_bytes_no_conversion"

        def entry(data, preload, index, offset):
            return struct.pack("<IHHIIH", zlib.crc32(data) & 0xffffffff, preload, index, offset, len(data) - preload, 0xffff) + data[:preload]

        tree = b"vmt\0materials/fixture\0mat\0" + entry(material, 8, 0, 0) + b"\0\0"
        tree += b"vtf\0materials/fixture\0tex\0" + entry(texture, 4, 0x7fff, 0) + b"\0\0\0"
        header = struct.pack("<7I", 0x55aa1234, 2, len(tree), len(texture) - 4, 0, 0, 0)
        (gmod / "garrysmod_dir.vpk").write_bytes(header + tree + texture[4:])
        (gmod / "garrysmod_000.vpk").write_bytes(material[8:])
        (game / "sourceengine").mkdir()
        declared = b'"UnlitGeneric" { "$color" "[1 1 1]" }'
        optional = b'"UnlitGeneric" { "$color" "[0 0 0]" }'
        for name, content in (("hl2_misc_dir.vpk", declared), ("content_cstrike_dir.vpk", optional)):
            candidate_tree = b"vmt\0materials/priority\0mat\0" + entry(content, 0, 0x7fff, 0) + b"\0\0\0"
            candidate_header = struct.pack("<7I", 0x55aa1234, 2, len(candidate_tree), len(content), 0, 0, 0)
            (game / "sourceengine" / name).write_bytes(candidate_header + candidate_tree + content)
        (gmod / "addons").mkdir()
        addon = b"GMAD" + bytes([3]) + struct.pack("<QQ", 42, 123) + b"\0fixture\0description\0author\0" + struct.pack("<I", 1)
        addon += struct.pack("<I", 1) + b"lua/autorun/fixture.lua\0" + struct.pack("<QI", 5, zlib.crc32(b"hello") & 0xffffffff) + struct.pack("<I", 0) + b"hello"
        (gmod / "addons/fixture.gma").write_bytes(addon)
        args = [sys.executable, str(SCRIPT), "--game-root", str(game), "--project-root", str(project), "--output", str(out), "--stage"]
        first = subprocess.run(args, capture_output=True, text=True)
        assert first.returncode == 0, first.stderr
        provenance = json.loads((out / "asset_provenance.json").read_text())["entries"]
        indexed = {e["internal_path"]: e for e in provenance}
        assert indexed["lua/includes/modules/spawnmenu.lua"]["status"] == "reused_verified_original"
        for internal, original in [("materials/fixture/mat.vmt", material), ("materials/fixture/tex.vtf", texture)]:
            item = indexed[internal]
            assert item["crc32_validated"] is True
            assert item["sha256_match"] is True
            assert Path(item["destination_path"]).read_bytes() == original
        assert indexed["materials/fixture/mat.vmt"]["material_shader"] == "UnlitGeneric"
        priority = indexed["materials/priority/mat.vmt"]
        assert Path(priority["archive_path"]).name == "hl2_misc_dir.vpk"
        assert Path(priority["destination_path"]).read_bytes() == declared
        assert priority["archive_candidates"] == 2
        font = indexed["resource/fonts/unrelated-filename.ttf"]
        assert Path(font["destination_path"]).read_bytes() == sfnt
        requirements = json.loads((out / "font_requirements.json").read_text())["entries"]
        assert next(e for e in requirements if e["font_identity"] == "ToolFont")["status"] == "original_game_font_family_resolved"
        host_font = next(e for e in requirements if e["font_identity"] == "HostFont")
        assert host_font["status"] == "host_font_interface_requirement_unresolved_in_game_files"
        assert not host_font["original_font_candidates"]
        addon_record = json.loads((out / "addon_archive_inventory.json").read_text())["archives"][0]
        assert addon_record["entry_count"] == 1 and addon_record["entries"][0]["size"] == 5
        assert not (out / "original_payload/lua/autorun/fixture.lua").exists()
        second = subprocess.run(args, capture_output=True, text=True)
        assert second.returncode == 0, second.stderr
        (out / "original_payload/materials/fixture/tex.vtf").write_bytes(b"changed")
        third = subprocess.run(args, capture_output=True, text=True)
        assert third.returncode != 0
        assert "Refusing overwrite of different staged original" in third.stderr
        archive = module.VPK(gmod / "garrysmod_dir.vpk")
        (gmod / "garrysmod_000.vpk").write_bytes(b"corrupt" + material[15:])
        try:
            archive.payload(archive.entries["materials/fixture/mat.vmt"])
        except ValueError as error:
            assert "CRC mismatch" in str(error)
        else:
            raise AssertionError("Corrupted source was accepted")
        try:
            module.safe_internal("../../outside.txt")
        except ValueError:
            pass
        else:
            raise AssertionError("Traversal path was accepted")
        print("PASS: VPK inline/external preload+body CRC; VMT/VTF closure; declared sourceengine HL2 priority; SFNT family mapping independent of filenames; absent host fonts retained as requirements; exact prior reuse; GMAD directory-only indexing; repeat run; changed destination/corrupt-source/traversal refusal")


if __name__ == "__main__":
    main()
