#include "nvse/PluginAPI.h"
#include "nvse/GameAPI.h"
#include "nvse/GameObjects.h"
#include "nvse/GameForms.h"
#include "nvse/GameData.h"
#include "nvse/GameScript.h"
#include "nvse/GameRTTI.h"
#include <windows.h>
#include <mmsystem.h>
#include <cmath>
#include <cstdio>

#pragma comment(lib, "winmm.lib")

IDebugLog gLog("REMGoodspringsResponse.log");

static PluginHandle g_pluginHandle = kPluginHandle_Invalid;
static NVSEMessagingInterface* g_messaging = nullptr;

static const char* kEncounterPlugin = "REM_Goodsprings_CombineDeathclawEncounter.esp";
static const UInt32 kCombineRefLocal = 0x00000803;
static const UInt32 kResponseFirstLocal = 0x00000804;
static const UInt32 kResponseCount = 10;
static const UInt32 kCaptainRefLocal = 0x0000080E;
static const UInt32 kRewardGlobalLocal = 0x0000080F;
static const UInt32 kDeathclawEgg = 0x000E6627;
static const char* kCaptainAudio =
    "Data\\Sound\\fx\\rem\\goodsprings\\captain_claw_thanks.wav";

static bool g_gameplayReady = false;
static bool g_captainActivated = false;
static bool g_captainRewarded = false;
static bool g_guardDefeatLogged = false;
static DWORD g_nextPollTick = 0;
static DWORD g_nextCombatRefreshTick = 0;

static UInt32 RuntimeFormID(UInt32 localID)
{
    DataHandler* data = DataHandler::Get();
    if (!data) return 0;

    const ModInfo* mod = data->LookupModByName(kEncounterPlugin);
    if (!mod || mod->modIndex == 0xFF)
        return 0;

    return (static_cast<UInt32>(mod->modIndex) << 24) | (localID & 0x00FFFFFF);
}

static TESObjectREFR* LookupEncounterRef(UInt32 localID)
{
    const UInt32 formID = RuntimeFormID(localID);
    if (!formID) return nullptr;

    TESForm* form = LookupFormByID(formID);
    if (!form || !form->GetIsReference())
        return nullptr;

    return static_cast<TESObjectREFR*>(form);
}

static Actor* LookupEncounterActor(UInt32 localID)
{
    TESObjectREFR* ref = LookupEncounterRef(localID);
    if (!ref) return nullptr;
    return DYNAMIC_CAST(ref, TESObjectREFR, Actor);
}

static TESGlobal* LookupEncounterGlobal(UInt32 localID)
{
    const UInt32 formID = RuntimeFormID(localID);
    if (!formID) return nullptr;
    TESForm* form = LookupFormByID(formID);
    if (!form || form->typeID != kFormType_TESGlobal)
        return nullptr;
    return static_cast<TESGlobal*>(form);
}

static bool SameLoadedCell(TESObjectREFR* a, TESObjectREFR* b)
{
    return a && b && a->parentCell && b->parentCell && a->parentCell == b->parentCell;
}

static float DistanceSquared(const TESObjectREFR* a, const TESObjectREFR* b)
{
    if (!a || !b) return 1.0e30f;
    const float dx = a->posX - b->posX;
    const float dy = a->posY - b->posY;
    const float dz = a->posZ - b->posZ;
    return dx * dx + dy * dy + dz * dz;
}

static void RunOnRef(TESObjectREFR* ref, const char* command)
{
    if (ref && command && *command)
        Script::RunScriptLine2(command, ref, true);
}

static void ForceResponseUnitTarget(Actor* unit, Actor* guard)
{
    if (!unit || !guard) return;

    Actor* target = unit->GetCombatTarget();
    if (target == guard)
        return;

    if (target)
        RunOnRef(unit, "stopcombat");

    char cmd[64];
    std::snprintf(cmd, sizeof(cmd), "startcombat %08X", guard->refID);
    RunOnRef(unit, cmd);
}

static void StopResponseUnitCombat()
{
    for (UInt32 i = 0; i < kResponseCount; ++i)
    {
        Actor* unit = LookupEncounterActor(kResponseFirstLocal + i);
        if (unit && unit->GetCombatTarget())
            RunOnRef(unit, "stopcombat");
    }
}

static void ActivateCaptainClaw(Actor* captain)
{
    if (!captain || g_captainActivated)
        return;

    RunOnRef(captain, "enable");

    // RunToPlayerForever is authored persistently on Captain's CREA base in the
    // encounter ESP. EVP makes him immediately evaluate that vanilla package.
    // No MoveTo or teleport command exists in this path.
    RunOnRef(captain, "evp");

    g_captainActivated = true;
    _MESSAGE("[RESPONSE] Captain Claw enabled; persistent RunToPlayerForever evaluated, no teleport");
}

static void DeliverCaptainReward(Actor* captain, PlayerCharacter* player)
{
    if (!captain || !player || g_captainRewarded)
        return;

    const float triggerRadius = 275.0f;
    if (!SameLoadedCell(captain, player) ||
        DistanceSquared(captain, player) > triggerRadius * triggerRadius)
        return;

    PlaySoundA(kCaptainAudio, nullptr,
        SND_FILENAME | SND_ASYNC | SND_NODEFAULT);

    RunOnRef(player,
        "MessageBox \"Captain Claw: Thanks for killing that Combine soldier. "
        "You did Goodsprings a favor. Take this Deathclaw egg. You've earned it.\" "
        "\"Thanks, Captain Claw.\"");

    char rewardCmd[64];
    std::snprintf(rewardCmd, sizeof(rewardCmd), "additem %08X 1", kDeathclawEgg);
    RunOnRef(player, rewardCmd);

    TESGlobal* rewarded = LookupEncounterGlobal(kRewardGlobalLocal);
    if (rewarded)
        rewarded->data = 1.0f;
    RunOnRef(player, "set REMCaptainClawRewarded to 1");

    g_captainRewarded = true;
    _MESSAGE("[RESPONSE] Captain Claw reached player; TTS/dialogue/egg reward delivered and persisted");
}

static void UpdateGoodspringsResponse()
{
    if (!g_gameplayReady)
        return;

    const DWORD now = GetTickCount();
    if (now < g_nextPollTick)
        return;
    g_nextPollTick = now + 200;

    PlayerCharacter* player = PlayerCharacter::GetSingleton();
    if (!player || !player->parentCell)
        return;

    Actor* guard = LookupEncounterActor(kCombineRefLocal);
    if (!guard)
        return;

    // Do not issue AI commands to the encounter while the player is elsewhere.
    // The fight is staged specifically for the loaded Goodsprings exterior cell.
    if (!SameLoadedCell(guard, player))
        return;

    // Any non-alive life state counts as defeated for this deliberately staged
    // encounter (death/dying/unconscious). This matches the requested
    // killed/defeated/death trigger semantics.
    const bool guardDefeated = guard->lifeState != 0;

    if (!guardDefeated)
    {
        if (now >= g_nextCombatRefreshTick)
        {
            g_nextCombatRefreshTick = now + 750;
            for (UInt32 i = 0; i < kResponseCount; ++i)
            {
                Actor* unit = LookupEncounterActor(kResponseFirstLocal + i);
                if (!unit) continue;

                // Response units are authored Unaggressive with no factions or
                // packages. Runtime targeting therefore has exactly one legal
                // combat target: the Combine guard.
                ForceResponseUnitTarget(unit, guard);
            }
        }
        return;
    }

    if (!g_guardDefeatLogged)
    {
        _MESSAGE("[RESPONSE] Combine Solider defeated lifeState=%u", guard->lifeState);
        g_guardDefeatLogged = true;
    }

    // Keep the response units peaceful after the target is gone, including if
    // the player or a Goodsprings NPC later provokes one of them.
    StopResponseUnitCombat();

    Actor* captain = LookupEncounterActor(kCaptainRefLocal);
    if (!captain)
        return;

    ActivateCaptainClaw(captain);
    DeliverCaptainReward(captain, player);
}

static void ResetEncounterRuntime()
{
    g_gameplayReady = true;
    g_captainActivated = false;
    TESGlobal* rewarded = LookupEncounterGlobal(kRewardGlobalLocal);
    g_captainRewarded = rewarded && rewarded->data >= 1.0f;
    g_guardDefeatLogged = false;
    g_nextPollTick = GetTickCount() + 2500;
    g_nextCombatRefreshTick = 0;
}

static void MessageHandler(NVSEMessagingInterface::Message* msg)
{
    if (!msg) return;

    switch (msg->type)
    {
    case NVSEMessagingInterface::kMessage_PostLoad:
        g_gameplayReady = false;
        break;
    case NVSEMessagingInterface::kMessage_PostLoadGame:
    case NVSEMessagingInterface::kMessage_NewGame:
        ResetEncounterRuntime();
        break;
    case NVSEMessagingInterface::kMessage_MainGameLoop:
        UpdateGoodspringsResponse();
        break;
    case NVSEMessagingInterface::kMessage_ExitGame:
        g_gameplayReady = false;
        PlaySoundA(nullptr, nullptr, SND_PURGE);
        break;
    default:
        break;
    }
}

bool NVSEPlugin_Query(const NVSEInterface* nvse, PluginInfo* info)
{
    info->infoVersion = PluginInfo::kInfoVersion;
    info->name = "REMGoodspringsResponse";
    info->version = 2;

    if (!nvse || nvse->isEditor)
        return false;
    if (nvse->runtimeVersion < RUNTIME_VERSION_1_4_0_525)
        return false;
    return true;
}

bool NVSEPlugin_Load(NVSEInterface* nvse)
{
    g_pluginHandle = nvse->GetPluginHandle();

    g_messaging = static_cast<NVSEMessagingInterface*>(
        nvse->QueryInterface(kInterface_Messaging));
    if (!g_messaging)
        return false;

    g_messaging->RegisterListener(g_pluginHandle, "NVSE", MessageHandler);
    _MESSAGE("[RESPONSE] REMGoodspringsResponse v2 loaded - natural Captain approach + persistent reward");
    return true;
}
