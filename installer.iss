; Script de instalador para BysCode
; Creado con Inno Setup

[Setup]
AppName=BysCode
AppVersion=1.0.0
AppPublisher=BysPro
AppPublisherURL=https://byspro.com.co
AppSupportURL=https://byspro.com.co
AppUpdatesURL=https://byspro.com.co
DefaultDirName={autopf}\BysPro\BysCode
DefaultGroupName=BysCode
AllowNoIcons=yes
OutputDir=Instalador
OutputBaseFilename=BysCode_Setup
SetupIconFile=media\logo-byscode.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\BysCode.exe
AppID={{BYSCODE-2024-MALOLO}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Otras tareas:"
Name: "quicklaunchicon"; Description: "Crear un icono en la barra de acceso rápido"; GroupDescription: "Otras tareas:"; Flags: unchecked

[Files]
; Archivo ejecutable principal
Source: "BysCode_Portable\BysCode.exe"; DestDir: "{app}"; Flags: ignoreversion

; Archivos de la interfaz
Source: "BysCode_Portable\src\mainWindow.ui"; DestDir: "{app}\src"; Flags: ignoreversion
Source: "BysCode_Portable\src\services\sap_service.py"; DestDir: "{app}\src\services"; Flags: ignoreversion

; Archivos multimedia
Source: "BysCode_Portable\media\logo-byscode.ico"; DestDir: "{app}\media"; Flags: ignoreversion
Source: "BysCode_Portable\media\logo-byspro.png"; DestDir: "{app}\media"; Flags: ignoreversion

; Documentación
Source: "BysCode_Portable\LEEME.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\BysCode"; Filename: "{app}\BysCode.exe"; IconFilename: "{app}\media\logo-byscode.ico"
Name: "{group}\Desinstalar BysCode"; Filename: "{uninstallexe}"
Name: "{autodesktop}\BysCode"; Filename: "{app}\BysCode.exe"; IconFilename: "{app}\media\logo-byscode.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\BysCode"; Filename: "{app}\BysCode.exe"; IconFilename: "{app}\media\logo-byscode.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\BysCode.exe"; Description: "Ejecutar BysCode"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;