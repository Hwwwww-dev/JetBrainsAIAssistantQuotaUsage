# -*- mode: python ; coding: utf-8 -*-
import sys

block_cipher = None

a = Analysis(
    ['JetBrainsAIQuotaAnalyzer_CLI.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'sqlite3',
        'xml.etree.ElementTree',
        'datetime',
        'argparse',
        'platform',
        'socket',
        'signal',
        'traceback',
        'subprocess',
        'time',
        'json',
        'pathlib',
        'os',
        'sys',
        're',
        'glob',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JetBrainsAIQuotaAnalyzer_CLI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  
)

# 如果是macOS，创建一个.app包
if 'darwin' in sys.platform:
    app = BUNDLE(
        exe,
        name='JetBrainsAIQuotaAnalyzer_CLI.app',
        icon=None,  
        bundle_identifier=None,
        info_plist={
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'NSHighResolutionCapable': 'True',
            'NSPrincipalClass': 'NSApplication',
        },
    )
