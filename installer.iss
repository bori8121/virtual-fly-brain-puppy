[Setup]
AppName=Virtual Fly Brain Puppy
AppVersion=1.0
DefaultDirName={autopf}\VirtualFlyBrainPuppy
DefaultGroupName=VirtualFlyBrainPuppy
OutputBaseFilename=VirtualFlyBrainPuppyInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\\VirtualFlyBrainPuppy\\*"; DestDir: "{app}"; Flags: recursesubdirs
Source: "docs\\사용자_매뉴얼_ko.md"; DestDir: "{app}\\docs"

[Icons]
Name: "{group}\\Virtual Fly Brain Puppy"; Filename: "{app}\\VirtualFlyBrainPuppy.exe"
Name: "{commondesktop}\\Virtual Fly Brain Puppy"; Filename: "{app}\\VirtualFlyBrainPuppy.exe"
