@echo on
@setlocal ENABLEDELAYEDEXPANSION ENABLEEXTENSIONS

set "temp_computername=!COMPUTERNAME: =_!"
IF /I "!temp_computername!" == "3900X" (
    echo Forbidden to run %dpnx0 in computer "3900X" ... "!temp_computername!"
    pause
    goto :eof
)

REM
REM    <MappedFolder>
REM      <HostFolder>D:\VM\MABS</HostFolder>
REM      <SandboxFolder>C:\HOST_MABS</SandboxFolder>
REM      <ReadOnly>false</ReadOnly>
REM    </MappedFolder>
REM

mkdir C:\TEMP

REM Create a link on the sandbox desktop which is mapped to our read-only SOFTWARE folder on the host system
REM which contains our set of downloaded software that we use all the time. ie make it available in the sandbox.
set create_shortcut_SCRIPT="%TEMP%\create_HOST_software_desktop_link_%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
del %create_shortcut_SCRIPT%
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %create_shortcut_SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\HOST_software.lnk" >> %create_shortcut_SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %create_shortcut_SCRIPT%
echo oLink.TargetPath = "C:\host_software\" >> %create_shortcut_SCRIPT%
echo oLink.Arguments = "" >> %create_shortcut_SCRIPT%
echo oLink.Description = "HOST_software" >> %create_shortcut_SCRIPT%
echo 'oLink.HotKey = "" >> %create_shortcut_SCRIPT%
echo 'oLink.IconLocation = "" >> %create_shortcut_SCRIPT%
echo 'oLink.WindowStyle = "" >> %create_shortcut_SCRIPT%
echo 'oLink.WorkingDirectory = "" >> %create_shortcut_SCRIPT%
echo oLink.Save >> %create_shortcut_SCRIPT%
cscript /nologo %create_shortcut_SCRIPT%
del %create_shortcut_SCRIPT%

REM Create a link on the sandbox desktop which is mapped to our mapped read-write HOST_OUTLANDISH_01 folder on the host system
REM which contains our set of downloaded software that we use all the time. ie make it available in the sandbox.
set create_shortcut_SCRIPT="%TEMP%\create_HOST_software_desktop_link_%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"
del %create_shortcut_SCRIPT%
echo Set oWS = WScript.CreateObject("WScript.Shell") >> %create_shortcut_SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\HOST_OUTLANDISH_01.lnk" >> %create_shortcut_SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %create_shortcut_SCRIPT%
echo oLink.TargetPath = "C:\HOST_OUTLANDISH_01\" >> %create_shortcut_SCRIPT%
echo oLink.Arguments = "" >> %create_shortcut_SCRIPT%
echo oLink.Description = "HOST_OUTLANDISH_01" >> %create_shortcut_SCRIPT%
echo 'oLink.HotKey = "" >> %create_shortcut_SCRIPT%
echo 'oLink.IconLocation = "" >> %create_shortcut_SCRIPT%
echo 'oLink.WindowStyle = "" >> %create_shortcut_SCRIPT%
echo 'oLink.WorkingDirectory = "" >> %create_shortcut_SCRIPT%
echo oLink.Save >> %create_shortcut_SCRIPT%
cscript /nologo %create_shortcut_SCRIPT%
del %create_shortcut_SCRIPT%

REM ---------------------------

REM change explorer View settings to be as we like them
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V AlwaysShowMenus /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V SeparateProcess /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V NavPaneExpandToCurrentFolder /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V NavPaneShowAllFolders /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V HideFileExt /T REG_DWORD /D 00000000 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V Hidden /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V ShowSuperHidden /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V ShowEncryptCompressedColor /T REG_DWORD /D 00000001 /F
REG Add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced /V ShowStatusBar /T REG_DWORD /D 00000001 /F

REM add "Edit with Notepad++" to right click context pop-up
REM ... Notepad++ is located in the host's SOFTWARE\NPP folder
MKDIR C:\TEMP
set fnpp="C:\TEMP\EDIT_WITH_NPP.REG"
del %fnpp%
ECHO Windows Registry Editor Version 5.00                     > %fnpp%
ECHO.                                                        >> %fnpp%
ECHO [HKEY_CLASSES_ROOT\*\shell\Edit with Notepad++]         >> %fnpp%
REM ECHO "Icon"="C:\\SOFTWARE\\NPP\\notepad++.exe"
ECHO "Icon"="C:\\HOST_SOFTWARE\\NPP\\notepad++.exe"               >> %fnpp%
ECHO [HKEY_CLASSES_ROOT\*\shell\Edit with Notepad++\command] >> %fnpp%
REM ECHO @="\"C:\\SOFTWARE\\NPP\\notepad++.exe\" \"%%1\""
ECHO @="\"C:\\HOST_SOFTWARE\\NPP\\notepad++.exe\" \"%%1\""        >> %fnpp%
regedit /s %fnpp%

REM restart explorer so that eveything appears including on the desktop
REM taskkill /f /im explorer.exe "C:\HOST_TEMP"
REM start explorer.exe

REM start an explorer window at the specified directory
explorer.exe "C:\HOST_OUTLANDISH_01\"

goto :eof
