# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['IrradInterPy.py'],
    pathex=[],
    binaries=[],
    datas=[("G:\OneDrive - NIST\Documents\BraineCode\IrradInterPy\src\GUI\icons\icon_64.png", ".")],
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

splash = Splash(
    "G:\OneDrive - NIST\Documents\BraineCode\IrradInterPy\src\GUI\splash\splash.png",
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 50),
    text_size=12,
    text_color="black",
    always_on_top=False,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IrradInterPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['G:\\OneDrive - NIST\\Documents\\BraineCode\\IrradInterPy\\src\\GUI\\icons\\icon_64.png'],
)
