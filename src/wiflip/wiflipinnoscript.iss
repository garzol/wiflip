; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING IName: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; \
    Tasks: desktopiconNNO SETUP SCRIPT FILES!

#define MyAppName "WiFlip"
#define MyAppVersion "0.98.29.0"
#define MyAppPublisher "AA55 Consulting"
#define MyAppURL "https://www.pps4.fr/"
#define MyAppExeName "wiflip.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".nvr"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt
#define MyAppIcoName "flipp.ico"

[Setup]
SignTool=signtool
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{88F02ED8-884D-4F44-9C97-2D705B05BC9C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
; "ArchitecturesAllowed=x64compatible" specifies that Setup cannot run
; on anything but x64 and Windows 11 on Arm.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" requests that the
; install be done in "64-bit mode" on x64 or Windows 11 on Arm,
; meaning it should use the native 64-bit Program Files directory and
; the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=C:\Users\garzo\git\wiflip2\license.txt
; InfoAfterFile=C:\Users\garzo\git\wiflip_tracer\after.txt
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=C:\Users\garzo\git\wiflip2
OutputBaseFilename=wiflipsetup
SetupIconFile=C:\Users\garzo\git\wiflip2\images\aa55_logo_2.ico
UninstallDisplayIcon="C:\Users\garzo\git\wiflip2\dist\{#MyAppExeName}"
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\garzo\git\wiflip2\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "C:\Users\garzo\git\wiflip2\images\{#MyAppIcoName}"; DestDir: "{app}"

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
;Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppIcoName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

