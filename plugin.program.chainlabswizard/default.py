import sys, os, urllib.request
import xbmc, xbmcgui, xbmcplugin, xbmcvfs, xbmcaddon

addon = xbmcaddon.Addon()
handle = int(sys.argv[1])
base_url = sys.argv[0]

# Auto-generated full-build URL
FULL_BUILD_URL = ""

def list_menu():
    item = xbmcgui.ListItem(label="Install Full Neurochain Build")
    url = f"{base_url}?action=install"
    xbmcplugin.addDirectoryItem(handle, url, item, isFolder=False)
    xbmcplugin.endOfDirectory(handle)

def install_build():
    dest = xbmcvfs.translatePath("special://home/")
    zippath = os.path.join(dest, "Neurochainlabs_FullBuild.zip")
    xbmcgui.Dialog().notification("ChainLabs Wizard", "Downloading build...", xbmcgui.NOTIFICATION_INFO)
    response = urllib.request.urlopen(FULL_BUILD_URL)
    with open(zippath, "wb") as f:
        f.write(response.read())
    xbmcgui.Dialog().notification("ChainLabs Wizard", "Installing build...", xbmcgui.NOTIFICATION_INFO)
    xbmc.executebuiltin(f"InstallFromZip({zippath})")

if len(sys.argv) > 2 and "action=install" in sys.argv[2]:
    install_build()
else:
    list_menu()
