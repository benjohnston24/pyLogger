;-------------------------------------------------------------------
#NSIS Installer Script for pyLogger system 
#Author: Ben Johnston
#Date:  Fri Sep 12 15:50:48 EST 2014
#Version: 0.1
;-------------------------------------------------------------------

#Include the modern ui
!include "MUI2.nsh"

#Configure general settings
!define APPNAME "pyLogger"
!define INSTALLER_NAME "pyLogger"
!define ADD_REMOVE_NAME "pyLogger"
!define COMPANYNAME "PIPD"
!define START_FOLDER "pyLogger"
!define DESCRIPTION "Data Logger"
!define INSTALL_FOLDER "pyLogger"
# These three must be integers
!define VERSIONMAJOR 0
!define VERSIONMINOR 3
!define VERSIONBUILD 0
# This is the size (in kB) of all the files copied into "Program Files"
!define INSTALLSIZE 16400 
 
!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend
 
function .onInit
	setShellVarContext all
	!insertmacro VerifyUserIsAdmin
functionEnd
 
InstallDir "$PROGRAMFILES\${COMPANYNAME}\${INSTALL_FOLDER}"
 
# rtf or txt file - remember if it is txt, it must be in the DOS text format (\r\n)
#LicenseData "license.rtf"
# This will be in the installer/uninstaller's title bar
Name "${INSTALLER_NAME}"
Icon "pyLogger.ico"
outFile "pyLogger_setup_v${VERSIONMAJOR}${VERSIONMINOR}${VERSIONBUILD}.exe"

#Interface Settings
!define MUI_ABORTWARNING

#Pages
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

#Languages
!insertmacro MUI_LANGUAGE "English"

#Installer Sections
Section "pyLogger" SecFiles
    #Files for the installdirectory
    setOutPath $INSTDIR

    #Files to be added here are to be removed by the uninstaller
    file "pyLogger.exe"
    file "pyLogger.gif"
    file "pyLogger.ico"
    file "cli.exe"
    file "drivers.exe"
    file "README.txt"

    #Create Folder for storing results
    createDirectory "$INSTDIR\dat" 

    #Return to the installation directory
    setOutPath $INSTDIR

    #Create uninstaller
    writeUninstaller "$INSTDIR\uninstall.exe"

    #Start Menu
    createDirectory "$SMPROGRAMS\${START_FOLDER}"
    createShortCut "$SMPROGRAMS\${START_FOLDER}\${APPNAME}.lnk" "$INSTDIR\pyLogger.exe"
    createShortCut "$SMPROGRAMS\${START_FOLDER}\Data.lnk" "$INSTDIR\dat"
    createShortCut "$SMPROGRAMS\${START_FOLDER}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
	
	# Registry information for add/remove programs
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayName" "${ADD_REMOVE_NAME}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$\"$INSTDIR\pyLogger.ico$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"
	#WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "HelpLink" "$\"${HELPURL}$\""
	#WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "$\"${UPDATEURL}$\""
	#WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "$\"${ABOUTURL}$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}
	# There is no option for modifying or repairing the install
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "NoRepair" 1
	# Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}

    #Set the required UAC level in the shortcut
    ShellLink::SetRunAsAdministrator "$SMPROGRAMS\${START_FOLDER}\${APPNAME}.lnk"
    Pop $0
    DetailPrint "SetRunAsAdministrator: $0"
    DetailPrint ""

    #Set the required UAC level in the shortcut
    ShellLink::SetRunAsAdministrator "$SMPROGRAMS\${START_FOLDER}\Uninstall.lnk"
    Pop $0
    DetailPrint "SetRunAsAdministrator: $0"
    DetailPrint ""
    
sectionEnd
 
# Uninstaller
 
function un.onInit
	SetShellVarContext all
 
	#Verify the uninstaller - last chance to back out
	MessageBox MB_OKCANCEL "Permanantly remove ${APPNAME}?" IDOK next
		Abort
	next:
	!insertmacro VerifyUserIsAdmin
functionEnd
 
Section "Device Drivers" SecDrivers
    ExecWait "$INSTDIR\drivers.exe"
    Pop $0 
    ${if} $0 != "0" 
        Abort
    ${endif}
SectionEnd 

#Descriptions
LangString DESC_SecFiles ${LANG_ENGLISH} "pyLogger Software"
LangString DESC_SecDrivers ${LANG_ENGLISH} "pyLogger Device Drivers"
!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecFiles} $(DESC_SecFiles)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDrivers} $(DESC_SecDrivers)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

section "uninstall"
 
	# Remove Start Menu launcher
	delete "$SMPROGRAMS\${APPNAME}.lnk"
    delete "$SMPROGRAMS\${START_FOLDER}\${APPNAME}.lnk" 
    delete "$SMPROGRAMS\${START_FOLDER}\Uninstall.lnk"
    delete "$SMPROGRAMS\${START_FOLDER}\Reports.lnk"
 
	# Try to remove the Start Menu folder - this will only happen if it is empty
	rmDir "$SMPROGRAMS\${START_FOLDER}\"   
 
	# Remove files
    delete "$INSTDIR\pyLogger.exe"
    delete "$INSTDIR\pyLogger.gif"
    delete "$INSTDIR\pyLogger.ico"
    delete "$INSTDIR\cli.exe"
    delete "$INSTDIR\drivers.exe"
    delete "$INSTDIR\README.txt"

	# Always delete uninstaller as the last action
	delete $INSTDIR\uninstall.exe
 
	# Remove uninstaller information from the registry
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${COMPANYNAME} ${APPNAME}"
	
	#Need to permanently remove config and results files manually
	MessageBox MB_OK "Report, log and database files must be manually removed from $INSTDIR"

SectionEnd
