# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("yawning_titan_gui/templates","yawning_titan_gui/templates"),
        ("yawning_titan_gui/static","yawning_titan_gui/static"),
        ("yawning_titan/game_modes/_package_data/game_modes.json","yawning_titan/game_modes/_package_data"),
        ("yawning_titan/networks/_package_data/network.json","yawning_titan/networks/_package_data"),
        ("yawning_titan/config/_package_data/logging_config.yaml","yawning_titan/config/_package_data"),
        ("VERSION","data"),
        ("yawning_titan_gui/management/commands","django/core/management/commands"),
        (".venv/Lib/site-packages/stable_baselines3/version.txt","stable_baselines3")
    ],
    hiddenimports=['flaskwebgui'],
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
    [],
    exclude_binaries=True,
    name='YAWNING-TITAN',
    icon='yawning_titan_gui/static/lib/ytlogo.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='yawning_titan',
)
