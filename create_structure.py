import os
import shutil
import re

# Root of the GitHub clone (current working directory)
ROOT = os.getcwd()

# Directories to create
dirs = [
    os.path.join(ROOT, 'repo.chainlabswizard'),
    os.path.join(ROOT, 'plugin.program.chainlabswizard'),
    os.path.join(ROOT, 'plugin.program.chainlabswizard', 'resources', 'media'),
    os.path.join(ROOT, 'docs')
]

# Create directory structure
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1) Write repo.chainlabswizard/addon.xml
repo_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.chainlabswizard"
       version="1.0.0"
       name="ChainLabs Wizard Repository"
       provider-name="YourName">
  <extension point="xbmc.addon.repository" name="ChainLabs Wizard Repo">
    <info compressed="false">addons.xml</info>
  </extension>
  <summary lang="en">Hosts the ChainLabs Wizard program add-on</summary>
  <description lang="en">
    Contains the program add-on that installs the full Neurochain Kodi build.
  </description>
  <platform>all</platform>
</addon>
"""
with open(os.path.join(ROOT, 'repo.chainlabswizard', 'addon.xml'), 'w', encoding='utf-8') as f:
    f.write(repo_xml)

# 2) Write plugin.program.chainlabswizard/addon.xml
wizard_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="plugin.program.chainlabswizard"
       name="ChainLabs Wizard"
       version="1.0.0"
       provider-name="YourName">
  <extension point="xbmc.python.program" library="default.py">
    <program>
      <title>ChainLabs Wizard</title>
      <description>Installs the full Neurochain build.</description>
    </program>
  </extension>
  <icon>resources/media/icon.png</icon>
  <fanart>resources/media/fanart.jpg</fanart>
  <thumbnail>resources/media/icon.png</thumbnail>
  <platform>all</platform>
</addon>
"""
with open(os.path.join(ROOT, 'plugin.program.chainlabswizard', 'addon.xml'), 'w', encoding='utf-8') as f:
    f.write(wizard_xml)

# 3) Read FULL_BUILD_URL from download link.txt
download_txt = os.path.join(ROOT, 'download link.txt')
full_url = ''
if os.path.isfile(download_txt):
    text = open(download_txt, encoding='utf-8', errors='ignore').read()
    match = re.search(r'https?://\S+', text)
    if match:
        full_url = match.group(0)

# 4) Write plugin.program.chainlabswizard/default.py with REAL URL
default_py = f"""import sys, os, urllib.request
import xbmc, xbmcgui, xbmcplugin, xbmcvfs, xbmcaddon

addon = xbmcaddon.Addon()
handle = int(sys.argv[1])
base_url = sys.argv[0]

# Auto-generated full-build URL
FULL_BUILD_URL = "{full_url}"

def list_menu():
    item = xbmcgui.ListItem(label="Install Full Neurochain Build")
    url = f"{{base_url}}?action=install"
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
    xbmc.executebuiltin(f"InstallFromZip({{zippath}})")

if len(sys.argv) > 2 and "action=install" in sys.argv[2]:
    install_build()
else:
    list_menu()
"""
with open(os.path.join(ROOT, 'plugin.program.chainlabswizard', 'default.py'), 'w', encoding='utf-8') as f:
    f.write(default_py)

# 5) Copy user-supplied images if present
src_logo = os.path.join(ROOT, 'Logo.png')
dst_fanart = os.path.join(ROOT, 'plugin.program.chainlabswizard', 'resources', 'media', 'fanart.jpg')
if os.path.isfile(src_logo):
    shutil.copy(src_logo, dst_fanart)

src_icon = os.path.join(ROOT, 'icon.png')
dst_icon = os.path.join(ROOT, 'plugin.program.chainlabswizard', 'resources', 'media', 'icon.png')
if os.path.isfile(src_icon):
    shutil.copy(src_icon, dst_icon)

print("✅ Folder structure created with addon.xml, default.py, and media files.")
print(f" - Repo add-on: {os.path.join('repo.chainlabswizard', 'addon.xml')}")
print(f" - Wizard add-on: {os.path.join('plugin.program.chainlabswizard', 'addon.xml')}")
print(f" - Wizard script: {os.path.join('plugin.program.chainlabswizard', 'default.py')}")
print(" - Media folder populated with fanart.jpg and icon.png")
