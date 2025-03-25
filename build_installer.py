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
    
    # Get the current directory and Python paths
    current_dir = Path(__file__).parent.absolute()
    current_dir_str = str(current_dir).replace('\\', '/')
    python_dir = Path(sys.executable).parent
    
    # Get all required Python DLLs
    python_dlls = []
    for file in python_dir.glob('python*.dll'):
        python_dlls.append((str(file), f'python/{file.name}'))
    
    # Create the spec file
    spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Include all necessary files
added_files = [
    ('app.py', '.'),
    ('requirements.txt', '.'),
    ('templates', 'templates'),
    ('img', 'img'),
    ('config', 'config'),
    ('templates.json', '.'),
    (r'{str(sys.executable)}', 'python/python.exe'),
    (r'{str(python_dir / "Scripts" / "pip.exe")}', 'python/Scripts/pip.exe'),
    (r'{str(python_dir / "Scripts" / "pip3.exe")}', 'python/Scripts/pip3.exe'),
] + {python_dlls}

# Add site-packages
site_packages = [
    'flask',
    'google_generativeai',
    'PIL',
    'requests',
    'python-dotenv'
]

for package in site_packages:
    added_files.append((os.path.join(r'{python_dir}', 'Lib', 'site-packages', package), f'python/Lib/site-packages/{{package}}'))

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
        'python-dotenv',
        'webbrowser',
        'pathlib',
        'json',
        'shutil',
        'subprocess'
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
    console=True,  # Changed to True temporarily for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/vintly-icon.ico',
    onefile=True
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
    ], check=True)
    
    # Clean up
    spec_path.unlink()
    
    print("\nInstaller created successfully!")
    print(f"Location: {current_dir / 'dist' / 'Vintly_Installer.exe'}")

if __name__ == '__main__':
    build_installer() 