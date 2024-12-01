# -*- mode: python ; coding: utf-8 -*-

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mac", action="store_true")
options = parser.parse_args()


a = Analysis(
    ['wiflip.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['QtSql', 'QtOpenGL', 'QtTextToSpeech', 'PyQt5.QtDesigner'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='wiflip',
    version='version.txt',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False if options.mac else True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images/flipp.icns'] if options.mac else ['C:\\Users\\garzo\\git\\wiflip2\\images\\flipp.ico'],
)
# version mac
if options.mac:
	app = BUNDLE(
	    exe,
	    name='wiflip.app',
	    icon='images/flipp.icns',
	    bundle_identifier=None,
	)
