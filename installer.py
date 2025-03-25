import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import json
import shutil
from pathlib import Path
from datetime import datetime

class VintlyInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Vintly Installer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Welcome message
        self.welcome_label = tk.Label(
            self.main_frame,
            text="Welcome to Vintly Installer",
            font=("Helvetica", 16, "bold")
        )
        self.welcome_label.pack(pady=(0, 20))
        
        # Installation directory selection
        self.dir_frame = tk.Frame(self.main_frame)
        self.dir_frame.pack(fill='x', pady=10)
        
        self.dir_label = tk.Label(
            self.dir_frame,
            text="Installation Directory:",
            font=("Helvetica", 10)
        )
        self.dir_label.pack(anchor='w')
        
        self.dir_entry = tk.Entry(self.dir_frame)
        self.dir_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.browse_button = tk.Button(
            self.dir_frame,
            text="Browse",
            command=self.browse_directory
        )
        self.browse_button.pack(side='right')
        
        # API Key input
        self.api_frame = tk.Frame(self.main_frame)
        self.api_frame.pack(fill='x', pady=10)
        
        self.api_label = tk.Label(
            self.api_frame,
            text="Google API Key:",
            font=("Helvetica", 10)
        )
        self.api_label.pack(anchor='w')
        
        self.api_entry = tk.Entry(self.api_frame, show="*")
        self.api_entry.pack(fill='x')
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.main_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill='x', pady=(20, 5))
        
        # Log text widget
        self.log_frame = tk.Frame(self.main_frame)
        self.log_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.log_text = tk.Text(
            self.log_frame,
            height=8,
            width=50,
            font=("Consolas", 9),
            bg='black',
            fg='white'
        )
        self.log_text.pack(side='left', fill='both', expand=True)
        
        # Add scrollbar for logs
        self.scrollbar = ttk.Scrollbar(self.log_frame, orient='vertical', command=self.log_text.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Status label
        self.status_label = tk.Label(
            self.main_frame,
            text="Ready to install",
            font=("Helvetica", 10)
        )
        self.status_label.pack()
        
        # Install button
        self.install_button = tk.Button(
            self.main_frame,
            text="Install",
            command=self.start_installation,
            font=("Helvetica", 12)
        )
        self.install_button.pack(pady=20)
        
        # Set default installation directory
        default_dir = os.path.join(os.path.expanduser("~"), "Vintly")
        self.dir_entry.insert(0, default_dir)
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progress_var.set(progress)
        # Add log message with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] {message}\n")
        self.log_text.see('end')  # Auto-scroll to the bottom
        self.root.update()
    
    def log_error(self, error_message):
        # Add error messages in red
        self.log_text.tag_configure('error', foreground='red')
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert('end', f"[{timestamp}] ERROR: {error_message}\n", 'error')
        self.log_text.see('end')
        self.root.update()
    
    def start_installation(self):
        install_dir = self.dir_entry.get()
        api_key = self.api_entry.get()
        
        if not api_key:
            messagebox.showerror("Error", "Please enter your Google API key")
            return
        
        try:
            # Create installation directory
            os.makedirs(install_dir, exist_ok=True)
            self.update_status("Creating installation directory...", 10)
            
            # Copy program files
            self.update_status("Copying program files...", 20)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            program_files = [
                'app.py',
                'requirements.txt',
                'templates',
                'img',
                'config',
                'templates.json'
            ]
            
            for file in program_files:
                src = os.path.join(current_dir, file)
                dst = os.path.join(install_dir, file)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            
            # Create .env file
            self.update_status("Creating configuration file...", 40)
            env_path = os.path.join(install_dir, '.env')
            with open(env_path, 'w') as f:
                f.write(f"GOOGLE_API_KEY={api_key}")
            
            # Create virtual environment with better error handling
            self.update_status("Setting up Python environment...", 60)
            venv_path = os.path.join(install_dir, '.venv')
            
            try:
                # First, try using the venv module directly
                import venv
                venv.create(venv_path, with_pip=True)
            except Exception as e:
                # If that fails, try using the command line approach
                try:
                    subprocess.run([sys.executable, '-m', 'venv', venv_path], 
                                 check=True, 
                                 capture_output=True,
                                 text=True)
                except subprocess.CalledProcessError as e:
                    error_msg = f"Failed to create virtual environment:\n{e.stdout}\n{e.stderr}"
                    self.log_error(error_msg)
                    messagebox.showerror("Error", error_msg)
                    return
            
            # Install requirements with better error handling
            self.update_status("Installing required packages...", 80)
            if sys.platform == 'win32':
                pip_cmd = os.path.join(venv_path, 'Scripts', 'pip.exe')
            else:
                pip_cmd = os.path.join(venv_path, 'bin', 'pip')
            
            try:
                requirements_path = os.path.join(install_dir, 'requirements.txt')
                result = subprocess.run([pip_cmd, 'install', '-r', requirements_path],
                                     check=True,
                                     capture_output=True,
                                     text=True)
                self.update_status(f"Successfully installed packages", 85)
            except subprocess.CalledProcessError as e:
                error_msg = f"Failed to install requirements:\n{e.stdout}\n{e.stderr}"
                self.log_error(error_msg)
                messagebox.showerror("Error", error_msg)
                return
            
            # Create launcher script
            self.update_status("Creating launcher...", 90)
            launcher_path = os.path.join(install_dir, 'launch_vintly.py')
            with open(launcher_path, 'w') as f:
                f.write('''import os
import subprocess
import webbrowser
import sys
from pathlib import Path

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Activate virtual environment
    if sys.platform == 'win32':
        python_path = script_dir / '.venv' / 'Scripts' / 'python.exe'
    else:
        python_path = script_dir / '.venv' / 'bin' / 'python'
    
    if not python_path.exists():
        print("Error: Virtual environment not found!")
        return
    
    # Run the Flask application
    app_path = script_dir / 'app.py'
    if not app_path.exists():
        print("Error: Application not found!")
        return
    
    # Start the Flask application
    subprocess.Popen([str(python_path), str(app_path)], 
                    cwd=str(script_dir),
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0)
    
    # Wait a moment for the server to start
    import time
    time.sleep(2)
    
    # Open the web browser
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    main()
''')
            
            # Create desktop shortcut
            self.update_status("Creating desktop shortcut...", 95)
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            shortcut_path = os.path.join(desktop_path, "Vintly.lnk")
            
            # Create shortcut using PowerShell
            ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "pythonw"
$Shortcut.Arguments = "{launcher_path}"
$Shortcut.WorkingDirectory = "{install_dir}"
$Shortcut.IconLocation = "{os.path.join(install_dir, 'img', 'vintly-icon.ico')}"
$Shortcut.Save()
'''
            subprocess.run(['powershell', '-Command', ps_script], check=True)
            
            self.update_status("Installation completed successfully!", 100)
            messagebox.showinfo("Success", 
                "Vintly has been installed successfully!\nYou can now launch it from the desktop shortcut.")
            
            # Close installer
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during installation:\n{str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    installer = VintlyInstaller()
    installer.run() 