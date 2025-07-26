# PyInstaller spec file for UtilityPro
import os
import sys
# New import to find PyQt6 plugins path
from PyInstaller.utils.hooks import get_qt_plugins_path

block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    # --- CHANGE HERE ---
    # Manually add the PyQt6 plugins to ensure they are bundled
    datas=[
        ("assets", "assets"),
        (get_qt_plugins_path("PyQt6", "platforms"), "platforms"),
        (get_qt_plugins_path("PyQt6", "styles"), "styles")
    ],
    hiddenimports=[
        "PyQt6",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        "PyPDF2",
        "pdf2docx",
        "PIL",
        "PIL.Image",
        "PIL.ImageFilter"
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib"],
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
    # --- CHANGE HERE ---
    # Removed 'exclude_binaries=True'
    name="UtilityPro",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Use True for debugging startup issues
    icon="assets/icon.png" if os.path.exists("assets/icon.png") else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="UtilityPro",
)

# macOS App Bundle
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="UtilityPro.app",
        icon="assets/icon.png" if os.path.exists("assets/icon.png") else None,
        bundle_identifier="com.viveksrivastava.utilitypro",
    )