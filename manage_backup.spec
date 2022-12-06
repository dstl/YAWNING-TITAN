# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("yawning_titan_gui/templates/base.html","yawning_titan_gui/templates"),
        ("yawning_titan_gui/templates/home.html","yawning_titan_gui/templates"),
        ("yawning_titan_gui/templates/docs.html","yawning_titan_gui/templates"),
        ("yawning_titan_gui/templates/game_modes.html","yawning_titan_gui/templates"),
        ("yawning_titan_gui/templates/game_mode_config.html","yawning_titan_gui/templates"),
        ("yawning_titan_gui/templates/elements/el_dialogue_center.html","yawning_titan_gui/templates/elements"),
        ("yawning_titan_gui/templates/elements/el_game_mode.html","yawning_titan_gui/templates/elements"),
        ("yawning_titan_gui/static/ytlogo.ico","yawning_titan_gui/static"),
        ("yawning_titan_gui/static/js/app.js","yawning_titan_gui/static/js"),
        ("yawning_titan_gui/static/js/game_mode.js","yawning_titan_gui/static/js"),
        ("yawning_titan_gui/static/js/game_mode_config.js","yawning_titan_gui/static/js"),
        ("yawning_titan_gui/static/lib/bootstrap-icons.css","yawning_titan_gui/static/lib"),
        ("yawning_titan_gui/static/lib/bootstrap-icons.woff","yawning_titan_gui/static/lib"),
        ("yawning_titan_gui/static/lib/bootstrap-icons.woff2","yawning_titan_gui/static/lib"),
        ("yawning_titan_gui/static/lib/bootstrap.bundle.min.js","yawning_titan_gui/static/lib"),
        ("yawning_titan_gui/static/lib/bootstrap.min.css","yawning_titan_gui/static/lib"),
        ("yawning_titan_gui/static/lib/jquery.js","yawning_titan_gui/static/lib"),
        (".venv/Lib/site-packages/stable_baselines3-1.6.2-py3.9.egg/stable_baselines3/version.txt","stable_baselines3"),
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
    icon='yawning_titan_gui/static/ytlogo.ico',
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
