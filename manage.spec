# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("yt_front_end/templates/home.html","yt_front_end/templates"),
        ("yt_front_end/templates/base.html","yt_front_end/templates"),
        ("yt_front_end/static/js/app.js","yt_front_end/static/js"),
        ("yt_front_end/static/ytlogo.ico","yt_front_end/static"),
        ("venv/Lib/site-packages/stable_baselines3/version.txt","stable_baselines3"),
        ("yawning_titan/config/_package_data/logging_config.yaml","yawning_titan/config/_package_data"),
        ("yawning_titan/config/_package_data/game_modes/default_game_mode.yaml","yawning_titan/config/_package_data/game_modes"),
        ("yawning_titan/config/_package_data/game_modes/low_skill_red_with_random_infection_perfect_detection.yaml","yawning_titan/config/_package_data/game_modes")
    ],
    hiddenimports=[],
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
    name='yawning_titan',
    icon='yt_front_end/static/ytlogo.ico',
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
    name='manage',
)
