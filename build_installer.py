import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk  # Add this import for the progress bar
from tkinter import filedialog, messagebox

def build_installer():
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    # Convert to string with forward slashes for the spec file
    current_dir_str = str(current_dir).replace('\\', '/')
    
    # Create the spec file
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Include Python runtime and all required packages
added_files = [
    ('app.py', '.'),
    ('requirements.txt', '.'),
    ('templates', 'templates'),
    ('img', 'img'),
    ('config', 'config'),
    ('templates.json', '.'),
    ('{sys.executable}', '.'),  # Include Python interpreter
]

a = Analysis(
    ['installer.py'],
    pathex=[r'{current_dir_str}'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'flask',
        'google.generativeai',
        'PIL',
        'requests',
        'python-dotenv'
    ],
    hookspath=[],
    hooksconfig={{}},
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
    name='Vintly_Installer',
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
    icon='img/vintly-icon.ico',
    onefile=True  # This setting in the spec file controls single-file output
)
'''
    
    # Write the spec file
    spec_path = current_dir / 'installer.spec'
    with open(spec_path, 'w') as f:
        f.write(spec_content)
    
    # Build the installer
    print("Building installer...")
    subprocess.run([
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(spec_path)
    ], check=True)  # Removed the --onefile flag since it's in the spec file
    
    # Clean up
    spec_path.unlink()
    
    print("\nInstaller created successfully!")
    print(f"Location: {current_dir / 'dist' / 'Vintly_Installer.exe'}")

if __name__ == '__main__':
    build_installer() 