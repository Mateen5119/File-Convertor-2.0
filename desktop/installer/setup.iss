[Setup]
AppName=File Harbor
AppVersion=1.0.0
Publisher=Web Harbor Solutions
DefaultDirName={pf}\Web Harbor Solutions\File Harbor
DefaultGroupName=File Harbor
OutputDir=dist\installer
OutputBaseFilename=FileHarbor_Setup
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\FileHarbor\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Optional LibreOffice bundle
; Source: "..\libreoffice_portable\*"; DestDir: "{app}\libreoffice_portable"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\File Harbor"; Filename: "{app}\FileHarbor.exe"
Name: "{commondesktop}\File Harbor"; Filename: "{app}\FileHarbor.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FileHarbor.exe"; Description: "{cm:LaunchProgram,File Harbor}"; Flags: nowait postinstall skipifsilent
