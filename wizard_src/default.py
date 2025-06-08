import xbmc, xbmcgui, zipfile, tempfile, urllib.request

BUILD_ZIP_URL = (
  "https://github.com/lonewolf8555/"
  "neurochain-wizard/releases/download/v1.0.0/"
  "Neurochainlabs-1.0.0-full.zip"
)

def install_build():
    dlg = xbmcgui.DialogProgress()
    dlg.create("NeuroChain Wizard", "Downloading build…")
    tmp = xbmc.translatePath("special://temp/neuro_full.zip")
    urllib.request.urlretrieve(BUILD_ZIP_URL, tmp,
        lambda c, b, t: dlg.update(int(c*b*100/t)))
    dlg.update(100, "Installing…")
    with zipfile.ZipFile(tmp, 'r') as zf:
        zf.extractall(xbmc.translatePath("special://home/"))
    dlg.close()
    xbmc.executebuiltin("Notification(NeuroChain, Installation complete, 5000)")

if __name__ == '__main__':
    install_build()
