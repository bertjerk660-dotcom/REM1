#!/usr/bin/env python3
"""Inventory installed GMOD and stage a bounded original dependency closure locally.

This tool does not convert assets, disassemble binaries, deploy, or modify runtime
sources. Outputs containing original payloads must stay outside Git. VPK data is
reconstructed from preload + body and checked against the directory-entry CRC.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import sys
import zlib

VERSION = "gmod-dependency-inventory-20261007.7"
EXT_TYPES = {
    ".exe": "executable_module", ".dll": "native_module", ".so": "native_module",
    ".dylib": "native_module", ".lua": "lua", ".vpk": "vpk_archive",
    ".gma": "addon_archive", ".mdl": "model", ".vvd": "model_vertex_data",
    ".vtx": "model_index_data", ".phy": "model_physics_data", ".vtf": "texture",
    ".vmt": "material", ".png": "icon_or_image", ".jpg": "image", ".tga": "image",
    ".wav": "sound", ".mp3": "sound", ".ogg": "sound", ".ttf": "font",
    ".otf": "font", ".fnt": "font", ".res": "resource", ".cfg": "configuration",
    ".vsf": "shader", ".vcs": "shader", ".txt": "script_or_resource",
}

def classify(path):
    low = path.replace("\\", "/").lower()
    kind = EXT_TYPES.get(PurePosixPath(low).suffix, "other")
    if "/autorun/" in low and kind == "lua": return "lua_autorun"
    if "/stools/" in low and kind == "lua": return "lua_tool"
    if "/weapons/" in low and kind == "lua": return "lua_weapon"
    if "/spawnmenu/" in low and kind == "lua": return "lua_spawnmenu"
    if "/contextmenu/" in low and kind == "lua": return "lua_contextmenu"
    if "/vgui/" in low and kind == "lua": return "lua_vgui"
    if "/derma/" in low and kind == "lua": return "lua_derma"
    if "spawnlists/" in low: return "spawnlist"
    if "scripts/" in low and kind == "script_or_resource": return "script_definition"
    return kind

def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(4 * 1024 * 1024), b""): h.update(block)
    return h.hexdigest().upper()

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def safe_internal(value):
    value = value.replace("\\", "/").strip("/")
    parts = PurePosixPath(value).parts
    if not parts or ".." in parts or ":" in value:
        raise ValueError("Unsafe internal archive/source path: " + value)
    return value

class VPK:
    def __init__(self, path):
        self.path = Path(path)
        self.sha256 = sha(self.path)
        self.entries = {}
        with self.path.open("rb") as f:
            magic, version, tree_size = struct.unpack("<III", f.read(12))
            if magic != 0x55AA1234 or version not in (1, 2):
                raise ValueError("unsupported VPK header")
            self.version = version
            if version == 2: f.read(16)
            self.header_size = 28 if version == 2 else 12
            self.tree_end = self.header_size + tree_size
            def string():
                value = bytearray()
                while True:
                    c = f.read(1)
                    if not c: raise EOFError("VPK string ended unexpectedly")
                    if c == b"\0": return value.decode("utf-8", "replace")
                    value.extend(c)
            while True:
                ext = string()
                if not ext: break
                while True:
                    folder = string()
                    if not folder: break
                    while True:
                        name = string()
                        if not name: break
                        crc, preload, index, offset, size, terminator = struct.unpack("<IHHIIH", f.read(18))
                        if terminator != 0xFFFF: raise ValueError("bad VPK entry terminator")
                        internal = safe_internal(("" if folder == " " else folder + "/") + name + ("" if ext == " " else "." + ext))
                        self.entries[internal.lower()] = {
                            "internal_path": internal, "crc32": f"{crc:08X}",
                            "preload_bytes": preload, "archive_index": index,
                            "archive_offset": offset, "body_bytes": size,
                            "size": preload + size, "preload_offset": f.tell(),
                        }
                        f.seek(preload, 1)

    def payload(self, entry):
        with self.path.open("rb") as f:
            f.seek(entry["preload_offset"])
            preload = f.read(entry["preload_bytes"])
        if entry["archive_index"] == 0x7FFF:
            chunk = self.path
            position = self.tree_end + entry["archive_offset"]
        else:
            chunk = self.path.with_name(self.path.name[:-8] + f"_{entry['archive_index']:03d}.vpk")
            position = entry["archive_offset"]
        with chunk.open("rb") as f:
            f.seek(position)
            body = f.read(entry["body_bytes"])
        result = preload + body
        if len(result) != entry["size"]: raise ValueError("short VPK payload")
        if f"{zlib.crc32(result) & 0xFFFFFFFF:08X}" != entry["crc32"]:
            raise ValueError("VPK payload CRC mismatch")
        return result, chunk

def iter_strings(obj):
    if isinstance(obj, dict):
        for value in obj.values(): yield from iter_strings(value)
    elif isinstance(obj, list):
        for value in obj: yield from iter_strings(value)
    elif isinstance(obj, str): yield obj

def keyvalues_blocks(text):
    """Read sound-script top-level blocks without evaluating script expressions."""
    tokens = re.findall(r'"((?:\\.|[^"\\])*)"|([{}])|([^\s{}"]+)', re.sub(r'//[^\n]*', '', text))
    values = [a if a else b if b else c for a, b, c in tokens]
    i = 0
    while i + 1 < len(values):
        name = values[i]
        if values[i + 1] != '{': i += 1; continue
        start = i + 2; depth = 1; i = start
        while i < len(values) and depth:
            if values[i] == '{': depth += 1
            elif values[i] == '}': depth -= 1
            i += 1
        body = values[start:i - 1]
        waves = [body[n + 1] for n in range(len(body) - 1) if body[n].lower() == 'wave']
        yield name, waves

def gma_directory(path):
    """Read the GMAD file directory, without extracting addon content."""
    with path.open("rb") as f:
        if f.read(4) != b"GMAD": raise ValueError("not a GMAD addon")
        version = f.read(1)[0]
        steam_id, timestamp = struct.unpack("<QQ", f.read(16))
        def string():
            value = bytearray()
            while True:
                c = f.read(1)
                if not c: raise EOFError("short GMAD string")
                if c == b"\0": return value.decode("utf-8", "replace")
                value.extend(c)
        required = []
        if version > 1:
            while True:
                value = string()
                if not value: break
                required.append(value)
        name, description, author = string(), string(), string()
        addon_version = struct.unpack("<I", f.read(4))[0]
        entries = []
        while True:
            number = struct.unpack("<I", f.read(4))[0]
            if number == 0: break
            internal = safe_internal(string())
            size, crc = struct.unpack("<QI", f.read(12))
            entries.append({"number": number, "internal_path": internal, "size": size, "crc32": f"{crc:08X}", "type": classify(internal)})
        directory_end = f.tell()
        f.seek(0)
        header_sha = hashlib.sha256(f.read(directory_end)).hexdigest().upper()
        offset = directory_end
        for entry in entries:
            entry["archive_offset"] = offset
            offset += entry["size"]
        return {"archive_path": str(path), "directory_sha256": header_sha,
                "version": version, "steam_id": str(steam_id), "timestamp": timestamp,
                "name": name, "author": author, "addon_version": addon_version,
                "required_content": required, "size": path.stat().st_size,
                "entry_count": len(entries), "entries": entries,
                "mount_status": "not_proven_active", "payloads_extracted": False}

def sfnt_names(path):
    """Read original SFNT name records; never infer a font family from filenames."""
    content = path.read_bytes()
    if content[:4] not in (b"\x00\x01\x00\x00", b"OTTO", b"true"):
        raise ValueError("unsupported SFNT signature")
    count = struct.unpack_from(">H", content, 4)[0]
    name_offset = None
    for n in range(count):
        tag, checksum, offset, size = struct.unpack_from(">4sIII", content, 12 + n * 16)
        if tag == b"name":
            if offset + size > len(content): raise ValueError("SFNT name table outside file")
            name_offset = offset
            break
    if name_offset is None: return []
    format_id, records, string_base = struct.unpack_from(">HHH", content, name_offset)
    names = []
    for n in range(records):
        platform, encoding, language, name_id, size, offset = struct.unpack_from(">6H", content, name_offset + 6 + n * 12)
        if name_id not in (1, 2, 4, 6, 16, 17): continue
        start = name_offset + string_base + offset
        if start + size > len(content): raise ValueError("SFNT name record outside file")
        raw = content[start:start + size]
        value = raw.decode("utf-16-be" if platform in (0, 3) else "mac_roman", "replace").strip()
        record = {"platform_id": platform, "encoding_id": encoding, "language_id": language,
                  "name_id": name_id, "value": value}
        if value and record not in names: names.append(record)
    return names

def subsystem(path):
    low = path.lower()
    if "gmod_tool" in low or "toolgun" in low or "tool_tracer" in low or "tooltracer" in low: return "toolgun"
    if "phys" in low or "halo" in low: return "physgun"
    if "notification" in low or "notices/" in low or "cl_notice" in low: return "notifications"
    if "deathnotice" in low or "killicon" in low: return "death_notices"
    if "spawnicon" in low or "dmodelpanel" in low: return "prop_icons"
    if "spawnmenu" in low or "spawnlists" in low: return "qmenu"
    if "contextmenu" in low: return "context_menu"
    if "/vgui/" in low or "/derma/" in low or "/skins/" in low: return "vgui_derma"
    if "cfg/" in low or "gameinfo" in low: return "input_filesystem"
    return "shared_overlay_dependency"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--seeds", help="additional JSON seed paths or entries[]")
    parser.add_argument("--stage", action="store_true", help="stage selected exact originals locally")
    args = parser.parse_args()
    game, project, out = map(lambda x: Path(x).resolve(), (args.game_root, args.project_root, args.output))
    if out == game or game in out.parents: raise SystemExit("output must not be inside installation")
    if not (game / "garrysmod").is_dir(): raise SystemExit("supplied garrysmod directory missing")
    out.mkdir(parents=True, exist_ok=True)
    errors, inventory, archives, addon_archives = [], [], [], []
    counts = collections.Counter()
    native_modules, configurations, fonts, packages = [], [], [], []
    print("Inventory started", flush=True)
    with (out / "installation_inventory.jsonl").open("w", encoding="utf-8") as index:
        for parent, dirs, files in os.walk(game, onerror=lambda e: errors.append(str(e))):
            dirs.sort(); files.sort()
            for name in files:
                p = Path(parent) / name
                rel = p.relative_to(game).as_posix()
                try:
                    st = p.stat()
                    record = {"source_absolute_path": str(p), "installation_relative_path": rel,
                              "size": st.st_size, "mtime_ns": st.st_mtime_ns, "type": classify(rel)}
                    counts[record["type"]] += 1
                    # Payload hashing of every texture/model is deliberately deferred to closure.
                    important = p.suffix.lower() in (".exe", ".dll", ".so", ".dylib", ".ttf", ".otf", ".fnt", ".cfg") or name.endswith("_dir.vpk") or name.lower() in ("gameinfo.txt", "steam.inf", "garrysmod.ver")
                    if important: record["sha256"] = sha(p)
                    index.write(json.dumps(record, ensure_ascii=False) + "\n")
                    inventory.append(record)
                    if record["type"] in ("native_module", "executable_module"): native_modules.append(record)
                    if record["type"] == "configuration" or name.lower() in ("gameinfo.txt", "steam.inf", "garrysmod.ver"): configurations.append(record)
                    if record["type"] == "font": fonts.append(record)
                    if record["type"] in ("vpk_archive", "addon_archive"): packages.append(record)
                    if name.endswith("_dir.vpk"):
                        try: archives.append(VPK(p))
                        except Exception as exc: errors.append(str(p) + ": " + str(exc))
                    if p.suffix.lower() == ".gma":
                        try: addon_archives.append(gma_directory(p))
                        except Exception as exc: errors.append(str(p) + ": " + str(exc))
                except OSError as exc: errors.append(str(p) + ": " + str(exc))
    print(f"Loose inventory: {len(inventory)} files; VPKs: {len(archives)}", flush=True)
    dump(out / "native_modules.json", {"modules": native_modules, "note": "Identity/hash only; no non-IDA disassembly performed."})
    dump(out / "configuration_inventory.json", {"entries": configurations})
    font_families = collections.defaultdict(list)
    for record in fonts:
        p = Path(record["source_absolute_path"])
        try:
            record["sfnt_name_records"] = sfnt_names(p)
            record["family_names"] = sorted(set(n["value"] for n in record["sfnt_name_records"] if n["name_id"] in (1, 16)))
            virtual = None
            for root in (game / "garrysmod", game / "sourceengine", game / "hl2", game / "platform"):
                try: virtual = p.relative_to(root).as_posix(); break
                except ValueError: pass
            if virtual and virtual.startswith("resource/"):
                for family in record["family_names"]:
                    font_families[family.casefold()].append({"family_name": family, "internal_path": virtual,
                         "source_absolute_path": str(p), "sha256": record["sha256"], "name_table_evidence": "SFNT name IDs 1/16"})
        except (ValueError, struct.error) as exc:
            record["sfnt_names_status"] = "unresolved: " + str(exc)
    dump(out / "font_inventory.json", {"entries": fonts, "family_mapping_method": "Original SFNT name table IDs 1/16; filenames never establish family aliases"})
    dump(out / "package_inventory.json", {"entries": packages})
    dump(out / "addon_archive_inventory.json", {"archives": addon_archives})
    archive_index = collections.defaultdict(list)
    for archive in archives:
        with (out / (archive.path.parent.name + "_" + archive.path.name + ".index.jsonl")).open("w", encoding="utf-8") as f:
            for low, entry in archive.entries.items():
                archive_index[low].append((archive, entry))
                f.write(json.dumps({"archive_path": str(archive.path), "archive_sha256": archive.sha256, "type": classify(entry["internal_path"]), **entry}) + "\n")
    roots = [game / "garrysmod", game / "sourceengine", game / "hl2", game / "platform", game]
    available_paths = set(archive_index)
    for record in inventory:
        file = Path(record["source_absolute_path"])
        for root in roots[:-1]:
            try: available_paths.add(file.relative_to(root).as_posix())
            except ValueError: pass
    def package_priority(archive):
        parent, name = archive.path.parent.name.lower(), archive.path.name.lower()
        if parent == "garrysmod" and name == "garrysmod_dir.vpk": return 0
        if parent in ("hl2", "sourceengine") and name.startswith("hl2_"): return 1
        if parent == "platform": return 2
        if "fallback" in name: return 4
        return 3
    def resolve(path):
        path = safe_internal(path)
        if path.startswith("sandbox/") or path.startswith("base/"):
            path = "gamemodes/" + path
        for root in roots:
            candidate = root / Path(path)
            if candidate.is_file(): return {"kind": "loose", "file": candidate, "path": path}
        options = archive_index.get(path.lower(), [])
        if not options: return None
        # Explicit installation package priority; runtime dynamic mounts remain unresolved.
        options = sorted(options, key=lambda a: (package_priority(a[0]), str(a[0].path)))
        archive, entry = options[0]
        return {"kind": "vpk", "archive": archive, "entry": entry, "path": entry["internal_path"], "candidates": len(options)}
    def data(source):
        if source["kind"] == "loose": return source["file"].read_bytes(), None
        return source["archive"].payload(source["entry"])

    prior_paths = [
        project / "build/prepared/gmod_qmenu_source_inventory/manifest.json",
        project / "build/prepared/gmod_tool_physgun_assets/manifest.json",
        project / "build/prepared/gmod_tool_physgun_asset_handoff/manifest.json",
    ]
    prior_audit, seeds, registry_patterns = [], {}, []
    def add(path, reason, owner=None):
        try: path = safe_internal(path)
        except ValueError: return
        if path.startswith("sandbox/") or path.startswith("base/"): path = "gamemodes/" + path
        if "*" in path or "?" in path:
            matched = sorted(candidate for candidate in available_paths if fnmatch.fnmatchcase(candidate.lower(), path.lower()))
            registry_patterns.append({"pattern": path, "matched_count": len(matched), "reason": reason})
            for candidate in matched: add(candidate, "Exact original path expanded from directory registry " + path, owner)
            return
        if path not in seeds: seeds[path] = {"reason": reason, "subsystem": owner or subsystem(path)}
    for p in prior_paths:
        if not p.is_file():
            prior_audit.append({"path": str(p), "status": "absent"}); continue
        try:
            obj = json.loads(p.read_text(encoding="utf-8-sig"))
            prior_audit.append({"path": str(p), "sha256": sha(p), "status": "read_metadata_not_assumed_payload"})
            for value in iter_strings(obj):
                low = value.replace("\\", "/").lower()
                if low.startswith(("lua/", "gamemodes/", "materials/", "models/", "sound/", "scripts/", "resource/", "settings/")) and " " not in low and len(low) < 220:
                    if PurePosixPath(low).suffix in EXT_TYPES: add(value, "Existing subsystem manifest; re-resolve exact installed source")
        except Exception as exc: errors.append(str(p) + ": " + str(exc))
    explicit = [
        "gamemodes/sandbox/gamemode/cl_spawnmenu.lua", "gamemodes/sandbox/gamemode/cl_init.lua",
        "gamemodes/sandbox/gamemode/cl_contextmenu.lua", "gamemodes/sandbox/gamemode/cl_hints.lua",
        "gamemodes/sandbox/gamemode/cl_notice.lua", "gamemodes/base/gamemode/cl_deathnotice.lua",
        "lua/includes/modules/spawnmenu.lua", "lua/includes/modules/notification.lua",
        "lua/includes/modules/killicon.lua", "lua/includes/modules/halo.lua", "lua/includes/modules/duplicator.lua",
        "lua/derma/init.lua", "lua/vgui/vgui.lua", "lua/skins/default.lua",
        "scripts/gmod_sounds.txt", "resource/ClientScheme.res", "gameinfo.txt",
        "resource/HALFLIFE2.ttf", "resource/HL2MP.ttf", "resource/HL2crosshairs.ttf",
        "cfg/config_default.cfg", "cfg/mount.cfg", "cfg/userconfig.cfg",
        "materials/gui/tool.png", "sound/ui/buttonclickrelease.wav",
        "models/weapons/c_toolgun.mdl", "models/weapons/w_toolgun.mdl", "models/weapons/w_physics.mdl",
        "models/weapons/v_physics.mdl", "models/weapons/v_physics.vvd", "models/weapons/v_physics.dx90.vtx",
        "materials/cable/physbeam.vmt", "materials/sprites/physbeam.vmt",
        "lua/effects/ToolTracer/init.lua", "lua/effects/selection_indicator/init.lua",
        "gamemodes/sandbox/entities/effects/selection_indicator.lua",
        "gamemodes/sandbox/entities/effects/selection_ring.lua",
        "gamemodes/sandbox/entities/effects/entity_remove.lua",
        "materials/effects/select_dot.vmt", "materials/effects/select_ring.vmt", "materials/effects/spark.vmt",
    ]
    for path in explicit: add(path, "Investigation seed; exact path verified only if present in supplied installation")
    for leaf in ("init.lua", "shared.lua", "cl_init.lua", "stool.lua", "stool_cl.lua", "object.lua", "ghostentity.lua", "cl_viewscreen.lua"):
        add("gamemodes/sandbox/entities/weapons/gmod_tool/" + leaf, "Original Tool Gun SWEP/tool registry boundary", "toolgun")
    for leaf in ("generic", "error", "undo", "hint", "cleanup"):
        add("materials/vgui/notices/" + leaf + ".vmt", "Original notification image dependency", "notifications")
    for n in range(1, 5): add(f"sound/ambient/water/drip{n}.wav", "Original Sandbox hint feedback audio", "notifications")
    for path in ("materials/sprites/physcannon_bluelight2.vmt", "materials/sprites/glow04_noz.vmt"):
        add(path, "Prior native evidence asset candidate; shared Gravity Gun provenance possible, Physgun renderer ownership unproven", "physgun_candidate_shared")
        seeds[path]["ownership_confidence"] = "candidate_shared_gravitygun_unproven_physgun"
    # These subtrees are registries explicitly loaded by sandbox/Derma initialization.
    dynamic_prefixes = ("gamemodes/sandbox/gamemode/spawnmenu/", "gamemodes/sandbox/gamemode/contextmenu/", "gamemodes/sandbox/entities/weapons/gmod_tool/stools/", "settings/spawnlists/")
    for root in roots[:1]:
        for prefix in dynamic_prefixes:
            folder = root / prefix
            if folder.is_dir():
                for p in sorted(folder.rglob("*")):
                    if p.is_file(): add(p.relative_to(root).as_posix(), "Source loader directory registry", subsystem(prefix))
    for low, options in archive_index.items():
        if low.startswith(dynamic_prefixes): add(options[0][1]["internal_path"], "Original archived directory registry")
    if args.seeds:
        obj = json.loads(Path(args.seeds).read_text(encoding="utf-8-sig"))
        for value in iter_strings(obj):
            if isinstance(value, str) and value.startswith(("lua/", "gamemodes/", "materials/", "models/", "sound/", "scripts/", "resource/", "settings/", "cfg/")): add(value, "Trace-agent explicit seed")

    # Register/DefineControl lookup identifies actual original classes and bases.
    panel_sources = {}
    for p in (game / "garrysmod/lua").rglob("*.lua"):
        try: text = p.read_text(encoding="utf-8-sig", errors="replace")
        except OSError: continue
        for match in re.finditer(r'(?:vgui\.Register|derma\.DefineControl)\s*\(\s*["\']([^"\']+)["\']', text):
            panel_sources[match.group(1)] = p.relative_to(game / "garrysmod").as_posix()
    hook_pattern = r'\b(?:DrawPhysgunBeam|PhysgunPickup|PhysgunDrop|PhysgunFreeze|OnPhysgunFreeze|PhysgunReload|PreDrawHalos|halo\.Add)\b'
    for folder in (game / "garrysmod/lua", game / "garrysmod/gamemodes"):
        if folder.is_dir():
            for p in sorted(folder.rglob("*.lua")):
                try: text = p.read_text(encoding="utf-8-sig", errors="replace")
                except OSError: continue
                hooks = sorted(set(re.findall(hook_pattern, text)))
                if hooks: add(p.relative_to(game / "garrysmod").as_posix(), "Original source hook references: " + ", ".join(hooks), "physgun")

    # Index original named sound events; only referenced event definitions/waves
    # enter staging. Indexing does not imply all mounted games are active.
    sound_events = collections.defaultdict(list)
    sound_scripts = set()
    for root in roots[:-1]:
        folder = root / "scripts"
        if folder.is_dir():
            for p in folder.rglob("*.txt"):
                if "sound" in p.name.lower(): sound_scripts.add(p.relative_to(root).as_posix())
    for low, options in archive_index.items():
        if low.startswith("scripts/") and low.endswith(".txt") and "sound" in low: sound_scripts.add(options[0][1]["internal_path"])
    for path in sorted(sound_scripts):
        try:
            source = resolve(path)
            if not source: continue
            content, unused_chunk = data(source)
            for name, waves in keyvalues_blocks(content.decode("utf-8-sig", "replace")):
                if waves: sound_events[name.lower()].append({"event": name, "script": path, "waves": waves})
        except Exception as exc: errors.append("Sound-definition metadata " + path + ": " + str(exc))
    native_sound_evidence = []
    for event in ("Toolgun.Single", "Weapon_Physgun.On", "Weapon_Physgun.Off", "Weapon_Physgun.Special1"):
        definitions = sound_events.get(event.lower(), [])
        native_sound_evidence.append({"event": event, "definitions": definitions, "behavior_inference": "none; event name does not establish held-beam loop semantics"})
        for definition in definitions:
            add(definition["script"], "Original native/script named sound-event definition: " + event, "toolgun" if event.startswith("Toolgun") else "physgun")
            for wave in definition["waves"]:
                wave = wave.lstrip("*!#@<>^)}")
                add(wave if wave.startswith("sound/") else "sound/" + wave, "Original wave declared by exact event " + event, "toolgun" if event.startswith("Toolgun") else "physgun")

    reuse_roots = [project / "build/gmod_spawnmenu_original", project / "build/prepared/pre_opus_20261006/source_payload", project / "build/prepared/gmod_hl_weapon_models/packages", out / "original_payload", out / "original_payload_by_package"]
    existing = collections.defaultdict(list)
    for folder in reuse_roots:
        if folder.is_dir():
            for p in folder.rglob("*"):
                if p.is_file() and p.suffix.lower() in EXT_TYPES:
                    existing[p.stat().st_size].append(p)
    existing_hash = {}
    prior_stage_entries = {}
    prior_stage_manifest = out / "asset_provenance.json"
    if prior_stage_manifest.is_file():
        try:
            prior_stage_entries = {e["internal_path"].lower(): e for e in json.loads(prior_stage_manifest.read_text(encoding="utf-8-sig"))["entries"]}
        except (ValueError, KeyError, TypeError) as exc:
            raise SystemExit("Refusing to use unreadable existing provenance: " + str(exc))
    entries, unresolved, font_requirements, queue = [], [], [], collections.deque(seeds)
    visited = set()
    selected_chunks = {}
    while queue:
        path = queue.popleft()
        if path.lower() in visited: continue
        visited.add(path.lower())
        info = seeds[path]
        source = resolve(path)
        base = {"internal_path": path, "type": classify(path), "subsystem": info["subsystem"],
                "reason": info["reason"], "dependencies": [], "commit_safe": False,
                "proprietary": True, "payload_location_policy": "local_only", "closure_status": "incomplete_native_and_dynamic_boundaries"}
        if "ownership_confidence" in info: base["ownership_confidence"] = info["ownership_confidence"]
        if source is None:
            status = "unverified_seed_source_absent" if info["reason"].startswith("Investigation seed") else "unresolved_source_absent"
            base.update({"source_path": str(game / "garrysmod" / path), "destination_path": None, "sha256": None, "status": status})
            entries.append(base); unresolved.append({"path": path, "reason": "Absent loose and indexed supplied installation VPKs; no substitute"}); continue
        try: content, chunk = data(source)
        except Exception as exc:
            base.update({"source_path": str(source.get("file", source.get("archive").path if source.get("archive") else "")), "status": "unresolved_read_error", "sha256": None, "destination_path": None, "error": str(exc)})
            entries.append(base); errors.append(path + ": " + str(exc)); continue
        digest = hashlib.sha256(content).hexdigest().upper()
        base.update({"source_path": str(source["file"] if source["kind"] == "loose" else source["archive"].path),
                     "source_kind": source["kind"], "sha256": digest, "size": len(content)})
        if source["kind"] == "vpk":
            archive = source["archive"]
            base.update({"archive_path": str(archive.path), "archive_sha256": archive.sha256,
                         "archive_version": archive.version, **source["entry"], "archive_candidates": source["candidates"],
                         "archive_body_path": str(chunk), "crc32_validated": True,
                         "resolution_note": "explicit garrysmod_dir > declared hl2_* > platform > optional content > fallback; supplied loose file chosen first; runtime mount priority not proven"})
            selected_chunks[str(chunk)] = chunk
        dependencies = []
        def dep(value, why):
            if value.startswith("sandbox/") or value.startswith("base/"): value = "gamemodes/" + value
            if "*" in value or "?" in value:
                matched = sorted(candidate for candidate in available_paths if fnmatch.fnmatchcase(candidate.lower(), value.lower()))
                base.setdefault("dynamic_registry_patterns", []).append({"pattern": value, "matched_count": len(matched)})
                for candidate in matched: dep(candidate, why + " expanded from " + value)
                return
            if value not in dependencies: dependencies.append(value)
            if value not in seeds:
                before = set(seeds)
                add(value, why, base["subsystem"])
                for added in sorted(seeds.keys() - before): queue.append(added)
        low = path.lower()
        text = content.decode("utf-8-sig", "replace") if PurePosixPath(low).suffix in (".lua", ".vmt", ".txt", ".res", ".cfg") else ""
        if low.endswith(".lua"):
            requested_families = []
            for call in re.finditer(r'surface\.CreateFont\s*\(\s*["\']([^"\']+)["\']\s*,\s*\{(.*?)\}\s*\)', text, re.S):
                identity, descriptor = call.groups()
                match = re.search(r'\bfont\s*=\s*["\']([^"\']+)["\']', descriptor)
                if not match: continue
                family = match.group(1)
                requested_families.append(family)
                candidates = font_families.get(family.casefold(), [])
                requirement = {"lua_source": path, "font_identity": identity, "requested_family": family,
                    "original_font_candidates": candidates, "mapping_basis": "exact literal family matches original SFNT name-table family IDs 1/16",
                    "status": "original_game_font_family_resolved" if candidates else "host_font_interface_requirement_unresolved_in_game_files"}
                font_requirements.append(requirement)
                for candidate in candidates:
                    dep(candidate["internal_path"], "Original SFNT family " + family + " requested by " + identity + " in " + path)
            if requested_families: base["literal_createfont_families"] = sorted(set(requested_families))
            for match in re.finditer(r'(?:include|AddCSLuaFile)\s*\(\s*["\']([^"\']+\.lua)["\']\s*\)', text):
                name = match.group(1)
                local = str(PurePosixPath(path).parent / name)
                local_source = resolve(local)
                lua_source = resolve("lua/" + name) if not local_source else None
                direct_source = resolve(name) if not local_source and not lua_source else None
                actual = (local_source or lua_source or direct_source or {}).get("path", name)
                dep(actual, "Literal include/AddCSLuaFile from " + path)
            for match in re.finditer(r'(?:vgui\.Create|vgui\.Register|derma\.DefineControl)\s*\(\s*["\']([^"\']+)["\']', text):
                panel = match.group(1)
                if panel in panel_sources: dep(panel_sources[panel], "Original registered VGUI/Derma class " + panel)
            for panel, panel_path in panel_sources.items():
                if re.search(r'["\']' + re.escape(panel) + r'["\']', text): dep(panel_path, "Original panel class/base reference " + panel)
            for match in re.finditer(r'["\']([^"\'\n]+\.(?:mdl|wav|mp3|png|vmt|vtf))["\']', text, re.I):
                value = match.group(1)
                if value.startswith("models/"): dep(value, "Literal model resource from " + path)
                elif value.startswith("materials/"): dep(value, "Literal material/image resource from " + path)
                elif value.endswith((".wav", ".mp3")): dep(value if value.startswith("sound/") else "sound/" + value.lstrip("*!#@<>^)}"), "Literal audio resource from " + path)
                elif value.endswith(".png"): dep("materials/" + value, "Literal material image from " + path)
            generated = re.findall(r'CreateMaterial\s*\(\s*["\']([^"\']+)["\']', text)
            if generated: base["generated_material_boundaries"] = generated
            for match in re.finditer(r'(?<!Create)Material\s*\(\s*["\']([^"\']+)["\']', text):
                value = match.group(1)
                if value.startswith(("!", "_")) or value in generated:
                    base.setdefault("runtime_material_boundaries", []).append(value)
                    continue
                if value.endswith("/"):
                    base.setdefault("dynamic_material_prefix_boundaries", []).append(value)
                    continue
                value = value if value.startswith("materials/") else "materials/" + value
                if not PurePosixPath(value).suffix: value += ".vmt"
                dep(value, "Original Lua material from " + path)
            used_events = []
            for match in re.finditer(r'(?:EmitSound|Sound|CreateSound|surface\.PlaySound)\s*\(\s*["\']([^"\']+)["\']', text):
                event = match.group(1)
                if event.lower() not in sound_events: continue
                used_events.append(event)
                for definition in sound_events[event.lower()]:
                    dep(definition["script"], "Original named sound-event definition: " + event)
                    for wave in definition["waves"]:
                        wave = wave.lstrip("*!#@<>^)}")
                        dep(wave if wave.startswith("sound/") else "sound/" + wave, "Original wave for sound event " + event)
            if used_events: base["named_sound_events"] = sorted(set(used_events))
        if low.endswith(".vmt"):
            clean = re.sub(r'//[^\n]*', '', text)
            base["material_shader"] = next(iter(re.findall(r'^\s*["\']?([\w]+)["\']?\s*\{', clean)), None)
            base["material_proxy_names"] = re.findall(r'(?mi)^\s*["\']?([\w]+)["\']?\s*$', text) if "proxies" in text.lower() else []
            for match in re.finditer(r'["\']?(\$(?:basetexture|bumpmap|normalmap|detail|envmapmask|phongexponenttexture|selfillummask|lightwarptexture|blendmodulatetexture|basetexture2|bumpmap2)|include)["\']?\s+["\']([^"\']+)["\']', text, re.I):
                key, value = match.groups()
                if value.startswith(("_", "!")):
                    base.setdefault("runtime_render_target_boundaries", []).append(value)
                    continue
                value = value.removeprefix("materials/")
                dep("materials/" + value + ("" if PurePosixPath(value).suffix else ".vmt" if key.lower() == "include" else ".vtf"), "Original VMT texture/patch dependency from " + path)
            for proxy in ("PlayerColor", "WeaponColor"):
                if proxy.lower() in text.lower():
                    for p in (game / "garrysmod/lua/matproxy").glob("*.lua"):
                        if proxy.lower() in p.read_text(encoding="utf-8-sig", errors="replace").lower(): dep(p.relative_to(game / "garrysmod").as_posix(), "Original material proxy " + proxy)
        if low.endswith(".mdl"):
            stem = path[:-4]
            for ext in (".vvd", ".dx90.vtx", ".phy"):
                if ext != ".phy" or resolve(stem + ext): dep(stem + ext, "Original Source model companion")
            # MDL texture table inspection is format parsing, not code disassembly.
            if content[:4] == b"IDST" and len(content) >= 220:
                try:
                    ntex, texoff, ncd, cdoff = struct.unpack_from("<4i", content, 204)
                    dirs = []
                    for n in range(min(ncd, 128)):
                        off = struct.unpack_from("<i", content, cdoff + n * 4)[0]
                        dirs.append(content[off:content.index(b"\0", off)].decode("ascii", "replace"))
                    for n in range(min(ntex, 256)):
                        off = texoff + n * 64
                        nameoff = off + struct.unpack_from("<i", content, off)[0]
                        name = content[nameoff:content.index(b"\0", nameoff)].decode("ascii", "replace")
                        matches = ["materials/" + folder + name + ".vmt" for folder in dirs]
                        resolved = [candidate for candidate in matches if resolve(candidate)]
                        if resolved: dep(resolved[0], "Original MDL texture directory/name table")
                        else: unresolved.append({"path": path, "reason": "MDL texture material unresolved", "candidates": matches})
                except (ValueError, struct.error) as exc: errors.append(path + " MDL texture metadata: " + str(exc))
        base["dependencies"] = dependencies
        # Reuse only after equality with the newly resolved original is proven.
        reused = None
        if args.stage:
            for candidate in existing.get(len(content), []):
                if candidate not in existing_hash: existing_hash[candidate] = sha(candidate)
                if existing_hash[candidate] == digest: reused = candidate; break
            dest = reused or out / "original_payload" / path
            if not reused:
                if dest.exists() and sha(dest) != digest:
                    if prior_stage_entries.get(path.lower(), {}).get("sha256") == digest:
                        raise SystemExit("Refusing overwrite of different staged original: " + str(dest))
                    base["preserved_prior_stage_conflict"] = {"path": str(dest), "sha256": sha(dest), "reason": "Different package-priority source selected; original first pass retained"}
                    package = source["archive"].path.stem if source["kind"] == "vpk" else source["file"].parent.name
                    dest = out / "original_payload_by_package" / package / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists() and sha(dest) != digest: raise SystemExit("Refusing overwrite of different staged original: " + str(dest))
                if not dest.exists(): dest.write_bytes(content)
            base["destination_path"] = str(dest)
            base["status"] = "reused_verified_current_stage" if reused and out in reused.parents else "reused_verified_original" if reused else "staged_verified_original"
            base["destination_sha256"] = sha(dest)
            base["sha256_match"] = base["destination_sha256"] == digest
        else:
            base["destination_path"] = None
            base["status"] = "inventoried_not_staged"
        entries.append(base)
        if len(entries) % 100 == 0: print(f"Closure processed {len(entries)} entries", flush=True)

    for chunk_path, p in selected_chunks.items():
        print("Hashing selected VPK body " + p.name, flush=True)
        selected_chunks[chunk_path] = {"path": chunk_path, "sha256": sha(p), "size": p.stat().st_size}
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    summary = {"tool": VERSION, "generated_utc": now, "source_root": str(game), "project_root": str(project),
               "output_root": str(out), "loose_file_count": len(inventory), "loose_type_counts": dict(sorted(counts.items())),
               "vpk_directory_count": len(archives), "vpk_entry_count": sum(len(a.entries) for a in archives),
               "gma_archive_count": len(addon_archives), "gma_entry_count": sum(a["entry_count"] for a in addon_archives),
               "vpk_archives": [{"path": str(a.path), "sha256": a.sha256, "entries": len(a.entries), "version": a.version} for a in archives],
               "selected_archive_bodies": list(selected_chunks.values()), "native_module_count": len(native_modules),
               "status_counts": dict(collections.Counter(e["status"] for e in entries)), "closure_entry_count": len(entries),
               "closure_status": "incomplete_native_and_dynamic_boundaries", "errors": errors,
               "limitations": ["Runtime mount state and addon priorities not executed; GMA directories indexed without mounting/staging payloads", "Native interfaces require IDA 6.8 evidence; inventory never substitutes native behavior", "Dynamic Lua includes, generated SpawnIcons, system fonts, localization and global GLua APIs require runtime closure", "Literal-path closure is conservative and includes unresolved optional branches rather than asset substitutes"],
               "prior_manifests": prior_audit}
    summary["expanded_registry_patterns"] = registry_patterns
    summary["named_sound_event_evidence"] = native_sound_evidence
    dump(out / "inventory_summary.json", summary)
    dump(out / "asset_provenance.json", {"tool": VERSION, "generated_utc": now, "source_root": str(game), "closure_status": summary["closure_status"], "entries": entries})
    dump(out / "unresolved_staging_dependencies.json", {"entries": unresolved, "errors": errors})
    dump(out / "font_requirements.json", {"entries": font_requirements,
         "policy": "Only exact installed SFNT family matches stage original font files; absent families remain host requirements, no Windows system fonts copied"})
    bad = [e["internal_path"] for e in entries if e.get("sha256_match") is False]
    dump(out / "staging_validation.json", {"tool": VERSION, "source_sha_destination_sha_match": not bad, "hash_mismatches": bad,
         "vpk_crc_verified_entries": sum(e.get("crc32_validated", False) for e in entries), "proprietary_commit_safe_false": all(e["commit_safe"] is False for e in entries),
         "stage_enabled": args.stage, "status_counts": summary["status_counts"], "runtime_changed": False, "gameplay_validation": "not_performed", "closure_status": summary["closure_status"]})
    print(json.dumps(summary, ensure_ascii=False), flush=True)

if __name__ == "__main__": main()
