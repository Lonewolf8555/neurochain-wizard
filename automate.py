#!/usr/bin/env python3
import os
import sys
import zipfile
import shutil
import hashlib
import xml.etree.ElementTree as ET
import subprocess

# Paths (adjust if needed)
ROOT = os.path.abspath(os.path.dirname(__file__))
DOCS = os.path.join(ROOT, 'docs')
REPO_DIR = os.path.join(ROOT, 'repo.chainlabswizard')
WIZARD_DIR = os.path.join(ROOT, 'plugin.program.chainlabswizard')

# Usage
USAGE = '''
Usage: python automate.py <new_version> [--git]

<new_version>: version string, e.g. 1.0.2
--git       : optional flag to auto-commit & push
'''


def bump_version(xml_path, new_version):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    root.attrib['version'] = new_version
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)
    print(f"✔ Bumped {xml_path} to version {new_version}")


def zip_addon(src_dir, dest_zip):
    if os.path.exists(dest_zip): os.remove(dest_zip)
    with zipfile.ZipFile(dest_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                absf = os.path.join(root, f)
                relf = os.path.relpath(absf, src_dir)
                zf.write(absf, relf)
    print(f"✔ Created {dest_zip}")


def generate_addons_xml(zip_files, output_xml):
    addons_el = ET.Element('addons')
    for zipf in zip_files:
        with zipfile.ZipFile(zipf) as zf:
            # find addon.xml
            candidates = [n for n in zf.namelist() if n.lower().endswith('addon.xml')]
            if not candidates:
                print(f"⚠ Skipping {zipf}, no addon.xml")
                continue
            data = zf.read(candidates[0])
            addon = ET.fromstring(data)
            addons_el.append(addon)
    tree = ET.ElementTree(addons_el)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)
    print(f"✔ Written {output_xml}")


def generate_md5(xml_path, md5_path):
    data = open(xml_path, 'rb').read()
    md5 = hashlib.md5(data).hexdigest()
    with open(md5_path, 'w') as f: f.write(md5)
    print(f"✔ Written {md5_path}")


def git_commit_push(files, version):
    try:
        subprocess.check_call(['git', 'add'] + files)
        subprocess.check_call(['git', 'commit', '-m', f'Release v{version}'])
        subprocess.check_call(['git', 'push'])
        print("✔ Git commit & push succeeded")
    except Exception as e:
        print("⚠ Git step failed:", e)


def main():
    if len(sys.argv) < 2:
        print(USAGE); sys.exit(1)
    version = sys.argv[1]
    use_git = '--git' in sys.argv

    # 1) bump versions
    bump_version(os.path.join(REPO_DIR, 'addon.xml'), version)
    bump_version(os.path.join(WIZARD_DIR, 'addon.xml'), version)

    # 2) zip add-ons
    os.makedirs(DOCS, exist_ok=True)
    repo_zip = os.path.join(DOCS, f'repository.chainlabswizard-{version}.zip')
    wiz_zip  = os.path.join(DOCS, f'plugin.program.chainlabswizard-{version}.zip')
    zip_addon(REPO_DIR, repo_zip)
    zip_addon(WIZARD_DIR, wiz_zip)

    # 3) generate addons.xml + md5
    xml_out = os.path.join(DOCS, 'addons.xml')
    md5_out = os.path.join(DOCS, 'addons.xml.md5')
    generate_addons_xml([repo_zip, wiz_zip], xml_out)
    generate_md5(xml_out, md5_out)

    # 4) optional git
    if use_git:
        git_commit_push([xml_out, md5_out, repo_zip, wiz_zip], version)

    print(f"\n✅ Automation complete for version {version}")

if __name__ == '__main__':
    main()