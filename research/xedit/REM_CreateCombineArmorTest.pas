unit REM_CreateCombineArmorTest;

const
  OUT_NAME = 'REM_CombineArmor_Test.esp';
  COMBINE_BIPED = 'rem\gmod\armor\CombineSoldierFullBody.nif';
  COMBINE_WORLD = 'rem\gmod\Combine_Soldier.nif';
  GMOD_LARGE = 'Interface\Icons\PipboyImages\Weapons\rem_gmod_origin.dds';
  GMOD_SMALL = 'Interface\Icons\PipboyImages_small\Weapons_small\glow_rem_gmod_origin.dds';

var
  MasterFile, OutFile: IInterface;
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

function FindByEDID(aFile: IInterface; const Sig, EDID: string): IInterface;
var g, r: IInterface; i: Integer;
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

function Initialize: Integer;
var donor, armor: IInterface; fs: TFileStream; outPath: string;
begin
  Result := 0;
  Report := TStringList.Create;
  MasterFile := FindFileByName('FalloutNV.esm');
  if not Assigned(MasterFile) then begin
    Report.Add('FATAL: FalloutNV.esm not loaded');
    Result := 1;
    Exit;
  end;

  OutFile := FindFileByName(OUT_NAME);
  if not Assigned(OutFile) then
    OutFile := AddNewFileName(OUT_NAME);
  if not Assigned(OutFile) then begin
    Report.Add('FATAL: could not create ' + OUT_NAME);
    Result := 1;
    Exit;
  end;
  AddMasterIfMissing(OutFile, 'FalloutNV.esm');

  armor := FindByEDID(OutFile, 'ARMO', 'REMCombineSoldierFullBodyTest');
  if not Assigned(armor) then begin
    donor := FindByEDID(MasterFile, 'ARMO', 'ArmorPowerRemnants');
    if not Assigned(donor) then begin
      Report.Add('FATAL: ArmorPowerRemnants donor missing');
      Result := 1;
      Exit;
    end;
    armor := wbCopyElementToFile(donor, OutFile, True, True);
  end;
  if not Assigned(armor) then begin
    Report.Add('FATAL: armor record creation failed');
    Result := 1;
    Exit;
  end;

  SetElementEditValues(armor, 'EDID', 'REMCombineSoldierFullBodyTest');
  SetElementEditValues(armor, 'FULL', 'Combine Soldier Full-Body Armor (Test)');
  SetElementNativeValues(armor, 'BMDT\Biped Flags', 17951);

  SetElementEditValues(armor, 'Male Biped Model\MODL - Model FileName', COMBINE_BIPED);
  SetElementEditValues(armor, 'Male World Model\MOD2 - Model FileName', COMBINE_WORLD);
  SetElementEditValues(armor, 'Female Biped Model\MOD3 - Model FileName', COMBINE_BIPED);
  SetElementEditValues(armor, 'Female World Model\MOD4 - Model FileName', COMBINE_WORLD);

  SetElementEditValues(armor, 'ICON - Male Icon Filename', GMOD_LARGE);
  SetElementEditValues(armor, 'MICO - Male Message Icon Filename', GMOD_SMALL);
  SetElementEditValues(armor, 'ICO2 - Female Icon Filename', GMOD_LARGE);
  SetElementEditValues(armor, 'MIC2 - Female Message Icon Filename', GMOD_SMALL);

  RemoveElement(armor, 'BIPL - Biped Model List');
  CleanMasters(OutFile);

  outPath := DataPath + OUT_NAME;
  fs := TFileStream.Create(outPath, fmCreate);
  try
    FileWriteToStream(OutFile, fs, False);
  finally
    fs.Free;
  end;

  Report.Add('OUTPUT=' + outPath);
  Report.Add('FORM=' + Name(armor));
  Report.Add('FORMID=' + IntToHex(GetLoadOrderFormID(armor), 8));
  Report.Add('FLAGS=' + GetElementEditValues(armor, 'BMDT\Biped Flags'));
  Report.Add('MALE_BIPED=' + GetElementEditValues(armor, 'Male Biped Model\MODL - Model FileName'));
  Report.Add('MALE_WORLD=' + GetElementEditValues(armor, 'Male World Model\MOD2 - Model FileName'));
  Report.Add('FEMALE_BIPED=' + GetElementEditValues(armor, 'Female Biped Model\MOD3 - Model FileName'));
  Report.Add('FEMALE_WORLD=' + GetElementEditValues(armor, 'Female World Model\MOD4 - Model FileName'));
  Report.Add('ICON=' + GetElementEditValues(armor, 'ICON - Male Icon Filename'));
  Report.Add('MICO=' + GetElementEditValues(armor, 'MICO - Male Message Icon Filename'));
  Report.SaveToFile('C:\Users\BRAD\Documents\------\Engineer Station\FNV_GMOD_THUG2\build\combine_armor\esp_build_report.txt');
  AddMessage('[REMCOMBINE] wrote ' + outPath + ' ' + Name(armor));
end;

function Finalize: Integer;
begin
  Result := 0;
  if Assigned(Report) then Report.Free;
end;

end.