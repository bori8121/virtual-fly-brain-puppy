#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#define AppName "Virtual Fly Brain Puppy"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={autopf}\VirtualFlyBrainPuppy
DefaultGroupName=VirtualFlyBrainPuppy
OutputBaseFilename=VirtualFlyBrainPuppyInstaller_{#AppVersion}
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\VirtualFlyBrainPuppy.exe"; DestDir: "{app}"
Source: "docs\\사용자_매뉴얼_ko.md"; DestDir: "{app}\\docs"

[Icons]
Name: "{group}\\Virtual Fly Brain Puppy"; Filename: "{app}\\VirtualFlyBrainPuppy.exe"
Name: "{commondesktop}\\Virtual Fly Brain Puppy"; Filename: "{app}\\VirtualFlyBrainPuppy.exe"
