; NSIS installer script for Cooper River Deal Finder
Name "Cooper River Deal Finder"
OutFile "CooperRiverDealFinder-setup.exe"
InstallDir "$PROGRAMFILES64\CooperRiverDealFinder"
SetOutPath "$INSTDIR"

; Request application privileges for Windows
RequestExecutionLevel admin

Section "Install"
  SetOutPath "$INSTDIR"
  File "installer\\CooperRiverDealFinder.exe"
  ; Create a shortcut on the desktop
  CreateShortCut "$DESKTOP\\Cooper River Deal Finder.lnk" "$INSTDIR\\CooperRiverDealFinder.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\\CooperRiverDealFinder.exe"
  Delete "$DESKTOP\\Cooper River Deal Finder.lnk"
  RMDir "$INSTDIR"
SectionEnd
