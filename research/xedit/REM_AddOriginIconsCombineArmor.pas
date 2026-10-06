unit REM_AddOriginIconsCombineArmor;

const
  GMOD_LARGE = 'Interface\Icons\PipboyImages\Weapons\rem_gmod_origin.dds';
  GMOD_SMALL = 'Interface\Icons\PipboyImages_small\Weapons_small\glow_rem_gmod_origin.dds';
  THUG_LARGE = 'Interface\Icons\PipboyImages\Weapons\rem_thug2_origin.dds';
  THUG_SMALL = 'Interface\Icons\PipboyImages_small\Weapons_small\glow_rem_thug2_origin.dds';
  COMBINE_BIPED = 'rem\gmod\armor\CombineSoldierFullBody.nif';
  COMBINE_WORLD = 'rem\gmod\Combine_Soldier.nif';

var
  Report: TStringList;
  ModFile, MasterFile: IInterface;

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

function FindByEDID(aFile: IInterface; const Sig, EDID: string): IInterface;
var
  g, r: IInterface;
  i: Integer;
begin
  Result := nil;
  g := GroupBySignature(aFile, Sig);
  if not Assigned(g) then Exit;
  for i := 0 to ElementCount(g) - 1 do begin
    r := ElementByIndex(g, i);
    if SameText(GetElementEditValues(r, 'EDID'), EDID) then begin
      Result := r;
      Exit;
    end;
  end;
end;

procedure SetWeaponOriginIcon(r: IInterface; const LargePath, SmallPath: string);
begin
  SetElementEditValues(r, 'Icon\ICON - Large Icon FileName', LargePath);
  SetElementEditValues(r, 'Icon\MICO - Small Icon FileName', SmallPath);
end;

function EnsureCombineArmor: IInterface;
var
  donor, existing: IInterface;
begin
  existing := FindByEDID(ModFile, 'ARMO', 'REMCombineSoldierFullBody');
  if Assigned(existing) then begin
    Result := existing;
    Report.Add('ARMOR existing: ' + Name(existing));
  end else begin
    donor := FindByEDID(MasterFile, 'ARMO', 'ArmorPowerRemnants');
    if not Assigned(donor) then begin
      Report.Add('ERROR: ArmorPowerRemnants donor not found');
      Result := nil;
      Exit;
    end;
    Result := wbCopyElementToFile(donor, ModFile, True, True);
    if not Assigned(Result) then begin
      Report.Add('ERROR: armor copy failed');
      Exit;
    end;
    Report.Add('ARMOR copied from Remnants: ' + Name(Result));
  end;

  SetElementEditValues(Result, 'EDID', 'REMCombineSoldierFullBody');
  SetElementEditValues(Result, 'FULL', 'Combine Soldier Full-Body Armor');

  { Body + helmet/head slots + both hands. Retains the donor Power Armor/Heavy flags. }
  SetElementNativeValues(Result, 'BMDT\Biped Flags', 17951);

  SetElementEditValues(Result, 'Male Biped Model\MODL - Model FileName', COMBINE_BIPED);
  SetElementEditValues(Result, 'Male World Model\MOD2 - Model FileName', COMBINE_WORLD);

  { The Remnants BIPL points at Advanced Power Armor-specific model-list data and
    must not be carried into this custom skinned full-body visual. }
  RemoveElement(Result, 'BIPL - Biped Model List');

  SetElementEditValues(Result, 'ICON - Male Icon Filename', GMOD_LARGE);
  SetElementEditValues(Result, 'MICO - Male Message Icon Filename', GMOD_SMALL);

  Report.Add('ARMOR final FormID=' + IntToHex(GetLoadOrderFormID(Result), 8));
  Report.Add('ARMOR biped=' + GetElementEditValues(Result, 'Male Biped Model\MODL - Model FileName'));
  Report.Add('ARMOR world=' + GetElementEditValues(Result, 'Male World Model\MOD2 - Model FileName'));
  Report.Add('ARMOR flags=' + GetElementEditValues(Result, 'BMDT\Biped Flags'));
end;

function Initialize: Integer;
var
  g, r, armor: IInterface;
  i, GModCount, THUGCount: Integer;
  edid: string;
begin
  Result := 0;
  Report := TStringList.Create;
  GModCount := 0;
  THUGCount := 0;

  MasterFile := FindFileByName('FalloutNV.esm');
  ModFile := FindFileByName('REM_GModTHUG2.esp');

  if not Assigned(MasterFile) then begin
    AddMessage('REM: FalloutNV.esm not loaded');
    Exit;
  end;
  if not Assigned(ModFile) then begin
    AddMessage('REM: REM_GModTHUG2.esp not loaded');
    Exit;
  end;

  g := GroupBySignature(ModFile, 'WEAP');
  if Assigned(g) then
    for i := 0 to ElementCount(g) - 1 do begin
      r := ElementByIndex(g, i);
      edid := GetElementEditValues(r, 'EDID');
      if Pos('REMGW_', edid) = 1 then begin
        SetWeaponOriginIcon(r, GMOD_LARGE, GMOD_SMALL);
        Inc(GModCount);
      end else if Pos('REMTHUG2', edid) = 1 then begin
        SetWeaponOriginIcon(r, THUG_LARGE, THUG_SMALL);
        Inc(THUGCount);
      end;
    end;

  armor := EnsureCombineArmor;

  Report.Add('GMOD weapons patched=' + IntToStr(GModCount));
  Report.Add('THUG2 weapons patched=' + IntToStr(THUGCount));
  if Assigned(armor) then Report.Add('Combine armor=READY');
  Report.SaveToFile('C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\quick_assets_install_report.txt');

  AddMessage('REM origin icons / Combine armor: GMod=' + IntToStr(GModCount) +
    ' THUG2=' + IntToStr(THUGCount));
end;

function Finalize: Integer;
begin
  Result := 0;
  if Assigned(Report) then Report.Free;
end;

end.