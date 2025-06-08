#!/usr/bin/env python3
import glob, zipfile, xml.etree.ElementTree as ET, hashlib, sys

addons_root = ET.Element('addons')

for zfname in glob.glob('*.zip'):
    try:
        with zipfile.ZipFile(zfname) as z:
            # find the first path that ends with addon.xml
            xml_paths = [n for n in z.namelist() if n.lower().endswith('addon.xml')]
            if not xml_paths:
                print(f"⚠️  Skipping {zfname}: no addon.xml found", file=sys.stderr)
                continue
            xml_path = xml_paths[0]
            with z.open(xml_path) as f:
                tree = ET.parse(f)
                addon_elem = tree.getroot()
                addons_root.append(addon_elem)
                print(f"✔️  Added {addon_elem.attrib.get('id')} from {zfname}")
    except zipfile.BadZipFile:
        print(f"⚠️  {zfname} is not a valid zip archive", file=sys.stderr)

# write addons.xml
tree = ET.ElementTree(addons_root)
tree.write('addons.xml', encoding='utf-8', xml_declaration=True)

# write MD5
data = open('addons.xml','rb').read()
md5 = hashlib.md5(data).hexdigest()
with open('addons.xml.md5','w') as f:
    f.write(md5)

print("\nGenerated addons.xml and addons.xml.md5")
