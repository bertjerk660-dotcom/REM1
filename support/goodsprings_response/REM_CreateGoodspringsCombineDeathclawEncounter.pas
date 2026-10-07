unit REM_CreateGoodspringsCombineDeathclawEncounter;

const
  OUT_NAME = 'REM_Goodsprings_CombineDeathclawEncounter.esp';
  ARMOR_FILE_NAME = 'REM_CombineArmor_Test_TorsoLowered.esp';
  ARMOR_EDID = 'REMCombineSoldierFullBodyTest';

var
  MasterFile, ArmorFile, OutFile: IInterface;
  RaiderDonor, DeathclawDonor, Minigun, Ammo5mm, Armor, GoodsCell, RunToPlayer, GlobalDonor: IInterface;
  RewardGlobal: IInterface;
  CombineNpc, ResponseCreature, CaptainCreature, CellCopy, CombineRef, CaptainRef: IInterface;
  ResponseRefs: array[0..9] of IInterface;
  Report: TStringList;

function FindFileByName(const aName: string): IInterface;
var i: Integer;
begin
  Result := nil;
  for i := 0 to FileCount - 1 do
    if SameText(GetFileName(FileByIndex(i)), aName) then begin
      Result := FileByIndex(i);
      Exit;
    end;
end;

function FindRecordByEDID(f: IInterface; const Sig, Edid: string): IInterface;
var g, e: IInterface; i: Integer;
begin
  Result := nil;
  if not Assigned(f) then Exit;
  g := GroupBySignature(f, Sig);
  if not Assigned(g) then Exit;
  for i := 0 to Pred(ElementCount(g)) do begin
    e := ElementByIndex(g, i);
    if SameText(GetElementEditValues(e, 'EDID'), Edid) then begin
      Result := e;
      Exit;
    end;
  end;
end;

procedure AddInventoryItem(actorRec, itemRec: IInterface; count: Integer);
var items, entry: IInterface;
begin
  items := ElementByName(actorRec, 'Items');
  if not Assigned(items) then begin
    items := Add(actorRec, 'Items', False);
    entry := ElementByIndex(items, 0);
  end else
    entry := ElementAssign(items, HighInteger, nil, False);
  SetElementEditValues(entry, 'CNTO\Item', Name(itemRec));
  SetElementNativeValues(entry, 'CNTO\Count', count);
end;

procedure ClearCreatureAI(crea: IInterface);
var pk: IInterface;
begin
  RemoveElement(crea, 'TPLT');
  RemoveElement(crea, 'Factions');

  { "Packages" is a virtual grouped view and cannot itself be edited in xEdit.
    Remove concrete PKID subrecords one at a time instead. }
  pk := ElementBySignature(crea, 'PKID');
  while Assigned(pk) do begin
    Remove(pk);
    pk := ElementBySignature(crea, 'PKID');
  end;

  SetElementNativeValues(crea, 'ACBS\Template Flags', 0);
  SetElementNativeValues(crea, 'AIDT\Aggression', 0);
  SetElementNativeValues(crea, 'AIDT\Confidence', 4);
  SetElementNativeValues(crea, 'AIDT\Energy level', 100);
end;

function PlaceCreature(cellRec, baseRec: IInterface; x, y, z: Float; initiallyDisabled: Boolean): IInterface;
begin
  Result := Add(cellRec, 'ACRE', True);
  if not Assigned(Result) then Exit;
  SetElementEditValues(Result, 'NAME - Base', Name(baseRec));
  SetElementNativeValues(Result, 'DATA\Position\X', x);
  SetElementNativeValues(Result, 'DATA\Position\Y', y);
  SetElementNativeValues(Result, 'DATA\Position\Z', z);
  SetElementNativeValues(Result, 'DATA\Rotation\X', 0);
  SetElementNativeValues(Result, 'DATA\Rotation\Y', 0);
  SetElementNativeValues(Result, 'DATA\Rotation\Z', 0);
  if initiallyDisabled then
    SetIsInitiallyDisabled(Result, True);
end;

function Initialize: Integer;
var i: Integer;
    xs, ys: array[0..9] of Float;
    pk: IInterface;
begin
  Result := 0;
  Report := TStringList.Create;

  MasterFile := FindFileByName('FalloutNV.esm');
  ArmorFile := FindFileByName(ARMOR_FILE_NAME);
  if not Assigned(MasterFile) or not Assigned(ArmorFile) then begin Result := 1; Exit; end;

  RaiderDonor := RecordByFormID(MasterFile, $000CEAB3, True);
  DeathclawDonor := RecordByFormID(MasterFile, $0001CF9A, True);
  Minigun := RecordByFormID(MasterFile, $0000433F, True);
  Ammo5mm := RecordByFormID(MasterFile, $0006B53D, True);
  GoodsCell := RecordByFormID(MasterFile, $000DAEBB, True);
  RunToPlayer := RecordByFormID(MasterFile, $000CAFC6, True);
  GlobalDonor := RecordByFormID(MasterFile, $00176537, True); // VNight: short global, initial 0
  Armor := FindRecordByEDID(ArmorFile, 'ARMO', ARMOR_EDID);

  if not Assigned(RaiderDonor) or not Assigned(DeathclawDonor) or
     not Assigned(Minigun) or not Assigned(Ammo5mm) or not Assigned(GoodsCell) or
     not Assigned(RunToPlayer) or not Assigned(GlobalDonor) or not Assigned(Armor) then begin Result := 1; Exit; end;

  OutFile := AddNewFileName(OUT_NAME);
  if not Assigned(OutFile) then begin Result := 1; Exit; end;

  AddRequiredElementMasters(RaiderDonor, OutFile, False);
  AddRequiredElementMasters(DeathclawDonor, OutFile, False);
  AddRequiredElementMasters(Minigun, OutFile, False);
  AddRequiredElementMasters(Ammo5mm, OutFile, False);
  AddRequiredElementMasters(GoodsCell, OutFile, False);
  AddRequiredElementMasters(RunToPlayer, OutFile, False);
  AddRequiredElementMasters(GlobalDonor, OutFile, False);
  AddRequiredElementMasters(Armor, OutFile, False);

  CombineNpc := wbCopyElementToFile(RaiderDonor, OutFile, True, True);
  SetElementEditValues(CombineNpc, 'EDID', 'REMCombineSoliderGoodspringsRampage');
  SetElementEditValues(CombineNpc, 'FULL', 'Combine Solider');
  RemoveElement(CombineNpc, 'TPLT');
  SetElementNativeValues(CombineNpc, 'ACBS\Template Flags', 0);
  SetElementNativeValues(CombineNpc, 'DATA\Base Health', 100000);
  SetElementNativeValues(CombineNpc, 'ACBS\Speed Multiplier', 200);
  SetElementNativeValues(CombineNpc, 'AIDT\Aggression', 3);
  SetElementNativeValues(CombineNpc, 'AIDT\Confidence', 4);
  SetElementNativeValues(CombineNpc, 'AIDT\Energy level', 100);
  RemoveElement(CombineNpc, 'Factions');
  RemoveElement(CombineNpc, 'Items');
  AddInventoryItem(CombineNpc, Armor, 1);
  AddInventoryItem(CombineNpc, Minigun, 1);
  AddInventoryItem(CombineNpc, Ammo5mm, 10000000);

  ResponseCreature := wbCopyElementToFile(DeathclawDonor, OutFile, True, True);
  SetElementEditValues(ResponseCreature, 'EDID', 'REMDeathclawResponseUnit');
  SetElementEditValues(ResponseCreature, 'FULL', 'DEATHCLAW RESPONSE UNIT');
  ClearCreatureAI(ResponseCreature);

  CaptainCreature := wbCopyElementToFile(DeathclawDonor, OutFile, True, True);
  SetElementEditValues(CaptainCreature, 'EDID', 'REMCaptainClaw');
  SetElementEditValues(CaptainCreature, 'FULL', 'Captain Claw');
  ClearCreatureAI(CaptainCreature);
  { Bake Bethesda's own RunToPlayerForever package into Captain Claw. The runtime
    bridge still calls EVP after enable so he immediately evaluates this package.
    No MoveTo/teleport command is used anywhere in the Captain path. }
  pk := Add(CaptainCreature, 'PKID', True);
  if Assigned(pk) then
    SetEditValue(pk, Name(RunToPlayer));

  CellCopy := wbCopyElementToFile(GoodsCell, OutFile, False, True);

  CombineRef := Add(CellCopy, 'ACHR', True);
  SetElementEditValues(CombineRef, 'NAME - Base', Name(CombineNpc));
  SetElementNativeValues(CombineRef, 'DATA\Position\X', -71300.0);
  SetElementNativeValues(CombineRef, 'DATA\Position\Y', 1800.0);
  SetElementNativeValues(CombineRef, 'DATA\Position\Z', 8352.0);

  xs[0]:=-72000; ys[0]:=1800;
  xs[1]:=-71900; ys[1]:=2300;
  xs[2]:=-71600; ys[2]:=2700;
  xs[3]:=-71000; ys[3]:=2750;
  xs[4]:=-70500; ys[4]:=2300;
  xs[5]:=-70400; ys[5]:=1700;
  xs[6]:=-70600; ys[6]:=1100;
  xs[7]:=-71100; ys[7]:=900;
  xs[8]:=-71600; ys[8]:=1000;
  xs[9]:=-72000; ys[9]:=1400;

  for i := 0 to 9 do
    ResponseRefs[i] := PlaceCreature(CellCopy, ResponseCreature, xs[i], ys[i], 8352.0, False);

  // Captain Claw starts well outside the immediate fight and remains disabled until
  // the runtime death-event bridge enables him. RunToPlayerForever then drives a
  // real pathfinding approach; no MoveTo/teleport is used.
  CaptainRef := PlaceCreature(CellCopy, CaptainCreature, -73000.0, 1800.0, 8352.0, True);

  { Append the persistent one-time reward flag after all encounter bases/refs so
    local IDs 0800-080E remain stable for the runtime support plugin. }
  RewardGlobal := wbCopyElementToFile(GlobalDonor, OutFile, True, True);
  SetElementEditValues(RewardGlobal, 'EDID', 'REMCaptainClawRewarded');
  SetElementNativeValues(RewardGlobal, 'FLTV', 0.0);

  Report.Add('OUT=' + GetFileName(OutFile));
  Report.Add('COMBINE_BASE=' + IntToHex(GetLoadOrderFormID(CombineNpc), 8));
  Report.Add('RESPONSE_BASE=' + IntToHex(GetLoadOrderFormID(ResponseCreature), 8));
  Report.Add('CAPTAIN_BASE=' + IntToHex(GetLoadOrderFormID(CaptainCreature), 8));
  Report.Add('COMBINE_REF=' + IntToHex(GetLoadOrderFormID(CombineRef), 8));
  for i := 0 to 9 do
    Report.Add('RESPONSE_REF_' + IntToStr(i+1) + '=' + IntToHex(GetLoadOrderFormID(ResponseRefs[i]), 8));
  Report.Add('CAPTAIN_REF=' + IntToHex(GetLoadOrderFormID(CaptainRef), 8));
  if GetIsInitiallyDisabled(CaptainRef) then
    Report.Add('CAPTAIN_DISABLED=True')
  else
    Report.Add('CAPTAIN_DISABLED=False');
  Report.Add('CAPTAIN_RUN_PACKAGE=' + IntToHex(GetLoadOrderFormID(RunToPlayer), 8));
  Report.Add('REWARD_GLOBAL=' + IntToHex(GetLoadOrderFormID(RewardGlobal), 8));
  Report.SaveToFile('C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\goodsprings_response\encounter_build.txt');

  AddMessage('[REMRESPONSE] encounter records created');
end;

function Finalize: Integer;
begin
  Result := 0;
  if Assigned(Report) then Report.Free;
end;

end.
