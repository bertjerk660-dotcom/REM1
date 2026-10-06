# Opus code context — visual integration boundaries

Generated from current project-authored runtime source. This is visual/model/animation integration context, not authorization to take over Astra-owned deep runtime mechanics.
Source: third_party/NVSE-6.4.9/fnv_gmod_thug2_plugin/main.cpp
SHA256: CE3628AE131F42424459F5441051817EC132A7AE53414765047EBA6A9A4727A5

## ApplyGModWeaponAnimationProfile
Recorded anchor line 1449; excerpt 1415-1483.
~~~cpp
01415:         if (obj->typeID != kFormType_TESObjectWEAP) continue;
01416:         TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
01417:         if (!weapon->IsPlayable()) continue;
01418: 
01419:         if (kind == GModWeaponKind::Toolgun && WeaponNameContains(weapon, "10mm pistol"))
01420:             return weapon;
01421:         if (kind == GModWeaponKind::Physgun && WeaponNameContains(weapon, "flamer"))
01422:             return weapon;
01423:     }
01424: 
01425:     const UInt8 desired = PreferredFNVWeaponType(kind);
01426:     TESObjectWEAP* fallback = nullptr;
01427: 
01428:     for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
01429:     {
01430:         if (obj->typeID != kFormType_TESObjectWEAP) continue;
01431:         TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
01432:         if (!weapon->IsPlayable() || weapon->eWeaponType != desired) continue;
01433: 
01434:         if (!fallback) fallback = weapon;
01435: 
01436:         if (kind == GModWeaponKind::Shotgun && WeaponNameContains(weapon, "shotgun")) return weapon;
01437:         if (kind == GModWeaponKind::Pistol && WeaponNameContains(weapon, "9mm pistol")) return weapon;
01438:         if ((kind == GModWeaponKind::Automatic || kind == GModWeaponKind::Flechette) &&
01439:             (WeaponNameContains(weapon, "smg") || WeaponNameContains(weapon, "machine"))) return weapon;
01440:         if (kind == GModWeaponKind::Rifle && WeaponNameContains(weapon, "rifle")) return weapon;
01441:         if (kind == GModWeaponKind::Launcher && WeaponNameContains(weapon, "missile")) return weapon;
01442:         if (kind == GModWeaponKind::Grenade && WeaponNameContains(weapon, "grenade")) return weapon;
01443:         if (kind == GModWeaponKind::Melee && WeaponNameContains(weapon, "lead pipe")) return weapon;
01444:     }
01445: 
01446:     return fallback;
01447: }
01448: 
01449: static void ApplyGModWeaponAnimationProfile(const GModWeaponDef& def, TESObjectWEAP* weapon)
01450: {
01451:     if (!weapon) return;
01452: 
01453:     TESObjectWEAP* donor = FindGModWeaponTemplate(def.kind);
01454:     if (!donor || donor == weapon) return;
01455: 
01456:     // Safe primitive-only profile copy for persistent WEAP records.
01457:     // Model, sound and form pointers remain ESP-owned.
01458:     weapon->eWeaponType = donor->eWeaponType;
01459:     weapon->handGrip = donor->handGrip;
01460:     weapon->reloadAnim = donor->reloadAnim;
01461:     weapon->attackAnim = donor->attackAnim;
01462:     weapon->animMult = donor->animMult;
01463:     weapon->animAttackMult = donor->animAttackMult;
01464:     weapon->animShotsPerSec = donor->animShotsPerSec;
01465:     weapon->animReloadTime = donor->animReloadTime;
01466:     weapon->animJamTime = donor->animJamTime;
01467: 
01468:     const bool donorNo3PIS =
01469:         donor->weaponFlags2.IsSet(TESObjectWEAP::eFlag_No3rdPersonISAnims);
01470:     weapon->weaponFlags2.Write(TESObjectWEAP::eFlag_No3rdPersonISAnims, donorNo3PIS);
01471: 
01472:     _MESSAGE("[GMOD-WEAP] anim profile %s <- %08X type=%u grip=%u",
01473:         def.className, donor->refID,
01474:         static_cast<unsigned>(weapon->eWeaponType),
01475:         static_cast<unsigned>(weapon->handGrip));
01476: }
01477: 
01478: static TESObjectWEAP* FindExistingGModWeaponForm(const GModWeaponDef& def)
01479: {
01480:     DataHandler* data = DataHandler::Get();
01481:     if (!data || !data->boundObjectList) return nullptr;
01482: 
01483:     for (TESBoundObject* obj = data->boundObjectList->first; obj; obj = obj->next)
~~~

## GetEquippedGModRuntimeWeapon
Recorded anchor line 1519; excerpt 1485-1553.
~~~cpp
01485:         if (obj->typeID != kFormType_TESObjectWEAP) continue;
01486:         TESObjectWEAP* weapon = static_cast<TESObjectWEAP*>(obj);
01487: 
01488:         const char* name = weapon->fullName.name.m_data;
01489:         if (!name || _stricmp(name, def.displayName) != 0) continue;
01490: 
01491:         if (!def.worldNif || !*def.worldNif)
01492:             return weapon;
01493: 
01494:         const char* path = weapon->textureSwap.nifPath.m_data;
01495:         if (path && _stricmp(path, def.worldNif) == 0)
01496:             return weapon;
01497:     }
01498:     return nullptr;
01499: }
01500: 
01501: static void GiveWeaponToPlayer(TESObjectWEAP* weapon)
01502: {
01503:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01504:     if (!player || !weapon) return;
01505: 
01506:     char cmd[96];
01507:     std::snprintf(cmd, sizeof(cmd), "additem %08X 1", weapon->refID);
01508:     Script::RunScriptLine2(cmd, player, true);
01509: }
01510: 
01511: static GModRuntimeWeapon* FindRuntimeGModWeapon(TESObjectWEAP* weapon)
01512: {
01513:     if (!weapon) return nullptr;
01514:     for (auto& runtime : g_gmodRuntimeWeapons)
01515:         if (runtime.weapon == weapon) return &runtime;
01516:     return nullptr;
01517: }
01518: 
01519: static GModRuntimeWeapon* GetEquippedGModRuntimeWeapon()
01520: {
01521:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01522:     if (!player) return nullptr;
01523:     return FindRuntimeGModWeapon(player->GetEquippedWeapon());
01524: }
01525: 
01526: static void EnsureGModWeaponForms()
01527: {
01528:     if (g_gmodWeaponFormsReady) return;
01529: 
01530:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01531:     if (!player || !player->parentCell) return;
01532: 
01533:     g_gmodRuntimeWeapons.clear();
01534:     const size_t defCount = 14;
01535: 
01536:     for (size_t i = 0; i < defCount; ++i)
01537:     {
01538:         const GModWeaponDef& def = kGModWeaponDefs[i];
01539:         TESObjectWEAP* weapon = FindExistingGModWeaponForm(def);
01540:         TESObjectSTAT* worldStatic = weapon ? weapon->worldStatic : nullptr;
01541:         bool created = false;
01542: 
01543:         if (!weapon)
01544:         {
01545:             TESObjectWEAP* source = FindGModWeaponTemplate(def.kind);
01546:             if (!source)
01547:             {
01548:                 _MESSAGE("[GMOD-WEAP] no FNV template for %s", def.className);
01549:                 continue;
01550:             }
01551: 
01552:             TESForm* cloned = source->CloneForm(true);
01553:             if (!cloned || cloned->typeID != kFormType_TESObjectWEAP)
~~~

## EnsureGModWeaponForms
Recorded anchor line 1526; excerpt 1492-1560.
~~~cpp
01492:             return weapon;
01493: 
01494:         const char* path = weapon->textureSwap.nifPath.m_data;
01495:         if (path && _stricmp(path, def.worldNif) == 0)
01496:             return weapon;
01497:     }
01498:     return nullptr;
01499: }
01500: 
01501: static void GiveWeaponToPlayer(TESObjectWEAP* weapon)
01502: {
01503:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01504:     if (!player || !weapon) return;
01505: 
01506:     char cmd[96];
01507:     std::snprintf(cmd, sizeof(cmd), "additem %08X 1", weapon->refID);
01508:     Script::RunScriptLine2(cmd, player, true);
01509: }
01510: 
01511: static GModRuntimeWeapon* FindRuntimeGModWeapon(TESObjectWEAP* weapon)
01512: {
01513:     if (!weapon) return nullptr;
01514:     for (auto& runtime : g_gmodRuntimeWeapons)
01515:         if (runtime.weapon == weapon) return &runtime;
01516:     return nullptr;
01517: }
01518: 
01519: static GModRuntimeWeapon* GetEquippedGModRuntimeWeapon()
01520: {
01521:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01522:     if (!player) return nullptr;
01523:     return FindRuntimeGModWeapon(player->GetEquippedWeapon());
01524: }
01525: 
01526: static void EnsureGModWeaponForms()
01527: {
01528:     if (g_gmodWeaponFormsReady) return;
01529: 
01530:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01531:     if (!player || !player->parentCell) return;
01532: 
01533:     g_gmodRuntimeWeapons.clear();
01534:     const size_t defCount = 14;
01535: 
01536:     for (size_t i = 0; i < defCount; ++i)
01537:     {
01538:         const GModWeaponDef& def = kGModWeaponDefs[i];
01539:         TESObjectWEAP* weapon = FindExistingGModWeaponForm(def);
01540:         TESObjectSTAT* worldStatic = weapon ? weapon->worldStatic : nullptr;
01541:         bool created = false;
01542: 
01543:         if (!weapon)
01544:         {
01545:             TESObjectWEAP* source = FindGModWeaponTemplate(def.kind);
01546:             if (!source)
01547:             {
01548:                 _MESSAGE("[GMOD-WEAP] no FNV template for %s", def.className);
01549:                 continue;
01550:             }
01551: 
01552:             TESForm* cloned = source->CloneForm(true);
01553:             if (!cloned || cloned->typeID != kFormType_TESObjectWEAP)
01554:             {
01555:                 _MESSAGE("[GMOD-WEAP] clone failed for %s", def.className);
01556:                 continue;
01557:             }
01558: 
01559:             weapon = static_cast<TESObjectWEAP*>(cloned);
01560:             weapon->fullName.name.Set(def.displayName);
~~~

## EnterSkateMode
Recorded anchor line 1745; excerpt 1711-1779.
~~~cpp
01711: static void UpdateRideBoardVisual()
01712: {
01713:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01714:     if (!player || !g_skate.active) return;
01715: 
01716:     if (!g_skateboardRideRef && g_skateboardRidePendingForm)
01717:     {
01718:         g_skateboardRideRef = FindReferenceForBaseForm(g_skateboardRidePendingForm);
01719:         if (g_skateboardRideRef)
01720:         {
01721:             g_skateboardRidePendingForm = nullptr;
01722:             g_skateboardRidePendingTick = 0;
01723:         }
01724:         else if (GetTickCount() - g_skateboardRidePendingTick > 3000)
01725:         {
01726:             g_skateboardRidePendingForm = nullptr;
01727:             g_skateboardRidePendingTick = 0;
01728:         }
01729:     }
01730: 
01731:     if (!g_skateboardRideRef) return;
01732: 
01733:     SetRefPosition(g_skateboardRideRef, player->posX, player->posY, player->posZ - 3.0f);
01734:     const float toRadians = 0.0174532925199f;
01735:     const float trickSpinRadians = (g_skate.moveState == SkateMoveState::Air)
01736:         ? (g_skate.spinDegrees * toRadians)
01737:         : 0.0f;
01738:     const float trickFlipRadians = (g_skate.moveState == SkateMoveState::Air)
01739:         ? (g_skate.flipDegrees * toRadians)
01740:         : 0.0f;
01741:     SetRefAngles(g_skateboardRideRef, trickFlipRadians, 0.0f,
01742:         player->rotZ + trickSpinRadians);
01743: }
01744: 
01745: static void EnterSkateMode()
01746: {
01747:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01748:     if (!player || g_skate.active) return;
01749: 
01750:     g_skate.active = true;
01751:     g_skate.moveState = SkateMoveState::Ground;
01752:     g_skate.velocityX = 0.0f;
01753:     g_skate.velocityY = 0.0f;
01754:     g_skate.velocityZ = 0.0f;
01755:     g_skate.spinDegrees = 0.0f;
01756:     g_skate.flipDegrees = 0.0f;
01757:     g_skate.flipRemaining = 0.0f;
01758:     g_skate.balance = 0.0f;
01759:     g_skate.comboScore = 0.0f;
01760:     g_skate.comboMultiplier = 1.0f;
01761:     g_skate.totalScore = 0.0f;
01762:     g_skate.special01 = 0.0f;
01763:     g_skate.comboActive = false;
01764:     g_skate.trickCount = 0;
01765:     g_skate.manualVariant = 0;
01766:     g_skate.grindVariant = 0;
01767:     g_skate.lipVariant = 0;
01768:     g_skate.comboBankDeadline = 0;
01769:     g_skate.lastTrick[0] = 0;
01770:     g_skate.speed01 = 0.32f;
01771:     g_skate.originalSpeedMult = player->avOwner.Fn_03(eActorVal_SpeedMultiplier);
01772:     if (g_skate.originalSpeedMult < 1.0f || !std::isfinite(g_skate.originalSpeedMult))
01773:         g_skate.originalSpeedMult = 100.0f;
01774:     g_skate.lastTick = GetTickCount();
01775:     g_skate.lastSpeedApplyTick = 0;
01776:     g_skate.lastHudTick = 0;
01777:     g_skate.jumpWasDown = false;
01778:     g_skate.flipWasDown = false;
01779:     g_skate.grabWasDown = false;
~~~

## ExitSkateMode
Recorded anchor line 1842; excerpt 1808-1876.
~~~cpp
01808:     _MESSAGE("[THUG2] skate enter: raw THUG2 camera profile QUARANTINED; vanilla FNV third-person active");
01809: 
01810:     g_physgunEnabled = false;
01811:     g_toolgunEnabled = false;
01812:     DropHeld();
01813: 
01814:     ClearTHUG2RetargetCacheNoRestore();
01815:     g_thug2RetargetEarliestTick = GetTickCount() + 900;
01816:     g_thug2FirstUpdateDiag = false;
01817:     g_thug2DiagFrameCount = 0;
01818:     if (kTHUG2RetargetDiagnosticEnabled)
01819:     {
01820:         LoadTHUG2RetargetBank();
01821:         // Bone resolution is deferred until the third-person actor graph has remained
01822:         // stable for 900 ms after the camera transition.
01823:         StartTHUG2RetargetClip("idle", true, true);
01824:         _MESSAGE("[THUG2] skate enter: animation armed; bone resolve deferred");
01825:     }
01826:     else
01827:     {
01828:         _MESSAGE("[THUG2-DIAG] v85 retarget subsystem QUARANTINED");
01829:     }
01830:     BeginRideBoardVisual();
01831:     _MESSAGE("[THUG2] skate enter: ride board requested");
01832:     PlayTHUG2BoardRollSound();
01833:     _MESSAGE("[THUG2] skate enter: board roll sound complete");
01834:     SetPlayerSpeedMultiplier(player, g_skate.originalSpeedMult * 0.85f);
01835:     _MESSAGE("[THUG2] skate enter: speed path bypassed safely");
01836:     UpdateTHUGHudOverlay();
01837:     _MESSAGE("[THUG2] skate enter: HUD complete");
01838: 
01839:     Notify("[THUG2] Skate ON - Space jump, N nollie, P pressure, V revert, K skitch, M manual, G grind, L lip, Q/E spin or cycle, LMB+RMB special, R exit");
01840: }
01841: 
01842: static void ExitSkateMode()
01843: {
01844:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
01845:     if (!player || !g_skate.active) return;
01846: 
01847:     g_skate.active = false;
01848: 
01849:     if (!g_skate.fightWasDisabled)
01850:         player->disabledControlFlags &= ~PlayerCharacter::kControlFlag_Fight;
01851: 
01852:     // Restore the exact camera style the player was using before deploying the board.
01853:     player->bThirdPerson = g_skate.cameraWasThirdPerson;
01854:     player->UpdateCamera(false, false);
01855:     // No raw camera-node transform was touched in v84, so there is nothing to restore.
01856:     g_skate.thugCamNodeSaved = false;
01857:     ApplyGModCameraFov(player, g_skate.originalFov);
01858:     UpdateTHUGHudOverlay();
01859: 
01860:     // Release the xNVSE-injected forward hold before restoring normal Fallout input.
01861:     if (g_skate.forwardHoldInjected)
01862:     {
01863:         Script::RunScriptLine2("releasekey 17", player, true); // DirectInput DIK_W
01864:         g_skate.forwardHoldInjected = false;
01865:     }
01866: 
01867:     RestoreTHUG2RetargetBones(player);
01868: 
01869:     // Restore the exact pre-skate movement multiplier and remove the ride-only board visual.
01870:     SetPlayerSpeedMultiplier(player, g_skate.originalSpeedMult);
01871:     EndRideBoardVisual();
01872: 
01873:     // The skateboard remains the same equipped inventory weapon; draw it again for normal FNV use.
01874:     player->SetWantsWeaponOut(true);
01875: 
01876:     g_skate.velocityX = g_skate.velocityY = g_skate.velocityZ = 0.0f;
~~~

## SpawnConvertedProp
Recorded anchor line 4522; excerpt 4488-4556.
~~~cpp
04488:         ToolgunPhysPropReset();
04489:     else
04490:         ShowToolModeStatus();
04491: }
04492: 
04493: static TESObjectREFR* FindReferenceForBaseForm(TESForm* baseForm)
04494: {
04495:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
04496:     if (!player || !player->parentCell || !baseForm)
04497:         return nullptr;
04498: 
04499:     TESObjectREFR* best = nullptr;
04500:     float bestDistSq = 3.402823466e+38F;
04501: 
04502:     for (TESObjectCELL::RefList::Iterator it = player->parentCell->objectList.Begin(); !it.End(); ++it)
04503:     {
04504:         TESObjectREFR* ref = it.Get();
04505:         if (!ref || ref->baseForm != baseForm)
04506:             continue;
04507: 
04508:         const float dx = ref->posX - player->posX;
04509:         const float dy = ref->posY - player->posY;
04510:         const float dz = ref->posZ - player->posZ;
04511:         const float d2 = dx * dx + dy * dy + dz * dz;
04512:         if (d2 < bestDistSq)
04513:         {
04514:             bestDistSq = d2;
04515:             best = ref;
04516:         }
04517:     }
04518: 
04519:     return best;
04520: }
04521: 
04522: static TESObjectREFR* SpawnConvertedProp(const char* nifPath, float distance, const char* displayName)
04523: {
04524:     if (g_pendingSpawnForm)
04525:     {
04526:         _MESSAGE("[GMOD] Spawn rejected: base %08X is still awaiting reference creation", g_pendingSpawnForm->refID);
04527:         Notify("[GMOD] Previous prop is still spawning");
04528:         return nullptr;
04529:     }
04530: 
04531:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
04532:     if (!player || !player->parentCell || !nifPath || !*nifPath)
04533:     {
04534:         Notify("[GMOD] Spawn failed: player is not in a loaded cell");
04535:         return nullptr;
04536:     }
04537: 
04538:     // FalloutNV.esm MISC 0005B6CA = TinCan02, a known movable Havok junk item.
04539:     TESForm* templateForm = LookupFormByID(0x0005B6CA);
04540:     if (!templateForm)
04541:     {
04542:         _MESSAGE("[GMOD] Spawn failure: LookupFormByID(0005B6CA TinCan02) returned null");
04543:         Notify("[GMOD] Spawn failed: TinCan02 template not found");
04544:         return nullptr;
04545:     }
04546:     _MESSAGE("[GMOD] template TinCan02 id=%08X type=%02X ptr=%p", templateForm->refID, templateForm->typeID, templateForm);
04547: 
04548:     TESForm* propForm = templateForm->CloneForm(true);
04549:     if (!propForm)
04550:     {
04551:         _MESSAGE("[GMOD] Spawn failure: CloneForm returned null for template %08X", templateForm->refID);
04552:         Notify("[GMOD] Spawn failed: could not clone prop template");
04553:         return nullptr;
04554:     }
04555:     _MESSAGE("[GMOD] clone id=%08X type=%02X ptr=%p", propForm->refID, propForm->typeID, propForm);
04556: 
~~~

## UpdatePendingSpawn
Recorded anchor line 4646; excerpt 4612-4680.
~~~cpp
04612:     if (!spawned)
04613:         spawned = FindReferenceForBaseForm(propForm);
04614:     if (!spawned)
04615:     {
04616:         // PlaceAtMe inserts the reference into the cell asynchronously.
04617:         g_pendingSpawnForm = propForm;
04618:         g_pendingSpawnStartTick = GetTickCount();
04619:         Console_Print("[GMOD] Spawn form %08X placed; reference pending", propForm->refID);
04620:         _MESSAGE("[GMOD] spawn reference pending for base %08X", propForm->refID);
04621:         return nullptr;
04622:     }
04623: 
04624:     g_spawnUndo.push_back(spawned->refID);
04625:     _MESSAGE("[GMOD] captured spawned reference %08X base=%08X rigidBody=%p",
04626:         spawned->refID, propForm->refID, GetRootHavokRigidBody(spawned));
04627: 
04628:     char msg[128];
04629:     std::snprintf(msg, sizeof(msg), "[GMOD] Spawned prop %08X", spawned->refID);
04630:     Notify(msg);
04631:     return spawned;
04632: }
04633: 
04634: static void CompleteAutoTestSpawn(TESObjectREFR* spawned)
04635: {
04636:     if (!g_autoTestEnabled || !spawned)
04637:         return;
04638: 
04639:     _MESSAGE("[AUTOTEST] PASS spawned=%08X rigidBody=%p", spawned->refID, GetRootHavokRigidBody(spawned));
04640:     DeleteFileA(kAutoTestFlag);
04641:     g_autoTestEnabled = false;
04642:     g_autoTestSpawnPending = false;
04643:     g_autoTestSpawnRequested = false;
04644: }
04645: 
04646: static void UpdatePendingSpawn()
04647: {
04648:     if (!g_pendingSpawnForm)
04649:         return;
04650: 
04651:     TESObjectREFR* spawned = FindReferenceForBaseForm(g_pendingSpawnForm);
04652:     if (spawned)
04653:     {
04654:         g_spawnUndo.push_back(spawned->refID);
04655:         _MESSAGE("[GMOD] async capture spawned reference %08X base=%08X rigidBody=%p",
04656:             spawned->refID, g_pendingSpawnForm->refID, GetRootHavokRigidBody(spawned));
04657: 
04658:         char msg[128];
04659:         std::snprintf(msg, sizeof(msg), "[GMOD] Spawned prop %08X", spawned->refID);
04660:         Notify(msg);
04661: 
04662:         if (g_pendingDynamite)
04663:             CompletePendingDynamiteSpawn(spawned);
04664:         else if (g_pendingLampTargetRefID)
04665:             CompletePendingLampSpawn(spawned);
04666:         else if (g_pendingWheelAnchorRefID)
04667:             CompletePendingWheelSpawn(spawned);
04668:         else if (g_pendingBalloonTargetRefID)
04669:             CompletePendingBalloonSpawn(spawned);
04670:         else if (g_pendingNpcDef)
04671:             CompletePendingNpcSpawn(spawned);
04672: 
04673:         g_pendingSpawnForm = nullptr;
04674:         g_pendingSpawnStartTick = 0;
04675:         CompleteAutoTestSpawn(spawned);
04676:         return;
04677:     }
04678: 
04679:     if (GetTickCount() - g_pendingSpawnStartTick > 5000)
04680:     {
~~~

## OpenBuildMenu
Recorded anchor line 4752; excerpt 4718-4786.
~~~cpp
04718: static UInt32 GetBuildCategoryCount()
04719: {
04720:     return static_cast<UInt32>(sizeof(kGModPropCategories) / sizeof(kGModPropCategories[0]));
04721: }
04722: 
04723: static const GModPropCategoryRange* GetSelectedBuildCategory()
04724: {
04725:     const UInt32 count = GetBuildCategoryCount();
04726:     if (!count) return nullptr;
04727:     if (g_buildMenu.categoryIndex >= count)
04728:         g_buildMenu.categoryIndex = 0;
04729:     return &kGModPropCategories[g_buildMenu.categoryIndex];
04730: }
04731: 
04732: static const GModPropDef* GetSelectedBuildProp()
04733: {
04734:     const GModPropCategoryRange* category = GetSelectedBuildCategory();
04735:     if (!category || !category->count) return nullptr;
04736: 
04737:     if (g_buildMenu.itemIndex >= category->count)
04738:         g_buildMenu.itemIndex = 0;
04739: 
04740:     const UInt32 index = category->start + g_buildMenu.itemIndex;
04741:     const UInt32 total = static_cast<UInt32>(sizeof(kGModPropDefs) / sizeof(kGModPropDefs[0]));
04742:     return index < total ? &kGModPropDefs[index] : nullptr;
04743: }
04744: 
04745: static void ShowBuildMenuStatus(bool force = false)
04746: {
04747:     if (!g_buildMenu.open || !force) return;
04748:     g_buildMenu.lastHudTick = GetTickCount();
04749:     RefreshGModSpawnOverlay();
04750: }
04751: 
04752: static void OpenBuildMenu()
04753: {
04754:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
04755:     if (!player || !player->parentCell)
04756:     {
04757:         Notify("[GMOD] Build menu requires loaded gameplay");
04758:         return;
04759:     }
04760: 
04761:     if (g_skate.active)
04762:     {
04763:         Notify("[GMOD] Exit skate mode before opening build menu");
04764:         return;
04765:     }
04766: 
04767:     if (!GetBuildCategoryCount())
04768:     {
04769:         Notify("[GMOD] No converted spawn props are registered");
04770:         return;
04771:     }
04772: 
04773:     g_buildMenu.open = true;
04774:     g_buildMenu.lastHudTick = 0;
04775:     PlayGModUISound("ui_return", "fx\\rem\\gmod\\garrysmod\\ui_return.wav");
04776:     g_buildMenu.fightWasDisabled =
04777:         (player->disabledControlFlags & PlayerCharacter::kControlFlag_Fight) != 0;
04778:     g_buildMenu.movementWasDisabled =
04779:         (player->disabledControlFlags & PlayerCharacter::kControlFlag_Movement) != 0;
04780:     player->disabledControlFlags |=
04781:         PlayerCharacter::kControlFlag_Fight | PlayerCharacter::kControlFlag_Movement;
04782: 
04783:     ShowGModSpawnOverlay();
04784:     ShowBuildMenuStatus(true);
04785:     UpdatePhysBeamOverlay();
04786:     _MESSAGE("[GMOD-BUILD] menu opened category=%u item=%u",
~~~

## UpdateSkateMode
Recorded anchor line 5462; excerpt 5438-5486.
~~~cpp
05438: {
05439:     const float absoluteSpin = std::fabs(g_skate.spinDegrees);
05440:     int spin = static_cast<int>((absoluteSpin + 90.0f) / 180.0f) * 180;
05441:     if (spin < 180)
05442:         return;
05443:     if (spin > 1440)
05444:         spin = 1440;
05445: 
05446:     char base[64] = {};
05447:     if (g_skate.lastTrick[0])
05448:         strncpy_s(base, sizeof(base), g_skate.lastTrick, _TRUNCATE);
05449:     else
05450:         strncpy_s(base, sizeof(base), "Ollie", _TRUNCATE);
05451: 
05452:     char named[64] = {};
05453:     std::snprintf(
05454:         named, sizeof(named), "%s %d %s",
05455:         g_skate.spinDegrees >= 0.0f ? "FS" : "BS",
05456:         spin, base);
05457:     strncpy_s(g_skate.lastTrick, sizeof(g_skate.lastTrick), named, _TRUNCATE);
05458: 
05459:     g_skate.comboScore += static_cast<float>(spin) * 0.35f;
05460: }
05461: 
05462: static void UpdateSkateMode()
05463: {
05464:     if (!g_skate.active) return;
05465: 
05466:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
05467:     if (!player) return;
05468: 
05469:     // Dedicated THUG2 exit: holding R or Backspace always returns to Fallout.
05470:     if ((GetAsyncKeyState('R') & 0x8000) ||
05471:         (GetAsyncKeyState(VK_BACK) & 0x8000))
05472:     {
05473:         ExitSkateMode();
05474:         return;
05475:     }
05476: 
05477:     const UInt32 diagFrame = ++g_thug2DiagFrameCount;
05478:     const bool firstDiag = diagFrame <= 15;
05479:     const bool heartbeatDiag = firstDiag || (diagFrame <= 180 && (diagFrame % 15u) == 0u);
05480:     if (heartbeatDiag)
05481:         _MESSAGE("[THUG2-DIAG] skate frame %u begin", static_cast<unsigned>(diagFrame));
05482: 
05483:     // Skate mode owns the camera while active.
05484:     if (!player->bThirdPerson)
05485:     {
05486:         player->bThirdPerson = true;
~~~

## PollControls
Recorded anchor line 6263; excerpt 6239-6287.
~~~cpp
06239:                 Gdiplus::Bitmap image(bitmap, nullptr);
06240:                 status = image.Save(shotPath, &jpegClsid, nullptr);
06241:             }
06242:             saved = status == Gdiplus::Ok;
06243:         }
06244:     }
06245: 
06246:     DeleteObject(bitmap);
06247:     DeleteDC(memoryDC);
06248:     ReleaseDC(hwnd, windowDC);
06249: 
06250:     if (saved)
06251:     {
06252:         char utf8Path[MAX_PATH * 3] = {};
06253:         WideCharToMultiByte(
06254:             CP_UTF8, 0, shotPath, -1,
06255:             utf8Path, static_cast<int>(sizeof(utf8Path)),
06256:             nullptr, nullptr);
06257:         _MESSAGE("[GMOD Camera] saved %s", utf8Path);
06258:     }
06259: 
06260:     return saved;
06261: }
06262: 
06263: static void PollControls()
06264: {
06265:     // Never run gameplay/script-command logic on the title screen or during save transitions.
06266:     // RunScriptLine2 depends on ConsoleManager::scriptContext, which is not valid until gameplay is loaded.
06267:     if (!g_gameplayReady)
06268:         return;
06269: 
06270:     PlayerCharacter* player = PlayerCharacter::GetSingleton();
06271:     if (!player || !player->parentCell)
06272:         return;
06273: 
06274:     // Runtime form creation must not run on the first NewGame/PostLoadGame frames.
06275:     // A loaded cell can exist before ConsoleManager::scriptContext is ready; calling
06276:     // CloneForm/AddItem during that window was producing the repeatable FalloutNV.exe
06277:     // access violation seen after v73.  Wait for both a grace period and a valid script context.
06278:     const DWORD runtimeNow = GetTickCount();
06279:     const bool runtimeFormContextReady =
06280:         runtimeNow >= g_runtimeFormInitEarliestTick &&
06281:         HasSafeConsoleScriptContext();
06282: 
06283:     if (runtimeFormContextReady)
06284:     {
06285:         if (!g_runtimeFormInitLogged)
06286:         {
06287:             _MESSAGE("[RUNTIME] safe form-init window reached");
~~~

## gmod_weapon_defs.inc
SHA256: 9CA36F22F617BB5E31141497FA2E9C85C1AEB477B1C802320C3D90A4A2B75265
~~~cpp
// Generated from gmod_weapon_manifest.json
static const GModWeaponDef kGModWeaponDefs[] = {
    {"gmod_camera", "GMod Camera", "rem\\gmod\\MaxOfS2D\\camera.nif", GModWeaponKind::Camera, true},
    {"gmod_tool", "Tool Gun", "rem\\gmod\\weapons\\w_toolgun.nif", GModWeaponKind::Toolgun, true},
    {"manhack_welder", "Manhack Welder", "rem\\gmod\\weapons\\w_pistol.nif", GModWeaponKind::Utility, false},
    {"weapon_357", ".357 Magnum", "rem\\gmod\\weapons\\w_357.nif", GModWeaponKind::Pistol, false},
    {"weapon_ar2", "AR2", "rem\\gmod\\weapons\\w_irifle.nif", GModWeaponKind::Automatic, false},
    {"weapon_crossbow", "Crossbow", "rem\\gmod\\weapons\\w_crossbow.nif", GModWeaponKind::Rifle, false},
    {"weapon_crowbar", "Crowbar", "rem\\gmod\\weapons\\w_crowbar.nif", GModWeaponKind::Melee, true},
    {"weapon_fists", "Fists", "rem\\gmod\\weapons\\c_arms.nif", GModWeaponKind::Melee, false},
    {"weapon_flechettegun", "Flechette Gun", "rem\\gmod\\weapons\\w_smg1.nif", GModWeaponKind::Flechette, false},
    {"weapon_frag", "Frag Grenade", "rem\\gmod\\weapons\\w_grenade.nif", GModWeaponKind::Grenade, false},
    {"weapon_medkit", "Medkit", "rem\\gmod\\weapons\\w_medkit.nif", GModWeaponKind::Medkit, false},
    {"weapon_physcannon", "Gravity Gun", "rem\\gmod\\weapons\\w_physics.nif", GModWeaponKind::Physcannon, true},
    {"weapon_physgun", "Physics Gun", "rem\\gmod\\weapons\\w_physics.nif", GModWeaponKind::Physgun, true},
    {"weapon_pistol", "Pistol", "rem\\gmod\\weapons\\w_pistol.nif", GModWeaponKind::Pistol, false},
    {"weapon_rpg", "RPG", "rem\\gmod\\weapons\\w_rocket_launcher.nif", GModWeaponKind::Launcher, false},
    {"weapon_shotgun", "Shotgun", "rem\\gmod\\weapons\\w_shotgun.nif", GModWeaponKind::Shotgun, false},
    {"weapon_slam", "S.L.A.M.", "rem\\gmod\\weapons\\w_slam.nif", GModWeaponKind::Utility, false},
    {"weapon_smg1", "SMG1", "rem\\gmod\\weapons\\w_smg1.nif", GModWeaponKind::Automatic, false},
    {"weapon_stunstick", "Stunstick", "rem\\gmod\\weapons\\w_stunbaton.nif", GModWeaponKind::Melee, false},
    {"weapon_ttt_beacon", "Beacon", "rem\\gmod\\props_lab\\reciever01b.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_binoculars", "Binoculars", "rem\\gmod\\props\\cs_office\\paper_towels.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_c4", "C4", "rem\\gmod\\weapons\\w_c4.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_confgrenade", "Discombobulator", "rem\\gmod\\weapons\\w_eq_fraggrenade.nif", GModWeaponKind::Grenade, false},
    {"weapon_ttt_cse", "Visualizer", "rem\\gmod\\Items\\battery.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_decoy", "Decoy", "rem\\gmod\\props_lab\\reciever01b.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_defuser", "Defuser", "rem\\gmod\\weapons\\w_defuser.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_flaregun", "Flare Gun", "rem\\gmod\\weapons\\w_357.nif", GModWeaponKind::Pistol, false},
    {"weapon_ttt_glock", "Glock", "rem\\gmod\\weapons\\w_pist_glock18.nif", GModWeaponKind::Pistol, false},
    {"weapon_ttt_health_station", "Health Station", "rem\\gmod\\props\\cs_office\\microwave.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_knife", "Knife", "rem\\gmod\\weapons\\w_knife_t.nif", GModWeaponKind::Melee, false},
    {"weapon_ttt_m16", "M16", "rem\\gmod\\weapons\\w_rif_m4a1.nif", GModWeaponKind::Automatic, false},
    {"weapon_ttt_phammer", "Poltergeist", "rem\\gmod\\weapons\\w_IRifle.nif", GModWeaponKind::Rifle, false},
    {"weapon_ttt_push", "Newton Launcher", "rem\\gmod\\weapons\\w_physics.nif", GModWeaponKind::Rifle, false},
    {"weapon_ttt_radio", "Radio", "rem\\gmod\\props\\cs_office\\radio.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_sipistol", "Silenced USP", "rem\\gmod\\weapons\\w_pist_usp_silencer.nif", GModWeaponKind::Pistol, false},
    {"weapon_ttt_smokegrenade", "Smoke Grenade", "rem\\gmod\\weapons\\w_eq_smokegrenade.nif", GModWeaponKind::Grenade, false},
    {"weapon_ttt_stungun", "Stun Gun", "rem\\gmod\\weapons\\w_smg_ump45.nif", GModWeaponKind::Automatic, false},
    {"weapon_ttt_teleport", "Teleporter", "rem\\gmod\\weapons\\w_slam.nif", GModWeaponKind::Utility, false},
    {"weapon_ttt_unarmed", "Unarmed", "rem\\gmod\\weapons\\w_crowbar.nif", GModWeaponKind::Melee, false},
    {"weapon_ttt_wtester", "DNA Scanner", "rem\\gmod\\props_lab\\huladoll.nif", GModWeaponKind::Utility, false},
    {"weapon_zm_carry", "Magneto-stick", "rem\\gmod\\weapons\\w_stunbaton.nif", GModWeaponKind::Melee, false},
    {"weapon_zm_improvised", "Crowbar", "rem\\gmod\\weapons\\w_crowbar.nif", GModWeaponKind::Melee, false},
    {"weapon_zm_mac10", "MAC10", "rem\\gmod\\weapons\\w_smg_mac10.nif", GModWeaponKind::Automatic, false},
    {"weapon_zm_molotov", "Molotov", "rem\\gmod\\weapons\\w_eq_flashbang.nif", GModWeaponKind::Grenade, false},
    {"weapon_zm_pistol", "Five-Seven", "rem\\gmod\\weapons\\w_pist_fiveseven.nif", GModWeaponKind::Pistol, false},
    {"weapon_zm_revolver", "Desert Eagle", "rem\\gmod\\weapons\\w_pist_deagle.nif", GModWeaponKind::Pistol, false},
    {"weapon_zm_rifle", "Scout Rifle", "rem\\gmod\\weapons\\w_snip_scout.nif", GModWeaponKind::Rifle, false},
    {"weapon_zm_shotgun", "XM1014 Shotgun", "rem\\gmod\\weapons\\w_shot_xm1014.nif", GModWeaponKind::Shotgun, false},
    {"weapon_zm_sledge", "H.U.G.E-249", "rem\\gmod\\weapons\\w_mach_m249para.nif", GModWeaponKind::Automatic, false},
};
~~~

## gmod_tool_defs.inc
SHA256: 559B121AF438522101F943F7C3812A058B8D35424B919E95666E82062F246DF8
~~~cpp
// Generated from GMod stools manifest
static const GModToolDef kGModToolDefs[] = {
    {"axis", "Constraints", "Axis"},
    {"balloon", "Construction", "Balloon"},
    {"ballsocket", "Constraints", "Ballsocket"},
    {"button", "Construction", "Button"},
    {"camera", "Render", "Camera"},
    {"colour", "Render", "Colour"},
    {"creator", "Other", "Creator"},
    {"duplicator", "Construction", "Duplicator"},
    {"dynamite", "Construction", "Dynamite"},
    {"editentity", "Construction", "Editentity"},
    {"elastic", "Constraints", "Elastic"},
    {"emitter", "Construction", "Emitter"},
    {"example", "My Category", "Example"},
    {"eyeposer", "Poser", "Eyeposer"},
    {"faceposer", "Poser", "Faceposer"},
    {"finger", "Poser", "Finger"},
    {"hoverball", "Construction", "Hoverball"},
    {"hydraulic", "Constraints", "Hydraulic"},
    {"inflator", "Poser", "Inflator"},
    {"lamp", "Construction", "Lamp"},
    {"leafblower", "Other", "Leafblower"},
    {"light", "Construction", "Light"},
    {"material", "Render", "Material"},
    {"motor", "Constraints", "Motor"},
    {"muscle", "Constraints", "Muscle"},
    {"nocollide", "Construction", "Nocollide"},
    {"paint", "Render", "Paint"},
    {"physprop", "Construction", "Physprop"},
    {"pulley", "Constraints", "Pulley"},
    {"remover", "Construction", "Remover"},
    {"rope", "Constraints", "Rope"},
    {"slider", "Constraints", "Slider"},
    {"thruster", "Construction", "Thruster"},
    {"trails", "Render", "Trails"},
    {"weld", "Constraints", "Weld"},
    {"wheel", "Construction", "Wheel"},
    {"winch", "Constraints", "Winch"},
};
~~~

## thug2_anim_data.inc structural excerpt
Full file SHA256: 64ACD47209733BDC797335B360DEAA69CEC804B7E84D7C5555F80BCB08621998
Excerpt 1-35:
~~~cpp
00001: // Generated from original THUG2 PS2 SKA + thps6_human.ske.ps2
00002: struct THUG2QuatKey { float t,x,y,z,w; };
00003: struct THUG2Vec3Key { float t,x,y,z; };
00004: struct THUG2AnimTrack { const char* sourceBone; const char* targetBone; float srcQx,srcQy,srcQz,srcQw; float srcTx,srcTy,srcTz; const THUG2QuatKey* q; UInt16 qCount; const THUG2Vec3Key* v; UInt16 vCount; };
00005: struct THUG2AnimClip { const char* name; float duration; const THUG2AnimTrack* tracks; UInt16 trackCount; };
00006: static const THUG2QuatKey thug2_idle_0_q[] = {
00007:     {0f,0.0127563477f,-0.0182495117f,0.573425293f,0.818955243f},
00008:     {1.33333337f,0.0127563477f,-0.0182495117f,0.573425293f,0.818955243f},
00009: };
00010: static const THUG2Vec3Key thug2_idle_0_v[] = {
00011:     {0f,-2.1875f,-1.90625f,39.9533081f},
00012:     {0.0666666701f,-2.1875f,-1.90625f,40.0158081f},
00013:     {0.13333334f,-2.1875f,-1.90625f,40.1720581f},
00014:     {0.233333334f,-2.1875f,-1.90625f,40.5158081f},
00015:     {0.466666669f,-2.1875f,-1.90625f,41.5158081f},
00016:     {0.566666663f,-2.1875f,-1.90625f,41.8283081f},
00017:     {0.633333325f,-2.1875f,-1.90625f,41.9220581f},
00018:     {0.699999988f,-2.1875f,-1.90625f,41.9220581f},
00019:     {0.766666651f,-2.1875f,-1.90625f,41.8283081f},
00020:     {0.866666675f,-2.1875f,-1.90625f,41.5158081f},
00021:     {1.13333333f,-2.1875f,-1.90625f,40.3908081f},
00022:     {1.23333335f,-2.1875f,-1.90625f,40.0783081f},
00023:     {1.29999995f,-2.1875f,-1.90625f,39.9533081f},
00024:     {1.33333337f,-2.1875f,-1.90625f,39.9533081f},
00025: };
00026: static const THUG2QuatKey thug2_idle_1_q[] = {
00027:     {0f,0.0951538086f,-0.0552978516f,-0.0087890625f,0.99388665f},
00028:     {0.333333343f,0.113830566f,-0.067199707f,-0.00146484375f,0.991223812f},
00029:     {0.666666687f,0.0941162109f,-0.0514526367f,-0.0144042969f,0.994126379f},
00030:     {1f,0.0741577148f,-0.0357666016f,-0.00787353516f,0.996573865f},
00031:     {1.33333337f,0.0951538086f,-0.0552978516f,-0.0087890625f,0.99388665f},
00032: };
00033: static const THUG2Vec3Key thug2_idle_1_v[] = {
00034:     {0f,-1.05959953e-06f,0.67000109f,4.966465f},
00035:     {1.33333337f,-1.05959953e-06f,0.67000109f,4.966465f},
~~~
Excerpt 7146-7165:
~~~cpp
07146: static const THUG2AnimClip kTHUG2AnimClips[] = {
07147:     {"idle",1.33333337f,thug2_idle_tracks,static_cast<UInt16>(sizeof(thug2_idle_tracks)/sizeof(thug2_idle_tracks[0]))},
07148:     {"push",0.300000012f,thug2_push_tracks,static_cast<UInt16>(sizeof(thug2_push_tracks)/sizeof(thug2_push_tracks[0]))},
07149:     {"pushcycle",0.966666639f,thug2_pushcycle_tracks,static_cast<UInt16>(sizeof(thug2_pushcycle_tracks)/sizeof(thug2_pushcycle_tracks[0]))},
07150:     {"turnleft",0.766666651f,thug2_turnleft_tracks,static_cast<UInt16>(sizeof(thug2_turnleft_tracks)/sizeof(thug2_turnleft_tracks[0]))},
07151:     {"turnright",0.766666651f,thug2_turnright_tracks,static_cast<UInt16>(sizeof(thug2_turnright_tracks)/sizeof(thug2_turnright_tracks[0]))},
07152:     {"airidle",1.33333337f,thug2_airidle_tracks,static_cast<UInt16>(sizeof(thug2_airidle_tracks)/sizeof(thug2_airidle_tracks[0]))},
07153:     {"ollie",0.633333325f,thug2_ollie_tracks,static_cast<UInt16>(sizeof(thug2_ollie_tracks)/sizeof(thug2_ollie_tracks[0]))},
07154:     {"nollie",0.733333349f,thug2_nollie_tracks,static_cast<UInt16>(sizeof(thug2_nollie_tracks)/sizeof(thug2_nollie_tracks[0]))},
07155:     {"land",1.06666672f,thug2_land_tracks,static_cast<UInt16>(sizeof(thug2_land_tracks)/sizeof(thug2_land_tracks[0]))},
07156:     {"crouch",0.366666675f,thug2_crouch_tracks,static_cast<UInt16>(sizeof(thug2_crouch_tracks)/sizeof(thug2_crouch_tracks[0]))},
07157:     {"manual",0.433333337f,thug2_manual_tracks,static_cast<UInt16>(sizeof(thug2_manual_tracks)/sizeof(thug2_manual_tracks[0]))},
07158:     {"nosemanual",0.433333337f,thug2_nosemanual_tracks,static_cast<UInt16>(sizeof(thug2_nosemanual_tracks)/sizeof(thug2_nosemanual_tracks[0]))},
07159:     {"revertbs",0.666666687f,thug2_revertbs_tracks,static_cast<UInt16>(sizeof(thug2_revertbs_tracks)/sizeof(thug2_revertbs_tracks[0]))},
07160:     {"revertfs",0.666666687f,thug2_revertfs_tracks,static_cast<UInt16>(sizeof(thug2_revertfs_tracks)/sizeof(thug2_revertfs_tracks[0]))},
07161:     {"skitchinit",0.666666687f,thug2_skitchinit_tracks,static_cast<UInt16>(sizeof(thug2_skitchinit_tracks)/sizeof(thug2_skitchinit_tracks[0]))},
07162:     {"skitchrange",1.33333337f,thug2_skitchrange_tracks,static_cast<UInt16>(sizeof(thug2_skitchrange_tracks)/sizeof(thug2_skitchrange_tracks[0]))},
07163:     {"wallridefront",0.666666687f,thug2_wallridefront_tracks,static_cast<UInt16>(sizeof(thug2_wallridefront_tracks)/sizeof(thug2_wallridefront_tracks[0]))},
07164:     {"wallrideback",0.666666687f,thug2_wallrideback_tracks,static_cast<UInt16>(sizeof(thug2_wallrideback_tracks)/sizeof(thug2_wallrideback_tracks[0]))},
07165: };
~~~

Astra owns live retarget/cache/runtime integration. Opus should return visual/rig/animation assets plus explicit bone/attachment mappings for Astra to consume.