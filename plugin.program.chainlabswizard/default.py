import sys, os, urllib.request
import xbmc, xbmcgui, xbmcplugin, xbmcvfs, xbmcaddon

addon = xbmcaddon.Addon()
handle = int(sys.argv[1])
base_url = sys.argv[0]

# Auto-generated full-build URL
FULL_BUILD_URL = "https://objects.githubusercontent.com/github-production-release-asset-2e65be/998212461/84707867-132b-4ba9-9e85-137a7a954eb1?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250608%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250608T152320Z&X-Amz-Expires=300&X-Amz-Signature=e9a36b45d76a426c68b5c6a549a4f150a9c70ffd298aeed2f295b62333798fdd&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DNeurochainlabs_FullBuild.zip&response-content-type=application%2Foctet-stream
"

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
