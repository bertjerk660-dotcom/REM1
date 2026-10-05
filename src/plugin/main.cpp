#include "nvse/PluginAPI.h"
#include "nvse/GameAPI.h"
#include "nvse/GameObjects.h"
#include "nvse/NiObjects.h"
#include "nvse/GameForms.h"
#include "nvse/GameData.h"
#include "nvse/GameUI.h"
#include "nvse/GameScript.h"
#include "nvse/CommandTable.h"
#include <windows.h>
#include <windowsx.h>
#include <gdiplus.h>
#pragma comment(lib, "gdiplus.lib")
#include <cmath>
#include <cstdio>
#include <cstring>
#include <vector>
#include <string>
#include <unordered_map>
#include <fstream>

IDebugLog gLog("FNVGModTHUG2.log");
PluginHandle g_pluginHandle = kPluginHandle_Invalid;
NVSEMessagingInterface* g_messaging = nullptr;
NVSEInterface* g_nvse = nullptr;

static bool g_noClip = false;
static bool g_noClipMovementWasDisabled = false;
static DWORD g_noClipLastTick = 0;
static bool g_physgunEnabled = false;
static bool g_toolgunEnabled = false;
static bool g_gameplayReady = false;
static bool g_buildMenuToggleWasDown = false;
static DWORD g_runtimeFormInitEarliestTick = 0;
static bool g_runtimeFormInitLogged = false;

enum class GModWeaponKind : UInt8
{
    Utility = 0,
    Melee,
    Pistol,
    Automatic,
    Rifle,
    Shotgun,
    Launcher,
    Grenade,
    Toolgun,
    Physgun,
    Physcannon,
    Camera,
    Medkit,
    Flechette
};

struct GModWeaponDef
{
    const char* className;
    const char* displayName;
    const char* worldNif;
    GModWeaponKind kind;
    bool autoGive;
};

#include "gmod_weapon_defs.inc"

struct GModWeaponSoundDef
{
    const char* className;
    GModWeaponKind kind;
    UInt8 variantCount;
    const char* variants[4];
};

static const GModWeaponSoundDef kGModWeaponSoundDefs[] =
{
#include "gmod_weapon_sounds.inc"
};

struct GModPropDef
{
    const char* category;
    const char* displayName;
    const char* nifPath;
    const char* sourceModel;
};

#include "gmod_prop_defs.inc"

struct GModToolDef
{
    const char* id;
    const char* category;
    const char* displayName;
};

#include "gmod_tool_defs.inc"
#include "gmod_npc_defs.inc"

struct GModRuntimeWeapon
{
    const GModWeaponDef* def = nullptr;
    TESObjectWEAP* weapon = nullptr;
    TESObjectSTAT* worldStatic = nullptr;
};

static std::vector<GModRuntimeWeapon> g_gmodRuntimeWeapons;
static bool g_gmodWeaponFormsReady = false;
static bool g_gmodAttackWasDown = false;
static bool g_gmodSecondaryWasDown = false;
static bool g_weaponPhysgunActive = false;
static bool g_weaponToolgunActive = false;
static bool g_cameraWeaponActive = false;
static float g_cameraDefaultFov = 75.0f;
static UInt32 g_cameraZoomStep = 0;
static ULONG_PTR g_gdiplusToken = 0;

struct GModRuntimeSound
{
    const char* key = nullptr;
    TESSound* sound = nullptr;
};

static std::vector<GModRuntimeSound> g_gmodSoundForms;
static UInt32 g_toolgunSoundVariant = 0;
static UInt32 g_physgunLaunchVariant = 0;
static UInt32 g_gmodMappedSoundVariant = 0;

struct GModBuildMenuState
{
    bool open = false;
    UInt32 categoryIndex = 0;
    UInt32 itemIndex = 0;
    bool fightWasDisabled = false;
    bool movementWasDisabled = false;
    DWORD lastHudTick = 0;
};

static GModBuildMenuState g_buildMenu;

struct GModThrusterBinding
{
    UInt32 refID = 0;
    float dirX = 0.0f;
    float dirY = 0.0f;
    float dirZ = 0.0f;
    float speed = 650.0f;
};

struct GModHoverBinding
{
    UInt32 refID = 0;
    float targetZ = 0.0f;
};

struct GModMotorBinding
{
    UInt32 refID = 0;
    UInt32 anchorRefID = 0; // nonzero only for spawned wheel attachments
    float offX = 0.0f;
    float offY = 0.0f;
    float offZ = 0.0f;
    float axisX = 0.0f;
    float axisY = 0.0f;
    float axisZ = 1.0f;
    float speed = 8.0f;
    bool wheel = false;
};

struct GModBalloonBinding
{
    UInt32 balloonRefID = 0;
    UInt32 targetRefID = 0;
    float height = 150.0f;
    float lift = 95.0f;
};

enum class GModConstraintKind : UInt8
{
    Weld = 0,
    Pivot,
    Distance,
    Rope,
    Slider,
    Hydraulic,
    Muscle,
    Winch,
    Pulley
};

struct GModConstraintBinding
{
    UInt32 refA = 0;
    UInt32 refB = 0;
    GModConstraintKind kind = GModConstraintKind::Distance;
    float offX = 0.0f;
    float offY = 0.0f;
    float offZ = 0.0f;
    float rotOffX = 0.0f;
    float rotOffY = 0.0f;
    float rotOffZ = 0.0f;
    float axisX = 0.0f;
    float axisY = 0.0f;
    float axisZ = 1.0f;
    float restDistance = 0.0f;
    float baseDistance = 0.0f;
    float minDistance = 0.0f;
    float maxDistance = 0.0f;
    float stiffness = 8.0f;
    DWORD createdTick = 0;
};

struct GModButtonBinding
{
    UInt32 buttonRefID = 0;
    UInt32 targetRefID = 0;
};

struct GModFrozenBinding
{
    UInt32 refID = 0;
    float x = 0.0f;
    float y = 0.0f;
    float z = 0.0f;
};

struct GModLampBinding
{
    UInt32 lightRefID = 0;
    UInt32 targetRefID = 0;
    float offX = 0.0f;
    float offY = 0.0f;
    float offZ = 55.0f;
};

struct GModDynamiteBinding
{
    UInt32 refID = 0;
    DWORD explodeTick = 0;
    float radius = 850.0f;
    float impulse = 900.0f;
};

struct GModPhysPropBinding
{
    UInt32 refID = 0;
    UInt8 mode = 1; // 1 low gravity, 2 zero gravity, 3 high drag
};

enum class GModVehicleKind : UInt8
{
    None = 0,
    Buggy,
    Airboat,
    Jalopy,
    GenericLand,
    GenericBoat,
    Seat
};

struct GModVehicleState
{
    bool active = false;
    UInt32 refID = 0;
    GModVehicleKind kind = GModVehicleKind::None;
    bool movementWasDisabled = false;
    bool fightWasDisabled = false;
    bool cameraWasThirdPerson = false;
    bool useWasDown = false;
    DWORD lastTick = 0;
    DWORD lastHudTick = 0;
};

static UInt32 g_toolModeIndex = 29; // authentic manifest index for Remover
static DWORD g_toolModeHudTick = 0;
static std::vector<GModThrusterBinding> g_toolThrusters;
static std::vector<GModHoverBinding> g_toolHoverballs;
static std::vector<GModMotorBinding> g_toolMotors;
static std::vector<GModBalloonBinding> g_toolBalloons;
static std::vector<GModLampBinding> g_toolLamps;
static std::vector<GModDynamiteBinding> g_toolDynamite;
static std::vector<GModPhysPropBinding> g_toolPhysProps;
static DWORD g_physPropUpdateTick = 0;
static bool g_pendingDynamite = false;
static DWORD g_pendingDynamiteFuseMs = 3000;
static UInt32 g_pendingLampTargetRefID = 0;
static float g_pendingLampOffX = 0.0f;
static float g_pendingLampOffY = 0.0f;
static float g_pendingLampOffZ = 55.0f;
static UInt32 g_pendingBalloonTargetRefID = 0;
static float g_pendingBalloonHeight = 150.0f;
static float g_pendingBalloonLift = 95.0f;
static UInt32 g_pendingWheelAnchorRefID = 0;
static float g_pendingWheelOffX = 0.0f;
static float g_pendingWheelOffY = 0.0f;
static float g_pendingWheelOffZ = 0.0f;
static float g_pendingWheelAxisX = 1.0f;
static float g_pendingWheelAxisY = 0.0f;
static float g_pendingWheelAxisZ = 0.0f;
static float g_pendingWheelSpeed = 8.0f;
static std::vector<GModConstraintBinding> g_toolConstraints;
static UInt32 g_constraintFirstRefID = 0;
static std::vector<GModButtonBinding> g_toolButtons;
static UInt32 g_buttonFirstRefID = 0;
static std::vector<GModFrozenBinding> g_frozenProps;
static DWORD g_frozenUpdateTick = 0;
static char g_duplicatorNif[260] = {};
static char g_duplicatorName[128] = {};
static GModVehicleState g_vehicle;

struct GModNpcProxy
{
    UInt32 refID = 0;
    const GModNpcDef* def = nullptr;
    float health = 100.0f;
    bool dead = false;
    DWORD lastAttackTick = 0;
};

static std::vector<GModNpcProxy> g_gmodNpcProxies;
static const GModNpcDef* g_pendingNpcDef = nullptr;

// One-shot integration self-test. It is active only while the .autotest flag exists.
static bool g_autoTestEnabled = false;
static bool g_autoTestLoadIssued = false;
static bool g_autoTestSpawnPending = false;
static bool g_autoTestSpawnRequested = false;
static bool g_autoTestContextWaitLogged = false;
static DWORD g_autoTestStartTick = 0;
static DWORD g_autoTestSpawnTick = 0;
static const char* kAutoTestFlag = "Data\\NVSE\\Plugins\\FNVGModTHUG2.autotest";

enum class SkateMoveState : UInt8
{
    Ground = 0,
    Air,
    Grind,
    Manual,
    Lip,
    Skitch
};

struct SkateState
{
    bool active = false;
    SkateMoveState moveState = SkateMoveState::Ground;
    float velocityX = 0.0f;
    float velocityY = 0.0f;
    float velocityZ = 0.0f;
    float spinDegrees = 0.0f;
    float flipDegrees = 0.0f;
    float flipRemaining = 0.0f;
    float balance = 0.0f;
    float comboScore = 0.0f;
    float comboMultiplier = 1.0f;
    float totalScore = 0.0f;
    float special01 = 0.0f;
    float speed01 = 0.0f;
    float originalSpeedMult = 100.0f;
    float originalFov = 75.0f;
    bool thugCamNodeSaved = false;
    float thugCamOriginalTranslate[3] = {};
    float thugCamOriginalRotate[9] = {};
    bool fightWasDisabled = false;
    bool cameraWasThirdPerson = false;
    bool jumpWasDown = false;
    bool flipWasDown = false;
    bool grabWasDown = false;
    bool forwardHoldInjected = false;
    bool sawDescending = false;
    bool comboActive = false;
    bool nollieActive = false;
    bool nollieToggleWasDown = false;
    bool pressureActive = false;
    bool pressureToggleWasDown = false;
    bool revertWasDown = false;
    bool revertAvailable = false;
    bool skitchWasDown = false;
    UInt32 skitchTargetRefID = 0;
    UInt32 landingStableFrames = 0;
    UInt32 trickCount = 0;
    UInt8 manualVariant = 0;
    UInt8 grindVariant = 0;
    UInt8 lipVariant = 0;
    float lastPlayerZ = 0.0f;
    DWORD lastTick = 0;
    DWORD airStartTick = 0;
    DWORD comboBankDeadline = 0;
    DWORD lastSpeedApplyTick = 0;
    DWORD lastHudTick = 0;
    char lastTrick[64] = {};
    SInt32 thugAnimClipIndex = -1;
    DWORD thugAnimStartTick = 0;
    bool thugAnimLoop = true;
    bool thugAnimBonesSaved = false;
};

static SkateState g_skate;

struct THUG2RetargetClip
{
    char name[16] = {};
    float duration = 0.0f;
    UInt32 frameCount = 0;
    float fps = 60.0f;
    std::vector<float> rotations;
};

static const UInt32 kTHUG2RetargetBoneCount = 22;
static const char* kTHUG2RetargetBoneNames[kTHUG2RetargetBoneCount] = {
    "Bip01 Pelvis", "Bip01 Spine", "Bip01 Spine1", "Bip01 Spine2",
    "Bip01 Neck", "Bip01 Head",
    "Bip01 L Clavicle", "Bip01 L UpperArm", "Bip01 L Forearm", "Bip01 L Hand",
    "Bip01 R Clavicle", "Bip01 R UpperArm", "Bip01 R Forearm", "Bip01 R Hand",
    "Bip01 L Thigh", "Bip01 L Calf", "Bip01 L Foot", "Bip01 L Toe0",
    "Bip01 R Thigh", "Bip01 R Calf", "Bip01 R Foot", "Bip01 R Toe0"
};
static std::vector<THUG2RetargetClip> g_thug2RetargetClips;
static NiAVObject* g_thug2RetargetBones[kTHUG2RetargetBoneCount] = {};
static NiAVObject::RotAndTranslate g_thug2RetargetSaved[kTHUG2RetargetBoneCount] = {};
static NiNode* g_thug2RetargetRoot = nullptr;
static DWORD g_thug2RetargetEarliestTick = 0;
static bool g_thug2FirstUpdateDiag = false;
static UInt32 g_thug2DiagFrameCount = 0;
// v85 single-subsystem isolation: keep all skate movement/camera/HUD paths live,
// but completely suppress THUG2 skeleton retarget writes. If the crash disappears,
// delayed retarget activation is proven causal; if it persists, retarget is cleared.
static constexpr bool kTHUG2RetargetDiagnosticEnabled = false;

static bool LoadTHUG2RetargetBank()
{
    if (!g_thug2RetargetClips.empty()) return true;
    std::ifstream in("Data\\NVSE\\Plugins\\FNVGModTHUG2_THUG2\\animations_v72.bin", std::ios::binary);
    if (!in) { _MESSAGE("[THUG2-ANIM] animation bank missing"); return false; }

    char magic[4] = {};
    UInt32 version=0,bones=0,clips=0;
    in.read(magic,4); in.read(reinterpret_cast<char*>(&version),4);
    in.read(reinterpret_cast<char*>(&bones),4); in.read(reinterpret_cast<char*>(&clips),4);
    if (std::memcmp(magic,"T2A1",4)!=0 || version!=1 || bones!=kTHUG2RetargetBoneCount)
    { _MESSAGE("[THUG2-ANIM] invalid bank header"); return false; }

    char boneName[32];
    for (UInt32 i=0;i<bones;++i) in.read(boneName,32);
    for (UInt32 c=0;c<clips;++c)
    {
        THUG2RetargetClip clip;
        in.read(clip.name,16);
        in.read(reinterpret_cast<char*>(&clip.duration),4);
        in.read(reinterpret_cast<char*>(&clip.frameCount),4);
        in.read(reinterpret_cast<char*>(&clip.fps),4);
        if (!in || clip.frameCount<1 || clip.frameCount>10000) return false;
        const size_t count=static_cast<size_t>(clip.frameCount)*bones*4;
        clip.rotations.resize(count);
        in.read(reinterpret_cast<char*>(clip.rotations.data()),count*sizeof(float));
        if (!in) return false;
        g_thug2RetargetClips.push_back(std::move(clip));
    }
    _MESSAGE("[THUG2-ANIM] loaded %u exact THUG2 retarget clips",(unsigned)g_thug2RetargetClips.size());
    return !g_thug2RetargetClips.empty();
}

static SInt32 FindTHUG2RetargetClip(const char* name)
{
    for (UInt32 i=0;i<g_thug2RetargetClips.size();++i)
        if (_stricmp(g_thug2RetargetClips[i].name,name)==0) return static_cast<SInt32>(i);
    return -1;
}

static void ClearTHUG2RetargetCacheNoRestore()
{
    std::memset(g_thug2RetargetBones, 0, sizeof(g_thug2RetargetBones));
    g_skate.thugAnimBonesSaved = false;
    g_thug2RetargetRoot = nullptr;
}

static void ResolveTHUG2RetargetBones(PlayerCharacter* player)
{
    if (!player) return;
    if (GetTickCount() < g_thug2RetargetEarliestTick) return;

    NiNode* root = player->GetNiNode();
    if (!root)
    {
        _MESSAGE("[THUG2-ANIM] active player NiNode not ready; retarget deferred");
        return;
    }

    if (g_skate.thugAnimBonesSaved)
    {
        if (root == g_thug2RetargetRoot)
            return;

        // New Vegas can rebuild the actor 3D when changing camera/weapon state.
        // Never touch cached bones from an old scene root after that happens.
        _MESSAGE("[THUG2-ANIM] player root changed %p -> %p; dropping stale bone cache",
            g_thug2RetargetRoot, root);
        ClearTHUG2RetargetCacheNoRestore();
    }

    UInt32 resolved = 0;
    for (UInt32 i = 0; i < kTHUG2RetargetBoneCount; ++i)
    {
        NiObjectNET* obj = root->GetObject(kTHUG2RetargetBoneNames[i]);
        if (!obj)
        {
            g_thug2RetargetBones[i] = nullptr;
            continue;
        }

        // GetObject returns NiObjectNET; do not reinterpret it as NiAVObject.
        // v77/v80 could cache a non-AV object and later jump through invalid
        // scene-graph state. RTTI-check every resolved target first.
        NiAVObject* bone = DYNAMIC_CAST(obj, NiObjectNET, NiAVObject);
        g_thug2RetargetBones[i] = bone;
        if (!bone)
            continue;

        g_thug2RetargetSaved[i] = bone->dat0034;
        ++resolved;
    }

    // A normal New Vegas biped resolves essentially the full table. Refuse to
    // animate a partially constructed/reloading skeleton and retry next frame.
    if (resolved < 16)
    {
        _MESSAGE("[THUG2-ANIM] only %u/%u safe AV bones resolved; retrying",
            static_cast<unsigned>(resolved),
            static_cast<unsigned>(kTHUG2RetargetBoneCount));
        ClearTHUG2RetargetCacheNoRestore();
        return;
    }

    g_thug2RetargetRoot = root;
    g_skate.thugAnimBonesSaved = true;
    _MESSAGE("[THUG2-ANIM] resolved %u/%u RTTI-validated bones root=%p",
        static_cast<unsigned>(resolved),
        static_cast<unsigned>(kTHUG2RetargetBoneCount),
        root);
}

static void RestoreTHUG2RetargetBones(PlayerCharacter* player)
{
    if (!g_skate.thugAnimBonesSaved)
    {
        g_skate.thugAnimClipIndex = -1;
        return;
    }

    NiNode* currentRoot = player ? player->GetNiNode() : nullptr;
    if (currentRoot && currentRoot == g_thug2RetargetRoot)
    {
        for (UInt32 i = 0; i < kTHUG2RetargetBoneCount; ++i)
            if (g_thug2RetargetBones[i])
                g_thug2RetargetBones[i]->dat0034 = g_thug2RetargetSaved[i];

        currentRoot->UpdateTransform();
    }
    else
    {
        _MESSAGE("[THUG2-ANIM] restore skipped because actor root changed");
    }

    ClearTHUG2RetargetCacheNoRestore();
    g_skate.thugAnimClipIndex = -1;
}

static void StartTHUG2RetargetClip(const char* name, bool loop, bool restart=false)
{
    if (!LoadTHUG2RetargetBank()) return;
    const SInt32 idx=FindTHUG2RetargetClip(name);
    if (idx<0) return;
    if (!restart && g_skate.thugAnimClipIndex==idx) return;
    g_skate.thugAnimClipIndex=idx;
    g_skate.thugAnimStartTick=GetTickCount();
    g_skate.thugAnimLoop=loop;
}

static bool THUG2RetargetOneShotPlaying(DWORD now)
{
    if (g_skate.thugAnimClipIndex<0 || g_skate.thugAnimLoop) return false;
    const THUG2RetargetClip& c=g_thug2RetargetClips[g_skate.thugAnimClipIndex];
    return ((now-g_skate.thugAnimStartTick)/1000.0f) < c.duration;
}

static void QuaternionToNiMatrix(const float* q, NiMatrix33& m)
{
    const float x=q[0],y=q[1],z=q[2],w=q[3];
    const float xx=x*x, yy=y*y, zz=z*z, xy=x*y, xz=x*z, yz=y*z, wx=w*x, wy=w*y, wz=w*z;
    float* a=reinterpret_cast<float*>(&m);
    a[0]=1.0f-2.0f*(yy+zz); a[1]=2.0f*(xy-wz);       a[2]=2.0f*(xz+wy);
    a[3]=2.0f*(xy+wz);       a[4]=1.0f-2.0f*(xx+zz); a[5]=2.0f*(yz-wx);
    a[6]=2.0f*(xz-wy);       a[7]=2.0f*(yz+wx);       a[8]=1.0f-2.0f*(xx+yy);
}

static void ApplyTHUG2RetargetAnimation(PlayerCharacter* player, DWORD now)
{
    if (!player || now < g_thug2RetargetEarliestTick)
        return;
    if (g_skate.thugAnimClipIndex < 0 || !LoadTHUG2RetargetBank())
        return;
    if (static_cast<size_t>(g_skate.thugAnimClipIndex) >= g_thug2RetargetClips.size())
    {
        _MESSAGE("[THUG2-ANIM] invalid clip index %d", g_skate.thugAnimClipIndex);
        g_skate.thugAnimClipIndex = -1;
        return;
    }

    ResolveTHUG2RetargetBones(player);
    if (!g_skate.thugAnimBonesSaved || !g_thug2RetargetRoot)
        return;

    NiNode* currentRoot = player->GetNiNode();
    if (!currentRoot || currentRoot != g_thug2RetargetRoot)
    {
        _MESSAGE("[THUG2-ANIM] root changed before frame apply; deferring");
        ClearTHUG2RetargetCacheNoRestore();
        return;
    }

    const THUG2RetargetClip& c = g_thug2RetargetClips[g_skate.thugAnimClipIndex];
    if (!c.frameCount || c.fps <= 0.0f || !std::isfinite(c.fps) ||
        c.rotations.size() < static_cast<size_t>(c.frameCount) * kTHUG2RetargetBoneCount * 4)
    {
        _MESSAGE("[THUG2-ANIM] rejected malformed clip %s", c.name);
        return;
    }

    float t = (now - g_skate.thugAnimStartTick) / 1000.0f;
    if (g_skate.thugAnimLoop && c.duration > 0.001f)
        t = std::fmod(t, c.duration);
    else if (t > c.duration)
        t = c.duration;
    if (t < 0.0f || !std::isfinite(t))
        t = 0.0f;

    UInt32 frame = static_cast<UInt32>(t * c.fps + 0.5f);
    if (frame >= c.frameCount) frame = c.frameCount - 1;
    const size_t base = static_cast<size_t>(frame) * kTHUG2RetargetBoneCount * 4;

    for (UInt32 i = 0; i < kTHUG2RetargetBoneCount; ++i)
    {
        NiAVObject* bone = g_thug2RetargetBones[i];
        if (!bone) continue;

        const float* q = &c.rotations[base + i * 4];
        if (!std::isfinite(q[0]) || !std::isfinite(q[1]) ||
            !std::isfinite(q[2]) || !std::isfinite(q[3]))
            continue;

        QuaternionToNiMatrix(q, bone->dat0034.rotate);
    }

    currentRoot->UpdateTransform();
}

static void UpdateTHUG2RetargetSelection(bool push, bool left, bool right, SkateMoveState before, DWORD now)
{
    // One-shot source clips win until their exact authored duration expires.
    if (THUG2RetargetOneShotPlaying(now)) return;

    if (before==SkateMoveState::Air && g_skate.moveState==SkateMoveState::Ground)
    { StartTHUG2RetargetClip("land",false,true); return; }

    switch (g_skate.moveState)
    {
    case SkateMoveState::Ground:
        if (left && !right) StartTHUG2RetargetClip("turnleft",true);
        else if (right && !left) StartTHUG2RetargetClip("turnright",true);
        else if (push) StartTHUG2RetargetClip("pushcycle",true);
        else StartTHUG2RetargetClip("idle",true);
        break;
    case SkateMoveState::Manual:
        StartTHUG2RetargetClip("manual",true);
        break;
    default:
        break; // Grind/lip/complex air sets are added from their exact ANR/SKA assets later.
    }
}

static TESObjectWEAP* g_skateboardWeapon = nullptr;
static TESObjectSTAT* g_skateboardWorldStatic = nullptr;
static TESObjectSTAT* g_skateboardRideStatic = nullptr;
static TESObjectREFR* g_skateboardRideRef = nullptr;
static TESForm* g_skateboardRidePendingForm = nullptr;
static DWORD g_skateboardRidePendingTick = 0;
static bool g_skateboardAttackWasDown = false;
static bool g_skateboardFightSuppressed = false;
static bool g_skateboardFightWasDisabledBeforeSuppress = false;
static const char* kSkateboardName = "THUG2 Skateboard";
static const char* kSkateboardNif = "rem\\thug2\\skateboard.nif";
static const char* kSkateboardRideNif = "rem\\thug2\\skateboard_visual.nif";

static void* GetNativeMouseSpring(PlayerCharacter* player)
{
    return player ? *reinterpret_cast<void**>(reinterpret_cast<UInt8*>(player) + 0x634) : nullptr;
}

static TESObjectREFR* GetNativeGrabbedRef(PlayerCharacter* player)
{
    return player ? *reinterpret_cast<TESObjectREFR**>(reinterpret_cast<UInt8*>(player) + 0x638) : nullptr;
}

static UInt32 GetNativeGrabMode(PlayerCharacter* player)
{
    return player ? *reinterpret_cast<UInt32*>(reinterpret_cast<UInt8*>(player) + 0x63C) : 0;
}

static float GetNativeGrabbedWeight(PlayerCharacter* player)
{
    return player ? *reinterpret_cast<float*>(reinterpret_cast<UInt8*>(player) + 0x640) : 0.0f;
}

static float GetNativeGrabDistance(PlayerCharacter* player)
{
    return player ? *reinterpret_cast<float*>(reinterpret_cast<UInt8*>(player) + 0x644) : 0.0f;
}

static TESObjectREFR* g_heldRef = nullptr;
static UInt32 g_physgunActorWakeRefID = 0;
static DWORD g_physgunActorWakeTick = 0;
static UInt8 g_physgunHeldOriginalKnockedState = 0;
static UInt8 g_physgunHeldForcedKnockedState = 1;
static UInt8 g_physgunActorWakeRestoreState = 0;
static bool g_physgunHeldUsingRagdollBodies = false;
static std::vector<UInt32> g_undoDisabled;
static std::vector<UInt32> g_spawnUndo;
static std::vector<TESForm*> g_runtimePropForms;
static TESForm* g_pendingSpawnForm = nullptr;
static DWORD g_pendingSpawnStartTick = 0;
static float g_holdDistance = 220.0f;

// Garry's Mod Physics Gun controller defaults, recovered from the installed
// 32-bit GMod server/client binaries with IDA Pro 6.8.
static constexpr float kGModPhysgunMinRange = 40.0f;
static constexpr float kGModPhysgunMaxRange = 4096.0f;
static constexpr float kGModPhysgunWheelSpeed = 10.0f;
static constexpr float kGModPhysgunMaxSpeed = 5000.0f;
static constexpr float kGModPhysgunMaxSpeedDamping = 10000.0f;
static constexpr float kGModPhysgunDampingFactor = 0.8f;
static constexpr float kGModPhysgunTimeToArrive = 0.05f;
static constexpr float kGModPhysgunTimeToArriveRagdoll = 0.10f;
static constexpr float kGModPhysgunSpinSpeed = 200.0f;
static constexpr float kGModPhysgunRotationSensitivity = 0.05f;
static DWORD g_lastHoldUpdate = 0;

struct ThrowState {
    TESObjectREFR* ref = nullptr;
    float vx = 0.0f;
    float vy = 0.0f;
    float vz = 0.0f;
    DWORD lastTick = 0;
    DWORD endTick = 0;
};
static ThrowState g_throw;

static bool GameHasFocus()
{
    HWND hwnd = GetForegroundWindow();
    if (!hwnd) return false;
    DWORD pid = 0;
    GetWindowThreadProcessId(hwnd, &pid);
    return pid == GetCurrentProcessId();
}

static void Notify(const char* msg)
{
    if (QueueUIMessage) QueueUIMessage(msg, 2, nullptr, nullptr, 2.0f, false);
    Console_Print("%s", msg);
}

static bool IsActorReference(const TESObjectREFR* ref)
{
    return ref && (ref->typeID == kFormType_Character || ref->typeID == kFormType_Creature);
}

static Actor* GetActorObject(TESObjectREFR* ref)
{
    if (!IsActorReference(ref)) return nullptr;
    return DYNAMIC_CAST(ref, TESObjectREFR, Actor);
}

static bool TryGetActorKnockedState(TESObjectREFR* ref, UInt8& stateOut)
{
    Actor* actor = GetActorObject(ref);
    if (!actor || !actor->baseProcess)
        return false;

    // IDA Pro 6.8 verified the getter reads BaseProcess +0x13C.
    // Mask to the low byte because the SDK stores HighProcess::knockedState as UInt8.
    const SInt32 rawState = actor->baseProcess->GetKnockedState();
    stateOut = static_cast<UInt8>(rawState & 0xFF);
    return true;
}

static bool TrySetActorKnockedState(TESObjectREFR* ref, UInt8 state)
{
    Actor* actor = GetActorObject(ref);
    if (!actor || !actor->baseProcess)
        return false;

    // Use the verified SDK virtual setter rather than hard-coding the getter address
    // discovered in IDA 6.8. This follows the actor's real BaseProcess vtable.
    actor->baseProcess->SetKnockedState(static_cast<char>(state));
    return true;
}

static void SetHavokLinearVelocity(void* body, float x, float y, float z);

static SInt32 GetActorRagdollRigidBodies(TESObjectREFR* ref, void*** bodiesOut)
{
    if (bodiesOut) *bodiesOut = nullptr;

    Actor* actor = GetActorObject(ref);
    if (!actor || !actor->ragDollController)
        return 0;

    // IDA Pro 6.8, FalloutNV 1.4.0.525:
    // Actor +0xAC -> bhkRagdollController*
    // bhkRagdollController +0x48 -> hkaRagdollInstance*
    // hkaRagdollInstance +0x08 -> hkArray<hkpRigidBody*>::data
    // hkaRagdollInstance +0x0C -> hkArray<hkpRigidBody*>::size
    UInt8* controller = reinterpret_cast<UInt8*>(actor->ragDollController);
    UInt8* instance = *reinterpret_cast<UInt8**>(controller + 0x48);
    if (!instance)
        return 0;

    void** bodies = *reinterpret_cast<void***>(instance + 0x08);
    const SInt32 count = *reinterpret_cast<SInt32*>(instance + 0x0C);

    if (!bodies || count <= 0 || count > 64)
        return 0;

    if (bodiesOut) *bodiesOut = bodies;
    return count;
}

static bool IsRagdollRigidBodyUsable(void* body)
{
    if (!body) return false;
    UInt8* bytes = reinterpret_cast<UInt8*>(body);

    if (*(bytes + 0x28) != 1)
        return false;

    return (*(bytes + 0xE8) & 2) != 0;
}

static SInt32 SetActorRagdollLinearVelocity(TESObjectREFR* ref, float x, float y, float z)
{
    void** bodies = nullptr;
    const SInt32 count = GetActorRagdollRigidBodies(ref, &bodies);
    if (count <= 0 || !bodies)
        return 0;

    SInt32 applied = 0;
    for (SInt32 i = 0; i < count; ++i)
    {
        void* body = bodies[i];
        if (!IsRagdollRigidBodyUsable(body))
            continue;

        SetHavokLinearVelocity(body, x, y, z);
        ++applied;
    }
    return applied;
}

static TESObjectREFR* GetCrosshairTarget()
{
    InterfaceManager* ui = *(InterfaceManager**)0x011D8A80;
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!ui || !player || !ui->crosshairRef || ui->crosshairRef == player)
        return nullptr;
    return ui->crosshairRef;
}

static void* GetRootHavokRigidBody(TESObjectREFR* ref)
{
    if (!ref || IsActorReference(ref))
        return nullptr;

    UInt8* renderState = *reinterpret_cast<UInt8**>(reinterpret_cast<UInt8*>(ref) + 0x64);
    if (!renderState) return nullptr;

    UInt8* rootNode = *reinterpret_cast<UInt8**>(renderState + 0x14);
    if (!rootNode) return nullptr;

    UInt8* collisionObject = *reinterpret_cast<UInt8**>(rootNode + 0x1C);
    if (!collisionObject) return nullptr;

    UInt8* bhkWorldObject = *reinterpret_cast<UInt8**>(collisionObject + 0x10);
    if (!bhkWorldObject) return nullptr;

    UInt8* hkpWorldObject = *reinterpret_cast<UInt8**>(bhkWorldObject + 0x08);
    if (!hkpWorldObject || *(hkpWorldObject + 0x28) != 1)
        return nullptr;

    // hkpRigidBody::motion is +0xE0; hkpMotion::type is +0x08.
    if ((*(hkpWorldObject + 0xE8) & 2) == 0)
        return nullptr;

    return hkpWorldObject;
}

static void SetHavokLinearVelocity(void* body, float x, float y, float z)
{
    if (!body) return;

    float* velocity = reinterpret_cast<float*>(reinterpret_cast<UInt8*>(body) + 0x1B0);
    velocity[0] = x;
    velocity[1] = y;
    velocity[2] = z;
    velocity[3] = 0.0f;

    using UpdateMotionFn = void(__thiscall*)(void*);
    reinterpret_cast<UpdateMotionFn>(0x00C9C1D0)(body);
}

static void GetHavokLinearVelocity(void* body, float& x, float& y, float& z)
{
    x = y = z = 0.0f;
    if (!body) return;

    const float* velocity =
        reinterpret_cast<const float*>(reinterpret_cast<const UInt8*>(body) + 0x1B0);
    x = velocity[0];
    y = velocity[1];
    z = velocity[2];
}

// Verified in the live/decrypted FalloutNV executable with IDA Pro 6.8:
// +0x1B0 is linear velocity and +0x1C0 is angular velocity on this hkpRigidBody layout.
// Both vectors use sub_C9C1D0 (0x00C9C1D0) to wake/update the body before Havok consumes them.
static void SetHavokAngularVelocity(void* body, float x, float y, float z)
{
    if (!body) return;

    float* velocity =
        reinterpret_cast<float*>(reinterpret_cast<UInt8*>(body) + 0x1C0);
    velocity[0] = x;
    velocity[1] = y;
    velocity[2] = z;
    velocity[3] = 0.0f;

    using UpdateMotionFn = void(__thiscall*)(void*);
    reinterpret_cast<UpdateMotionFn>(0x00C9C1D0)(body);
}

static void DropHeld();
static void GiveWeaponToPlayer(TESObjectWEAP* weapon);
static void SetRefPosition(TESObjectREFR* ref, float x, float y, float z);
static TESObjectREFR* FindReferenceForBaseForm(TESForm* baseForm);
static TESObjectREFR* LookupReference(UInt32 refID);
static UInt32 GetBuildCategoryCount();
static const GModPropCategoryRange* GetSelectedBuildCategory();
static const GModPropDef* GetSelectedBuildProp();
static void ChangeBuildCategory(int delta);
static void SpawnSelectedBuildProp();
static void CloseBuildMenu();
static void PlayGModUISound(const char* key, const char* relativePath);
static bool EnsureGdiPlus();
static float ReadCurrentWorldFov();
static void ApplyGModCameraFov(PlayerCharacter* player, float fov);
static TESObjectREFR* SpawnConvertedProp(const char* nifPath, float distance, const char* displayName = nullptr);
static void ResetActiveSkateCombo();
static void UpdateToolLights();
static void UpdateGModDynamite();
static void UpdateGModPhysProps();

#include "gmod_overlay.inc"

static TESObjectWEAP* FindExistingSkateboardWeapon()
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList) return nullptr;

    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weap = static_cast<TESObjectWEAP*>(obj);
        const char* name = weap->fullName.name.m_data;
        if (name && _stricmp(name, kSkateboardName) == 0)
            return weap;
    }
    return nullptr;
}

static NiAVObject* GetThirdPersonCameraNode()
{
    // Verified xNVSE/FNV 1.4.0.525 Camera3rd global.
    NiObject** slot = reinterpret_cast<NiObject**>(0x011E07D4);
    if (!slot || !*slot) return nullptr;
    return reinterpret_cast<NiAVObject*>(*slot);
}

static void SaveTHUG2CameraNode()
{
    if (g_skate.thugCamNodeSaved) return;
    NiAVObject* cam = GetThirdPersonCameraNode();
    if (!cam) return;

    g_skate.thugCamOriginalTranslate[0] = cam->dat0034.translate.x;
    g_skate.thugCamOriginalTranslate[1] = cam->dat0034.translate.y;
    g_skate.thugCamOriginalTranslate[2] = cam->dat0034.translate.z;

    const float* matrix = reinterpret_cast<const float*>(&cam->dat0034.rotate);
    for (int i = 0; i < 9; ++i)
        g_skate.thugCamOriginalRotate[i] = matrix[i];

    g_skate.thugCamNodeSaved = true;
}

static void RestoreTHUG2CameraNode()
{
    if (!g_skate.thugCamNodeSaved) return;
    NiAVObject* cam = GetThirdPersonCameraNode();
    if (cam)
    {
        cam->dat0034.translate.x = g_skate.thugCamOriginalTranslate[0];
        cam->dat0034.translate.y = g_skate.thugCamOriginalTranslate[1];
        cam->dat0034.translate.z = g_skate.thugCamOriginalTranslate[2];

        float* matrix = reinterpret_cast<float*>(&cam->dat0034.rotate);
        for (int i = 0; i < 9; ++i)
            matrix[i] = g_skate.thugCamOriginalRotate[i];

        cam->UpdateTransform();
    }
    g_skate.thugCamNodeSaved = false;
}

static void ApplyTHUG2NativeCameraProfile(PlayerCharacter* player)
{
    if (!player) return;
    SaveTHUG2CameraNode();

    NiAVObject* cam = GetThirdPersonCameraNode();
    if (!cam) return;

    // THUG2 PS2 physics.qb + IDA 6.8 sub_2E3B70:
    // Skater_Camera_Standard_Medium:
    // horiz_fov=72, behind=12, above=4.3, tilt=0.18,
    // slerp=.04, vert_air_slerp=.04, lerp_xz=.25, lerp_y=.75.
    // sub_2E3B70 converts behind/above to engine units by *12.
    const float behind = 12.0f * 12.0f;
    float above = 4.3f * 12.0f;
    float tilt = 0.18f;

    // Original THUG2 lip camera modifiers.
    if (g_skate.moveState == SkateMoveState::Lip)
    {
        above += 0.4f * 12.0f;
        tilt += -0.8f;
    }

    cam->dat0034.translate.x = 0.0f;
    cam->dat0034.translate.y = -behind;
    cam->dat0034.translate.z = above;

    // Keep Camera3rd locked to the skater parent rotation, with the native
    // THUG2 local pitch. This removes Fallout's slow third-person rotational lag.
    const float c = std::cos(tilt);
    const float sn = std::sin(tilt);
    float* m = reinterpret_cast<float*>(&cam->dat0034.rotate);
    m[0]=1.0f; m[1]=0.0f; m[2]=0.0f;
    m[3]=0.0f; m[4]=c;    m[5]=-sn;
    m[6]=0.0f; m[7]=sn;   m[8]=c;

    cam->UpdateTransform();
    ApplyGModCameraFov(player, 72.0f);
}


static TESObjectWEAP* FindSkateboardMeleeTemplate()
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList) return nullptr;

    TESObjectWEAP* fallback = nullptr;
    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weap = static_cast<TESObjectWEAP*>(obj);
        if (!weap->IsPlayable()) continue;
        if (weap->eWeaponType != TESObjectWEAP::kWeapType_OneHandMelee &&
            weap->eWeaponType != TESObjectWEAP::kWeapType_TwoHandMelee)
            continue;

        if (!fallback) fallback = weap;
        const char* name = weap->fullName.name.m_data;
        if (name && (_stricmp(name, "Baseball Bat") == 0 || _stricmp(name, "Lead Pipe") == 0))
            return weap;
    }
    return fallback;
}

static void EnsureSkateboardWeapon()
{
    if (g_skateboardWeapon) return;

    if (GetFileAttributesA("Data\\meshes\\rem\\thug2\\skateboard.nif") == INVALID_FILE_ATTRIBUTES)
    {
        _MESSAGE("[THUG2] skateboard visual NIF missing");
        return;
    }

    // The merge ESP already owns the persistent WEAP/STAT records (01000800/01000801).
    // Do not clone or rewrite them at runtime: the v78 grenade CloneForm path was the
    // source of all three repeatable startup crashes.
    g_skateboardWeapon = FindExistingSkateboardWeapon();
    if (!g_skateboardWeapon)
    {
        _MESSAGE("[THUG2] persistent REM_GModTHUG2 skateboard WEAP not found; runtime clone disabled");
        return;
    }

    g_skateboardWorldStatic = g_skateboardWeapon->worldStatic;
    const char* heldPath = g_skateboardWeapon->textureSwap.nifPath.m_data;
    const char* worldPath = g_skateboardWorldStatic ? g_skateboardWorldStatic->model.nifPath.m_data : nullptr;
    _MESSAGE("[THUG2] persistent skateboard %08X world=%08X held=%s worldModel=%s",
        g_skateboardWeapon->refID,
        g_skateboardWorldStatic ? g_skateboardWorldStatic->refID : 0,
        heldPath ? heldPath : "<null>",
        worldPath ? worldPath : "<null>");

    // Do not add another copy on every save load. The explicit
    // gmod_giveskateboard command handles inventory insertion when requested.
}

static bool IsSkateboardEquipped()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    return player && g_skateboardWeapon && player->GetEquippedWeapon() == g_skateboardWeapon;
}

static void UpdateSkateboardCombatSuppression(PlayerCharacter* player, bool skateboardEquipped)
{
    if (!player) return;

    if (skateboardEquipped)
    {
        if (!g_skateboardFightSuppressed)
        {
            g_skateboardFightWasDisabledBeforeSuppress =
                (player->disabledControlFlags & PlayerCharacter::kControlFlag_Fight) != 0;
            g_skateboardFightSuppressed = true;
        }

        player->disabledControlFlags |= PlayerCharacter::kControlFlag_Fight;
    }
    else if (g_skateboardFightSuppressed)
    {
        if (!g_skateboardFightWasDisabledBeforeSuppress)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Fight;

        g_skateboardFightSuppressed = false;
        g_skateboardFightWasDisabledBeforeSuppress = false;
    }
}

static bool IsCustomUtilityKind(GModWeaponKind kind)
{
    switch (kind)
    {
    case GModWeaponKind::Utility:
    case GModWeaponKind::Toolgun:
    case GModWeaponKind::Physgun:
    case GModWeaponKind::Physcannon:
    case GModWeaponKind::Camera:
    case GModWeaponKind::Medkit:
        return true;
    default:
        return false;
    }
}

static UInt8 PreferredFNVWeaponType(GModWeaponKind kind)
{
    switch (kind)
    {
    case GModWeaponKind::Melee:
    case GModWeaponKind::Utility:
    case GModWeaponKind::Physcannon:
    case GModWeaponKind::Camera:
    case GModWeaponKind::Medkit:
        return TESObjectWEAP::kWeapType_OneHandMelee;
    case GModWeaponKind::Toolgun:
    case GModWeaponKind::Pistol:
        return TESObjectWEAP::kWeapType_OneHandPistol;
    case GModWeaponKind::Physgun:
        return TESObjectWEAP::kWeapType_TwoHandHandle;
    case GModWeaponKind::Automatic:
    case GModWeaponKind::Flechette:
        return TESObjectWEAP::kWeapType_TwoHandAutomatic;
    case GModWeaponKind::Rifle:
    case GModWeaponKind::Shotgun:
        return TESObjectWEAP::kWeapType_TwoHandRifle;
    case GModWeaponKind::Launcher:
        return TESObjectWEAP::kWeapType_TwoHandLauncher;
    case GModWeaponKind::Grenade:
        return TESObjectWEAP::kWeapType_OneHandGrenade;
    default:
        return TESObjectWEAP::kWeapType_OneHandMelee;
    }
}
static bool WeaponNameContains(const TESObjectWEAP* weapon, const char* needle)
{
    if (!weapon || !needle) return false;
    const char* name = weapon->fullName.name.m_data;
    if (!name) return false;

    char lowerName[256] = {};
    char lowerNeedle[64] = {};
    strncpy_s(lowerName, sizeof(lowerName), name, _TRUNCATE);
    strncpy_s(lowerNeedle, sizeof(lowerNeedle), needle, _TRUNCATE);
    _strlwr_s(lowerName, sizeof(lowerName));
    _strlwr_s(lowerNeedle, sizeof(lowerNeedle));
    return std::strstr(lowerName, lowerNeedle) != nullptr;
}

static TESSound* FindAnyWeaponSoundTemplate()
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList) return nullptr;

    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
        for (UInt32 i = 0; i < 12; ++i)
            if (weapon->sounds[i])
                return weapon->sounds[i];
    }
    return nullptr;
}

static TESSound* GetOrCreateGModSound(const char* key, const char* relativePath, bool twoD, bool menuSound)
{
    if (!key || !relativePath) return nullptr;

    for (auto& runtime : g_gmodSoundForms)
        if (runtime.key && _stricmp(runtime.key, key) == 0)
            return runtime.sound;

    TESSound* source = FindAnyWeaponSoundTemplate();
    if (!source) return nullptr;

    TESForm* cloned = source->CloneForm(true);
    if (!cloned || cloned->typeID != kFormType_TESSound)
        return nullptr;

    TESSound* sound = static_cast<TESSound*>(cloned);
    sound->soundFile.Set(relativePath);
    sound->SetFlag(TESSound::kFlag_Loop, false);
    sound->SetFlag(TESSound::kFlag_PlayAtRandom, false);
    sound->SetFlag(TESSound::kFlag_RandomLocation, false);
    sound->SetFlag(TESSound::kFlag_2D, twoD);
    sound->SetFlag(TESSound::kFlag_MenuSound, menuSound);
    g_gmodSoundForms.push_back({key, sound});

    _MESSAGE("[GMOD-SOUND] %s -> %s form=%08X", key, relativePath, sound->refID);
    return sound;
}

static void PlayGModSound(const char* key, const char* relativePath, bool menuSound = false)
{
    TESSound* sound = GetOrCreateGModSound(key, relativePath, true, menuSound);
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!sound || !player) return;

    char cmd[64];
    std::snprintf(cmd, sizeof(cmd), "playsound %08X", sound->refID);
    Script::RunScriptLine2(cmd, player, true);
}

static void PlayGModUISound(const char* key, const char* file)
{
    PlayGModSound(key, file, true);
}

static void PlayTHUG2Sound(const char* key, const char* file)
{
    PlayGModSound(key, file, false);
}

static void PlayTHUG2OllieSound()
{
    PlayTHUG2Sound("thug2_ollie", "fx\\rem\\thug2\\ollieconc.wav");
}

static void PlayTHUG2LandSound(bool clean)
{
    PlayTHUG2Sound(clean ? "thug2_land_perfect" : "thug2_land_sloppy",
        clean ? "fx\\rem\\thug2\\perfectlanding.wav" : "fx\\rem\\thug2\\sloppylanding.wav");
}

static void PlayTHUG2GrindSound()
{
    PlayTHUG2Sound("thug2_grind_metal", "fx\\rem\\thug2\\grindmetal.wav");
}

static void PlayTHUG2RevertSound()
{
    PlayTHUG2Sound("thug2_revert", "fx\\rem\\thug2\\revertconc.wav");
}

static void PlayTHUG2BoardRollSound()
{
    PlayTHUG2Sound("thug2_board_roll", "fx\\rem\\thug2\\sk6_boardrollin01_11.wav");
}

static void PlayToolgunShotSound()
{
    if ((g_toolgunSoundVariant++ & 1u) == 0)
        PlayGModSound("toolgun_single_1", "fx\\rem\\gmod\\weapons\\airboat\\airboat_gun_lastshot1.wav");
    else
        PlayGModSound("toolgun_single_2", "fx\\rem\\gmod\\weapons\\airboat\\airboat_gun_lastshot2.wav");
}

static void PlayPhysgunPickupSound()
{
    PlayGModSound("physgun_pickup", "fx\\rem\\gmod\\weapons\\physcannon\\physcannon_pickup.wav");
}

static void PlayPhysgunDropSound()
{
    PlayGModSound("physgun_drop", "fx\\rem\\gmod\\weapons\\physcannon\\physcannon_drop.wav");
}

static void PlayPhysgunDryFireSound()
{
    PlayGModSound("physgun_dryfire", "fx\\rem\\gmod\\weapons\\physcannon\\physcannon_dryfire.wav");
}

static void PlayPhysgunLaunchSound()
{
    switch (g_physgunLaunchVariant++ % 3u)
    {
    case 0:
        PlayGModSound("physgun_launch_1", "fx\\rem\\gmod\\weapons\\physcannon\\superphys_launch1.wav");
        break;
    case 1:
        PlayGModSound("physgun_launch_2", "fx\\rem\\gmod\\weapons\\physcannon\\superphys_launch2.wav");
        break;
    default:
        PlayGModSound("physgun_launch_4", "fx\\rem\\gmod\\weapons\\physcannon\\superphys_launch4.wav");
        break;
    }
}

static const GModWeaponSoundDef* FindGModWeaponSoundDef(const char* className)
{
    if (!className) return nullptr;
    for (const auto& soundDef : kGModWeaponSoundDefs)
        if (_stricmp(soundDef.className, className) == 0)
            return &soundDef;
    return nullptr;
}

static void PlayMappedGModActionSound(const char* className)
{
    const GModWeaponSoundDef* soundDef = FindGModWeaponSoundDef(className);
    if (!soundDef || !soundDef->variantCount) return;

    const UInt32 index = g_gmodMappedSoundVariant++ % soundDef->variantCount;
    const char* path = soundDef->variants[index];
    if (path && *path)
        PlayGModSound(path, path, false);
}

static void ApplyGModWeaponNativeSounds(const GModWeaponDef& def, TESObjectWEAP* weapon)
{
    if (!weapon) return;

    // Never inherit audio from the Fallout donor form.
    for (UInt32 i = 0; i < 12; ++i)
        weapon->sounds[i] = nullptr;

    const GModWeaponSoundDef* soundDef = FindGModWeaponSoundDef(def.className);
    if (!soundDef || !soundDef->variantCount)
        return;

    // Custom utilities trigger their Source sounds from explicit runtime actions.
    if (IsCustomUtilityKind(def.kind))
        return;

    const char* path = soundDef->variants[0];
    if (!path || !*path)
        return;

    TESSound* original = GetOrCreateGModSound(path, path, false, false);
    if (!original) return;

    if (def.kind == GModWeaponKind::Melee || def.kind == GModWeaponKind::Grenade)
    {
        weapon->sounds[TESObjectWEAP::kWeapSound_Swing] = original;
        return;
    }

    weapon->sounds[TESObjectWEAP::kWeapSound_Shoot3D] = original;
    weapon->sounds[TESObjectWEAP::kWeapSound_Shoot2D] = original;
}

static TESObjectWEAP* FindGModWeaponTemplate(GModWeaponKind kind)
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList) return nullptr;

    // Exact third-person hold requirements:
    // - Tool Gun clones the 10mm Pistol so it uses that one-hand pistol hold set.
    // - Physics Gun clones the Flamer so it uses the Flamer third-person hold set.
    // The imported GMod NIF still replaces the clone's displayed weapon model below.
    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
        if (!weapon->IsPlayable()) continue;

        if (kind == GModWeaponKind::Toolgun && WeaponNameContains(weapon, "10mm pistol"))
            return weapon;
        if (kind == GModWeaponKind::Physgun && WeaponNameContains(weapon, "flamer"))
            return weapon;
    }

    const UInt8 desired = PreferredFNVWeaponType(kind);
    TESObjectWEAP* fallback = nullptr;

    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
        if (!weapon->IsPlayable() || weapon->eWeaponType != desired) continue;

        if (!fallback) fallback = weapon;

        if (kind == GModWeaponKind::Shotgun && WeaponNameContains(weapon, "shotgun")) return weapon;
        if (kind == GModWeaponKind::Pistol && WeaponNameContains(weapon, "9mm pistol")) return weapon;
        if ((kind == GModWeaponKind::Automatic || kind == GModWeaponKind::Flechette) &&
            (WeaponNameContains(weapon, "smg") || WeaponNameContains(weapon, "machine"))) return weapon;
        if (kind == GModWeaponKind::Rifle && WeaponNameContains(weapon, "rifle")) return weapon;
        if (kind == GModWeaponKind::Launcher && WeaponNameContains(weapon, "missile")) return weapon;
        if (kind == GModWeaponKind::Grenade && WeaponNameContains(weapon, "grenade")) return weapon;
        if (kind == GModWeaponKind::Melee && WeaponNameContains(weapon, "lead pipe")) return weapon;
    }

    return fallback;
}

static void ApplyGModWeaponAnimationProfile(const GModWeaponDef& def, TESObjectWEAP* weapon)
{
    if (!weapon) return;

    TESObjectWEAP* donor = FindGModWeaponTemplate(def.kind);
    if (!donor || donor == weapon) return;

    // Safe primitive-only profile copy for persistent WEAP records.
    // Model, sound and form pointers remain ESP-owned.
    weapon->eWeaponType = donor->eWeaponType;
    weapon->handGrip = donor->handGrip;
    weapon->reloadAnim = donor->reloadAnim;
    weapon->attackAnim = donor->attackAnim;
    weapon->animMult = donor->animMult;
    weapon->animAttackMult = donor->animAttackMult;
    weapon->animShotsPerSec = donor->animShotsPerSec;
    weapon->animReloadTime = donor->animReloadTime;
    weapon->animJamTime = donor->animJamTime;

    const bool donorNo3PIS =
        donor->weaponFlags2.IsSet(TESObjectWEAP::eFlag_No3rdPersonISAnims);
    weapon->weaponFlags2.Write(TESObjectWEAP::eFlag_No3rdPersonISAnims, donorNo3PIS);

    _MESSAGE("[GMOD-WEAP] anim profile %s <- %08X type=%u grip=%u",
        def.className, donor->refID,
        static_cast<unsigned>(weapon->eWeaponType),
        static_cast<unsigned>(weapon->handGrip));
}

static TESObjectWEAP* FindExistingGModWeaponForm(const GModWeaponDef& def)
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList) return nullptr;

    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectWEAP) continue;
        TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);

        const char* name = weapon->fullName.name.m_data;
        if (!name || _stricmp(name, def.displayName) != 0) continue;

        if (!def.worldNif || !*def.worldNif)
            return weapon;

        const char* path = weapon->textureSwap.nifPath.m_data;
        if (path && _stricmp(path, def.worldNif) == 0)
            return weapon;
    }
    return nullptr;
}

static void GiveWeaponToPlayer(TESObjectWEAP* weapon)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !weapon) return;

    char cmd[96];
    std::snprintf(cmd, sizeof(cmd), "additem %08X 1", weapon->refID);
    Script::RunScriptLine2(cmd, player, true);
}

static GModRuntimeWeapon* FindRuntimeGModWeapon(TESObjectWEAP* weapon)
{
    if (!weapon) return nullptr;
    for (auto& runtime : g_gmodRuntimeWeapons)
        if (runtime.weapon == weapon) return &runtime;
    return nullptr;
}

static GModRuntimeWeapon* GetEquippedGModRuntimeWeapon()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player) return nullptr;
    return FindRuntimeGModWeapon(player->GetEquippedWeapon());
}

static void EnsureGModWeaponForms()
{
    if (g_gmodWeaponFormsReady) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell) return;

    g_gmodRuntimeWeapons.clear();
    const size_t defCount = 14;

    for (size_t i = 0; i < defCount; ++i)
    {
        const GModWeaponDef& def = kGModWeaponDefs[i];
        TESObjectWEAP* weapon = FindExistingGModWeaponForm(def);
        TESObjectSTAT* worldStatic = weapon ? weapon->worldStatic : nullptr;
        bool created = false;

        if (!weapon)
        {
            TESObjectWEAP* source = FindGModWeaponTemplate(def.kind);
            if (!source)
            {
                _MESSAGE("[GMOD-WEAP] no FNV template for %s", def.className);
                continue;
            }

            TESForm* cloned = source->CloneForm(true);
            if (!cloned || cloned->typeID != kFormType_TESObjectWEAP)
            {
                _MESSAGE("[GMOD-WEAP] clone failed for %s", def.className);
                continue;
            }

            weapon = static_cast<TESObjectWEAP*>(cloned);
            weapon->fullName.name.Set(def.displayName);
            weapon->weaponFlags1.Write(TESObjectWEAP::eFlag_CantDrop, false);
            weapon->weaponFlags1.Write(TESObjectWEAP::Eflag_NonPlayable, false);

            if (def.worldNif && *def.worldNif)
            {
                weapon->textureSwap.SetPath(const_cast<char*>(def.worldNif));

                if (source->worldStatic)
                {
                    TESForm* wsClone = source->worldStatic->CloneForm(true);
                    if (wsClone && wsClone->typeID == kFormType_TESObjectSTAT)
                    {
                        worldStatic = static_cast<TESObjectSTAT*>(wsClone);
                        worldStatic->model.SetPath(def.worldNif);
                        weapon->worldStatic = worldStatic;
                    }
                }
            }

            if (IsCustomUtilityKind(def.kind))
            {
                weapon->attackDmg.damage = 0;
                weapon->ammo.ammo = nullptr;
                weapon->ammoUse = 0;
                weapon->clipRounds.clipRounds = 0;
                weapon->SetIsAutomatic(false);

                // Do not leak the cloned Fallout weapon's sounds into GMod utilities.
                // Their Source/GMod sounds are played explicitly by the runtime actions.
                for (UInt32 soundIndex = 0; soundIndex < 12; ++soundIndex)
                    weapon->sounds[soundIndex] = nullptr;
            }

            created = true;
            _MESSAGE("[GMOD-WEAP] created %s class=%s form=%08X world=%08X",
                def.displayName, def.className, weapon->refID, weapon->worldStatic ? weapon->worldStatic->refID : 0);
        }
        else
        {
            _MESSAGE("[GMOD-WEAP] reused %s class=%s form=%08X", def.displayName, def.className, weapon->refID);
        }

        ApplyGModWeaponAnimationProfile(def, weapon);

        // v60 crash fix: do not mutate persistent/reused WEAP sound pointer arrays at
        // gameplay startup. v59 crashed while walking the persistent weapon list.
        // Original GMod sounds remain action-triggered by the runtime sound layer;
        // persistent native sound assignment will be rebuilt safely after load.
        if (created)
            ApplyGModWeaponNativeSounds(def, weapon);

        g_gmodRuntimeWeapons.push_back({&def, weapon, worldStatic});

        // Permanent project requirement: imported GMod weapons are real Pip-Boy
        // Weapons entries. This also guarantees Tool Gun, Crowbar and Physics Gun
        // are auto-added on first runtime-form creation; the THUG2 board has its
        // corresponding additem in EnsureSkateboardWeapon().
        if (created || def.autoGive)
            GiveWeaponToPlayer(weapon);
    }

    g_gmodWeaponFormsReady = true;
    char msg[128];
    std::snprintf(msg, sizeof(msg), "[GMOD] %u weapon forms ready", static_cast<unsigned>(g_gmodRuntimeWeapons.size()));
    Notify(msg);
}

static void SetPlayerSpeedMultiplier(PlayerCharacter* player, float value)
{
    // v79: intentionally disabled. Scripted setav SpeedMult was corrupting/entering
    // BaseExtraList during the skate transition. THUG2 speed state remains internal.
    (void)player;
    (void)value;
}

static void SetRefAngleZ(TESObjectREFR* ref, float radians)
{
    if (!ref) return;
    const float degrees = radians * 57.2957795131f;
    char cmd[96];
    std::snprintf(cmd, sizeof(cmd), "setangle z %.3f", degrees);
    Script::RunScriptLine2(cmd, ref, true);
}

static void SetRefAngles(TESObjectREFR* ref, float xRadians, float yRadians, float zRadians)
{
    if (!ref) return;

    const float toDegrees = 57.2957795131f;
    char cmd[96];

    std::snprintf(cmd, sizeof(cmd), "setangle x %.3f", xRadians * toDegrees);
    Script::RunScriptLine2(cmd, ref, true);
    std::snprintf(cmd, sizeof(cmd), "setangle y %.3f", yRadians * toDegrees);
    Script::RunScriptLine2(cmd, ref, true);
    std::snprintf(cmd, sizeof(cmd), "setangle z %.3f", zRadians * toDegrees);
    Script::RunScriptLine2(cmd, ref, true);
}

static void BeginRideBoardVisual()
{
    if (g_skateboardRideRef || g_skateboardRidePendingForm || !g_skateboardWorldStatic)
        return;

    // Reassessed clone strategy: the ride board must also use an ESP-owned form.
    // CloneForm on activation was the last skateboard-side runtime clone path.
    // Spawn the persistent STAT directly; no CloneForm and no SetPath mutation.
    g_skateboardRideStatic = g_skateboardWorldStatic;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
        return;

    _MESSAGE("[THUG2] ride board: place persistent STAT %08X",
        g_skateboardRideStatic->refID);

    char cmd[128];
    std::snprintf(cmd, sizeof(cmd), "placeatme %08X 1 0 0", g_skateboardRideStatic->refID);
    Script::RunScriptLine2(cmd, player, true);

    g_skateboardRideRef = FindReferenceForBaseForm(g_skateboardRideStatic);
    if (!g_skateboardRideRef)
    {
        g_skateboardRidePendingForm = g_skateboardRideStatic;
        g_skateboardRidePendingTick = GetTickCount();
        _MESSAGE("[THUG2] ride board: reference pending");
    }
    else
    {
        _MESSAGE("[THUG2] ride board: reference=%08X", g_skateboardRideRef->refID);
    }
}

static void EndRideBoardVisual()
{
    if (!g_skateboardRideRef && g_skateboardRidePendingForm)
        g_skateboardRideRef = FindReferenceForBaseForm(g_skateboardRidePendingForm);

    if (g_skateboardRideRef)
    {
        Script::RunScriptLine2("disable", g_skateboardRideRef, true);
        Script::RunScriptLine2("markfordelete", g_skateboardRideRef, true);
    }

    g_skateboardRideRef = nullptr;
    g_skateboardRideStatic = nullptr;
    g_skateboardRidePendingForm = nullptr;
    g_skateboardRidePendingTick = 0;
}

static void UpdateRideBoardVisual()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !g_skate.active) return;

    if (!g_skateboardRideRef && g_skateboardRidePendingForm)
    {
        g_skateboardRideRef = FindReferenceForBaseForm(g_skateboardRidePendingForm);
        if (g_skateboardRideRef)
        {
            g_skateboardRidePendingForm = nullptr;
            g_skateboardRidePendingTick = 0;
        }
        else if (GetTickCount() - g_skateboardRidePendingTick > 3000)
        {
            g_skateboardRidePendingForm = nullptr;
            g_skateboardRidePendingTick = 0;
        }
    }

    if (!g_skateboardRideRef) return;

    SetRefPosition(g_skateboardRideRef, player->posX, player->posY, player->posZ - 3.0f);
    const float toRadians = 0.0174532925199f;
    const float trickSpinRadians = (g_skate.moveState == SkateMoveState::Air)
        ? (g_skate.spinDegrees * toRadians)
        : 0.0f;
    const float trickFlipRadians = (g_skate.moveState == SkateMoveState::Air)
        ? (g_skate.flipDegrees * toRadians)
        : 0.0f;
    SetRefAngles(g_skateboardRideRef, trickFlipRadians, 0.0f,
        player->rotZ + trickSpinRadians);
}

#include "thug2_hud_visibility.inc"

static void EnterSkateMode()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || g_skate.active) return;

    g_skate.active = true;
    UpdateFalloutHudOwnership(true);
    g_skate.moveState = SkateMoveState::Ground;
    g_skate.velocityX = 0.0f;
    g_skate.velocityY = 0.0f;
    g_skate.velocityZ = 0.0f;
    g_skate.spinDegrees = 0.0f;
    g_skate.flipDegrees = 0.0f;
    g_skate.flipRemaining = 0.0f;
    g_skate.balance = 0.0f;
    g_skate.comboScore = 0.0f;
    g_skate.comboMultiplier = 1.0f;
    g_skate.totalScore = 0.0f;
    g_skate.special01 = 0.0f;
    g_skate.comboActive = false;
    g_skate.trickCount = 0;
    g_skate.manualVariant = 0;
    g_skate.grindVariant = 0;
    g_skate.lipVariant = 0;
    g_skate.comboBankDeadline = 0;
    g_skate.lastTrick[0] = 0;
    g_skate.speed01 = 0.32f;
    g_skate.originalSpeedMult = player->avOwner.Fn_03(eActorVal_SpeedMultiplier);
    if (g_skate.originalSpeedMult < 1.0f || !std::isfinite(g_skate.originalSpeedMult))
        g_skate.originalSpeedMult = 100.0f;
    g_skate.lastTick = GetTickCount();
    g_skate.lastSpeedApplyTick = 0;
    g_skate.lastHudTick = 0;
    g_skate.jumpWasDown = false;
    g_skate.flipWasDown = false;
    g_skate.grabWasDown = false;
    g_skate.forwardHoldInjected = false;
    g_skate.nollieActive = false;
    g_skate.nollieToggleWasDown = false;
    g_skate.pressureActive = false;
    g_skate.pressureToggleWasDown = false;
    g_skate.revertWasDown = false;
    g_skate.revertAvailable = false;
    g_skate.skitchWasDown = false;
    g_skate.skitchTargetRefID = 0;

    g_skate.fightWasDisabled = (player->disabledControlFlags & PlayerCharacter::kControlFlag_Fight) != 0;
    g_skate.cameraWasThirdPerson = player->bThirdPerson;
    g_skate.originalFov = ReadCurrentWorldFov();
    // v83 crash evidence + visible upward camera pan implicates the raw Camera3rd
    // transform path.  Quarantine it completely: only use New Vegas's public
    // third-person switch until the camera node layout is re-verified in IDA 6.8.
    g_skate.thugCamNodeSaved = false;

    // Skate mode owns movement/combat input, but merely equipping the board does not.
    player->disabledControlFlags |= PlayerCharacter::kControlFlag_Fight;
    _MESSAGE("[THUG2] skate enter: Fight suppressed; held board retained");

    // Force third person through the documented camera state only. Writing unk64A
    // directly conflicts with New Vegas camera internals and caused the broken view.
    _MESSAGE("[THUG2] skate enter: camera switch begin");
    player->bThirdPerson = true;
    player->UpdateCamera(false, false);
    _MESSAGE("[THUG2] skate enter: UpdateCamera complete");
    _MESSAGE("[THUG2] skate enter: raw THUG2 camera profile QUARANTINED; vanilla FNV third-person active");

    g_physgunEnabled = false;
    g_toolgunEnabled = false;
    DropHeld();

    ClearTHUG2RetargetCacheNoRestore();
    g_thug2RetargetEarliestTick = GetTickCount() + 900;
    g_thug2FirstUpdateDiag = false;
    g_thug2DiagFrameCount = 0;
    if (kTHUG2RetargetDiagnosticEnabled)
    {
        LoadTHUG2RetargetBank();
        // Bone resolution is deferred until the third-person actor graph has remained
        // stable for 900 ms after the camera transition.
        StartTHUG2RetargetClip("idle", true, true);
        _MESSAGE("[THUG2] skate enter: animation armed; bone resolve deferred");
    }
    else
    {
        _MESSAGE("[THUG2-DIAG] v85 retarget subsystem QUARANTINED");
    }
    BeginRideBoardVisual();
    _MESSAGE("[THUG2] skate enter: ride board requested");
    PlayTHUG2BoardRollSound();
    _MESSAGE("[THUG2] skate enter: board roll sound complete");
    SetPlayerSpeedMultiplier(player, g_skate.originalSpeedMult * 0.85f);
    _MESSAGE("[THUG2] skate enter: speed path bypassed safely");
    UpdateTHUGHudOverlay();
    _MESSAGE("[THUG2] skate enter: HUD complete");

    Notify("[THUG2] Skate ON - Space jump, N nollie, P pressure, V revert, K skitch, M manual, G grind, L lip, Q/E spin or cycle, LMB+RMB special, R exit");
}

static void ExitSkateMode()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !g_skate.active) return;

    g_skate.active = false;
    UpdateFalloutHudOwnership(false);

    if (!g_skate.fightWasDisabled)
        player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Fight;

    // Restore the exact camera style the player was using before deploying the board.
    player->bThirdPerson = g_skate.cameraWasThirdPerson;
    player->UpdateCamera(false, false);
    // No raw camera-node transform was touched in v84, so there is nothing to restore.
    g_skate.thugCamNodeSaved = false;
    ApplyGModCameraFov(player, g_skate.originalFov);
    UpdateTHUGHudOverlay();

    // Release the xNVSE-injected forward hold before restoring normal Fallout input.
    if (g_skate.forwardHoldInjected)
    {
        Script::RunScriptLine2("releasekey 17", player, true); // DirectInput DIK_W
        g_skate.forwardHoldInjected = false;
    }

    RestoreTHUG2RetargetBones(player);

    // Restore the exact pre-skate movement multiplier and remove the ride-only board visual.
    SetPlayerSpeedMultiplier(player, g_skate.originalSpeedMult);
    EndRideBoardVisual();

    // The skateboard remains the same equipped inventory weapon; draw it again for normal FNV use.
    player->SetWantsWeaponOut(true);

    g_skate.velocityX = g_skate.velocityY = g_skate.velocityZ = 0.0f;
    g_skate.spinDegrees = 0.0f;
    g_skate.flipDegrees = 0.0f;
    g_skate.flipRemaining = 0.0f;
    g_skate.balance = 0.0f;
    g_skate.speed01 = 0.0f;
    g_skate.skitchTargetRefID = 0;
    g_skate.skitchWasDown = false;
    ResetActiveSkateCombo();
    Notify("[THUG2] Skate mode OFF - Fallout movement restored");
}

static void ToggleSkateMode()
{
    if (g_skate.active) ExitSkateMode();
    else EnterSkateMode();
}

static void SetRefPosition(TESObjectREFR* ref, float x, float y, float z)
{
    if (!ref) return;
    char cmd[128];

    std::snprintf(cmd, sizeof(cmd), "setpos x %.3f", x);
    Script::RunScriptLine2(cmd, ref, true);
    std::snprintf(cmd, sizeof(cmd), "setpos y %.3f", y);
    Script::RunScriptLine2(cmd, ref, true);
    std::snprintf(cmd, sizeof(cmd), "setpos z %.3f", z);
    Script::RunScriptLine2(cmd, ref, true);
}

static bool IsFrozenRef(UInt32 refID)
{
    for (const auto& frozen : g_frozenProps)
        if (frozen.refID == refID)
            return true;
    return false;
}

static void FreezeRef(TESObjectREFR* ref)
{
    if (!ref || IsActorReference(ref))
    {
        Notify("[GMOD] Physgun freeze: invalid target");
        return;
    }

    for (auto& frozen : g_frozenProps)
    {
        if (frozen.refID == ref->refID)
        {
            frozen.x = ref->posX;
            frozen.y = ref->posY;
            frozen.z = ref->posZ;
            Notify("[GMOD] Physgun freeze position updated");
            return;
        }
    }

    GModFrozenBinding frozen;
    frozen.refID = ref->refID;
    frozen.x = ref->posX;
    frozen.y = ref->posY;
    frozen.z = ref->posZ;
    g_frozenProps.push_back(frozen);

    if (void* body = GetRootHavokRigidBody(ref))
        SetHavokLinearVelocity(body, 0.0f, 0.0f, 0.0f);

    Notify("[GMOD] Physgun frozen");
}

static void UnfreezeRef(TESObjectREFR* ref)
{
    if (!ref)
    {
        Notify("[GMOD] Physgun unfreeze: no target");
        return;
    }

    for (auto it = g_frozenProps.begin(); it != g_frozenProps.end(); ++it)
    {
        if (it->refID == ref->refID)
        {
            g_frozenProps.erase(it);
            Notify("[GMOD] Physgun unfrozen");
            return;
        }
    }

    Notify("[GMOD] Target is not frozen");
}

static void FreezeHeld()
{
    if (!g_heldRef)
    {
        Notify("[GMOD] Physgun freeze: nothing held");
        return;
    }

    TESObjectREFR* ref = g_heldRef;
    g_heldRef = nullptr;
    FreezeRef(ref);
}

static void UpdateFrozenProps()
{
    const DWORD now = GetTickCount();
    if (now - g_frozenUpdateTick < 50)
        return;
    g_frozenUpdateTick = now;

    for (auto it = g_frozenProps.begin(); it != g_frozenProps.end(); )
    {
        TESForm* form = LookupFormByID(it->refID);
        if (!form || !form->GetIsReference())
        {
            it = g_frozenProps.erase(it);
            continue;
        }

        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        if (void* body = GetRootHavokRigidBody(ref))
            SetHavokLinearVelocity(body, 0.0f, 0.0f, 0.0f);

        SetRefPosition(ref, it->x, it->y, it->z);
        ++it;
    }
}

static void ToggleNoClip()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !g_gameplayReady)
        return;

    if (!g_noClip)
    {
        g_noClipMovementWasDisabled =
            (player->disabledControlFlags & PlayerCharacter::kControlFlag_Movement) != 0;
        player->disabledControlFlags |= PlayerCharacter::kControlFlag_Movement;
        Script::RunScriptLine2("tcl", player, true);
        g_noClip = true;
        g_noClipLastTick = GetTickCount();
        Notify("[GMOD] Noclip ON - WASD/Space/Ctrl, Shift boost");
    }
    else
    {
        Script::RunScriptLine2("tcl", player, true);
        if (!g_noClipMovementWasDisabled)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Movement;
        g_noClip = false;
        Notify("[GMOD] Noclip OFF");
    }
}

static void UpdateNoClip()
{
    if (!g_noClip || !g_gameplayReady)
        return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
        return;

    const DWORD now = GetTickCount();
    if (!g_noClipLastTick)
        g_noClipLastTick = now;

    float dt = (now - g_noClipLastTick) / 1000.0f;
    if (dt <= 0.0f) return;
    if (dt > 0.05f) dt = 0.05f;
    g_noClipLastTick = now;

    const float yaw = player->rotZ;
    const float pitch = player->rotX;
    const float cp = std::cos(pitch);
    const float forwardX = std::sin(yaw) * cp;
    const float forwardY = std::cos(yaw) * cp;
    const float forwardZ = -std::sin(pitch);
    const float rightX = std::cos(yaw);
    const float rightY = -std::sin(yaw);

    float dx = 0.0f, dy = 0.0f, dz = 0.0f;
    if (GetAsyncKeyState('W') & 0x8000) { dx += forwardX; dy += forwardY; dz += forwardZ; }
    if (GetAsyncKeyState('S') & 0x8000) { dx -= forwardX; dy -= forwardY; dz -= forwardZ; }
    if (GetAsyncKeyState('D') & 0x8000) { dx += rightX; dy += rightY; }
    if (GetAsyncKeyState('A') & 0x8000) { dx -= rightX; dy -= rightY; }
    if (GetAsyncKeyState(VK_SPACE) & 0x8000) dz += 1.0f;
    if (GetAsyncKeyState(VK_CONTROL) & 0x8000) dz -= 1.0f;

    const float magSq = dx * dx + dy * dy + dz * dz;
    if (magSq <= 0.0001f)
        return;

    const float invMag = 1.0f / std::sqrt(magSq);
    dx *= invMag; dy *= invMag; dz *= invMag;

    float speed = 700.0f;
    if (GetAsyncKeyState(VK_SHIFT) & 0x8000)
        speed *= 3.0f;

    SetRefPosition(player,
        player->posX + dx * speed * dt,
        player->posY + dy * speed * dt,
        player->posZ + dz * speed * dt);
}

static const char* GModVehicleKindName(GModVehicleKind kind)
{
    switch (kind)
    {
    case GModVehicleKind::Buggy: return "Buggy";
    case GModVehicleKind::Airboat: return "Airboat";
    case GModVehicleKind::Jalopy: return "Jalopy";
    case GModVehicleKind::GenericLand: return "Source Vehicle";
    case GModVehicleKind::GenericBoat: return "Source Boat";
    case GModVehicleKind::Seat: return "Vehicle Seat";
    default: return "Vehicle";
    }
}

static GModVehicleKind GetGModVehicleKind(TESObjectREFR* ref)
{
    if (!ref || !ref->baseForm) return GModVehicleKind::None;

    TESModel* model = DYNAMIC_CAST(ref->baseForm, TESForm, TESModel);
    if (!model || !model->nifPath.m_data) return GModVehicleKind::None;

    char path[320] = {};
    strncpy_s(path, sizeof(path), model->nifPath.m_data, _TRUNCATE);
    _strlwr_s(path, sizeof(path));
    for (char* p = path; *p; ++p)
        if (*p == '/') *p = '\\';

    if (std::strstr(path, "rem\\gmod\\buggy.nif")) return GModVehicleKind::Buggy;
    if (std::strstr(path, "rem\\gmod\\airboat.nif")) return GModVehicleKind::Airboat;
    if (std::strstr(path, "rem\\gmod\\vehicle.nif")) return GModVehicleKind::Jalopy;

    // Narrow recognition for converted HL2/GMod vehicle physics bodies.
    if (std::strstr(path, "rem\\gmod\\props_vehicles\\") &&
        (std::strstr(path, "car001") ||
         std::strstr(path, "car002") ||
         std::strstr(path, "car003") ||
         std::strstr(path, "car004") ||
         std::strstr(path, "car005") ||
         std::strstr(path, "van001") ||
         std::strstr(path, "truck001") ||
         std::strstr(path, "truck002") ||
         std::strstr(path, "truck003") ||
         std::strstr(path, "apc001") ||
         std::strstr(path, "wagon001")))
        return GModVehicleKind::GenericLand;

    if ((std::strstr(path, "rem\\gmod\\props_canal\\boat") ||
         std::strstr(path, "rem\\gmod\\props_wasteland\\boat_") ||
         std::strstr(path, "rem\\gmod\\props_wasteland\\boat_fishing")) &&
        !std::strstr(path, "gib"))
        return GModVehicleKind::GenericBoat;

    // Converted Source vehicle bodies outside props_vehicles.
    // Keep doors/arms/rotators as ordinary props rather than accidentally making them driveable.
    if (std::strstr(path, "rem\\gmod\\vehicles\\vehicle_van.nif"))
        return GModVehicleKind::GenericLand;

    if (std::strstr(path, "rem\\gmod\\vehicles\\prisoner_pod.nif") ||
        std::strstr(path, "rem\\gmod\\vehicles\\prisoner_pod_inner.nif") ||
        std::strstr(path, "rem\\gmod\\nova\\jeep_seat.nif") ||
        std::strstr(path, "rem\\gmod\\nova\\airboat_seat.nif") ||
        std::strstr(path, "rem\\gmod\\nova\\jalopy_seat.nif"))
        return GModVehicleKind::Seat;

    return GModVehicleKind::None;
}

static float GModVehicleSeatHeight(GModVehicleKind kind)
{
    switch (kind)
    {
    case GModVehicleKind::Airboat: return 72.0f;
    case GModVehicleKind::Buggy: return 64.0f;
    case GModVehicleKind::Jalopy: return 66.0f;
    case GModVehicleKind::GenericLand: return 72.0f;
    case GModVehicleKind::GenericBoat: return 68.0f;
    case GModVehicleKind::Seat: return 42.0f;
    default: return 60.0f;
    }
}

static float GModVehicleTopSpeed(GModVehicleKind kind)
{
    switch (kind)
    {
    case GModVehicleKind::Airboat: return 1150.0f;
    case GModVehicleKind::Jalopy: return 1050.0f;
    case GModVehicleKind::Buggy: return 950.0f;
    case GModVehicleKind::GenericLand: return 760.0f;
    case GModVehicleKind::GenericBoat: return 820.0f;
    default: return 0.0f;
    }
}

static void ExitGModVehicle()
{
    if (!g_vehicle.active) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    TESObjectREFR* vehicle = LookupReference(g_vehicle.refID);

    if (player)
    {
        if (!g_vehicle.movementWasDisabled)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Movement;
        if (!g_vehicle.fightWasDisabled)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Fight;

        player->bThirdPerson = g_vehicle.cameraWasThirdPerson;
        player->unk64A = g_vehicle.cameraWasThirdPerson;
        player->UpdateCamera(false, false);
        player->SetWantsWeaponOut(true);

        if (vehicle)
        {
            const float yaw = vehicle->rotZ;
            const float sideX = std::cos(yaw) * 125.0f;
            const float sideY = -std::sin(yaw) * 125.0f;
            SetRefPosition(player,
                vehicle->posX + sideX,
                vehicle->posY + sideY,
                vehicle->posZ + 45.0f);
        }
    }

    g_vehicle = GModVehicleState{};
    Notify("[GMOD] Exited vehicle");
}

static void EnterGModVehicle(TESObjectREFR* vehicle, GModVehicleKind kind)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !vehicle || kind == GModVehicleKind::None) return;

    if (g_noClip)
        ToggleNoClip();
    if (g_skate.active)
        ExitSkateMode();
    if (g_heldRef)
        DropHeld();

    GModVehicleState state;
    state.active = true;
    state.refID = vehicle->refID;
    state.kind = kind;
    state.movementWasDisabled =
        (player->disabledControlFlags & PlayerCharacter::kControlFlag_Movement) != 0;
    state.fightWasDisabled =
        (player->disabledControlFlags & PlayerCharacter::kControlFlag_Fight) != 0;
    state.cameraWasThirdPerson = player->bThirdPerson;
    state.useWasDown = true;
    state.lastTick = GetTickCount();
    state.lastHudTick = 0;
    g_vehicle = state;

    player->disabledControlFlags |=
        PlayerCharacter::kControlFlag_Movement | PlayerCharacter::kControlFlag_Fight;
    player->SetWantsWeaponOut(false);
    player->unk64A = true;
    player->bThirdPerson = true;
    player->UpdateCamera(false, false);

    char msg[128];
    std::snprintf(msg, sizeof(msg), "[GMOD] Entered %s - WASD drive, Space brake, E exit",
        GModVehicleKindName(kind));
    Notify(msg);
}

static void UpdateGModVehicle()
{
    if (!g_gameplayReady) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell) return;

    const bool useDown = (GetAsyncKeyState('E') & 0x8000) != 0;
    const bool usePressed = useDown && !g_vehicle.useWasDown;

    if (!g_vehicle.active)
    {
        if (usePressed)
        {
            TESObjectREFR* target = GetCrosshairTarget();
            const GModVehicleKind kind = GetGModVehicleKind(target);
            if (kind != GModVehicleKind::None)
            {
                EnterGModVehicle(target, kind);
                return;
            }
        }
        g_vehicle.useWasDown = useDown;
        return;
    }

    TESObjectREFR* vehicle = LookupReference(g_vehicle.refID);
    if (!vehicle)
    {
        ExitGModVehicle();
        return;
    }

    if (usePressed)
    {
        ExitGModVehicle();
        return;
    }
    g_vehicle.useWasDown = useDown;

    const DWORD now = GetTickCount();
    float dt = (now - g_vehicle.lastTick) / 1000.0f;
    if (dt <= 0.0f) dt = 0.001f;
    if (dt > 0.05f) dt = 0.05f;
    g_vehicle.lastTick = now;

    void* body = GetRootHavokRigidBody(vehicle);
    float vx = 0.0f, vy = 0.0f, vz = 0.0f;
    if (body)
        GetHavokLinearVelocity(body, vx, vy, vz);

    if (g_vehicle.kind != GModVehicleKind::Seat && body)
    {
        const bool forward = (GetAsyncKeyState('W') & 0x8000) != 0;
        const bool reverse = (GetAsyncKeyState('S') & 0x8000) != 0;
        const bool left = (GetAsyncKeyState('A') & 0x8000) != 0;
        const bool right = (GetAsyncKeyState('D') & 0x8000) != 0;
        const bool handbrake = (GetAsyncKeyState(VK_SPACE) & 0x8000) != 0;

        float throttle = 0.0f;
        if (forward && !reverse) throttle = 1.0f;
        if (reverse && !forward) throttle = -0.65f;

        const float yaw = vehicle->rotZ;
        const float fx = std::sin(yaw);
        const float fy = std::cos(yaw);
        const float topSpeed = GModVehicleTopSpeed(g_vehicle.kind);

        if (throttle != 0.0f)
        {
            const float targetVX = fx * topSpeed * throttle;
            const float targetVY = fy * topSpeed * throttle;
            float blend = dt * 3.4f;
            if (blend > 1.0f) blend = 1.0f;
            vx += (targetVX - vx) * blend;
            vy += (targetVY - vy) * blend;
        }
        else
        {
            const float coast = std::pow(0.36f, dt);
            vx *= coast;
            vy *= coast;
        }

        if (handbrake)
        {
            vx *= 0.68f;
            vy *= 0.68f;
        }

        float steer = 0.0f;
        if (left && !right) steer = 1.0f;
        if (right && !left) steer = -1.0f;
        const float horizontalSpeed = std::sqrt(vx * vx + vy * vy);
        if (steer != 0.0f && (horizontalSpeed > 15.0f || throttle != 0.0f))
        {
            const float direction = (throttle < 0.0f) ? -1.0f : 1.0f;
            const float turnRate =
                (g_vehicle.kind == GModVehicleKind::Airboat ||
                 g_vehicle.kind == GModVehicleKind::GenericBoat) ? 1.25f : 1.65f;
            SetRefAngleZ(vehicle, vehicle->rotZ + steer * direction * turnRate * dt);
        }

        // Preserve native vertical Havok velocity so ramps, falls and collisions still work.
        SetHavokLinearVelocity(body, vx, vy, vz);
    }

    const float seatHeight = GModVehicleSeatHeight(g_vehicle.kind);
    SetRefPosition(player, vehicle->posX, vehicle->posY, vehicle->posZ + seatHeight);

    if (now - g_vehicle.lastHudTick >= 700)
    {
        char hud[128];
        const int speed = static_cast<int>(std::sqrt(vx * vx + vy * vy));
        std::snprintf(hud, sizeof(hud), "[GMOD] %s  SPEED %d",
            GModVehicleKindName(g_vehicle.kind), speed);
        if (QueueUIMessage) QueueUIMessage(hud, 2, nullptr, nullptr, 0.7f, false);
        g_vehicle.lastHudTick = now;
    }
}

static void DropHeld()
{
    if (!g_heldRef) return;

    TESObjectREFR* released = g_heldRef;
    const bool actorRelease = IsActorReference(released);

    if (void* rigidBody = GetRootHavokRigidBody(released))
        SetHavokLinearVelocity(rigidBody, 0.0f, 0.0f, 0.0f);

    g_heldRef = nullptr;
    PlayPhysgunDropSound();

    if (actorRelease)
    {
        if (g_physgunHeldUsingRagdollBodies)
            SetActorRagdollLinearVelocity(released, 0.0f, 0.0f, 0.0f);

        TrySetActorKnockedState(released, g_physgunHeldOriginalKnockedState);
        Script::RunScriptLine2("setunconscious 0", released, true);
        g_physgunHeldOriginalKnockedState = 0;
        g_physgunHeldForcedKnockedState = 1;
        g_physgunHeldUsingRagdollBodies = false;
        Notify("[GMOD] Physgun released NPC");
    }
    else
    {
        Notify("[GMOD] Physgun released");
    }
}

static void TogglePhysgun()
{
    if (g_skate.active)
        ToggleSkateMode();
    g_physgunEnabled = !g_physgunEnabled;
    if (g_physgunEnabled)
        g_toolgunEnabled = false;
    if (!g_physgunEnabled) DropHeld();
    Notify(g_physgunEnabled ? "[GMOD] Physgun mode ON" : "[GMOD] Physgun mode OFF");
}

static void ToggleToolgun()
{
    if (g_skate.active)
        ToggleSkateMode();
    g_toolgunEnabled = !g_toolgunEnabled;
    if (g_toolgunEnabled)
    {
        g_physgunEnabled = false;
        DropHeld();
    }
    Notify(g_toolgunEnabled ? "[GMOD] Toolgun ON - Remover" : "[GMOD] Toolgun OFF");
}

static void ToolgunRemove()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Remover: no valid target");
        return;
    }
    char msg[96];
    std::snprintf(msg, sizeof(msg), "[GMOD] Removed %08X", target->refID);
    g_undoDisabled.push_back(target->refID);
    Script::RunScriptLine2("disable", target, true);
    Notify(msg);
}

static void UndoLastRemoved()
{
    while (!g_undoDisabled.empty())
    {
        UInt32 refID = g_undoDisabled.back();
        g_undoDisabled.pop_back();

        TESForm* form = LookupFormByID(refID);
        if (!form || !form->GetIsReference())
            continue;

        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        Script::RunScriptLine2("enable", ref, true);

        char msg[96];
        std::snprintf(msg, sizeof(msg), "[GMOD] Undo restored %08X", refID);
        Notify(msg);
        return;
    }

    Notify("[GMOD] Nothing to undo");
}

static UInt32 GetToolModeCount()
{
    return static_cast<UInt32>(sizeof(kGModToolDefs) / sizeof(kGModToolDefs[0]));
}

static const GModToolDef* GetSelectedToolMode()
{
    const UInt32 count = GetToolModeCount();
    if (!count) return nullptr;
    if (g_toolModeIndex >= count)
        g_toolModeIndex = 0;
    return &kGModToolDefs[g_toolModeIndex];
}

static void ShowToolModeStatus()
{
    const GModToolDef* tool = GetSelectedToolMode();
    if (!tool) return;

    char msg[256];
    std::snprintf(msg, sizeof(msg),
        "[GMOD TOOL] %s / %s  [%u/%u] | R next  Shift+R previous",
        tool->category,
        tool->displayName,
        static_cast<unsigned>(g_toolModeIndex + 1),
        static_cast<unsigned>(GetToolModeCount()));
    Notify(msg);
    g_toolModeHudTick = GetTickCount();
}

static void CycleToolMode(int delta)
{
    const int count = static_cast<int>(GetToolModeCount());
    if (count <= 0) return;

    int next = static_cast<int>(g_toolModeIndex) + delta;
    while (next < 0) next += count;
    while (next >= count) next -= count;
    g_toolModeIndex = static_cast<UInt32>(next);
    g_constraintFirstRefID = 0;
    g_buttonFirstRefID = 0;
    PlayGModUISound("ui_click", "fx\\rem\\gmod\\garrysmod\\ui_click.wav");
    ShowToolModeStatus();
}

static void GetPlayerAimDirection(float& x, float& y, float& z)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player)
    {
        x = 0.0f; y = 1.0f; z = 0.0f;
        return;
    }

    const float yaw = player->rotZ;
    const float pitch = player->rotX;
    const float cp = std::cos(pitch);
    x = std::sin(yaw) * cp;
    y = std::cos(yaw) * cp;
    z = -std::sin(pitch);
}

static bool ApplyToolAimVelocity(TESObjectREFR* target, float speed)
{
    if (!target) return false;

    if (IsActorReference(target))
    {
        char cmd[64];
        const float magnitude = speed >= 0.0f ? 12.0f : -8.0f;
        std::snprintf(cmd, sizeof(cmd), "pushactoraway player %.1f", magnitude);
        Script::RunScriptLine2(cmd, target, true);
        return true;
    }

    void* rigidBody = GetRootHavokRigidBody(target);
    if (!rigidBody) return false;

    float x, y, z;
    GetPlayerAimDirection(x, y, z);
    SetHavokLinearVelocity(rigidBody, x * speed, y * speed, z * speed);
    return true;
}

static void ToolgunLeafblower()
{
    static DWORD lastApplyTick = 0;

    const DWORD now = GetTickCount();
    if (now - lastApplyTick < 16)
        return;
    lastApplyTick = now;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    TESObjectREFR* target = GetCrosshairTarget();
    if (!player || !target || IsActorReference(target))
        return;

    const float dx = target->posX - player->posX;
    const float dy = target->posY - player->posY;
    const float dz = target->posZ - player->posZ;
    const float distance = std::sqrt(dx * dx + dy * dy + dz * dz);
    const float maxDistance = 512.0f;

    if (distance < 1.0f || distance >= maxDistance)
        return;

    void* rigidBody = GetRootHavokRigidBody(target);
    if (!rigidBody)
        return;

    // Mirrors Garry's Mod leafblower.lua: force falls off to zero at 512 units
    // and points from the trace start toward the hit position.
    float ratio = 1.0f - (distance / maxDistance);
    if (ratio < 0.0f) ratio = 0.0f;
    if (ratio > 1.0f) ratio = 1.0f;

    const float invDistance = 1.0f / distance;
    const float impulse = 42.0f * ratio;

    float vx = 0.0f, vy = 0.0f, vz = 0.0f;
    GetHavokLinearVelocity(rigidBody, vx, vy, vz);
    vx += dx * invDistance * impulse;
    vy += dy * invDistance * impulse;
    vz += dz * invDistance * impulse;
    SetHavokLinearVelocity(rigidBody, vx, vy, vz);
}

static void ToolgunToggleThruster(bool reverse)
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Thruster: no valid target");
        return;
    }

    for (auto it = g_toolThrusters.begin(); it != g_toolThrusters.end(); ++it)
    {
        if (it->refID == target->refID)
        {
            g_toolThrusters.erase(it);
            Notify("[GMOD] Thruster removed");
            return;
        }
    }

    if (!GetRootHavokRigidBody(target))
    {
        Notify("[GMOD] Thruster: target has no rigid body");
        return;
    }

    float x, y, z;
    GetPlayerAimDirection(x, y, z);
    if (reverse)
    {
        x = -x; y = -y; z = -z;
    }

    GModThrusterBinding binding;
    binding.refID = target->refID;
    binding.dirX = x;
    binding.dirY = y;
    binding.dirZ = z;
    binding.speed = 650.0f;
    g_toolThrusters.push_back(binding);
    Notify(reverse ? "[GMOD] Reverse thruster attached" : "[GMOD] Thruster attached");
}

static void ToolgunToggleHoverball()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Hoverball: no valid target");
        return;
    }

    for (auto it = g_toolHoverballs.begin(); it != g_toolHoverballs.end(); ++it)
    {
        if (it->refID == target->refID)
        {
            g_toolHoverballs.erase(it);
            Notify("[GMOD] Hoverball removed");
            return;
        }
    }

    if (!GetRootHavokRigidBody(target))
    {
        Notify("[GMOD] Hoverball: target has no rigid body");
        return;
    }

    GModHoverBinding binding;
    binding.refID = target->refID;
    binding.targetZ = target->posZ + 120.0f;
    g_toolHoverballs.push_back(binding);
    Notify("[GMOD] Hoverball attached (+120 height)");
}

static bool IsConstraintToolId(const char* id)
{
    if (!id) return false;
    return _stricmp(id, "weld") == 0 ||
        _stricmp(id, "elastic") == 0 ||
        _stricmp(id, "rope") == 0 ||
        _stricmp(id, "hydraulic") == 0 ||
        _stricmp(id, "muscle") == 0 ||
        _stricmp(id, "slider") == 0 ||
        _stricmp(id, "axis") == 0 ||
        _stricmp(id, "ballsocket") == 0 ||
        _stricmp(id, "winch") == 0 ||
        _stricmp(id, "pulley") == 0;
}

static GModConstraintKind ConstraintKindForTool(const char* id)
{
    if (_stricmp(id, "weld") == 0)
        return GModConstraintKind::Weld;
    if (_stricmp(id, "axis") == 0 || _stricmp(id, "ballsocket") == 0)
        return GModConstraintKind::Pivot;
    if (_stricmp(id, "rope") == 0)
        return GModConstraintKind::Rope;
    if (_stricmp(id, "slider") == 0)
        return GModConstraintKind::Slider;
    if (_stricmp(id, "hydraulic") == 0)
        return GModConstraintKind::Hydraulic;
    if (_stricmp(id, "muscle") == 0)
        return GModConstraintKind::Muscle;
    if (_stricmp(id, "winch") == 0)
        return GModConstraintKind::Winch;
    if (_stricmp(id, "pulley") == 0)
        return GModConstraintKind::Pulley;
    return GModConstraintKind::Distance;
}

static float ConstraintStiffnessForTool(const char* id)
{
    if (_stricmp(id, "weld") == 0) return 12.0f;
    if (_stricmp(id, "axis") == 0 || _stricmp(id, "ballsocket") == 0) return 10.0f;
    if (_stricmp(id, "elastic") == 0) return 4.0f;
    if (_stricmp(id, "hydraulic") == 0 || _stricmp(id, "muscle") == 0) return 5.5f;
    if (_stricmp(id, "slider") == 0) return 8.0f;
    return 7.0f;
}

static TESObjectREFR* LookupReference(UInt32 refID)
{
    TESForm* form = LookupFormByID(refID);
    if (!form || !form->GetIsReference())
        return nullptr;
    return static_cast<TESObjectREFR*>(form);
}

static void ToolgunConstraintClick(const char* id)
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || IsActorReference(target))
    {
        Notify("[GMOD] Constraint: aim at a physics prop");
        return;
    }

    if (!g_constraintFirstRefID)
    {
        g_constraintFirstRefID = target->refID;
        char msg[128];
        std::snprintf(msg, sizeof(msg), "[GMOD] %s: first prop selected %08X", id, target->refID);
        Notify(msg);
        return;
    }

    TESObjectREFR* a = LookupReference(g_constraintFirstRefID);
    TESObjectREFR* b = target;
    if (!a || a == b)
    {
        g_constraintFirstRefID = 0;
        Notify("[GMOD] Constraint cancelled");
        return;
    }

    if (!GetRootHavokRigidBody(b))
    {
        g_constraintFirstRefID = 0;
        Notify("[GMOD] Constraint: second prop has no movable rigid body");
        return;
    }

    const float dx = b->posX - a->posX;
    const float dy = b->posY - a->posY;
    const float dz = b->posZ - a->posZ;
    float dist = std::sqrt(dx * dx + dy * dy + dz * dz);
    if (dist < 0.001f) dist = 0.001f;

    GModConstraintBinding binding;
    binding.refA = a->refID;
    binding.refB = b->refID;
    binding.kind = ConstraintKindForTool(id);
    binding.offX = dx;
    binding.offY = dy;
    binding.offZ = dz;
    binding.rotOffX = b->rotX - a->rotX;
    binding.rotOffY = b->rotY - a->rotY;
    binding.rotOffZ = b->rotZ - a->rotZ;
    binding.axisX = dx / dist;
    binding.axisY = dy / dist;
    binding.axisZ = dz / dist;
    binding.restDistance = dist;
    binding.baseDistance = dist;
    binding.minDistance = dist * 0.55f;
    binding.maxDistance = dist * 1.45f;
    binding.stiffness = ConstraintStiffnessForTool(id);
    binding.createdTick = GetTickCount();
    g_toolConstraints.push_back(binding);
    g_constraintFirstRefID = 0;

    char msg[160];
    std::snprintf(msg, sizeof(msg), "[GMOD] %s constraint linked %08X <-> %08X", id, a->refID, b->refID);
    Notify(msg);
}

static void ToolgunRemoveConstraintsOnTarget()
{
    if (g_constraintFirstRefID)
    {
        g_constraintFirstRefID = 0;
        Notify("[GMOD] Constraint selection cancelled");
        return;
    }

    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Constraint remove: no target");
        return;
    }

    UInt32 removed = 0;
    for (auto it = g_toolConstraints.begin(); it != g_toolConstraints.end(); )
    {
        if (it->refA == target->refID || it->refB == target->refID)
        {
            it = g_toolConstraints.erase(it);
            ++removed;
        }
        else ++it;
    }

    char msg[96];
    std::snprintf(msg, sizeof(msg), "[GMOD] Removed %u constraints", static_cast<unsigned>(removed));
    Notify(msg);
}

static void ToolgunButtonClick()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Button: aim at a prop");
        return;
    }

    if (!g_buttonFirstRefID)
    {
        g_buttonFirstRefID = target->refID;
        char msg[128];
        std::snprintf(msg, sizeof(msg), "[GMOD] Button prop selected %08X; choose target", target->refID);
        Notify(msg);
        return;
    }

    TESObjectREFR* button = LookupReference(g_buttonFirstRefID);
    if (!button || button == target)
    {
        g_buttonFirstRefID = 0;
        Notify("[GMOD] Button binding cancelled");
        return;
    }

    for (auto& b : g_toolButtons)
    {
        if (b.buttonRefID == button->refID)
        {
            b.targetRefID = target->refID;
            g_buttonFirstRefID = 0;
            Notify("[GMOD] Button binding updated");
            return;
        }
    }

    GModButtonBinding binding;
    binding.buttonRefID = button->refID;
    binding.targetRefID = target->refID;
    g_toolButtons.push_back(binding);
    g_buttonFirstRefID = 0;

    char msg[160];
    std::snprintf(msg, sizeof(msg), "[GMOD] Button %08X bound to %08X", button->refID, target->refID);
    Notify(msg);
}

static void ToolgunRemoveButtonBinding()
{
    if (g_buttonFirstRefID)
    {
        g_buttonFirstRefID = 0;
        Notify("[GMOD] Button selection cancelled");
        return;
    }

    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Button remove: no target");
        return;
    }

    UInt32 removed = 0;
    for (auto it = g_toolButtons.begin(); it != g_toolButtons.end(); )
    {
        if (it->buttonRefID == target->refID)
        {
            it = g_toolButtons.erase(it);
            ++removed;
        }
        else ++it;
    }

    Notify(removed ? "[GMOD] Button binding removed" : "[GMOD] No button binding on target");
}

static void UpdateButtonBindings()
{
    if (!(GetAsyncKeyState('E') & 1))
        return;

    TESObjectREFR* lookedAt = GetCrosshairTarget();
    if (!lookedAt)
        return;

    for (auto it = g_toolButtons.begin(); it != g_toolButtons.end(); )
    {
        TESObjectREFR* button = LookupReference(it->buttonRefID);
        TESObjectREFR* target = LookupReference(it->targetRefID);
        if (!button || !target)
        {
            it = g_toolButtons.erase(it);
            continue;
        }

        if (button == lookedAt)
        {
            Script::RunScriptLine2("activate player 1", target, true);
            Notify("[GMOD] Button activated target");
            return;
        }
        ++it;
    }
}

static void AddMotorBinding(
    TESObjectREFR* ref,
    float axisX, float axisY, float axisZ,
    float speed,
    bool wheel,
    UInt32 anchorRefID = 0,
    float offX = 0.0f, float offY = 0.0f, float offZ = 0.0f)
{
    if (!ref) return;

    for (auto& m : g_toolMotors)
    {
        if (m.refID == ref->refID)
        {
            m.axisX = axisX;
            m.axisY = axisY;
            m.axisZ = axisZ;
            m.speed = speed;
            m.wheel = wheel;
            m.anchorRefID = anchorRefID;
            m.offX = offX;
            m.offY = offY;
            m.offZ = offZ;
            return;
        }
    }

    GModMotorBinding m;
    m.refID = ref->refID;
    m.anchorRefID = anchorRefID;
    m.offX = offX;
    m.offY = offY;
    m.offZ = offZ;
    m.axisX = axisX;
    m.axisY = axisY;
    m.axisZ = axisZ;
    m.speed = speed;
    m.wheel = wheel;
    g_toolMotors.push_back(m);
}

static void CompletePendingWheelSpawn(TESObjectREFR* wheel)
{
    if (!wheel || !g_pendingWheelAnchorRefID)
        return;

    TESObjectREFR* anchorRef = LookupReference(g_pendingWheelAnchorRefID);
    if (!anchorRef)
    {
        g_pendingWheelAnchorRefID = 0;
        return;
    }

    SetRefPosition(
        wheel,
        anchorRef->posX + g_pendingWheelOffX,
        anchorRef->posY + g_pendingWheelOffY,
        anchorRef->posZ + g_pendingWheelOffZ);

    AddMotorBinding(
        wheel,
        g_pendingWheelAxisX, g_pendingWheelAxisY, g_pendingWheelAxisZ,
        g_pendingWheelSpeed,
        true,
        anchorRef->refID,
        g_pendingWheelOffX, g_pendingWheelOffY, g_pendingWheelOffZ);

    g_pendingWheelAnchorRefID = 0;
    Notify("[GMOD] Wheel attached and motorized");
}

static void ToolgunMotorClick()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || IsActorReference(target))
    {
        Notify("[GMOD] Motor: aim at a physics prop");
        return;
    }

    void* body = GetRootHavokRigidBody(target);
    if (!body)
    {
        Notify("[GMOD] Motor: target has no movable rigid body");
        return;
    }

    const bool reverse = (GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0;
    const float speed = reverse ? -8.0f : 8.0f;

    AddMotorBinding(target, 0.0f, 0.0f, 1.0f, speed, false);
    SetHavokAngularVelocity(body, 0.0f, 0.0f, speed);
    Notify(reverse ? "[GMOD] Motor attached - reverse" : "[GMOD] Motor attached");
}

static void ToolgunWheelClick()
{
    TESObjectREFR* anchorRef = GetCrosshairTarget();
    PlayerCharacter* player = PlayerCharacter::GetSingleton();

    if (!anchorRef || !player || IsActorReference(anchorRef))
    {
        Notify("[GMOD] Wheel: aim at a prop or world reference");
        return;
    }

    if (g_pendingSpawnForm)
    {
        Notify("[GMOD] Wheel: wait for the previous prop to finish spawning");
        return;
    }

    const float yaw = player->rotZ;
    const float axisX = std::cos(yaw);
    const float axisY = -std::sin(yaw);
    const float axisZ = 0.0f;
    const float offX = axisX * 65.0f;
    const float offY = axisY * 65.0f;
    const float offZ = 28.0f;
    const float speed = (GetAsyncKeyState(VK_SHIFT) & 0x8000) ? -10.0f : 10.0f;

    TESObjectREFR* wheel = SpawnConvertedProp(
        "rem\\gmod\\props_vehicles\\carparts_wheel01a.nif", 180.0f);

    if (wheel)
    {
        SetRefPosition(
            wheel,
            anchorRef->posX + offX,
            anchorRef->posY + offY,
            anchorRef->posZ + offZ);

        AddMotorBinding(
            wheel, axisX, axisY, axisZ, speed, true,
            anchorRef->refID, offX, offY, offZ);

        if (void* body = GetRootHavokRigidBody(wheel))
            SetHavokAngularVelocity(body, axisX * speed, axisY * speed, axisZ * speed);

        Notify("[GMOD] Wheel created and motorized");
        return;
    }

    if (g_pendingSpawnForm)
    {
        g_pendingWheelAnchorRefID = anchorRef->refID;
        g_pendingWheelOffX = offX;
        g_pendingWheelOffY = offY;
        g_pendingWheelOffZ = offZ;
        g_pendingWheelAxisX = axisX;
        g_pendingWheelAxisY = axisY;
        g_pendingWheelAxisZ = axisZ;
        g_pendingWheelSpeed = speed;
        Notify("[GMOD] Wheel spawning...");
    }
}

static void ToolgunRemoveMotorOnTarget()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Motor/Wheel remove: no target");
        return;
    }

    UInt32 removed = 0;
    for (auto it = g_toolBalloons.begin(); it != g_toolBalloons.end(); )
    {
        TESObjectREFR* target = LookupReference(it->targetRefID);
        TESObjectREFR* balloon = LookupReference(it->balloonRefID);
        if (!target || !balloon)
        {
            it = g_toolBalloons.erase(it);
            continue;
        }

        void* targetBody = GetRootHavokRigidBody(target);
        if (!targetBody)
        {
            it = g_toolBalloons.erase(it);
            continue;
        }

        // Keep the visible balloon tethered above the target while the target remains
        // fully Havok-driven. Preserve horizontal momentum and add only vertical lift.
        SetRefPosition(balloon, target->posX, target->posY, target->posZ + it->height);

        float vx = 0.0f, vy = 0.0f, vz = 0.0f;
        GetHavokLinearVelocity(targetBody, vx, vy, vz);
        if (vz < it->lift)
        {
            vz += 7.5f;
            if (vz > it->lift) vz = it->lift;
        }
        SetHavokLinearVelocity(targetBody, vx, vy, vz);
        ++it;
    }

    for (auto it = g_toolMotors.begin(); it != g_toolMotors.end(); )
    {
        if (it->refID == target->refID || it->anchorRefID == target->refID)
        {
            if (TESObjectREFR* driven = LookupReference(it->refID))
            {
                if (void* body = GetRootHavokRigidBody(driven))
                    SetHavokAngularVelocity(body, 0.0f, 0.0f, 0.0f);
            }
            it = g_toolMotors.erase(it);
            ++removed;
        }
        else ++it;
    }

    Notify(removed ? "[GMOD] Motor/Wheel binding removed" : "[GMOD] No Motor/Wheel binding on target");
}

static const GModNpcDef* FindGModNpcDef(const char* className, const char* alias = nullptr)
{
    if (!className || !*className)
        return nullptr;

    const UInt32 count =
        static_cast<UInt32>(sizeof(kGModNpcDefs) / sizeof(kGModNpcDefs[0]));

    if (alias && *alias)
    {
        for (UInt32 i = 0; i < count; ++i)
        {
            if (_stricmp(kGModNpcDefs[i].className, className) == 0 &&
                kGModNpcDefs[i].alias && _stricmp(kGModNpcDefs[i].alias, alias) == 0)
                return &kGModNpcDefs[i];
        }
    }

    for (UInt32 i = 0; i < count; ++i)
    {
        if (_stricmp(kGModNpcDefs[i].className, className) == 0)
            return &kGModNpcDefs[i];
    }
    return nullptr;
}

static bool GModNpcIsStationary(const GModNpcDef* def)
{
    if (!def || !def->className) return false;
    return std::strstr(def->className, "turret") != nullptr ||
           std::strstr(def->className, "barnacle") != nullptr;
}

static bool GModNpcIsFlying(const GModNpcDef* def)
{
    if (!def || !def->className) return false;
    return std::strstr(def->className, "scanner") != nullptr ||
           std::strstr(def->className, "manhack") != nullptr ||
           std::strstr(def->className, "gunship") != nullptr ||
           std::strstr(def->className, "dropship") != nullptr ||
           std::strstr(def->className, "helicopter") != nullptr ||
           std::strstr(def->className, "crow") != nullptr ||
           std::strstr(def->className, "pigeon") != nullptr ||
           std::strstr(def->className, "seagull") != nullptr;
}

static bool GModNpcIsRanged(const GModNpcDef* def)
{
    if (!def || !def->className) return false;
    const char* c = def->className;
    return std::strstr(c, "combine") != nullptr ||
           std::strstr(c, "metropolice") != nullptr ||
           std::strstr(c, "sniper") != nullptr ||
           std::strstr(c, "turret") != nullptr ||
           std::strstr(c, "strider") != nullptr ||
           std::strstr(c, "gunship") != nullptr ||
           std::strstr(c, "helicopter") != nullptr ||
           std::strstr(c, "hunter") != nullptr;
}

static float GModNpcAttackRange(const GModNpcDef* def, bool stationary)
{
    if (stationary) return 700.0f;
    if (!def || !def->className) return 115.0f;
    const char* c = def->className;
    if (std::strstr(c, "sniper")) return 1100.0f;
    if (std::strstr(c, "strider") || std::strstr(c, "gunship") ||
        std::strstr(c, "helicopter")) return 900.0f;
    if (std::strstr(c, "hunter")) return 650.0f;
    if (GModNpcIsRanged(def)) return 575.0f;
    return 115.0f;
}

static float GModNpcAttackDamage(const GModNpcDef* def)
{
    if (!def || !def->className) return 6.0f;
    const char* c = def->className;
    if (std::strstr(c, "strider")) return 24.0f;
    if (std::strstr(c, "gunship") || std::strstr(c, "helicopter")) return 18.0f;
    if (std::strstr(c, "hunter")) return 14.0f;
    if (std::strstr(c, "sniper")) return 20.0f;
    if (std::strstr(c, "turret")) return 8.0f;
    if (GModNpcIsRanged(def)) return 9.0f;
    if (std::strstr(c, "headcrab")) return 5.0f;
    if (std::strstr(c, "zombie")) return 10.0f;
    return 7.0f;
}

static void BindGModNpcProxy(TESObjectREFR* ref, const GModNpcDef* def)
{
    if (!ref || !def)
        return;

    GModNpcProxy proxy;
    proxy.refID = ref->refID;
    proxy.def = def;
    proxy.health = 100.0f;
    if (std::strstr(def->className, "strider") ||
        std::strstr(def->className, "gunship") ||
        std::strstr(def->className, "dropship") ||
        std::strstr(def->className, "helicopter"))
        proxy.health = 500.0f;
    else if (std::strstr(def->className, "antlionguard") ||
             std::strstr(def->className, "hunter"))
        proxy.health = 260.0f;
    else if (std::strstr(def->className, "headcrab"))
        proxy.health = 55.0f;
    else if (std::strstr(def->className, "zombie"))
        proxy.health = 135.0f;
    proxy.dead = false;
    proxy.lastAttackTick = 0;
    g_gmodNpcProxies.push_back(proxy);

    char msg[192];
    std::snprintf(msg, sizeof(msg), "[GMOD NPC] spawned %s (%s)",
        def->displayName && *def->displayName ? def->displayName : def->className,
        def->className);
    Notify(msg);
}

static void CompletePendingNpcSpawn(TESObjectREFR* ref)
{
    if (!ref || !g_pendingNpcDef)
        return;

    const GModNpcDef* def = g_pendingNpcDef;
    g_pendingNpcDef = nullptr;
    BindGModNpcProxy(ref, def);
}

static void SpawnGModNpcProxy(const GModPropDef* prop)
{
    if (!prop || !prop->sourceModel ||
        _strnicmp(prop->sourceModel, "npc:", 4) != 0)
        return;

    const char* selector = prop->sourceModel + 4;
    char className[96] = {};
    char alias[96] = {};
    const char* divider = std::strchr(selector, '|');
    if (divider)
    {
        const size_t classLen =
            static_cast<size_t>(divider - selector) < sizeof(className) - 1
                ? static_cast<size_t>(divider - selector)
                : sizeof(className) - 1;
        std::memcpy(className, selector, classLen);
        className[classLen] = 0;
        strncpy_s(alias, sizeof(alias), divider + 1, _TRUNCATE);
    }
    else
    {
        strncpy_s(className, sizeof(className), selector, _TRUNCATE);
    }

    const GModNpcDef* def = FindGModNpcDef(className, alias);
    if (!def)
    {
        Notify("[GMOD NPC] definition not found");
        return;
    }

    if (g_pendingSpawnForm)
    {
        Notify("[GMOD NPC] wait for previous entity spawn");
        return;
    }

    TESObjectREFR* ref = SpawnConvertedProp(prop->nifPath, 260.0f, def->displayName);
    if (ref)
    {
        BindGModNpcProxy(ref, def);
        return;
    }

    if (g_pendingSpawnForm)
    {
        g_pendingNpcDef = def;
        Notify("[GMOD NPC] spawning...");
    }
}

static void UpdateGModNpcProxies()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
        return;

    const DWORD now = GetTickCount();

    for (auto it = g_gmodNpcProxies.begin(); it != g_gmodNpcProxies.end(); )
    {
        TESObjectREFR* ref = LookupReference(it->refID);
        if (!ref || !it->def)
        {
            it = g_gmodNpcProxies.erase(it);
            continue;
        }

        // Let dead bodies remain as ordinary physics objects, and let the
        // physgun fully control a live proxy while it is held.
        if (it->dead || g_heldRef == ref)
        {
            ++it;
            continue;
        }

        void* body = GetRootHavokRigidBody(ref);
        if (!body)
        {
            it = g_gmodNpcProxies.erase(it);
            continue;
        }

        const float dx = player->posX - ref->posX;
        const float dy = player->posY - ref->posY;
        const float dz = player->posZ - ref->posZ;
        const float horizontalDist = std::sqrt(dx * dx + dy * dy);
        const float dist = std::sqrt(dx * dx + dy * dy + dz * dz);

        float oldVX = 0.0f, oldVY = 0.0f, oldVZ = 0.0f;
        GetHavokLinearVelocity(body, oldVX, oldVY, oldVZ);

        const bool stationary = GModNpcIsStationary(it->def);
        const bool flying = GModNpcIsFlying(it->def);

        if (horizontalDist > 1.0f)
            SetRefAngleZ(ref, std::atan2(dx, dy));

        if (it->def->hostile)
        {
            const bool ranged = GModNpcIsRanged(it->def);
            const float attackRange = GModNpcAttackRange(it->def, stationary);
            const float preferredRange = ranged ? attackRange * 0.68f : attackRange;

            if (!stationary && dist > attackRange)
            {
                const float inv =
                    1.0f / (flying ? (dist > 1.0f ? dist : 1.0f)
                                   : (horizontalDist > 1.0f ? horizontalDist : 1.0f));
                const float speed = flying ? 190.0f : (ranged ? 145.0f : 175.0f);
                const float vx = dx * inv * speed;
                const float vy = dy * inv * speed;
                const float vz = flying ? dz * inv * speed : oldVZ;
                SetHavokLinearVelocity(body, vx, vy, vz);
            }
            else if (!stationary && ranged && dist < preferredRange * 0.55f)
            {
                // Ranged NPCs back away instead of behaving like melee attackers.
                const float inv =
                    1.0f / (flying ? (dist > 1.0f ? dist : 1.0f)
                                   : (horizontalDist > 1.0f ? horizontalDist : 1.0f));
                const float retreatSpeed = flying ? 135.0f : 95.0f;
                SetHavokLinearVelocity(
                    body,
                    -dx * inv * retreatSpeed,
                    -dy * inv * retreatSpeed,
                    flying ? -dz * inv * retreatSpeed : oldVZ);
            }
            else if (dist <= attackRange)
            {
                SetHavokLinearVelocity(body, 0.0f, 0.0f, stationary ? 0.0f : oldVZ);

                const DWORD attackDelay = ranged ? 850 : 1100;
                if (now - it->lastAttackTick >= attackDelay)
                {
                    char cmd[64];
                    std::snprintf(cmd, sizeof(cmd), "damageav health %.1f",
                        GModNpcAttackDamage(it->def));
                    Script::RunScriptLine2(cmd, player, true);
                    it->lastAttackTick = now;
                }
            }
        }
        else
        {
            // Friendly/passive GMod NPCs follow the player without crowding them.
            if (!stationary && dist > 360.0f)
            {
                const float inv =
                    1.0f / (flying ? (dist > 1.0f ? dist : 1.0f)
                                   : (horizontalDist > 1.0f ? horizontalDist : 1.0f));
                const float speed = 115.0f;
                SetHavokLinearVelocity(
                    body,
                    dx * inv * speed,
                    dy * inv * speed,
                    flying ? dz * inv * speed : oldVZ);
            }
            else if (!stationary && dist < 230.0f)
            {
                SetHavokLinearVelocity(body, 0.0f, 0.0f, flying ? 0.0f : oldVZ);
            }
        }

        ++it;
    }
}

static float GModNpcWeaponDamage(const GModRuntimeWeapon* weapon)
{
    if (!weapon || !weapon->def)
        return 28.0f;

    switch (weapon->def->kind)
    {
    case GModWeaponKind::Melee: return 34.0f;
    case GModWeaponKind::Pistol: return 24.0f;
    case GModWeaponKind::Automatic: return 18.0f;
    case GModWeaponKind::Rifle: return 46.0f;
    case GModWeaponKind::Shotgun: return 58.0f;
    case GModWeaponKind::Launcher: return 120.0f;
    case GModWeaponKind::Grenade: return 90.0f;
    case GModWeaponKind::Flechette: return 30.0f;
    default: return 28.0f;
    }
}

static void DamageGModNpcProxyUnderCrosshair(const GModRuntimeWeapon* weapon)
{
    static DWORD lastDamageTick = 0;
    const DWORD now = GetTickCount();
    if (now - lastDamageTick < 180)
        return;

    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
        return;

    for (auto& proxy : g_gmodNpcProxies)
    {
        if (proxy.refID != target->refID || proxy.dead || !proxy.def)
            continue;

        proxy.health -= GModNpcWeaponDamage(weapon);
        lastDamageTick = now;

        if (proxy.health <= 0.0f)
        {
            proxy.health = 0.0f;
            proxy.dead = true;

            if (void* body = GetRootHavokRigidBody(target))
            {
                float vx = 0.0f, vy = 0.0f, vz = 0.0f;
                GetHavokLinearVelocity(body, vx, vy, vz);
                SetHavokLinearVelocity(body, vx, vy, vz + 120.0f);
                SetHavokAngularVelocity(body, 2.0f, 1.0f, 3.5f);
            }

            char msg[192];
            std::snprintf(msg, sizeof(msg), "[GMOD NPC] %s killed",
                proxy.def->displayName && *proxy.def->displayName
                    ? proxy.def->displayName : proxy.def->className);
            Notify(msg);
        }
        return;
    }
}

static void CompletePendingBalloonSpawn(TESObjectREFR* balloon)
{
    if (!balloon || !g_pendingBalloonTargetRefID)
        return;

    TESObjectREFR* target = LookupReference(g_pendingBalloonTargetRefID);
    if (!target)
    {
        g_pendingBalloonTargetRefID = 0;
        return;
    }

    SetRefPosition(balloon, target->posX, target->posY, target->posZ + g_pendingBalloonHeight);

    GModBalloonBinding binding;
    binding.balloonRefID = balloon->refID;
    binding.targetRefID = target->refID;
    binding.height = g_pendingBalloonHeight;
    binding.lift = g_pendingBalloonLift;
    g_toolBalloons.push_back(binding);

    g_pendingBalloonTargetRefID = 0;
    Notify("[GMOD] Balloon attached");
}

static void ToolgunBalloonClick()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || IsActorReference(target))
    {
        Notify("[GMOD] Balloon: aim at a physics prop");
        return;
    }

    if (!GetRootHavokRigidBody(target))
    {
        Notify("[GMOD] Balloon: target has no movable rigid body");
        return;
    }

    if (g_pendingSpawnForm)
    {
        Notify("[GMOD] Balloon: wait for previous prop spawn");
        return;
    }

    TESObjectREFR* balloon = SpawnConvertedProp(
        "rem\\gmod\\maxofs2d\\balloon_classic.nif", 180.0f);

    if (balloon)
    {
        SetRefPosition(balloon, target->posX, target->posY, target->posZ + 150.0f);

        GModBalloonBinding binding;
        binding.balloonRefID = balloon->refID;
        binding.targetRefID = target->refID;
        binding.height = 150.0f;
        binding.lift = 95.0f;
        g_toolBalloons.push_back(binding);
        Notify("[GMOD] Balloon attached");
        return;
    }

    if (g_pendingSpawnForm)
    {
        g_pendingBalloonTargetRefID = target->refID;
        g_pendingBalloonHeight = 150.0f;
        g_pendingBalloonLift = 95.0f;
        Notify("[GMOD] Balloon spawning...");
    }
}

static void ToolgunRemoveBalloonBinding()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Balloon remove: no target");
        return;
    }

    UInt32 removed = 0;
    for (auto it = g_toolBalloons.begin(); it != g_toolBalloons.end(); )
    {
        if (it->targetRefID == target->refID || it->balloonRefID == target->refID)
        {
            TESObjectREFR* balloon = LookupReference(it->balloonRefID);
            if (balloon)
            {
                g_undoDisabled.push_back(balloon->refID);
                Script::RunScriptLine2("disable", balloon, true);
            }
            it = g_toolBalloons.erase(it);
            ++removed;
        }
        else ++it;
    }

    Notify(removed ? "[GMOD] Balloon removed" : "[GMOD] No balloon binding on target");
}

static void UpdateToolgunPhysics()
{
    UpdateButtonBindings();
    UpdateToolLights();
    UpdateGModDynamite();
    UpdateGModPhysProps();

    for (auto it = g_toolThrusters.begin(); it != g_toolThrusters.end(); )
    {
        TESForm* form = LookupFormByID(it->refID);
        if (!form || !form->GetIsReference())
        {
            it = g_toolThrusters.erase(it);
            continue;
        }

        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        void* rigidBody = GetRootHavokRigidBody(ref);
        if (!rigidBody)
        {
            it = g_toolThrusters.erase(it);
            continue;
        }

        SetHavokLinearVelocity(rigidBody,
            it->dirX * it->speed,
            it->dirY * it->speed,
            it->dirZ * it->speed);
        ++it;
    }

    for (auto it = g_toolHoverballs.begin(); it != g_toolHoverballs.end(); )
    {
        TESForm* form = LookupFormByID(it->refID);
        if (!form || !form->GetIsReference())
        {
            it = g_toolHoverballs.erase(it);
            continue;
        }

        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        void* rigidBody = GetRootHavokRigidBody(ref);
        if (!rigidBody)
        {
            it = g_toolHoverballs.erase(it);
            continue;
        }

        float dz = it->targetZ - ref->posZ;
        float vz = dz * 4.5f;
        if (vz > 500.0f) vz = 500.0f;
        if (vz < -500.0f) vz = -500.0f;
        if (std::fabs(dz) < 2.0f) vz = 0.0f;
        SetHavokLinearVelocity(rigidBody, 0.0f, 0.0f, vz);
        ++it;
    }

    for (auto it = g_toolConstraints.begin(); it != g_toolConstraints.end(); )
    {
        TESObjectREFR* a = LookupReference(it->refA);
        TESObjectREFR* b = LookupReference(it->refB);
        if (!a || !b)
        {
            it = g_toolConstraints.erase(it);
            continue;
        }

        void* bodyB = GetRootHavokRigidBody(b);
        if (!bodyB)
        {
            it = g_toolConstraints.erase(it);
            continue;
        }

        const float dx = b->posX - a->posX;
        const float dy = b->posY - a->posY;
        const float dz = b->posZ - a->posZ;

        float vx = 0.0f, vy = 0.0f, vz = 0.0f;

        if (it->kind == GModConstraintKind::Weld ||
            it->kind == GModConstraintKind::Pivot)
        {
            vx = ((a->posX + it->offX) - b->posX) * it->stiffness;
            vy = ((a->posY + it->offY) - b->posY) * it->stiffness;
            vz = ((a->posZ + it->offZ) - b->posZ) * it->stiffness;

            if (it->kind == GModConstraintKind::Weld)
            {
                const float targetX = a->rotX + it->rotOffX;
                const float targetY = a->rotY + it->rotOffY;
                const float targetZ = a->rotZ + it->rotOffZ;
                if (std::fabs(b->rotX - targetX) > 0.01f ||
                    std::fabs(b->rotY - targetY) > 0.01f ||
                    std::fabs(b->rotZ - targetZ) > 0.01f)
                    SetRefAngles(b, targetX, targetY, targetZ);
                SetHavokAngularVelocity(bodyB, 0.0f, 0.0f, 0.0f);
            }
        }
        else if (it->kind == GModConstraintKind::Slider)
        {
            const float projection = dx * it->axisX + dy * it->axisY + dz * it->axisZ;
            const float px = dx - it->axisX * projection;
            const float py = dy - it->axisY * projection;
            const float pz = dz - it->axisZ * projection;
            vx = -px * it->stiffness;
            vy = -py * it->stiffness;
            vz = -pz * it->stiffness;
        }
        else
        {
            float dist = std::sqrt(dx * dx + dy * dy + dz * dz);
            if (dist < 0.001f)
            {
                ++it;
                continue;
            }

            if (it->kind == GModConstraintKind::Hydraulic)
            {
                // Fixed project key binding for now: hold H to extend, release to retract.
                const float targetRest =
                    (GetAsyncKeyState('H') & 0x8000) ? it->maxDistance : it->minDistance;
                it->restDistance += (targetRest - it->restDistance) * 0.10f;
            }
            else if (it->kind == GModConstraintKind::Muscle)
            {
                const float elapsed = (GetTickCount() - it->createdTick) / 1000.0f;
                it->restDistance =
                    it->baseDistance * (1.0f + 0.30f * std::sin(elapsed * 3.0f));
            }
            else if (it->kind == GModConstraintKind::Winch)
            {
                // H reels in, J pays out. With neither key held the winch holds its length.
                if (GetAsyncKeyState('H') & 0x8000)
                    it->restDistance -= 5.0f;
                if (GetAsyncKeyState('J') & 0x8000)
                    it->restDistance += 5.0f;
                if (it->restDistance < it->minDistance) it->restDistance = it->minDistance;
                if (it->restDistance > it->maxDistance) it->restDistance = it->maxDistance;
            }

            const float error = dist - it->restDistance;
            if ((it->kind == GModConstraintKind::Rope ||
                 it->kind == GModConstraintKind::Pulley) && error <= 0.0f)
            {
                ++it;
                continue;
            }

            const float scale = -(error * it->stiffness) / dist;
            vx = dx * scale;
            vy = dy * scale;
            vz = dz * scale;
        }

        const float maxV = 1200.0f;
        if (vx > maxV) vx = maxV; else if (vx < -maxV) vx = -maxV;
        if (vy > maxV) vy = maxV; else if (vy < -maxV) vy = -maxV;
        if (vz > maxV) vz = maxV; else if (vz < -maxV) vz = -maxV;
        SetHavokLinearVelocity(bodyB, vx, vy, vz);

        // Pulley acts on both movable bodies so motion transfers across the rope.
        if (it->kind == GModConstraintKind::Pulley)
        {
            if (void* bodyA = GetRootHavokRigidBody(a))
                SetHavokLinearVelocity(bodyA, -vx, -vy, -vz);
        }
        ++it;
    }
}

static void ToolgunCreator()
{
    const GModPropDef* prop = GetSelectedBuildProp();
    if (!prop)
    {
        Notify("[GMOD] Creator: no selected spawn-menu prop");
        return;
    }

    if (SpawnConvertedProp(prop->nifPath, 220.0f, prop->displayName))
    {
        char msg[192];
        std::snprintf(msg, sizeof(msg), "[GMOD] Creator spawned %s", prop->displayName);
        Notify(msg);
    }
}

static void ToolgunDuplicatorCopy()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || !target->baseForm)
    {
        Notify("[GMOD] Duplicator: no target");
        return;
    }

    TESModel* model = DYNAMIC_CAST(target->baseForm, TESForm, TESModel);
    if (!model || !model->nifPath.m_data || !*model->nifPath.m_data)
    {
        Notify("[GMOD] Duplicator: target has no reusable model");
        return;
    }

    strncpy_s(g_duplicatorNif, sizeof(g_duplicatorNif), model->nifPath.m_data, _TRUNCATE);
    const char* name = target->baseForm->GetName();
    strncpy_s(g_duplicatorName, sizeof(g_duplicatorName),
        (name && *name) ? name : "prop", _TRUNCATE);

    char msg[384];
    std::snprintf(msg, sizeof(msg), "[GMOD] Duplicator copied %s (%s)", g_duplicatorName, g_duplicatorNif);
    Notify(msg);
}

static void ToolgunDuplicatorPaste()
{
    if (!g_duplicatorNif[0])
    {
        Notify("[GMOD] Duplicator: right-click a prop to copy first");
        return;
    }

    if (SpawnConvertedProp(g_duplicatorNif, 220.0f, g_duplicatorName))
    {
        char msg[192];
        std::snprintf(msg, sizeof(msg), "[GMOD] Duplicator pasted %s", g_duplicatorName[0] ? g_duplicatorName : "prop");
        Notify(msg);
    }
}

static TESObjectLIGH* FindGModLightTemplate()
{
    DataHandler* data = DataHandler::Get();
    if (!data || !data->boundObjectList)
        return nullptr;

    TESObjectLIGH* fallback = nullptr;
    for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
    {
        if (obj->typeID != kFormType_TESObjectLIGH)
            continue;

        TESObjectLIGH* light = static_cast<TESObjectLIGH*>(obj);
        if (!fallback)
            fallback = light;

        if (!(light->lightFlags & TESObjectLIGH::kFlag_Negative) &&
            light->radius >= 128 &&
            !(light->lightFlags & TESObjectLIGH::kFlag_OffByDefault))
            return light;
    }
    return fallback;
}

static TESObjectREFR* SpawnGModLight(float distance)
{
    if (g_pendingSpawnForm)
    {
        Notify("[GMOD] Light: wait for previous entity spawn");
        return nullptr;
    }

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
    {
        Notify("[GMOD] Light: player is not in a loaded cell");
        return nullptr;
    }

    TESObjectLIGH* source = FindGModLightTemplate();
    if (!source)
    {
        Notify("[GMOD] Light: no vanilla light template found");
        return nullptr;
    }

    TESForm* cloned = source->CloneForm(false);
    if (!cloned || cloned->typeID != kFormType_TESObjectLIGH)
    {
        Notify("[GMOD] Light: clone failed");
        return nullptr;
    }

    TESObjectLIGH* light = static_cast<TESObjectLIGH*>(cloned);
    light->fullName.name.Set("GMod Light");
    light->radius = 640;
    light->red = 255;
    light->green = 244;
    light->blue = 220;
    light->time = 0;
    light->falloffExp = 1.0f;
    light->SetFlag(TESObjectLIGH::kFlag_Dynamic, true);
    light->SetFlag(TESObjectLIGH::kFlag_CanBeCarried, false);
    light->SetFlag(TESObjectLIGH::kFlag_Negative, false);
    light->SetFlag(TESObjectLIGH::kFlag_OffByDefault, false);
    light->SetFlag(TESObjectLIGH::kFlag_Flicker, false);
    light->SetFlag(TESObjectLIGH::kFlag_FlickerSlow, false);

    g_runtimePropForms.push_back(light);

    const UInt32 nextBefore = GetNextFreeFormID();
    char cmd[128];
    std::snprintf(cmd, sizeof(cmd), "placeatme %08X 1 %.1f 0", light->refID, distance);
    Script::RunScriptLine2(cmd, player, true);
    const UInt32 nextAfter = GetNextFreeFormID();

    TESObjectREFR* spawned = nullptr;
    if (nextAfter >= nextBefore && (nextAfter - nextBefore) < 0x100)
    {
        for (UInt32 id = nextBefore; id < nextAfter; ++id)
        {
            TESForm* candidate = LookupFormByID(id);
            if (!candidate || !candidate->GetIsReference())
                continue;
            TESObjectREFR* ref = static_cast<TESObjectREFR*>(candidate);
            if (ref->baseForm == light ||
                (ref->baseForm && ref->baseForm->refID == light->refID))
            {
                spawned = ref;
                break;
            }
        }
    }

    if (!spawned)
        spawned = FindReferenceForBaseForm(light);

    if (!spawned)
    {
        g_pendingSpawnForm = light;
        g_pendingSpawnStartTick = GetTickCount();
        Notify("[GMOD] Light spawning...");
        return nullptr;
    }

    g_spawnUndo.push_back(spawned->refID);
    return spawned;
}

static void BindGModLamp(TESObjectREFR* light, TESObjectREFR* target,
                         float offX, float offY, float offZ)
{
    if (!light || !target)
        return;

    SetRefPosition(light,
        target->posX + offX,
        target->posY + offY,
        target->posZ + offZ);

    GModLampBinding binding;
    binding.lightRefID = light->refID;
    binding.targetRefID = target->refID;
    binding.offX = offX;
    binding.offY = offY;
    binding.offZ = offZ;
    g_toolLamps.push_back(binding);
}

static void CompletePendingLampSpawn(TESObjectREFR* light)
{
    if (!light || !g_pendingLampTargetRefID)
        return;

    TESObjectREFR* target = LookupReference(g_pendingLampTargetRefID);
    if (target)
    {
        BindGModLamp(light, target,
            g_pendingLampOffX, g_pendingLampOffY, g_pendingLampOffZ);
        Notify("[GMOD] Lamp attached");
    }

    g_pendingLampTargetRefID = 0;
}

static void ToolgunLightClick(bool lamp)
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (lamp && (!target || IsActorReference(target)))
    {
        Notify("[GMOD] Lamp: aim at a prop");
        return;
    }

    const float offX = 0.0f;
    const float offY = 0.0f;
    const float offZ = 55.0f;

    if (lamp)
    {
        g_pendingLampTargetRefID = target->refID;
        g_pendingLampOffX = offX;
        g_pendingLampOffY = offY;
        g_pendingLampOffZ = offZ;
    }
    else
    {
        g_pendingLampTargetRefID = 0;
    }

    TESObjectREFR* light = SpawnGModLight(190.0f);
    if (light)
    {
        if (lamp)
        {
            BindGModLamp(light, target, offX, offY, offZ);
            g_pendingLampTargetRefID = 0;
            Notify("[GMOD] Lamp attached");
        }
        else
        {
            if (target)
                SetRefPosition(light, target->posX, target->posY, target->posZ + 35.0f);
            Notify("[GMOD] Light created");
        }
    }
}

static void ToolgunRemoveLight(bool lampOnly)
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Light remove: no target");
        return;
    }

    UInt32 removed = 0;
    for (auto it = g_toolLamps.begin(); it != g_toolLamps.end(); )
    {
        if (it->targetRefID == target->refID || it->lightRefID == target->refID)
        {
            if (TESObjectREFR* light = LookupReference(it->lightRefID))
            {
                g_undoDisabled.push_back(light->refID);
                Script::RunScriptLine2("disable", light, true);
            }
            it = g_toolLamps.erase(it);
            ++removed;
        }
        else ++it;
    }

    if (!lampOnly && target->baseForm && target->baseForm->typeID == kFormType_TESObjectLIGH)
    {
        g_undoDisabled.push_back(target->refID);
        Script::RunScriptLine2("disable", target, true);
        ++removed;
    }

    Notify(removed ? "[GMOD] Light removed" : "[GMOD] No light binding on target");
}

static void UpdateToolLights()
{
    for (auto it = g_toolLamps.begin(); it != g_toolLamps.end(); )
    {
        TESObjectREFR* light = LookupReference(it->lightRefID);
        TESObjectREFR* target = LookupReference(it->targetRefID);
        if (!light || !target)
        {
            it = g_toolLamps.erase(it);
            continue;
        }

        SetRefPosition(light,
            target->posX + it->offX,
            target->posY + it->offY,
            target->posZ + it->offZ);
        ++it;
    }
}

static void AddGModDynamite(TESObjectREFR* ref, DWORD fuseMs)
{
    if (!ref)
        return;

    GModDynamiteBinding binding;
    binding.refID = ref->refID;
    binding.explodeTick = GetTickCount() + fuseMs;
    binding.radius = 850.0f;
    binding.impulse = 900.0f;
    g_toolDynamite.push_back(binding);

    Notify("[GMOD] Dynamite armed - 3 second fuse");
}

static void CompletePendingDynamiteSpawn(TESObjectREFR* ref)
{
    if (!ref || !g_pendingDynamite)
        return;

    g_pendingDynamite = false;
    AddGModDynamite(ref, g_pendingDynamiteFuseMs);
}

static void BlastGModDynamite(TESObjectREFR* explosive, float radius, float impulse)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!explosive || !player || !player->parentCell)
        return;

    for (TESObjectCELL::RefList::Iterator it = player->parentCell->objectList.Begin(); !it.End(); ++it)
    {
        TESObjectREFR* ref = it.Get();
        if (!ref || ref == explosive)
            continue;

        const float dx = ref->posX - explosive->posX;
        const float dy = ref->posY - explosive->posY;
        const float dz = ref->posZ - explosive->posZ;
        const float distSq = dx * dx + dy * dy + dz * dz;
        if (distSq <= 0.0001f || distSq > radius * radius)
            continue;

        const float dist = std::sqrt(distSq);
        const float inv = 1.0f / dist;
        float falloff = 1.0f - (dist / radius);
        if (falloff < 0.0f) falloff = 0.0f;
        falloff *= falloff;

        // Native Fallout actors take blast damage too, so imported GMod explosives
        // interact with the actual New Vegas population rather than only proxy NPCs.
        if (IsActorReference(ref))
        {
            const float damage = 180.0f * falloff;
            if (damage >= 1.0f)
            {
                char damageCmd[96];
                std::snprintf(damageCmd, sizeof(damageCmd),
                    "damageav health %.1f", damage);
                Script::RunScriptLine2(damageCmd, ref, true);
            }
        }

        void* body = GetRootHavokRigidBody(ref);
        if (body)
        {
            float vx = 0.0f, vy = 0.0f, vz = 0.0f;
            GetHavokLinearVelocity(body, vx, vy, vz);

            const float push = impulse * falloff;
            vx += dx * inv * push;
            vy += dy * inv * push;
            vz += (dz * inv * push) + (180.0f * falloff);

            SetHavokLinearVelocity(body, vx, vy, vz);
        }
    }

    // Apply damage to runtime GMod NPC proxies in the same blast radius.
    for (auto& proxy : g_gmodNpcProxies)
    {
        if (proxy.dead)
            continue;

        TESObjectREFR* ref = LookupReference(proxy.refID);
        if (!ref)
            continue;

        const float dx = ref->posX - explosive->posX;
        const float dy = ref->posY - explosive->posY;
        const float dz = ref->posZ - explosive->posZ;
        const float dist = std::sqrt(dx * dx + dy * dy + dz * dz);
        if (dist >= radius)
            continue;

        const float falloff = 1.0f - (dist / radius);
        proxy.health -= 180.0f * falloff;
        if (proxy.health <= 0.0f)
        {
            proxy.health = 0.0f;
            proxy.dead = true;
        }
    }

    g_undoDisabled.push_back(explosive->refID);
    Script::RunScriptLine2("disable", explosive, true);
    Notify("[GMOD] BOOM");
}

static void UpdateGModDynamite()
{
    const DWORD now = GetTickCount();

    for (auto it = g_toolDynamite.begin(); it != g_toolDynamite.end(); )
    {
        TESObjectREFR* ref = LookupReference(it->refID);
        if (!ref)
        {
            it = g_toolDynamite.erase(it);
            continue;
        }

        if (now >= it->explodeTick)
        {
            BlastGModDynamite(ref, it->radius, it->impulse);
            it = g_toolDynamite.erase(it);
            continue;
        }
        ++it;
    }
}

static void ToolgunDynamiteClick()
{
    if (g_pendingSpawnForm)
    {
        Notify("[GMOD] Dynamite: wait for previous entity spawn");
        return;
    }

    TESObjectREFR* ref = SpawnConvertedProp(
        "rem\\gmod\\dynamite\\dynamite.nif", 185.0f, "GMod Dynamite");

    if (ref)
    {
        AddGModDynamite(ref, 3000);
        return;
    }

    if (g_pendingSpawnForm)
    {
        g_pendingDynamite = true;
        g_pendingDynamiteFuseMs = 3000;
        Notify("[GMOD] Dynamite spawning...");
    }
}

static void ToolgunRemoveDynamite()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] Dynamite remove: no target");
        return;
    }

    for (auto it = g_toolDynamite.begin(); it != g_toolDynamite.end(); ++it)
    {
        if (it->refID != target->refID)
            continue;

        g_undoDisabled.push_back(target->refID);
        Script::RunScriptLine2("disable", target, true);
        g_toolDynamite.erase(it);
        Notify("[GMOD] Dynamite defused");
        return;
    }

    Notify("[GMOD] Target is not armed dynamite");
}

static GModPhysPropBinding* FindPhysPropBinding(UInt32 refID)
{
    for (auto& binding : g_toolPhysProps)
        if (binding.refID == refID)
            return &binding;
    return nullptr;
}

static void ToolgunPhysPropClick()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || IsActorReference(target))
    {
        Notify("[GMOD] PhysProp: aim at a physics prop");
        return;
    }

    if (!GetRootHavokRigidBody(target))
    {
        Notify("[GMOD] PhysProp: target has no movable rigid body");
        return;
    }

    GModPhysPropBinding* existing = FindPhysPropBinding(target->refID);
    if (!existing)
    {
        GModPhysPropBinding binding;
        binding.refID = target->refID;
        binding.mode = 1;
        g_toolPhysProps.push_back(binding);
        Notify("[GMOD] PhysProp: low gravity");
        return;
    }

    existing->mode = static_cast<UInt8>((existing->mode % 3) + 1);
    switch (existing->mode)
    {
    case 1: Notify("[GMOD] PhysProp: low gravity"); break;
    case 2: Notify("[GMOD] PhysProp: zero gravity"); break;
    case 3: Notify("[GMOD] PhysProp: high drag"); break;
    default: break;
    }
}

static void ToolgunPhysPropReset()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        Notify("[GMOD] PhysProp reset: no target");
        return;
    }

    for (auto it = g_toolPhysProps.begin(); it != g_toolPhysProps.end(); ++it)
    {
        if (it->refID != target->refID)
            continue;

        g_toolPhysProps.erase(it);
        Notify("[GMOD] PhysProp: normal physics restored");
        return;
    }

    Notify("[GMOD] PhysProp: target already uses normal physics");
}

static void UpdateGModPhysProps()
{
    const DWORD now = GetTickCount();
    if (!g_physPropUpdateTick)
        g_physPropUpdateTick = now;

    float dt = static_cast<float>(now - g_physPropUpdateTick) * 0.001f;
    g_physPropUpdateTick = now;
    if (dt < 0.001f) dt = 0.001f;
    if (dt > 0.05f) dt = 0.05f;

    for (auto it = g_toolPhysProps.begin(); it != g_toolPhysProps.end(); )
    {
        TESObjectREFR* ref = LookupReference(it->refID);
        if (!ref)
        {
            it = g_toolPhysProps.erase(it);
            continue;
        }

        void* body = GetRootHavokRigidBody(ref);
        if (!body)
        {
            it = g_toolPhysProps.erase(it);
            continue;
        }

        float vx = 0.0f, vy = 0.0f, vz = 0.0f;
        GetHavokLinearVelocity(body, vx, vy, vz);

        switch (it->mode)
        {
        case 1:
            // Counter most of New Vegas gravity while retaining a visible downward pull.
            vz += 430.0f * dt;
            break;
        case 2:
            // Counter gravity and add very light damping for a GMod-style zero-gravity prop.
            vz += 700.0f * dt;
            vx *= 0.998f;
            vy *= 0.998f;
            vz *= 0.998f;
            break;
        case 3:
        {
            // Strong linear drag while leaving normal gravity in place.
            float damping = 1.0f - (4.5f * dt);
            if (damping < 0.0f) damping = 0.0f;
            vx *= damping;
            vy *= damping;
            vz *= damping;
            break;
        }
        default:
            break;
        }

        SetHavokLinearVelocity(body, vx, vy, vz);
        ++it;
    }
}

static void ToolgunInflator(bool shrink)
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target || IsActorReference(target))
    {
        Notify("[GMOD] Inflator: aim at a prop");
        return;
    }

    float next = target->scale * (shrink ? 0.90f : 1.10f);
    if (next < 0.10f) next = 0.10f;
    if (next > 5.00f) next = 5.00f;

    target->scale = next;
    target->Update3D_v1c();

    char msg[128];
    std::snprintf(msg, sizeof(msg), "[GMOD] Inflator scale %.2fx", next);
    Notify(msg);
}

static void ToolgunPrimaryAction()
{
    PlayToolgunShotSound();

    const GModToolDef* tool = GetSelectedToolMode();
    if (!tool) return;

    if (_stricmp(tool->id, "remover") == 0)
        ToolgunRemove();
    else if (_stricmp(tool->id, "leafblower") == 0)
        ToolgunLeafblower();
    else if (_stricmp(tool->id, "thruster") == 0)
        ToolgunToggleThruster(false);
    else if (_stricmp(tool->id, "hoverball") == 0)
        ToolgunToggleHoverball();
    else if (_stricmp(tool->id, "balloon") == 0)
        ToolgunBalloonClick();
    else if (IsConstraintToolId(tool->id))
        ToolgunConstraintClick(tool->id);
    else if (_stricmp(tool->id, "button") == 0)
        ToolgunButtonClick();
    else if (_stricmp(tool->id, "creator") == 0)
        ToolgunCreator();
    else if (_stricmp(tool->id, "duplicator") == 0)
        ToolgunDuplicatorPaste();
    else if (_stricmp(tool->id, "motor") == 0)
        ToolgunMotorClick();
    else if (_stricmp(tool->id, "wheel") == 0)
        ToolgunWheelClick();
    else if (_stricmp(tool->id, "inflator") == 0)
        ToolgunInflator(false);
    else if (_stricmp(tool->id, "light") == 0)
        ToolgunLightClick(false);
    else if (_stricmp(tool->id, "lamp") == 0)
        ToolgunLightClick(true);
    else if (_stricmp(tool->id, "dynamite") == 0)
        ToolgunDynamiteClick();
    else if (_stricmp(tool->id, "physprop") == 0)
        ToolgunPhysPropClick();
    else
    {
        char msg[192];
        std::snprintf(msg, sizeof(msg), "[GMOD TOOL] %s mode selected; native behavior is being ported", tool->displayName);
        Notify(msg);
    }
}

static void ToolgunSecondaryAction()
{
    const GModToolDef* tool = GetSelectedToolMode();
    if (!tool) return;

    if (_stricmp(tool->id, "leafblower") == 0)
        return; // stock leafblower.lua has no secondary action
    else if (_stricmp(tool->id, "thruster") == 0)
        ToolgunToggleThruster(true);
    else if (_stricmp(tool->id, "hoverball") == 0)
        ToolgunToggleHoverball();
    else if (_stricmp(tool->id, "balloon") == 0)
        ToolgunRemoveBalloonBinding();
    else if (IsConstraintToolId(tool->id))
        ToolgunRemoveConstraintsOnTarget();
    else if (_stricmp(tool->id, "button") == 0)
        ToolgunRemoveButtonBinding();
    else if (_stricmp(tool->id, "duplicator") == 0)
        ToolgunDuplicatorCopy();
    else if (_stricmp(tool->id, "motor") == 0 || _stricmp(tool->id, "wheel") == 0)
        ToolgunRemoveMotorOnTarget();
    else if (_stricmp(tool->id, "inflator") == 0)
        ToolgunInflator(true);
    else if (_stricmp(tool->id, "light") == 0)
        ToolgunRemoveLight(false);
    else if (_stricmp(tool->id, "lamp") == 0)
        ToolgunRemoveLight(true);
    else if (_stricmp(tool->id, "dynamite") == 0)
        ToolgunRemoveDynamite();
    else if (_stricmp(tool->id, "physprop") == 0)
        ToolgunPhysPropReset();
    else
        ShowToolModeStatus();
}

static TESObjectREFR* FindReferenceForBaseForm(TESForm* baseForm)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell || !baseForm)
        return nullptr;

    TESObjectREFR* best = nullptr;
    float bestDistSq = 3.402823466e+38F;

    for (TESObjectCELL::RefList::Iterator it = player->parentCell->objectList.Begin(); !it.End(); ++it)
    {
        TESObjectREFR* ref = it.Get();
        if (!ref || ref->baseForm != baseForm)
            continue;

        const float dx = ref->posX - player->posX;
        const float dy = ref->posY - player->posY;
        const float dz = ref->posZ - player->posZ;
        const float d2 = dx * dx + dy * dy + dz * dz;
        if (d2 < bestDistSq)
        {
            bestDistSq = d2;
            best = ref;
        }
    }

    return best;
}

static TESObjectREFR* SpawnConvertedProp(const char* nifPath, float distance, const char* displayName)
{
    if (g_pendingSpawnForm)
    {
        _MESSAGE("[GMOD] Spawn rejected: base %08X is still awaiting reference creation", g_pendingSpawnForm->refID);
        Notify("[GMOD] Previous prop is still spawning");
        return nullptr;
    }

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell || !nifPath || !*nifPath)
    {
        Notify("[GMOD] Spawn failed: player is not in a loaded cell");
        return nullptr;
    }

    // FalloutNV.esm MISC 0005B6CA = TinCan02, a known movable Havok junk item.
    TESForm* templateForm = LookupFormByID(0x0005B6CA);
    if (!templateForm)
    {
        _MESSAGE("[GMOD] Spawn failure: LookupFormByID(0005B6CA TinCan02) returned null");
        Notify("[GMOD] Spawn failed: TinCan02 template not found");
        return nullptr;
    }
    _MESSAGE("[GMOD] template TinCan02 id=%08X type=%02X ptr=%p", templateForm->refID, templateForm->typeID, templateForm);

    TESForm* propForm = templateForm->CloneForm(true);
    if (!propForm)
    {
        _MESSAGE("[GMOD] Spawn failure: CloneForm returned null for template %08X", templateForm->refID);
        Notify("[GMOD] Spawn failed: could not clone prop template");
        return nullptr;
    }
    _MESSAGE("[GMOD] clone id=%08X type=%02X ptr=%p", propForm->refID, propForm->typeID, propForm);

    TESModel* model = DYNAMIC_CAST(propForm, TESForm, TESModel);
    if (!model)
    {
        _MESSAGE("[GMOD] Spawn failure: DYNAMIC_CAST clone %08X to TESModel returned null", propForm->refID);
        Notify("[GMOD] Spawn failed: cloned form has no TESModel");
        return nullptr;
    }
    _MESSAGE("[GMOD] model component=%p oldPath=%s", model, model->nifPath.m_data ? model->nifPath.m_data : "<null>");

    model->SetPath(nifPath);

    if (displayName && *displayName)
    {
        TESFullName* fullName = propForm->GetFullName();
        if (fullName)
            fullName->name.Set(displayName);
    }

    g_runtimePropForms.push_back(propForm);
    _MESSAGE("[GMOD] runtime prop form %08X model=%s", propForm->refID, nifPath);

    const UInt32 nextBefore = GetNextFreeFormID();

    char cmd[160];
    std::snprintf(cmd, sizeof(cmd), "placeatme %08X 1 %.1f 0", propForm->refID, distance);
    const bool placed = Script::RunScriptLine2(cmd, player, true);
    const UInt32 nextAfter = GetNextFreeFormID();
    _MESSAGE("[GMOD] PlaceAtMe line '%s' result=%d nextID %08X -> %08X",
        cmd, placed ? 1 : 0, nextBefore, nextAfter);

    TESObjectREFR* spawned = nullptr;

    // PlaceAtMe allocates reference FormIDs from the same FFxxxxxx range.
    // Resolve any newly allocated forms directly before waiting on the cell list.
    if (nextAfter >= nextBefore && (nextAfter - nextBefore) < 0x100)
    {
        for (UInt32 id = nextBefore; id < nextAfter; ++id)
        {
            TESForm* candidate = LookupFormByID(id);
            if (!candidate || !candidate->GetIsReference())
                continue;

            TESObjectREFR* ref = static_cast<TESObjectREFR*>(candidate);
            _MESSAGE("[GMOD] new form candidate %08X base=%08X type=%02X",
                id, ref->baseForm ? ref->baseForm->refID : 0, ref->typeID);

            if (ref->baseForm == propForm ||
                (ref->baseForm && ref->baseForm->refID == propForm->refID))
            {
                spawned = ref;
                break;
            }
        }
    }

    if (!spawned)
        spawned = FindReferenceForBaseForm(propForm);
    if (!spawned)
    {
        // PlaceAtMe inserts the reference into the cell asynchronously.
        g_pendingSpawnForm = propForm;
        g_pendingSpawnStartTick = GetTickCount();
        Console_Print("[GMOD] Spawn form %08X placed; reference pending", propForm->refID);
        _MESSAGE("[GMOD] spawn reference pending for base %08X", propForm->refID);
        return nullptr;
    }

    g_spawnUndo.push_back(spawned->refID);
    _MESSAGE("[GMOD] captured spawned reference %08X base=%08X rigidBody=%p",
        spawned->refID, propForm->refID, GetRootHavokRigidBody(spawned));

    char msg[128];
    std::snprintf(msg, sizeof(msg), "[GMOD] Spawned prop %08X", spawned->refID);
    Notify(msg);
    return spawned;
}

static void CompleteAutoTestSpawn(TESObjectREFR* spawned)
{
    if (!g_autoTestEnabled || !spawned)
        return;

    _MESSAGE("[AUTOTEST] PASS spawned=%08X rigidBody=%p", spawned->refID, GetRootHavokRigidBody(spawned));
    DeleteFileA(kAutoTestFlag);
    g_autoTestEnabled = false;
    g_autoTestSpawnPending = false;
    g_autoTestSpawnRequested = false;
}

static void UpdatePendingSpawn()
{
    if (!g_pendingSpawnForm)
        return;

    TESObjectREFR* spawned = FindReferenceForBaseForm(g_pendingSpawnForm);
    if (spawned)
    {
        g_spawnUndo.push_back(spawned->refID);
        _MESSAGE("[GMOD] async capture spawned reference %08X base=%08X rigidBody=%p",
            spawned->refID, g_pendingSpawnForm->refID, GetRootHavokRigidBody(spawned));

        char msg[128];
        std::snprintf(msg, sizeof(msg), "[GMOD] Spawned prop %08X", spawned->refID);
        Notify(msg);

        if (g_pendingDynamite)
            CompletePendingDynamiteSpawn(spawned);
        else if (g_pendingLampTargetRefID)
            CompletePendingLampSpawn(spawned);
        else if (g_pendingWheelAnchorRefID)
            CompletePendingWheelSpawn(spawned);
        else if (g_pendingBalloonTargetRefID)
            CompletePendingBalloonSpawn(spawned);
        else if (g_pendingNpcDef)
            CompletePendingNpcSpawn(spawned);

        g_pendingSpawnForm = nullptr;
        g_pendingSpawnStartTick = 0;
        CompleteAutoTestSpawn(spawned);
        return;
    }

    if (GetTickCount() - g_pendingSpawnStartTick > 5000)
    {
        _MESSAGE("[GMOD] async spawn capture timed out for base %08X", g_pendingSpawnForm->refID);
        g_pendingSpawnForm = nullptr;
        g_pendingSpawnStartTick = 0;
        if (g_autoTestEnabled)
        {
            _MESSAGE("[AUTOTEST] FAIL reference never appeared in cell list");
            DeleteFileA(kAutoTestFlag);
            g_autoTestEnabled = false;
            g_autoTestSpawnPending = false;
            g_autoTestSpawnRequested = false;
        }
    }
}

static void UndoLastSpawn()
{
    while (!g_spawnUndo.empty())
    {
        const UInt32 refID = g_spawnUndo.back();
        g_spawnUndo.pop_back();
        TESForm* form = LookupFormByID(refID);
        if (!form || !form->GetIsReference())
            continue;

        TESObjectREFR* ref = static_cast<TESObjectREFR*>(form);
        Script::RunScriptLine2("disable", ref, true);
        Script::RunScriptLine2("markfordelete", ref, true);

        char msg[96];
        std::snprintf(msg, sizeof(msg), "[GMOD] Undo spawn %08X", refID);
        Notify(msg);
        return;
    }

    Notify("[GMOD] No spawned prop to undo");
}

static UInt32 GetBuildCategoryCount()
{
    return static_cast<UInt32>(sizeof(kGModPropCategories) / sizeof(kGModPropCategories[0]));
}

static const GModPropCategoryRange* GetSelectedBuildCategory()
{
    const UInt32 count = GetBuildCategoryCount();
    if (!count) return nullptr;
    if (g_buildMenu.categoryIndex >= count)
        g_buildMenu.categoryIndex = 0;
    return &kGModPropCategories[g_buildMenu.categoryIndex];
}

static const GModPropDef* GetSelectedBuildProp()
{
    const GModPropCategoryRange* category = GetSelectedBuildCategory();
    if (!category || !category->count) return nullptr;

    if (g_buildMenu.itemIndex >= category->count)
        g_buildMenu.itemIndex = 0;

    const UInt32 index = category->start + g_buildMenu.itemIndex;
    const UInt32 total = static_cast<UInt32>(sizeof(kGModPropDefs) / sizeof(kGModPropDefs[0]));
    return index < total ? &kGModPropDefs[index] : nullptr;
}

static void ShowBuildMenuStatus(bool force = false)
{
    if (!g_buildMenu.open || !force) return;
    g_buildMenu.lastHudTick = GetTickCount();
    RefreshGModSpawnOverlay();
}

static void OpenBuildMenu()
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
    {
        Notify("[GMOD] Build menu requires loaded gameplay");
        return;
    }

    if (g_skate.active)
    {
        Notify("[GMOD] Exit skate mode before opening build menu");
        return;
    }

    if (!GetBuildCategoryCount())
    {
        Notify("[GMOD] No converted spawn props are registered");
        return;
    }

    g_buildMenu.open = true;
    g_buildMenu.lastHudTick = 0;
    PlayGModUISound("ui_return", "fx\\rem\\gmod\\garrysmod\\ui_return.wav");
    g_buildMenu.fightWasDisabled =
        (player->disabledControlFlags & PlayerCharacter::kControlFlag_Fight) != 0;
    g_buildMenu.movementWasDisabled =
        (player->disabledControlFlags & PlayerCharacter::kControlFlag_Movement) != 0;
    player->disabledControlFlags |=
        PlayerCharacter::kControlFlag_Fight | PlayerCharacter::kControlFlag_Movement;

    ShowGModSpawnOverlay();
    ShowBuildMenuStatus(true);
    UpdatePhysBeamOverlay();
    _MESSAGE("[GMOD-BUILD] menu opened category=%u item=%u",
        g_buildMenu.categoryIndex, g_buildMenu.itemIndex);
}

static void CloseBuildMenu()
{
    if (!g_buildMenu.open) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (player)
    {
        if (!g_buildMenu.fightWasDisabled)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Fight;
        if (!g_buildMenu.movementWasDisabled)
            player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Movement;
    }

    g_buildMenu.open = false;
    g_buildMenu.lastHudTick = 0;
    HideGModSpawnOverlay();
    PlayGModUISound("ui_return", "fx\\rem\\gmod\\garrysmod\\ui_return.wav");
    Notify("[GMOD] Build menu closed");
}

static void ToggleBuildMenu()
{
    if (g_buildMenu.open) CloseBuildMenu();
    else OpenBuildMenu();
}

static void ChangeBuildCategory(int delta)
{
    const int count = static_cast<int>(GetBuildCategoryCount());
    if (count <= 0) return;

    int next = static_cast<int>(g_buildMenu.categoryIndex) + delta;
    while (next < 0) next += count;
    while (next >= count) next -= count;
    g_buildMenu.categoryIndex = static_cast<UInt32>(next);
    g_buildMenu.itemIndex = 0;
    PlayGModUISound("ui_hover", "fx\\rem\\gmod\\garrysmod\\ui_hover.wav");
    ShowBuildMenuStatus(true);
}

static void ChangeBuildItem(int delta)
{
    const GModPropCategoryRange* category = GetSelectedBuildCategory();
    if (!category || !category->count) return;

    const int count = static_cast<int>(category->count);
    int next = static_cast<int>(g_buildMenu.itemIndex) + delta;
    while (next < 0) next += count;
    while (next >= count) next -= count;
    g_buildMenu.itemIndex = static_cast<UInt32>(next);
    PlayGModUISound("ui_hover", "fx\\rem\\gmod\\garrysmod\\ui_hover.wav");
    ShowBuildMenuStatus(true);
}

static void SpawnSelectedBuildProp()
{
    PlayGModUISound("ui_click", "fx\\rem\\gmod\\garrysmod\\ui_click.wav");

    const GModPropDef* prop = GetSelectedBuildProp();
    if (!prop) return;

    _MESSAGE("[GMOD-BUILD] spawn category=%s name=%s source=%s nif=%s",
        prop->category, prop->displayName, prop->sourceModel, prop->nifPath);

    if (prop->sourceModel && _strnicmp(prop->sourceModel, "npc:", 4) == 0)
        SpawnGModNpcProxy(prop);
    else
        SpawnConvertedProp(prop->nifPath, 220.0f, prop->displayName);
    ShowBuildMenuStatus(true);
}

static void UpdateBuildMenuControls()
{
    if (!g_buildMenu.open) return;

    if (GetAsyncKeyState(VK_ESCAPE) & 1)
    {
        CloseBuildMenu();
        return;
    }

    const bool shift = (GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0;

    if (GetAsyncKeyState(VK_LEFT) & 1) ChangeBuildCategory(shift ? -5 : -1);
    if (GetAsyncKeyState(VK_RIGHT) & 1) ChangeBuildCategory(shift ? 5 : 1);
    if (GetAsyncKeyState(VK_UP) & 1) ChangeBuildItem(-1);
    if (GetAsyncKeyState(VK_DOWN) & 1) ChangeBuildItem(1);
    if (GetAsyncKeyState(VK_PRIOR) & 1) ChangeBuildItem(shift ? -100 : -10);
    if (GetAsyncKeyState(VK_NEXT) & 1) ChangeBuildItem(shift ? 100 : 10);

    const GModPropCategoryRange* selectedCategory = GetSelectedBuildCategory();
    if ((GetAsyncKeyState(VK_HOME) & 1) && selectedCategory && selectedCategory->count)
    {
        g_buildMenu.itemIndex = 0;
        ShowBuildMenuStatus(true);
    }
    if ((GetAsyncKeyState(VK_END) & 1) && selectedCategory && selectedCategory->count)
    {
        g_buildMenu.itemIndex = selectedCategory->count - 1;
        ShowBuildMenuStatus(true);
    }

    if (GetAsyncKeyState(VK_RETURN) & 1)
        SpawnSelectedBuildProp();

    if (GetAsyncKeyState('Z') & 1)
        UndoLastSpawn();

    ShowBuildMenuStatus(false);
}

static void SpawnBarrelTest()
{
    SpawnConvertedProp("rem\\gmod\\props_c17\\oildrum001.nif", 220.0f);
}

static bool HasSafeConsoleScriptContext()
{
    ConsoleManager* consoleManager = ConsoleManager::GetSingleton();
    return consoleManager && consoleManager->scriptContext;
}

static void DebugCOCTestCell()
{
    _MESSAGE("[TEST] F11 COC Goodsprings requested");

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell || !HasSafeConsoleScriptContext())
    {
        _MESSAGE("[TEST] COC skipped: gameplay/script context not ready");
        Notify("[TEST] COC is available only after gameplay has loaded");
        return;
    }

    const bool ok = Script::RunScriptLine2("coc Goodsprings", player, true);
    _MESSAGE("[TEST] COC command result=%d", ok ? 1 : 0);
}

static void UpdateAutoTest()
{
    if (!g_autoTestEnabled)
        return;

    const DWORD now = GetTickCount();

    if (!g_autoTestLoadIssued)
    {
        // Never execute console script commands from the main menu. New Vegas can expose
        // a non-null ConsoleManager/scriptContext there that is still unsafe to run.
        // The integration test now begins only after a real gameplay cell is loaded.
        PlayerCharacter* player = PlayerCharacter::GetSingleton();
        if (!player || !player->parentCell || !HasSafeConsoleScriptContext())
        {
            if (!g_autoTestContextWaitLogged && now - g_autoTestStartTick >= 8000)
            {
                _MESSAGE("[AUTOTEST] waiting for a loaded gameplay cell");
                g_autoTestContextWaitLogged = true;
            }
            return;
        }

        EnsureSkateboardWeapon();
        EnsureGModWeaponForms();
        _MESSAGE("[AUTOTEST] gameplay cell=%08X skateboard=%08X gmodWeapons=%u",
            player->parentCell->refID,
            g_skateboardWeapon ? g_skateboardWeapon->refID : 0,
            static_cast<unsigned>(g_gmodRuntimeWeapons.size()));

        g_autoTestLoadIssued = true;
        g_autoTestSpawnPending = true;
        g_autoTestSpawnTick = now + 2500;
        return;
    }

    if (g_autoTestSpawnPending && !g_autoTestSpawnRequested && now >= g_autoTestSpawnTick)
    {
        PlayerCharacter* player = PlayerCharacter::GetSingleton();
        if (!player || !player->parentCell)
            return;

        _MESSAGE("[AUTOTEST] loaded cell=%08X; spawning converted barrel", player->parentCell->refID);
        g_autoTestSpawnRequested = true;
        TESObjectREFR* spawned = SpawnConvertedProp("rem\\gmod\\props_c17\\oildrum001.nif", 220.0f);
        if (spawned)
            CompleteAutoTestSpawn(spawned);
        else if (!g_pendingSpawnForm)
        {
            _MESSAGE("[AUTOTEST] FAIL spawn did not start");
            DeleteFileA(kAutoTestFlag);
            g_autoTestEnabled = false;
            g_autoTestSpawnPending = false;
            g_autoTestSpawnRequested = false;
        }
    }
}

static void GrabCrosshairRef()
{
    TESObjectREFR* target = GetCrosshairTarget();
    if (!target)
    {
        PlayPhysgunDryFireSound();
        Notify("[GMOD] No valid target under crosshair");
        return;
    }

    if (IsFrozenRef(target->refID))
        UnfreezeRef(target);

    if (IsActorReference(target))
    {
        // Preserve the pre-grab process state. Then ask the engine to knock the actor
        // down and observe the exact state New Vegas selected instead of guessing it.
        UInt8 originalState = 0;
        TryGetActorKnockedState(target, originalState);
        g_physgunHeldOriginalKnockedState = originalState;

        Script::RunScriptLine2("setunconscious 1", target, true);
        Script::RunScriptLine2("pushactoraway player 1", target, true);

        UInt8 observedState = 0;
        if (TryGetActorKnockedState(target, observedState) && observedState != 0)
            g_physgunHeldForcedKnockedState = observedState;
        else
            g_physgunHeldForcedKnockedState = 1;

        g_physgunHeldUsingRagdollBodies = false;
        TrySetActorKnockedState(target, g_physgunHeldForcedKnockedState);

        _MESSAGE(
            "[GMOD Physgun] grabbed actor %08X originalKnocked=%u forcedKnocked=%u",
            target->refID,
            static_cast<unsigned>(g_physgunHeldOriginalKnockedState),
            static_cast<unsigned>(g_physgunHeldForcedKnockedState));

        if (g_physgunActorWakeRefID == target->refID)
        {
            g_physgunActorWakeRefID = 0;
            g_physgunActorWakeTick = 0;
            g_physgunActorWakeRestoreState = 0;
        }
    }

    g_heldRef = target;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player)
    {
        g_heldRef = nullptr;
        return;
    }

    const float dx = target->posX - player->posX;
    const float dy = target->posY - player->posY;
    const float dz = target->posZ - (player->posZ + 58.0f);
    g_holdDistance = std::sqrt(dx * dx + dy * dy + dz * dz);
    if (!std::isfinite(g_holdDistance))
        g_holdDistance = 220.0f;
    if (g_holdDistance < kGModPhysgunMinRange)
        g_holdDistance = kGModPhysgunMinRange;
    if (g_holdDistance > kGModPhysgunMaxRange)
        g_holdDistance = kGModPhysgunMaxRange;

    PlayPhysgunPickupSound();
    char msg[96];
    std::snprintf(msg, sizeof(msg), "[GMOD] Physgun grabbed %08X", g_heldRef->refID);
    Notify(msg);
}

static void ThrowHeld()
{
    if (!g_heldRef) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player) return;

    const float yaw = player->rotZ;
    const float pitch = player->rotX;
    const float cp = std::cos(pitch);

    const float vx = std::sin(yaw) * cp * 1550.0f;
    const float vy = std::cos(yaw) * cp * 1550.0f;
    const float vz = -std::sin(pitch) * 1550.0f + 180.0f;

    if (IsActorReference(g_heldRef))
    {
        TESObjectREFR* actorRef = g_heldRef;

        // Keep the exact engine-observed knocked state while the launch impulse is
        // applied, then restore the actor's pre-grab state after the recovery delay.
        Script::RunScriptLine2("setunconscious 1", actorRef, true);
        TrySetActorKnockedState(actorRef, g_physgunHeldForcedKnockedState);

        Script::RunScriptLine2("pushactoraway player 1", actorRef, true);
        TrySetActorKnockedState(actorRef, g_physgunHeldForcedKnockedState);

        const SInt32 launchedBodies =
            SetActorRagdollLinearVelocity(actorRef, vx, vy, vz);
        if (launchedBodies <= 0)
            Script::RunScriptLine2("pushactoraway player 22", actorRef, true);
        else
            _MESSAGE("[GMOD Physgun] launched %d actor ragdoll rigid bodies", launchedBodies);

        g_physgunActorWakeRefID = actorRef->refID;
        g_physgunActorWakeTick = GetTickCount() + 3500;
        g_physgunActorWakeRestoreState = g_physgunHeldOriginalKnockedState;
        g_physgunHeldOriginalKnockedState = 0;
        g_physgunHeldForcedKnockedState = 1;
        g_physgunHeldUsingRagdollBodies = false;
        g_heldRef = nullptr;
        PlayPhysgunLaunchSound();

        Notify("[GMOD] Physgun launched NPC ragdoll");
        return;
    }

    if (void* rigidBody = GetRootHavokRigidBody(g_heldRef))
    {
        SetHavokLinearVelocity(rigidBody, vx, vy, vz);
        g_heldRef = nullptr;
        PlayPhysgunLaunchSound();
        Notify("[GMOD] Physgun launch (Havok)");
        return;
    }

    g_throw.ref = g_heldRef;
    g_throw.vx = vx;
    g_throw.vy = vy;
    g_throw.vz = vz;
    g_throw.lastTick = GetTickCount();
    g_throw.endTick = g_throw.lastTick + 550;

    Script::RunScriptLine2("pushactoraway player 18", g_throw.ref, true);

    g_heldRef = nullptr;
    PlayPhysgunLaunchSound();
    Notify("[GMOD] Physgun launch");
}

static void UpdateHeldObject()
{
    if (!(g_physgunEnabled || g_weaponPhysgunActive) || !g_heldRef) return;

    const DWORD now = GetTickCount();
    if (now - g_lastHoldUpdate < 16) return;

    float dt = g_lastHoldUpdate ? (now - g_lastHoldUpdate) / 1000.0f : 0.016f;
    g_lastHoldUpdate = now;
    if (dt <= 0.0f) dt = 0.016f;
    if (dt > 0.050f) dt = 0.050f;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player) return;

    if (g_holdDistance < kGModPhysgunMinRange)
        g_holdDistance = kGModPhysgunMinRange;
    if (g_holdDistance > kGModPhysgunMaxRange)
        g_holdDistance = kGModPhysgunMaxRange;

    const float yaw = player->rotZ;
    const float pitch = player->rotX;
    const float cp = std::cos(pitch);
    const float eyeZ = player->posZ + 58.0f;

    const float targetX = player->posX + std::sin(yaw) * cp * g_holdDistance;
    const float targetY = player->posY + std::cos(yaw) * cp * g_holdDistance;
    const float targetZ = eyeZ - std::sin(pitch) * g_holdDistance;

    const float errorX = targetX - g_heldRef->posX;
    const float errorY = targetY - g_heldRef->posY;
    const float errorZ = targetZ - g_heldRef->posZ;

    const bool actorHeld = IsActorReference(g_heldRef);
    const float timeToArrive =
        actorHeld ? kGModPhysgunTimeToArriveRagdoll : kGModPhysgunTimeToArrive;

    // Source's CPhysGunControllerPoint passes these values into the Havok
    // shadow-controller. New Vegas doesn't expose that Source interface, so
    // reproduce its arrival target using the exact Source controller inputs:
    // desired velocity reaches the hold target within timeToArrive, then the
    // current velocity is damped by physgun_DampingFactor.
    float desiredX = errorX / timeToArrive;
    float desiredY = errorY / timeToArrive;
    float desiredZ = errorZ / timeToArrive;

    float currentX = 0.0f;
    float currentY = 0.0f;
    float currentZ = 0.0f;

    void* propBody = nullptr;
    if (!actorHeld)
    {
        propBody = GetRootHavokRigidBody(g_heldRef);
        if (propBody)
            GetHavokLinearVelocity(propBody, currentX, currentY, currentZ);
    }

    float vx = desiredX - currentX * kGModPhysgunDampingFactor;
    float vy = desiredY - currentY * kGModPhysgunDampingFactor;
    float vz = desiredZ - currentZ * kGModPhysgunDampingFactor;

    // Source has both maxSpeed=5000 and maxSpeedDamping=10000.
    const float maxDelta = kGModPhysgunMaxSpeedDamping * dt;
    float deltaSq = vx * vx + vy * vy + vz * vz;
    if (deltaSq > maxDelta * maxDelta && maxDelta > 0.0f)
    {
        const float scale = maxDelta / std::sqrt(deltaSq);
        vx *= scale;
        vy *= scale;
        vz *= scale;
    }

    const float speedSq = vx * vx + vy * vy + vz * vz;
    if (speedSq > kGModPhysgunMaxSpeed * kGModPhysgunMaxSpeed)
    {
        const float scale = kGModPhysgunMaxSpeed / std::sqrt(speedSq);
        vx *= scale;
        vy *= scale;
        vz *= scale;
    }

    if (actorHeld)
    {
        TrySetActorKnockedState(g_heldRef, g_physgunHeldForcedKnockedState);

        const SInt32 drivenBodies =
            SetActorRagdollLinearVelocity(g_heldRef, vx, vy, vz);
        if (drivenBodies > 0)
        {
            if (!g_physgunHeldUsingRagdollBodies)
            {
                g_physgunHeldUsingRagdollBodies = true;
                _MESSAGE(
                    "[GMOD Physgun] Source-derived ragdoll controller active %08X (%d bodies)",
                    g_heldRef->refID, drivenBodies);
            }
            return;
        }

        SetRefPosition(g_heldRef, targetX, targetY, targetZ);
        return;
    }

    if (propBody)
    {
        SetHavokLinearVelocity(propBody, vx, vy, vz);

        // Match GMod's movement-key rotation control using the recovered
        // phys_spinspeed=200 and rotation sensitivity=0.05.
        float spin = 0.0f;
        if (GetAsyncKeyState('A') & 0x8000) spin += 1.0f;
        if (GetAsyncKeyState('D') & 0x8000) spin -= 1.0f;
        if (spin != 0.0f)
        {
            const float angular =
                spin * kGModPhysgunSpinSpeed * kGModPhysgunRotationSensitivity;
            SetHavokAngularVelocity(propBody, 0.0f, 0.0f, angular);
        }
        return;
    }

    SetRefPosition(g_heldRef, targetX, targetY, targetZ);
}

static void UpdateThrow()
{
    DWORD now = GetTickCount();

    if (g_physgunActorWakeRefID &&
        g_physgunActorWakeTick &&
        now >= g_physgunActorWakeTick)
    {
        TESObjectREFR* actorRef = LookupReference(g_physgunActorWakeRefID);
        if (actorRef && IsActorReference(actorRef))
        {
            TrySetActorKnockedState(actorRef, g_physgunActorWakeRestoreState);
            Script::RunScriptLine2("setunconscious 0", actorRef, true);
            _MESSAGE(
                "[GMOD Physgun] woke actor %08X restoreKnocked=%u",
                actorRef->refID,
                static_cast<unsigned>(g_physgunActorWakeRestoreState));
        }

        g_physgunActorWakeRefID = 0;
        g_physgunActorWakeTick = 0;
        g_physgunActorWakeRestoreState = 0;
    }

    if (!g_throw.ref) return;
    if (now >= g_throw.endTick)
    {
        g_throw.ref = nullptr;
        return;
    }

    DWORD dtMs = now - g_throw.lastTick;
    if (dtMs < 16) return;
    g_throw.lastTick = now;

    const float dt = dtMs / 1000.0f;
    TESObjectREFR* ref = g_throw.ref;

    g_throw.vz -= 850.0f * dt;
    const float x = ref->posX + g_throw.vx * dt;
    const float y = ref->posY + g_throw.vy * dt;
    const float z = ref->posZ + g_throw.vz * dt;
    SetRefPosition(ref, x, y, z);
}

static void AddSkateTrick(const char* name, float baseScore, float flipDegrees = 0.0f)
{
    if (!name || !*name) return;

    if (!g_skate.comboActive)
    {
        g_skate.comboActive = true;
        g_skate.comboScore = 0.0f;
        g_skate.comboMultiplier = 1.0f;
        g_skate.trickCount = 0;
    }

    g_skate.comboScore += baseScore;
    ++g_skate.trickCount;
    g_skate.comboMultiplier += 0.25f;
    if (g_skate.comboMultiplier > 8.0f)
        g_skate.comboMultiplier = 8.0f;

    g_skate.special01 += baseScore / 1600.0f;
    if (g_skate.special01 > 1.0f)
        g_skate.special01 = 1.0f;

    if (flipDegrees != 0.0f)
        g_skate.flipRemaining += flipDegrees;

    strncpy_s(g_skate.lastTrick, sizeof(g_skate.lastTrick), name, _TRUNCATE);
    g_skate.comboBankDeadline = 0;
}

static void ResetActiveSkateCombo()
{
    g_skate.comboScore = 0.0f;
    g_skate.comboMultiplier = 1.0f;
    g_skate.comboActive = false;
    g_skate.trickCount = 0;
    g_skate.manualVariant = 0;
    g_skate.grindVariant = 0;
    g_skate.lipVariant = 0;
    g_skate.comboBankDeadline = 0;
    g_skate.lastTrick[0] = 0;
}

static void BankSkateCombo()
{
    if (!g_skate.comboActive || g_skate.comboScore <= 0.0f)
    {
        ResetActiveSkateCombo();
        return;
    }

    const float banked = g_skate.comboScore * g_skate.comboMultiplier;
    g_skate.totalScore += banked;
    g_skate.special01 += banked / 6000.0f;
    if (g_skate.special01 > 1.0f)
        g_skate.special01 = 1.0f;

    char msg[160];
    std::snprintf(msg, sizeof(msg), "[THUG2] COMBO BANKED %.0f  TOTAL %.0f",
        banked, g_skate.totalScore);
    Notify(msg);

    ResetActiveSkateCombo();
}

static const char* SkateMoveStateName(SkateMoveState state)
{
    switch (state)
    {
    case SkateMoveState::Ground: return "GROUND";
    case SkateMoveState::Air: return "AIR";
    case SkateMoveState::Grind: return "GRIND";
    case SkateMoveState::Manual: return "MANUAL";
    case SkateMoveState::Lip: return "LIP";
    case SkateMoveState::Skitch: return "SKITCH";
    default: return "SKATE";
    }
}

static const char* kManualTrickVariants[] = {
    "Manual",
    "Nose Manual",
    "One Foot Manual",
    "One Foot Nose Manual",
    "Handstand Manual"
};

static const char* kGrindTrickVariants[] = {
    "50-50 Grind",
    "Boardslide",
    "Lipslide",
    "Nosegrind",
    "5-0 Grind",
    "Crooked Grind",
    "Smith Grind",
    "Feeble Grind"
};

static const char* kLipTrickVariants[] = {
    "Lip Stall",
    "Axle Stall",
    "Rock to Fakie",
    "Blunt Stall",
    "Nose Stall"
};

static UInt8 CycleSkateVariant(UInt8 current, int delta, UInt32 count)
{
    if (!count) return 0;
    int next = static_cast<int>(current) + delta;
    while (next < 0) next += static_cast<int>(count);
    while (next >= static_cast<int>(count)) next -= static_cast<int>(count);
    return static_cast<UInt8>(next);
}

static void CycleManualTrick(int delta)
{
    const UInt32 count = static_cast<UInt32>(
        sizeof(kManualTrickVariants) / sizeof(kManualTrickVariants[0]));
    g_skate.manualVariant = CycleSkateVariant(g_skate.manualVariant, delta, count);
    AddSkateTrick(kManualTrickVariants[g_skate.manualVariant], 45.0f);
}

static void CycleGrindTrick(int delta)
{
    const UInt32 count = static_cast<UInt32>(
        sizeof(kGrindTrickVariants) / sizeof(kGrindTrickVariants[0]));
    g_skate.grindVariant = CycleSkateVariant(g_skate.grindVariant, delta, count);
    AddSkateTrick(kGrindTrickVariants[g_skate.grindVariant], 55.0f);
}

static void CycleLipTrick(int delta)
{
    const UInt32 count = static_cast<UInt32>(
        sizeof(kLipTrickVariants) / sizeof(kLipTrickVariants[0]));
    g_skate.lipVariant = CycleSkateVariant(g_skate.lipVariant, delta, count);
    AddSkateTrick(kLipTrickVariants[g_skate.lipVariant], 50.0f);
}

static void FinalizeSkateSpin()
{
    const float absoluteSpin = std::fabs(g_skate.spinDegrees);
    int spin = static_cast<int>((absoluteSpin + 90.0f) / 180.0f) * 180;
    if (spin < 180)
        return;
    if (spin > 1440)
        spin = 1440;

    char base[64] = {};
    if (g_skate.lastTrick[0])
        strncpy_s(base, sizeof(base), g_skate.lastTrick, _TRUNCATE);
    else
        strncpy_s(base, sizeof(base), "Ollie", _TRUNCATE);

    char named[64] = {};
    std::snprintf(
        named, sizeof(named), "%s %d %s",
        g_skate.spinDegrees >= 0.0f ? "FS" : "BS",
        spin, base);
    strncpy_s(g_skate.lastTrick, sizeof(g_skate.lastTrick), named, _TRUNCATE);

    g_skate.comboScore += static_cast<float>(spin) * 0.35f;
}

static void UpdateSkateMode()
{
    if (!g_skate.active) return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player) return;

    // Dedicated THUG2 exit: holding R or Backspace always returns to Fallout.
    if ((GetAsyncKeyState('R') & 0x8000) ||
        (GetAsyncKeyState(VK_BACK) & 0x8000))
    {
        ExitSkateMode();
        return;
    }

    const UInt32 diagFrame = ++g_thug2DiagFrameCount;
    const bool firstDiag = diagFrame <= 15;
    const bool heartbeatDiag = firstDiag || (diagFrame <= 180 && (diagFrame % 15u) == 0u);
    if (heartbeatDiag)
        _MESSAGE("[THUG2-DIAG] skate frame %u begin", static_cast<unsigned>(diagFrame));

    // Skate mode owns the camera while active.
    if (!player->bThirdPerson)
    {
        player->bThirdPerson = true;
        player->UpdateCamera(false, false);
    }
    // v84 diagnostic quarantine: repeated writes to the raw Camera3rd object's
    // local transform produced the visible upward pan immediately before the c0000005.
    // Leave the engine-owned camera untouched and verify the rest of skate mode.
    if (firstDiag) _MESSAGE("[THUG2-DIAG] raw camera profile skipped (v84 quarantine)");

    const DWORD now = GetTickCount();
    float dt = (now - g_skate.lastTick) / 1000.0f;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] timing raw dt=%.6f now=%u last=%u",
        dt, static_cast<unsigned>(now), static_cast<unsigned>(g_skate.lastTick));
    if (dt <= 0.0f)
    {
        if (firstDiag) _MESSAGE("[THUG2-DIAG] timing early return dt<=0");
        return;
    }
    if (dt > 0.05f) dt = 0.05f;
    g_skate.lastTick = now;
    const SkateMoveState stateBefore = g_skate.moveState;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] timing/state complete state=%u speed=%.4f",
        static_cast<unsigned>(stateBefore), g_skate.speed01);

    const bool push = (GetAsyncKeyState('W') & 0x8000) != 0;
    const bool brake = (GetAsyncKeyState('S') & 0x8000) != 0;
    const bool left = (GetAsyncKeyState('A') & 0x8000) != 0;
    const bool right = (GetAsyncKeyState('D') & 0x8000) != 0;
    const bool jump = (GetAsyncKeyState(VK_SPACE) & 0x8000) != 0;
    const bool spinLeft = (GetAsyncKeyState('Q') & 0x8000) != 0;
    const bool spinRight = (GetAsyncKeyState('E') & 0x8000) != 0;
    const bool manual = (GetAsyncKeyState('M') & 0x8000) != 0;
    const bool grind = (GetAsyncKeyState('G') & 0x8000) != 0;
    const bool lip = (GetAsyncKeyState('L') & 0x8000) != 0;
    const bool nollieToggleDown = (GetAsyncKeyState('N') & 0x8000) != 0;
    const bool pressureToggleDown = (GetAsyncKeyState('P') & 0x8000) != 0;
    const bool revertDown = (GetAsyncKeyState('V') & 0x8000) != 0;
    const bool revertPressed = revertDown && !g_skate.revertWasDown;
    const bool skitchDown = (GetAsyncKeyState('K') & 0x8000) != 0;
    const bool flipDown = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;
    const bool grabDown = (GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0;
    const bool fastPush = (GetAsyncKeyState(VK_LSHIFT) & 0x8000) != 0;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] input capture complete W=%u S=%u A=%u D=%u jump=%u LMB=%u RMB=%u",
        push?1u:0u, brake?1u:0u, left?1u:0u, right?1u:0u,
        jump?1u:0u, flipDown?1u:0u, grabDown?1u:0u);

    // THUG2 exposes InNollie/NollieOn/NollieOff as a distinct skater state.
    if (nollieToggleDown && !g_skate.nollieToggleWasDown)
    {
        g_skate.nollieActive = !g_skate.nollieActive;
        if (g_skate.nollieActive)
            g_skate.pressureActive = false;
        Notify(g_skate.nollieActive ? "[THUG2] Nollie stance ON" : "[THUG2] Nollie stance OFF");
    }
    g_skate.nollieToggleWasDown = nollieToggleDown;

    // The THUG2 script table exposes InPressure/PressureOn/PressureOff
    // immediately beside the Nollie state. Treat it as a separate stance.
    if (pressureToggleDown && !g_skate.pressureToggleWasDown)
    {
        g_skate.pressureActive = !g_skate.pressureActive;
        if (g_skate.pressureActive)
            g_skate.nollieActive = false;
        Notify(g_skate.pressureActive ? "[THUG2] Pressure stance ON" : "[THUG2] Pressure stance OFF");
    }
    g_skate.pressureToggleWasDown = pressureToggleDown;

    // THUG2 exposes Obj_AllowSkitching for moving objects. In this merge K
    // attaches to a recognized Source/GMod vehicle under the crosshair.
    if (skitchDown && !g_skate.skitchWasDown &&
        g_skate.moveState != SkateMoveState::Air &&
        !g_skate.skitchTargetRefID)
    {
        TESObjectREFR* skitchTarget = GetCrosshairTarget();
        const GModVehicleKind kind = GetGModVehicleKind(skitchTarget);
        if (skitchTarget && kind != GModVehicleKind::None && kind != GModVehicleKind::Seat)
        {
            g_skate.skitchTargetRefID = skitchTarget->refID;
            g_skate.moveState = SkateMoveState::Skitch;
            g_skate.balance = 0.0f;
            g_skate.comboBankDeadline = 0;
            g_skate.revertAvailable = false;
            AddSkateTrick("Skitch", 100.0f);
            Notify("[THUG2] Skitch attached");
        }
        else
        {
            Notify("[THUG2] Skitch: aim at a drivable Source/GMod vehicle");
        }
    }

    if (!skitchDown && g_skate.skitchTargetRefID)
    {
        g_skate.skitchTargetRefID = 0;
        if (g_skate.moveState == SkateMoveState::Skitch)
            g_skate.moveState = SkateMoveState::Ground;
        g_skate.balance = 0.0f;
        if (g_skate.comboActive)
            g_skate.comboBankDeadline = now + 850;
        Notify("[THUG2] Skitch released");
    }
    if (firstDiag) _MESSAGE("[THUG2-DIAG] stance/skitch section complete");

    // Momentum model: pushing builds speed, neutral input rolls down slowly, S brakes hard.
    if (push)
        g_skate.speed01 += (fastPush ? 0.95f : 0.62f) * dt;
    else
        g_skate.speed01 -= 0.055f * dt;

    if (brake)
        g_skate.speed01 -= 1.35f * dt;

    if (g_skate.speed01 < 0.0f) g_skate.speed01 = 0.0f;
    if (g_skate.speed01 > 1.0f) g_skate.speed01 = 1.0f;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] momentum complete speed=%.4f", g_skate.speed01);

    // THUG-style coast: keep New Vegas's own forward control held while momentum remains.
    // This preserves native collision, stairs, slopes and navmesh interaction instead of teleporting.
    const bool shouldCoastForward =
        g_skate.speed01 > 0.025f && !brake && !g_skate.skitchTargetRefID;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] coast decision desired=%u injected=%u",
        shouldCoastForward?1u:0u, g_skate.forwardHoldInjected?1u:0u);
    if (shouldCoastForward != g_skate.forwardHoldInjected)
    {
        if (firstDiag) _MESSAGE("[THUG2-DIAG] coast RunScriptLine2 begin");
        Script::RunScriptLine2(shouldCoastForward ? "holdkey 17" : "releasekey 17", player, true); // DIK_W
        if (firstDiag) _MESSAGE("[THUG2-DIAG] coast RunScriptLine2 complete");
        g_skate.forwardHoldInjected = shouldCoastForward;
    }
    if (firstDiag) _MESSAGE("[THUG2-DIAG] coast section complete");

    // Let New Vegas's own character controller move/collide; we only scale its movement speed.
    if (now - g_skate.lastSpeedApplyTick >= 50)
    {
        const float speedMult = g_skate.originalSpeedMult * (0.72f + 2.35f * g_skate.speed01);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] speed apply begin mult=%.4f", speedMult);
        SetPlayerSpeedMultiplier(player, speedMult);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] speed apply complete");
        g_skate.lastSpeedApplyTick = now;
    }
    if (firstDiag) _MESSAGE("[THUG2-DIAG] speed section complete");

    // Skate steering rotates the player's forward heading while preserving normal FNV collision.
    float steer = 0.0f;
    if (left && !right) steer = 1.0f;
    if (right && !left) steer = -1.0f;
    if (steer != 0.0f && g_skate.speed01 > 0.02f)
    {
        const float turnRate = 5.10f - (1.20f * g_skate.speed01);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] steer SetRefAngleZ begin");
        SetRefAngleZ(player, player->rotZ + steer * turnRate * dt);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] steer UpdateCamera begin");
        // THUG2 camera tracks the skater immediately instead of using the
        // slow vanilla Fallout third-person turn follow.
        player->UpdateCamera(false, false);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] steer UpdateCamera complete");
    }
    if (firstDiag) _MESSAGE("[THUG2-DIAG] steering section complete");

    // The native Space input still performs the actual collision-aware jump.
    // THUG2 also has a distinct late-wallplant path. A second Space press while
    // already airborne therefore attempts a wallplant instead of incorrectly
    // restarting the Ollie/air timer.
    const bool jumpPressed = jump && !g_skate.jumpWasDown;
    if (jumpPressed)
    {
        if (g_skate.moveState == SkateMoveState::Air)
        {
            TESObjectREFR* wall = GetCrosshairTarget();
            if (wall && !IsActorReference(wall))
            {
                const float dx = player->posX - wall->posX;
                const float dy = player->posY - wall->posY;
                const float dz = player->posZ - wall->posZ;
                const float distSq = dx * dx + dy * dy + dz * dz;

                // Keep wallplants local to the skater so aiming at distant geometry
                // cannot create a fake mid-air boost.
                if (distSq > 1.0f && distSq <= (260.0f * 260.0f))
                {
                    const DWORD airTime = now - g_skate.airStartTick;
                    const bool late = airTime >= 650;
                    AddSkateTrick(late ? "Late Wallplant" : "Wallplant",
                        late ? 225.0f : 175.0f);

                    const float horizontal =
                        std::sqrt(dx * dx + dy * dy);
                    if (horizontal > 1.0f)
                    {
                        const float inv = 1.0f / horizontal;
                        const float awayX = dx * inv;
                        const float awayY = dy * inv;

                        // Small separation impulse/step away from the contacted wall,
                        // while leaving subsequent travel to New Vegas's native
                        // character controller.
                        SetRefPosition(
                            player,
                            player->posX + awayX * 34.0f,
                            player->posY + awayY * 34.0f,
                            player->posZ + 24.0f);

                        SetRefAngleZ(
                            player,
                            std::atan2(awayX, awayY));
                    }
                    else
                    {
                        SetRefAngleZ(player, player->rotZ + 3.14159265f);
                    }

                    g_skate.airStartTick = now;
                    g_skate.sawDescending = false;
                    g_skate.landingStableFrames = 0;
                    g_skate.lastPlayerZ = player->posZ;
                    g_skate.comboBankDeadline = 0;
                    g_skate.revertAvailable = false;
                    g_skate.speed01 += 0.08f;
                    if (g_skate.speed01 > 1.0f) g_skate.speed01 = 1.0f;

                    Notify(late
                        ? "[THUG2] Late Wallplant"
                        : "[THUG2] Wallplant");
                }
            }
        }
        else
        {
            g_skate.moveState = SkateMoveState::Air;
            g_skate.airStartTick = now;
            g_skate.spinDegrees = 0.0f;
            g_skate.flipDegrees = 0.0f;
            g_skate.flipRemaining = 0.0f;
            g_skate.revertAvailable = false;
            AddSkateTrick(g_skate.nollieActive ? "Nollie" : "Ollie",
                g_skate.nollieActive ? 65.0f : 50.0f);
            PlayTHUG2OllieSound();
            StartTHUG2RetargetClip(g_skate.nollieActive ? "nollie" : "ollie", false, true);
            g_skate.sawDescending = false;
            g_skate.landingStableFrames = 0;
            g_skate.lastPlayerZ = player->posZ;
        }
    }
    g_skate.jumpWasDown = jump;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] jump section complete moveState=%u",
        static_cast<unsigned>(g_skate.moveState));

    if (g_skate.moveState == SkateMoveState::Air)
    {
        const bool specialPressed =
            flipDown && grabDown &&
            (!g_skate.flipWasDown || !g_skate.grabWasDown);
        bool specialTriggered = false;

        if (specialPressed && g_skate.special01 >= 0.999f)
        {
            AddSkateTrick("Special Trick", 900.0f, 720.0f);
            g_skate.special01 = 0.0f;
            specialTriggered = true;
            Notify("[THUG2] SPECIAL!");
        }

        if (!specialTriggered && flipDown && !g_skate.flipWasDown)
        {
            if (g_skate.pressureActive)
            {
                if (push)
                    AddSkateTrick("Pressure Flip", 150.0f, 360.0f);
                else if (brake)
                    AddSkateTrick("Pressure Heelflip", 165.0f, -360.0f);
                else if (left)
                {
                    AddSkateTrick("Pressure Shove-It", 190.0f);
                    g_skate.spinDegrees += 180.0f;
                }
                else if (right)
                    AddSkateTrick("Pressure Impossible", 260.0f, 720.0f);
                else
                    AddSkateTrick("Pressure Flip", 150.0f, 360.0f);
            }
            else
            {
                if (push)
                    AddSkateTrick(g_skate.nollieActive ? "Nollie Kickflip" : "Kickflip",
                        g_skate.nollieActive ? 125.0f : 100.0f, 360.0f);
                else if (brake)
                    AddSkateTrick(g_skate.nollieActive ? "Nollie Heelflip" : "Heelflip",
                        g_skate.nollieActive ? 145.0f : 120.0f, -360.0f);
                else if (left)
                {
                    AddSkateTrick(g_skate.nollieActive ? "Nollie Shove-It" : "Pop Shove-It",
                        g_skate.nollieActive ? 175.0f : 150.0f);
                    g_skate.spinDegrees += 180.0f;
                }
                else if (right)
                    AddSkateTrick(g_skate.nollieActive ? "Nollie Impossible" : "Impossible",
                        g_skate.nollieActive ? 245.0f : 220.0f, 720.0f);
                else
                    AddSkateTrick(g_skate.nollieActive ? "Nollie Kickflip" : "Kickflip",
                        g_skate.nollieActive ? 125.0f : 100.0f, 360.0f);
            }
        }

        if (!specialTriggered && grabDown && !g_skate.grabWasDown)
        {
            if (push)
                AddSkateTrick("Nosegrab", 160.0f);
            else if (brake)
                AddSkateTrick("Tailgrab", 160.0f);
            else if (left)
                AddSkateTrick("Melon", 180.0f);
            else
                AddSkateTrick("Indy", 180.0f);
        }

        if (grabDown && !specialTriggered)
            g_skate.comboScore += 24.0f * dt;

        if (std::fabs(g_skate.flipRemaining) > 0.01f)
        {
            const float direction = g_skate.flipRemaining > 0.0f ? 1.0f : -1.0f;
            float step = direction * 900.0f * dt;
            if (std::fabs(step) > std::fabs(g_skate.flipRemaining))
                step = g_skate.flipRemaining;
            g_skate.flipDegrees += step;
            g_skate.flipRemaining -= step;
        }

        float spinDir = 0.0f;
        if (spinLeft && !spinRight) spinDir = 1.0f;
        if (spinRight && !spinLeft) spinDir = -1.0f;
        if (spinDir != 0.0f)
        {
            const float spinDelta = spinDir * 420.0f * dt;
            g_skate.spinDegrees += spinDelta;
            g_skate.comboScore += std::fabs(spinDelta) * 1.25f;
        }

        // Use the player's real vertical movement instead of a fixed jump timer.
        // A landing is accepted only after the player has actually descended and then
        // remained vertically stable for several frames. A long timeout is a failsafe.
        const float verticalStep = player->posZ - g_skate.lastPlayerZ;
        if (verticalStep < -0.20f)
            g_skate.sawDescending = true;

        if (g_skate.sawDescending && std::fabs(verticalStep) < 0.12f)
            ++g_skate.landingStableFrames;
        else if (std::fabs(verticalStep) > 0.30f)
            g_skate.landingStableFrames = 0;

        const DWORD airTime = now - g_skate.airStartTick;

        // THUG2's SkaterCorePhysicsComponent contains an explicit
        // "GRINDING FROM ACID DROP" transition. Holding G while descending
        // transfers the live air combo directly into the grind state instead
        // of banking it as a normal landing.
        if (grind && g_skate.sawDescending && airTime > 300 && g_skate.speed01 > 0.10f)
        {
            FinalizeSkateSpin();
            AddSkateTrick("Acid Drop", 175.0f);
            g_skate.moveState = SkateMoveState::Grind;
            PlayTHUG2GrindSound();
            g_skate.grindVariant = 0;
            g_skate.balance = 0.0f;
            g_skate.comboBankDeadline = 0;
            g_skate.revertAvailable = false;
            g_skate.landingStableFrames = 0;
            g_skate.sawDescending = false;
            g_skate.speed01 += 0.06f;
            if (g_skate.speed01 > 1.0f) g_skate.speed01 = 1.0f;
            Notify("[THUG2] Acid Drop -> Grind");
        }
        else if ((g_skate.sawDescending && g_skate.landingStableFrames >= 4 && airTime > 300) ||
                 airTime > 2200)
        {
            g_skate.moveState = SkateMoveState::Ground;
            const bool cleanLanding =
                std::fabs(g_skate.flipRemaining) < 0.01f &&
                std::fabs(g_skate.balance) < 0.75f;
            PlayTHUG2LandSound(cleanLanding);
            FinalizeSkateSpin();
            g_skate.spinDegrees = 0.0f;
            g_skate.flipDegrees = 0.0f;
            g_skate.flipRemaining = 0.0f;
            g_skate.balance = 0.0f;
            if (g_skate.comboActive)
            {
                g_skate.comboBankDeadline = now + 850;
                g_skate.revertAvailable = true;
            }
            else
            {
                g_skate.revertAvailable = false;
            }
        }

        g_skate.lastPlayerZ = player->posZ;
    }
    else if (g_skate.skitchTargetRefID)
    {
        TESObjectREFR* skitchTarget = LookupReference(g_skate.skitchTargetRefID);
        const GModVehicleKind kind = GetGModVehicleKind(skitchTarget);

        if (!skitchTarget || kind == GModVehicleKind::None || kind == GModVehicleKind::Seat)
        {
            g_skate.skitchTargetRefID = 0;
            g_skate.moveState = SkateMoveState::Ground;
            g_skate.balance = 0.0f;
            if (g_skate.comboActive)
                g_skate.comboBankDeadline = now + 850;
            Notify("[THUG2] Skitch target lost");
        }
        else
        {
            float vehicleSpeed = 0.0f;
            if (void* body = GetRootHavokRigidBody(skitchTarget))
            {
                float vx = 0.0f, vy = 0.0f, vz = 0.0f;
                GetHavokLinearVelocity(body, vx, vy, vz);
                vehicleSpeed = std::sqrt(vx * vx + vy * vy);
            }

            const float topSpeed = GModVehicleTopSpeed(kind);
            if (topSpeed > 1.0f)
            {
                float normalized = vehicleSpeed / topSpeed;
                if (normalized < 0.12f) normalized = 0.12f;
                if (normalized > 1.0f) normalized = 1.0f;
                g_skate.speed01 = normalized;
            }

            const float yaw = skitchTarget->rotZ;
            const float behind = 155.0f;
            const float followX = skitchTarget->posX - std::sin(yaw) * behind;
            const float followY = skitchTarget->posY - std::cos(yaw) * behind;
            const float followZ = skitchTarget->posZ + 48.0f;
            SetRefPosition(player, followX, followY, followZ);
            SetRefAngleZ(player, yaw);

            g_skate.moveState = SkateMoveState::Skitch;
            g_skate.comboBankDeadline = 0;

            const float correction =
                (left ? -1.30f : 0.0f) + (right ? 1.30f : 0.0f);
            const float drift = std::sin(now * 0.0043f) * 0.40f;
            g_skate.balance += (correction + drift) * dt;
            g_skate.comboScore += 34.0f * dt;

            if (std::fabs(g_skate.balance) > 1.0f)
            {
                g_skate.skitchTargetRefID = 0;
                g_skate.moveState = SkateMoveState::Ground;
                g_skate.speed01 *= 0.35f;
                g_skate.balance = 0.0f;
                ResetActiveSkateCombo();
                Notify("[THUG2] BAIL - skitch balance lost");
            }
        }
    }
    else if (revertPressed &&
             g_skate.revertAvailable &&
             g_skate.comboActive &&
             g_skate.comboBankDeadline &&
             now < g_skate.comboBankDeadline)
    {
        // THUG2 core physics exposes a dedicated revert path used to carry a combo
        // through the post-landing grace period. R is reserved for leaving skate mode
        // in this merge, so V performs the revert.
        AddSkateTrick("Revert", 75.0f);
        PlayTHUG2RevertSound();
        StartTHUG2RetargetClip(g_skate.spinDegrees >= 0.0f ? "revertfs" : "revertbs", false, true);
        g_skate.comboBankDeadline = 0;
        g_skate.revertAvailable = false;
        g_skate.speed01 *= 0.90f;
        SetRefAngleZ(player, player->rotZ + 3.14159265f);
        Notify("[THUG2] Revert - combo continued");
    }
    else if (lip && g_skate.speed01 > 0.02f)
    {
        if (stateBefore != SkateMoveState::Lip)
        {
            g_skate.lipVariant = 0;
            AddSkateTrick(kLipTrickVariants[g_skate.lipVariant], 85.0f);
            g_skate.balance = 0.0f;
        }
        else if (GetAsyncKeyState('Q') & 1)
            CycleLipTrick(-1);
        else if (GetAsyncKeyState('E') & 1)
            CycleLipTrick(1);

        g_skate.moveState = SkateMoveState::Lip;
        g_skate.comboBankDeadline = 0;
        g_skate.speed01 -= 0.42f * dt;
        if (g_skate.speed01 < 0.015f)
            g_skate.speed01 = 0.015f;

        const float correction =
            (left ? -1.15f : 0.0f) + (right ? 1.15f : 0.0f);
        const float drift = std::sin(now * 0.0041f) * 0.38f;
        g_skate.balance += (correction + drift) * dt;
        g_skate.comboScore += 38.0f * dt;

        if (std::fabs(g_skate.balance) > 1.0f)
        {
            g_skate.moveState = SkateMoveState::Ground;
            g_skate.speed01 *= 0.25f;
            ResetActiveSkateCombo();
            g_skate.balance = 0.0f;
            Notify("[THUG2] BAIL - lip balance lost");
        }
    }
    else if (grind && g_skate.speed01 > 0.10f)
    {
        if (stateBefore != SkateMoveState::Grind)
        {
            g_skate.grindVariant = 0;
            AddSkateTrick(kGrindTrickVariants[g_skate.grindVariant], 75.0f);
            PlayTHUG2GrindSound();
        }
        else if (GetAsyncKeyState('Q') & 1)
            CycleGrindTrick(-1);
        else if (GetAsyncKeyState('E') & 1)
            CycleGrindTrick(1);
        g_skate.moveState = SkateMoveState::Grind;
        g_skate.comboBankDeadline = 0;
        const float correction =
            (left ? -1.35f : 0.0f) + (right ? 1.35f : 0.0f);
        const float drift = std::sin(now * 0.0045f) * 0.42f;
        g_skate.balance += (correction + drift) * dt;
        g_skate.comboScore += 45.0f * dt;

        if (std::fabs(g_skate.balance) > 1.0f)
        {
            g_skate.moveState = SkateMoveState::Ground;
            g_skate.speed01 *= 0.35f;
            ResetActiveSkateCombo();
            g_skate.balance = 0.0f;
            Notify("[THUG2] BAIL - grind balance lost");
        }
    }
    else if (manual && g_skate.speed01 > 0.05f)
    {
        if (stateBefore != SkateMoveState::Manual)
        {
            g_skate.manualVariant = 0;
            AddSkateTrick(kManualTrickVariants[g_skate.manualVariant], 60.0f);
        }
        else if (GetAsyncKeyState('Q') & 1)
            CycleManualTrick(-1);
        else if (GetAsyncKeyState('E') & 1)
            CycleManualTrick(1);
        g_skate.moveState = SkateMoveState::Manual;
        g_skate.comboBankDeadline = 0;
        const float correction =
            (left ? -1.20f : 0.0f) + (right ? 1.20f : 0.0f);
        const float drift = std::sin(now * 0.0037f) * 0.34f;
        g_skate.balance += (correction + drift) * dt;
        g_skate.comboScore += 30.0f * dt;

        if (std::fabs(g_skate.balance) > 1.0f)
        {
            g_skate.moveState = SkateMoveState::Ground;
            g_skate.speed01 *= 0.45f;
            ResetActiveSkateCombo();
            g_skate.balance = 0.0f;
            Notify("[THUG2] BAIL - manual balance lost");
        }
    }
    else
    {
        g_skate.moveState = SkateMoveState::Ground;
        g_skate.balance *= 0.90f;

        if (g_skate.comboActive)
        {
            if (!g_skate.comboBankDeadline)
                g_skate.comboBankDeadline = now + 850;
            else if (now >= g_skate.comboBankDeadline)
                BankSkateCombo();
        }
    }

    if (firstDiag) _MESSAGE("[THUG2-DIAG] move-state branch complete state=%u",
        static_cast<unsigned>(g_skate.moveState));
    g_skate.flipWasDown = flipDown;
    g_skate.grabWasDown = grabDown;
    g_skate.revertWasDown = revertDown;
    g_skate.skitchWasDown = skitchDown;
    if (firstDiag) _MESSAGE("[THUG2-DIAG] input latch complete");

    if (firstDiag) _MESSAGE("[THUG2-DIAG] ride board update begin");
    UpdateRideBoardVisual();
    if (firstDiag) _MESSAGE("[THUG2-DIAG] ride board update complete");

    // Dedicated skate HUD overlay; no Fallout QueueUIMessage spam while skating.
    if (kTHUG2RetargetDiagnosticEnabled)
    {
        if (firstDiag) _MESSAGE("[THUG2-DIAG] retarget selection begin");
        UpdateTHUG2RetargetSelection(push, left, right, stateBefore, now);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] retarget selection complete");

        if (firstDiag) _MESSAGE("[THUG2-DIAG] retarget apply begin (delay active=%u)",
            now < g_thug2RetargetEarliestTick ? 1u : 0u);
        ApplyTHUG2RetargetAnimation(player, now);
        if (firstDiag) _MESSAGE("[THUG2-DIAG] retarget apply complete");
    }
    else if (heartbeatDiag)
    {
        _MESSAGE("[THUG2-DIAG] retarget skipped frame=%u", static_cast<unsigned>(diagFrame));
    }

    UpdateTHUGHudOverlay();
    if (heartbeatDiag)
        _MESSAGE("[THUG2-DIAG] skate frame %u complete", static_cast<unsigned>(diagFrame));
    if (diagFrame >= 15)
        g_thug2FirstUpdateDiag = true;

}

static float ReadCurrentWorldFov()
{
    InterfaceManager* ui = *reinterpret_cast<InterfaceManager**>(0x011D8A80);
    if (!ui) return 75.0f;

    void* graphs[2] = {
        reinterpret_cast<void*>(ui->sceneGraph004),
        reinterpret_cast<void*>(ui->sceneGraph008)
    };

    for (void* graph : graphs)
    {
        if (!graph) continue;
        const float fov = *reinterpret_cast<float*>(
            reinterpret_cast<UInt8*>(graph) + 0xEC);
        if (std::isfinite(fov) && fov >= 10.0f && fov <= 179.0f)
            return fov;
    }

    return 75.0f;
}

static void ApplyGModCameraFov(PlayerCharacter* player, float fov)
{
    if (!player) return;
    if (fov < 5.0f) fov = 5.0f;
    if (fov > 175.0f) fov = 175.0f;

    char cmd[64];
    std::snprintf(cmd, sizeof(cmd), "fov %.2f", fov);
    Script::RunScriptLine2(cmd, player, true);
}

static bool EnsureGdiPlus()
{
    if (g_gdiplusToken)
        return true;

    Gdiplus::GdiplusStartupInput input;
    return Gdiplus::GdiplusStartup(
        &g_gdiplusToken, &input, nullptr) == Gdiplus::Ok;
}

static bool GetJpegEncoderClsid(CLSID& clsid)
{
    UINT count = 0;
    UINT bytes = 0;
    Gdiplus::GetImageEncodersSize(&count, &bytes);
    if (!count || !bytes)
        return false;

    std::vector<BYTE> storage(bytes);
    Gdiplus::ImageCodecInfo* codecs =
        reinterpret_cast<Gdiplus::ImageCodecInfo*>(storage.data());

    if (Gdiplus::GetImageEncoders(count, bytes, codecs) != Gdiplus::Ok)
        return false;

    for (UINT i = 0; i < count; ++i)
    {
        if (codecs[i].MimeType &&
            _wcsicmp(codecs[i].MimeType, L"image/jpeg") == 0)
        {
            clsid = codecs[i].Clsid;
            return true;
        }
    }

    return false;
}

static bool CaptureGModCameraJpeg()
{
    if (!EnsureGdiPlus())
        return false;

    HWND hwnd = GetForegroundWindow();
    if (!hwnd)
        return false;

    RECT rc = {};
    if (!GetClientRect(hwnd, &rc))
        return false;

    const int width = rc.right - rc.left;
    const int height = rc.bottom - rc.top;
    if (width <= 0 || height <= 0)
        return false;

    HDC windowDC = GetDC(hwnd);
    if (!windowDC)
        return false;

    HDC memoryDC = CreateCompatibleDC(windowDC);
    HBITMAP bitmap = CreateCompatibleBitmap(windowDC, width, height);
    if (!memoryDC || !bitmap)
    {
        if (bitmap) DeleteObject(bitmap);
        if (memoryDC) DeleteDC(memoryDC);
        ReleaseDC(hwnd, windowDC);
        return false;
    }

    HGDIOBJ oldBitmap = SelectObject(memoryDC, bitmap);
    const BOOL copied = BitBlt(
        memoryDC, 0, 0, width, height,
        windowDC, 0, 0, SRCCOPY | CAPTUREBLT);
    SelectObject(memoryDC, oldBitmap);

    wchar_t gameDir[MAX_PATH] = {};
    wchar_t shotsDir[MAX_PATH] = {};
    wchar_t shotPath[MAX_PATH] = {};
    bool saved = false;

    if (copied && GetCurrentDirectoryW(MAX_PATH, gameDir))
    {
        _snwprintf_s(
            shotsDir, _countof(shotsDir), _TRUNCATE,
            L"%s\\Data\\NVSE\\Plugins\\FNVGModTHUG2_Shots", gameDir);
        CreateDirectoryW(shotsDir, nullptr);

        SYSTEMTIME st = {};
        GetLocalTime(&st);
        _snwprintf_s(
            shotPath, _countof(shotPath), _TRUNCATE,
            L"%s\\gmod_camera_%04u%02u%02u_%02u%02u%02u_%03u.jpg",
            shotsDir,
            st.wYear, st.wMonth, st.wDay,
            st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);

        CLSID jpegClsid = {};
        if (GetJpegEncoderClsid(jpegClsid))
        {
            Gdiplus::Status status = Gdiplus::GenericError;
            {
                Gdiplus::Bitmap image(bitmap, nullptr);
                status = image.Save(shotPath, &jpegClsid, nullptr);
            }
            saved = status == Gdiplus::Ok;
        }
    }

    DeleteObject(bitmap);
    DeleteDC(memoryDC);
    ReleaseDC(hwnd, windowDC);

    if (saved)
    {
        char utf8Path[MAX_PATH * 3] = {};
        WideCharToMultiByte(
            CP_UTF8, 0, shotPath, -1,
            utf8Path, static_cast<int>(sizeof(utf8Path)),
            nullptr, nullptr);
        _MESSAGE("[GMOD Camera] saved %s", utf8Path);
    }

    return saved;
}

static void PollControls()
{
    UpdateFalloutHudOwnership(g_gameplayReady && g_skate.active);
    // Never run gameplay/script-command logic on the title screen or during save transitions.
    // RunScriptLine2 depends on ConsoleManager::scriptContext, which is not valid until gameplay is loaded.
    if (!g_gameplayReady)
        return;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
        return;

    // Runtime form creation must not run on the first NewGame/PostLoadGame frames.
    // A loaded cell can exist before ConsoleManager::scriptContext is ready; calling
    // CloneForm/AddItem during that window was producing the repeatable FalloutNV.exe
    // access violation seen after v73.  Wait for both a grace period and a valid script context.
    const DWORD runtimeNow = GetTickCount();
    const bool runtimeFormContextReady =
        runtimeNow >= g_runtimeFormInitEarliestTick &&
        HasSafeConsoleScriptContext();

    if (runtimeFormContextReady)
    {
        if (!g_runtimeFormInitLogged)
        {
            _MESSAGE("[RUNTIME] safe form-init window reached");
            g_runtimeFormInitLogged = true;
        }

        if (!g_skateboardWeapon)
        {
            _MESSAGE("[RUNTIME] EnsureSkateboardWeapon begin");
            EnsureSkateboardWeapon();
            _MESSAGE("[RUNTIME] EnsureSkateboardWeapon end weapon=%p", g_skateboardWeapon);
        }

        if (!g_gmodWeaponFormsReady)
        {
            _MESSAGE("[RUNTIME] EnsureGModWeaponForms begin");
            EnsureGModWeaponForms();
            _MESSAGE("[RUNTIME] EnsureGModWeaponForms end count=%u",
                static_cast<unsigned>(g_gmodRuntimeWeapons.size()));
        }
    }

    if (!GameHasFocus()) return;

    // Garry's Mod spawn menu convention: Q opens/closes the spawn browser.
    // F2 remains available as a fallback while the full visual menu is being built.
    const bool buildMenuToggleDown =
        ((GetAsyncKeyState('Q') & 0x8000) != 0) ||
        ((GetAsyncKeyState(VK_F2) & 0x8000) != 0);
    if (!g_skate.active && buildMenuToggleDown && !g_buildMenuToggleWasDown)
        ToggleBuildMenu();
    g_buildMenuToggleWasDown = buildMenuToggleDown;

    if (g_buildMenu.open)
    {
        UpdateBuildMenuControls();
        UpdatePendingSpawn();
        UpdateAutoTest();
        UpdatePhysBeamOverlay();
        return;
    }

    UpdateGModVehicle();
    if (g_vehicle.active)
    {
        UpdatePendingSpawn();
        UpdatePhysBeamOverlay();
        return;
    }

    if (GetAsyncKeyState(VK_F6) & 1) ToggleNoClip();
    if (GetAsyncKeyState(VK_F7) & 1) TogglePhysgun();

    const bool skateboardEquipped = IsSkateboardEquipped();
    const bool attackDown = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;

    UpdateSkateboardCombatSuppression(player, skateboardEquipped);

    // Holding/equipping the skateboard is ordinary New Vegas gameplay.
    // Only the first attack press with this exact weapon deploys skate mode.
    if (!g_skate.active && skateboardEquipped && attackDown && !g_skateboardAttackWasDown)
        EnterSkateMode();

    // Switching away from the skateboard or pressing R explicitly restores FNV gameplay.
    if (g_skate.active && (!skateboardEquipped || (GetAsyncKeyState('R') & 1)))
        ExitSkateMode();

    g_skateboardAttackWasDown = attackDown;

    // THUG2 mode is a dedicated gameplay state. While active, do not process
    // GMod tools, vehicle controls, or ordinary merged-game interaction paths.
    if (g_skate.active)
    {
        UpdateSkateMode();
        UpdatePendingSpawn();
        UpdatePhysBeamOverlay();
        return;
    }

    if (GetAsyncKeyState(VK_F9) & 1) ToggleToolgun();
    if (GetAsyncKeyState(VK_F10) & 1) SpawnBarrelTest();
    if (GetAsyncKeyState(VK_F11) & 1) DebugCOCTestCell();

    // Runtime GMod weapon items drive their own behavior directly from the Pip-Boy weapon form.
    GModRuntimeWeapon* equippedGMod = GetEquippedGModRuntimeWeapon();
    const GModWeaponKind equippedKind = equippedGMod && equippedGMod->def
        ? equippedGMod->def->kind
        : GModWeaponKind::Utility;

    const bool weaponPhysgunNow = equippedGMod &&
        (equippedKind == GModWeaponKind::Physgun || equippedKind == GModWeaponKind::Physcannon);
    const bool weaponToolgunNow = equippedGMod && equippedKind == GModWeaponKind::Toolgun;
    const bool weaponCameraNow = equippedGMod && equippedKind == GModWeaponKind::Camera;

    if (g_weaponPhysgunActive && !weaponPhysgunNow && !g_physgunEnabled && g_heldRef)
        DropHeld();

    if (weaponCameraNow && !g_cameraWeaponActive)
    {
        g_cameraDefaultFov = ReadCurrentWorldFov();
        g_cameraZoomStep = 0;
        g_cameraWeaponActive = true;
        _MESSAGE("[GMOD Camera] equipped; captured default FOV %.2f", g_cameraDefaultFov);
    }
    else if (!weaponCameraNow && g_cameraWeaponActive)
    {
        ApplyGModCameraFov(player, g_cameraDefaultFov);
        g_cameraWeaponActive = false;
        g_cameraZoomStep = 0;
    }

    g_weaponPhysgunActive = weaponPhysgunNow;
    g_weaponToolgunActive = weaponToolgunNow;

    const bool gmodPrimaryDown = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;
    const bool gmodSecondaryDown = (GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0;
    const bool gmodPrimaryPressed = gmodPrimaryDown && !g_gmodAttackWasDown;
    const bool gmodSecondaryPressed = gmodSecondaryDown && !g_gmodSecondaryWasDown;
    const GModToolDef* selectedToolNow = GetSelectedToolMode();
    const bool selectedLeafblower =
        selectedToolNow && _stricmp(selectedToolNow->id, "leafblower") == 0;

    if (equippedGMod && !g_skate.active)
    {
        switch (equippedKind)
        {
        case GModWeaponKind::Physgun:
            // Garry's Mod Physics Gun controls in the merged runtime:
            // LMB grabs/drops; RMB launches the currently held prop/actor.
            if (gmodPrimaryPressed)
            {
                if (g_heldRef) DropHeld();
                else GrabCrosshairRef();
            }
            if (gmodSecondaryPressed)
            {
                if (g_heldRef) ThrowHeld();
                else PlayPhysgunDryFireSound();
            }
            if (GetAsyncKeyState('R') & 1)
                UnfreezeRef(GetCrosshairTarget());
            break;

        case GModWeaponKind::Physcannon:
            // Gravity Gun: primary punts, secondary picks up / drops.
            if (gmodPrimaryPressed)
            {
                if (!g_heldRef)
                    GrabCrosshairRef();
                if (g_heldRef)
                    ThrowHeld();
            }
            if (gmodSecondaryPressed)
            {
                if (g_heldRef) DropHeld();
                else GrabCrosshairRef();
            }
            break;

        case GModWeaponKind::Toolgun:
            if ((selectedLeafblower && gmodPrimaryDown) ||
                (!selectedLeafblower && gmodPrimaryPressed))
                ToolgunPrimaryAction();
            if (gmodSecondaryPressed)
                ToolgunSecondaryAction();
            if (GetAsyncKeyState('R') & 1)
            {
                if (!g_buildMenu.open)
                    OpenBuildMenu();
            }
            if (GetAsyncKeyState('Z') & 1)
                UndoLastRemoved();
            break;

        case GModWeaponKind::Medkit:
            if (gmodPrimaryPressed)
            {
                PlayMappedGModActionSound(equippedGMod->def->className);
                TESObjectREFR* target = GetCrosshairTarget();
                if (target)
                {
                    Script::RunScriptLine2("restoreav health 25", target, true);
                    Notify("[GMOD] Medkit healed target");
                }
                else
                {
                    Script::RunScriptLine2("restoreav health 25", player, true);
                    Notify("[GMOD] Medkit healed player");
                }
            }
            if (gmodSecondaryPressed)
            {
                PlayMappedGModActionSound(equippedGMod->def->className);
                Script::RunScriptLine2("restoreav health 25", player, true);
                Notify("[GMOD] Medkit self-heal");
            }
            break;

        case GModWeaponKind::Camera:
            if (gmodPrimaryPressed)
            {
                PlayMappedGModActionSound(equippedGMod->def->className);
                if (CaptureGModCameraJpeg())
                    Notify("[GMOD] Camera photo saved");
                else
                    Notify("[GMOD] Camera capture failed");
            }

            if (gmodSecondaryPressed)
            {
                static const float kZoomFovs[] = { 55.0f, 40.0f, 25.0f, 15.0f };
                g_cameraZoomStep = (g_cameraZoomStep + 1) % 5;

                const float fov = g_cameraZoomStep == 0
                    ? g_cameraDefaultFov
                    : kZoomFovs[g_cameraZoomStep - 1];
                ApplyGModCameraFov(player, fov);

                char msg[96];
                std::snprintf(msg, sizeof(msg), "[GMOD] Camera zoom %.0f FOV", fov);
                Notify(msg);
            }

            if (GetAsyncKeyState('R') & 1)
            {
                g_cameraZoomStep = 0;
                ApplyGModCameraFov(player, g_cameraDefaultFov);
                Notify("[GMOD] Camera zoom reset");
            }
            break;

        default:
            // Firearms/melee/grenades retain the cloned New Vegas weapon behavior.
            break;
        }
    }

    g_gmodAttackWasDown = gmodPrimaryDown;
    g_gmodSecondaryWasDown = gmodSecondaryDown;

    const bool toolgunInputActive = g_toolgunEnabled || g_weaponToolgunActive;
    if (toolgunInputActive && !equippedGMod &&
        ((selectedLeafblower && (GetAsyncKeyState(VK_LBUTTON) & 0x8000)) ||
         (!selectedLeafblower && (GetAsyncKeyState(VK_LBUTTON) & 1))))
        ToolgunPrimaryAction();
    if (toolgunInputActive && !equippedGMod && (GetAsyncKeyState(VK_RBUTTON) & 1))
        ToolgunSecondaryAction();
    if (toolgunInputActive && !equippedGMod && (GetAsyncKeyState('R') & 1))
    {
        if (!g_buildMenu.open)
            OpenBuildMenu();
    }

    if (toolgunInputActive && !equippedGMod && (GetAsyncKeyState('Z') & 1))
        UndoLastRemoved();

    const bool physgunInputActive = g_physgunEnabled || g_weaponPhysgunActive;
    if (physgunInputActive)
    {
        if (GetAsyncKeyState(VK_OEM_4) & 1)
        {
            g_holdDistance -= kGModPhysgunWheelSpeed;
            if (g_holdDistance < kGModPhysgunMinRange)
                g_holdDistance = kGModPhysgunMinRange;
        }
        if (GetAsyncKeyState(VK_OEM_6) & 1)
        {
            g_holdDistance += kGModPhysgunWheelSpeed;
            if (g_holdDistance > kGModPhysgunMaxRange)
                g_holdDistance = kGModPhysgunMaxRange;
        }

        // Old F7 debug mode keeps its original mouse behavior when no real phys weapon is equipped.
        if (g_physgunEnabled && !g_weaponPhysgunActive)
        {
            if (GetAsyncKeyState(VK_LBUTTON) & 1)
            {
                if (g_heldRef) DropHeld();
                else GrabCrosshairRef();
            }

            if (GetAsyncKeyState(VK_RBUTTON) & 1)
                FreezeHeld();
            if (GetAsyncKeyState('R') & 1)
                UnfreezeRef(GetCrosshairTarget());
        }
    }

    if (!g_skate.active && !toolgunInputActive && !physgunInputActive &&
        (GetAsyncKeyState(VK_LBUTTON) & 0x8000))
        DamageGModNpcProxyUnderCrosshair(equippedGMod);

    UpdateNoClip();
    UpdateFrozenProps();
    UpdateToolgunPhysics();
    UpdateGModNpcProxies();
    UpdateSkateMode();
    UpdateHeldObject();
    UpdateThrow();
    UpdatePendingSpawn();
    UpdateAutoTest();
    UpdatePhysBeamOverlay();
}

bool Cmd_gmod_spawnmenu_Execute(COMMAND_ARGS)
{
    ToggleBuildMenu();
    *result = g_buildMenu.open ? 1.0 : 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_spawnmenu, "Toggle the GMod build/spawn menu", 0, nullptr);

bool Cmd_noclip_Execute(COMMAND_ARGS)
{
    ToggleNoClip();
    *result = g_noClip ? 1.0 : 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(noclip, "Toggle GMod-style noclip mode", 0, nullptr);

bool Cmd_physgun_Execute(COMMAND_ARGS)
{
    TogglePhysgun();
    *result = g_physgunEnabled ? 1.0 : 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(physgun, "Toggle FNV-GMod physgun mode", 0, nullptr);

bool Cmd_physgun_drop_Execute(COMMAND_ARGS)
{
    DropHeld();
    *result = 1.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(physgun_drop, "Drop the currently held physgun target", 0, nullptr);

bool Cmd_toolgun_Execute(COMMAND_ARGS)
{
    ToggleToolgun();
    *result = g_toolgunEnabled ? 1.0 : 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(toolgun, "Toggle FNV-GMod toolgun mode", 0, nullptr);

bool Cmd_gmod_undo_Execute(COMMAND_ARGS)
{
    UndoLastRemoved();
    *result = 1.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_undo, "Undo the last FNV-GMod removable action", 0, nullptr);

bool Cmd_skatemode_Execute(COMMAND_ARGS)
{
    ToggleSkateMode();
    *result = g_skate.active ? 1.0 : 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(skatemode, "Toggle THUG2 skate mode", 0, nullptr);

bool Cmd_gmod_giveskateboard_Execute(COMMAND_ARGS)
{
    EnsureSkateboardWeapon();
    if (g_skateboardWeapon)
    {
        GiveWeaponToPlayer(g_skateboardWeapon);
        *reinterpret_cast<UInt32*>(result) = g_skateboardWeapon->refID;
        Console_Print("[THUG2] Skateboard weapon form = %08X", g_skateboardWeapon->refID);
    }
    else
    {
        *result = 0.0;
        Console_Print("[THUG2] Skateboard weapon is not ready (load into gameplay first)");
    }
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_giveskateboard, "Create/recover the THUG2 Skateboard weapon and print its form ID", 0, nullptr);

bool Cmd_gmod_grabstatus_Execute(COMMAND_ARGS)
{
    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    TESObjectREFR* grabbed = GetNativeGrabbedRef(player);
    void* spring = GetNativeMouseSpring(player);
    UInt32 mode = GetNativeGrabMode(player);
    float weight = GetNativeGrabbedWeight(player);
    float distance = GetNativeGrabDistance(player);

    if (grabbed)
    {
        Console_Print("[GMOD] native grab ref=%08X spring=%p mode=%u weight=%.3f distance=%.3f",
            grabbed->refID, spring, mode, weight, distance);
        *reinterpret_cast<UInt32*>(result) = grabbed->refID;
    }
    else
    {
        Console_Print("[GMOD] native grab: none spring=%p mode=%u weight=%.3f distance=%.3f",
            spring, mode, weight, distance);
        *result = 0.0;
    }
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_grabstatus, "Print the native New Vegas grab-system state", 0, nullptr);

bool Cmd_gmod_spawnbarrel_Execute(COMMAND_ARGS)
{
    TESObjectREFR* spawned = SpawnConvertedProp("rem\\gmod\\props_c17\\oildrum001.nif", 220.0f);
    if (spawned)
        *reinterpret_cast<UInt32*>(result) = spawned->refID;
    else
        *result = 0.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_spawnbarrel, "Spawn the converted GMod oil drum", 0, nullptr);

bool Cmd_gmod_undospawn_Execute(COMMAND_ARGS)
{
    UndoLastSpawn();
    *result = 1.0;
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_undospawn, "Undo the last GMod prop spawn", 0, nullptr);

bool Cmd_gmod_cleanup_Execute(COMMAND_ARGS)
{
    UInt32 removed = 0;

    if (g_heldRef)
        DropHeld();

    for (UInt32 refID : g_spawnUndo)
    {
        TESObjectREFR* ref = LookupReference(refID);
        if (!ref)
            continue;
        Script::RunScriptLine2("disable", ref, true);
        ++removed;
    }
    g_spawnUndo.clear();

    // Some visual bindings can outlive an undo-stack entry if reference creation was
    // asynchronous, so explicitly disable their visuals as part of sandbox cleanup.
    for (const auto& balloonBinding : g_toolBalloons)
    {
        TESObjectREFR* balloon = LookupReference(balloonBinding.balloonRefID);
        if (balloon)
            Script::RunScriptLine2("disable", balloon, true);
    }

    g_toolThrusters.clear();
    g_toolHoverballs.clear();
    g_toolMotors.clear();
    g_toolBalloons.clear();
    g_toolLamps.clear();
    g_toolDynamite.clear();
    g_toolPhysProps.clear();
    g_physPropUpdateTick = 0;
    g_pendingDynamite = false;
    g_gmodNpcProxies.clear();
    g_pendingNpcDef = nullptr;
    g_toolConstraints.clear();
    g_toolButtons.clear();
    g_frozenProps.clear();

    g_pendingBalloonTargetRefID = 0;
    g_pendingLampTargetRefID = 0;
    g_pendingWheelAnchorRefID = 0;
    g_constraintFirstRefID = 0;
    g_buttonFirstRefID = 0;
    g_frozenUpdateTick = 0;

    Console_Print("[GMOD] cleanup removed %u spawned entities and cleared sandbox physics", removed);
    *result = static_cast<double>(removed);
    return true;
}
DEFINE_COMMAND_PLUGIN(gmod_cleanup, "Remove spawned GMod entities and clear sandbox Tool Gun physics", 0, nullptr);

static void MessageHandler(NVSEMessagingInterface::Message* msg)
{
    if (!msg) return;

    switch (msg->type)
    {
    case NVSEMessagingInterface::kMessage_PreLoadGame:
    case NVSEMessagingInterface::kMessage_ExitToMainMenu:
        UpdateFalloutHudOwnership(false);
        g_gameplayReady = false;
        g_skate.active = false;
        UpdateTHUGHudOverlay();
        break;
    case NVSEMessagingInterface::kMessage_PostLoad:
        g_gameplayReady = false;
        _MESSAGE("FNVGModTHUG2: PostLoad");
        g_autoTestEnabled = (GetFileAttributesA(kAutoTestFlag) != INVALID_FILE_ATTRIBUTES);
        if (g_autoTestEnabled)
        {
            g_autoTestLoadIssued = false;
            g_autoTestSpawnPending = false;
            g_autoTestSpawnRequested = false;
            g_autoTestStartTick = GetTickCount();
            _MESSAGE("[AUTOTEST] armed");
        }
        break;
    case NVSEMessagingInterface::kMessage_PostLoadGame:
        g_gameplayReady = true;
        g_runtimeFormInitEarliestTick = GetTickCount() + 2500;
        g_runtimeFormInitLogged = false;
        g_heldRef = nullptr;
        g_throw.ref = nullptr;
        g_pendingSpawnForm = nullptr;
        g_pendingSpawnStartTick = 0;
        g_undoDisabled.clear();
        UpdateFalloutHudOwnership(false);
        g_skate = SkateState{};
        g_skateboardWeapon = nullptr;
        g_skateboardWorldStatic = nullptr;
        g_skateboardAttackWasDown = false;
        g_skateboardFightSuppressed = false;
        g_skateboardFightWasDisabledBeforeSuppress = false;
        g_gmodRuntimeWeapons.clear();
        g_gmodSoundForms.clear();
        g_toolgunSoundVariant = 0;
        g_physgunLaunchVariant = 0;
        g_gmodMappedSoundVariant = 0;
        g_gmodWeaponFormsReady = false;
        g_gmodAttackWasDown = false;
        g_gmodSecondaryWasDown = false;
        g_weaponPhysgunActive = false;
        g_weaponToolgunActive = false;
        g_physgunActorWakeRefID = 0;
        g_physgunActorWakeTick = 0;
        g_physgunHeldOriginalKnockedState = 0;
        g_physgunHeldForcedKnockedState = 1;
        g_physgunActorWakeRestoreState = 0;
        g_physgunHeldUsingRagdollBodies = false;
        g_cameraWeaponActive = false;
        g_cameraDefaultFov = 75.0f;
        g_cameraZoomStep = 0;
        g_buildMenu = GModBuildMenuState{};
        g_noClip = false;
        g_noClipMovementWasDisabled = false;
        g_noClipLastTick = 0;
        g_toolThrusters.clear();
        g_toolHoverballs.clear();
        g_toolMotors.clear();
        g_toolBalloons.clear();
        g_toolLamps.clear();
        g_toolDynamite.clear();
        g_toolPhysProps.clear();
        g_physPropUpdateTick = 0;
        g_pendingDynamite = false;
        g_gmodNpcProxies.clear();
        g_pendingNpcDef = nullptr;
        g_pendingBalloonTargetRefID = 0;
        g_pendingLampTargetRefID = 0;
        g_pendingWheelAnchorRefID = 0;
        g_toolConstraints.clear();
        g_constraintFirstRefID = 0;
        g_toolButtons.clear();
        g_buttonFirstRefID = 0;
        g_frozenProps.clear();
        g_frozenUpdateTick = 0;
        g_duplicatorNif[0] = 0;
        g_duplicatorName[0] = 0;
        g_vehicle = GModVehicleState{};
        g_physgunEnabled = false;
        g_toolgunEnabled = false;
        _MESSAGE("FNVGModTHUG2: PostLoadGame - runtime forms deferred to first valid gameplay frame");
        if (g_autoTestEnabled)
        {
            g_autoTestSpawnPending = true;
            g_autoTestSpawnRequested = false;
            g_autoTestSpawnTick = GetTickCount() + 3000;
            _MESSAGE("[AUTOTEST] PostLoadGame received; spawn queued");
        }
        break;
    case NVSEMessagingInterface::kMessage_NewGame:
        g_gameplayReady = true;
        g_runtimeFormInitEarliestTick = GetTickCount() + 2500;
        g_runtimeFormInitLogged = false;
        g_heldRef = nullptr;
        g_throw.ref = nullptr;
        g_pendingSpawnForm = nullptr;
        g_pendingSpawnStartTick = 0;
        g_undoDisabled.clear();
        UpdateFalloutHudOwnership(false);
        g_skate = SkateState{};
        g_skateboardWeapon = nullptr;
        g_skateboardWorldStatic = nullptr;
        g_skateboardAttackWasDown = false;
        g_skateboardFightSuppressed = false;
        g_skateboardFightWasDisabledBeforeSuppress = false;
        g_gmodRuntimeWeapons.clear();
        g_gmodSoundForms.clear();
        g_toolgunSoundVariant = 0;
        g_physgunLaunchVariant = 0;
        g_gmodMappedSoundVariant = 0;
        g_gmodWeaponFormsReady = false;
        g_gmodAttackWasDown = false;
        g_gmodSecondaryWasDown = false;
        g_weaponPhysgunActive = false;
        g_weaponToolgunActive = false;
        g_physgunActorWakeRefID = 0;
        g_physgunActorWakeTick = 0;
        g_physgunHeldOriginalKnockedState = 0;
        g_physgunHeldForcedKnockedState = 1;
        g_physgunActorWakeRestoreState = 0;
        g_physgunHeldUsingRagdollBodies = false;
        g_cameraWeaponActive = false;
        g_cameraDefaultFov = 75.0f;
        g_cameraZoomStep = 0;
        g_buildMenu = GModBuildMenuState{};
        g_noClip = false;
        g_noClipMovementWasDisabled = false;
        g_noClipLastTick = 0;
        g_toolThrusters.clear();
        g_toolHoverballs.clear();
        g_toolMotors.clear();
        g_toolBalloons.clear();
        g_toolLamps.clear();
        g_toolDynamite.clear();
        g_toolPhysProps.clear();
        g_physPropUpdateTick = 0;
        g_pendingDynamite = false;
        g_gmodNpcProxies.clear();
        g_pendingNpcDef = nullptr;
        g_pendingBalloonTargetRefID = 0;
        g_pendingLampTargetRefID = 0;
        g_pendingWheelAnchorRefID = 0;
        g_toolConstraints.clear();
        g_constraintFirstRefID = 0;
        g_toolButtons.clear();
        g_buttonFirstRefID = 0;
        g_frozenProps.clear();
        g_frozenUpdateTick = 0;
        g_duplicatorNif[0] = 0;
        g_duplicatorName[0] = 0;
        g_vehicle = GModVehicleState{};
        g_physgunEnabled = false;
        g_toolgunEnabled = false;
        _MESSAGE("FNVGModTHUG2: NewGame - runtime forms deferred to first valid gameplay frame");
        break;
    case NVSEMessagingInterface::kMessage_MainGameLoop:
        PollControls();
        break;
    case NVSEMessagingInterface::kMessage_ExitGame_Console:
    case NVSEMessagingInterface::kMessage_ExitGame:
        UpdateFalloutHudOwnership(false);
        g_gameplayReady = false;
        g_noClip = false;
        g_noClipMovementWasDisabled = false;
        g_noClipLastTick = 0;
        g_heldRef = nullptr;
        g_throw.ref = nullptr;
        g_toolThrusters.clear();
        g_toolHoverballs.clear();
        g_toolMotors.clear();
        g_toolBalloons.clear();
        g_toolLamps.clear();
        g_toolDynamite.clear();
        g_toolPhysProps.clear();
        g_physPropUpdateTick = 0;
        g_pendingDynamite = false;
        g_gmodNpcProxies.clear();
        g_pendingNpcDef = nullptr;
        g_pendingBalloonTargetRefID = 0;
        g_pendingLampTargetRefID = 0;
        g_pendingWheelAnchorRefID = 0;
        g_toolConstraints.clear();
        g_constraintFirstRefID = 0;
        g_toolButtons.clear();
        g_buttonFirstRefID = 0;
        g_frozenProps.clear();
        g_frozenUpdateTick = 0;
        g_duplicatorNif[0] = 0;
        g_duplicatorName[0] = 0;
        g_vehicle = GModVehicleState{};
        break;
    default:
        break;
    }
}

bool NVSEPlugin_Query(const NVSEInterface* nvse, PluginInfo* info)
{
    info->infoVersion = PluginInfo::kInfoVersion;
    info->name = "FNVGModTHUG2";
    info->version = 86;

    if (!nvse || nvse->isEditor) return false;
    if (nvse->runtimeVersion < RUNTIME_VERSION_1_4_0_525) return false;
    return true;
}

bool NVSEPlugin_Load(NVSEInterface* nvse)
{
    g_nvse = nvse;
    g_pluginHandle = nvse->GetPluginHandle();

    g_messaging = static_cast<NVSEMessagingInterface*>(nvse->QueryInterface(kInterface_Messaging));
    if (!g_messaging) return false;
    g_messaging->RegisterListener(g_pluginHandle, "NVSE", MessageHandler);

    nvse->SetOpcodeBase(0x2000);
    nvse->RegisterCommand(&kCommandInfo_gmod_spawnmenu);
    nvse->RegisterCommand(&kCommandInfo_noclip);
    nvse->RegisterCommand(&kCommandInfo_physgun);
    nvse->RegisterCommand(&kCommandInfo_physgun_drop);
    nvse->RegisterCommand(&kCommandInfo_toolgun);
    nvse->RegisterCommand(&kCommandInfo_gmod_undo);
    nvse->RegisterCommand(&kCommandInfo_skatemode);
    nvse->RegisterCommand(&kCommandInfo_gmod_giveskateboard);
    nvse->RegisterCommand(&kCommandInfo_gmod_grabstatus);
    nvse->RegisterCommand(&kCommandInfo_gmod_spawnbarrel);
    nvse->RegisterCommand(&kCommandInfo_gmod_undospawn);
    nvse->RegisterCommand(&kCommandInfo_gmod_cleanup);

    _MESSAGE("FNVGModTHUG2 bridge loaded, version 86 (G6 HUD candidate; not THUG2 parity)");
    return true;
}