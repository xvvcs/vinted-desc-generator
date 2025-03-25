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
        self.root.geometry("700x600")
        self.root.minsize(600, 500)  # Set minimum window size
        
        # Configure grid weight for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frame with padding and configure grid
        self.main_frame = tk.Frame(self.root, padx=25, pady=25)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Welcome message with custom styling
        self.welcome_label = tk.Label(
            self.main_frame,
            text="Welcome to Vintly Installer",
            font=("Helvetica", 24, "bold"),
            pady=20
        )
        self.welcome_label.grid(row=0, column=0, sticky="ew")
        
        # Installation directory frame
        self.dir_frame = tk.LabelFrame(self.main_frame, text="Installation Location", padx=15, pady=10)
        self.dir_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.dir_frame.grid_columnconfigure(0, weight=1)
        
        self.dir_entry = tk.Entry(self.dir_frame)
        self.dir_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_button = tk.Button(
            self.dir_frame,
            text="Browse",
            command=self.browse_directory,
            width=10
        )
        self.browse_button.grid(row=0, column=1)
        
        # API Key frame
        self.api_frame = tk.LabelFrame(self.main_frame, text="Google API Key", padx=15, pady=10)
        self.api_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.api_frame.grid_columnconfigure(0, weight=1)
        
        self.api_entry = tk.Entry(self.api_frame, show="*")
        self.api_entry.grid(row=0, column=0, sticky="ew")
        
        # Progress section
        self.progress_frame = tk.LabelFrame(self.main_frame, text="Installation Progress", padx=15, pady=10)
        self.progress_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(1, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 10))
        
        # Log text widget with custom styling
        self.log_text = tk.Text(
            self.progress_frame,
            height=8,
            width=50,
            font=("Consolas", 9),
            bg='#1E1E1E',
            fg='#D4D4D4',
            padx=5,
            pady=5
        )
        self.log_text.grid(row=1, column=0, sticky="nsew", padx=5)
        
        # Scrollbar for logs
        self.scrollbar = ttk.Scrollbar(self.progress_frame, orient='vertical', command=self.log_text.yview)
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Status label with custom styling
        self.status_label = tk.Label(
            self.progress_frame,
            text="Ready to install",
            font=("Helvetica", 10),
            pady=5
        )
        self.status_label.grid(row=2, column=0, sticky="ew")
        
        # Bottom frame for install button
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        # Install button with custom styling
        self.install_button = tk.Button(
            self.button_frame,
            text="Install",
            command=self.start_installation,
            font=("Helvetica", 12, "bold"),
            bg="#007BFF",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.install_button.grid(row=0, column=0)
        
        # Hover effect for install button
        self.install_button.bind("<Enter>", lambda e: e.widget.configure(bg="#0056b3"))
        self.install_button.bind("<Leave>", lambda e: e.widget.configure(bg="#007BFF"))
        
        # Set default installation directory
        default_dir = os.path.join(os.path.expanduser("~"), "Vintly")
        self.dir_entry.insert(0, default_dir)
        
        # Configure main frame grid weights for proper resizing
        self.main_frame.grid_rowconfigure(3, weight=1)
        
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
        # Disable the install button to prevent multiple clicks
        self.install_button.config(state='disabled')
        
        try:
            install_dir = self.dir_entry.get()
            api_key = self.api_entry.get()
            
            if not api_key:
                messagebox.showerror("Error", "Please enter your Google API key")
                self.install_button.config(state='normal')
                return
            
            # Extract embedded files instead of copying
            self.update_status("Extracting program files...", 20)
            try:
                # Get the base path of the running executable
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.dirname(os.path.abspath(__file__))
                    
                # Copy files from the embedded resources
                for file in ['app.py', 'requirements.txt', 'templates', 'img', 'config', 'templates.json']:
                    src = os.path.join(base_path, file)
                    dst = os.path.join(install_dir, file)
                    if os.path.exists(src):
                        if os.path.isdir(src):
                            shutil.copytree(src, dst, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src, dst)
                    else:
                        raise FileNotFoundError(f"Required file not found: {file}")
                    
            except Exception as e:
                self.log_error(f"Error extracting files: {str(e)}")
                messagebox.showerror("Error", f"Failed to extract program files:\n{str(e)}")
                self.install_button.config(state='normal')
                return
            
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
            self.log_error(f"Installation failed: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during installation:\n{str(e)}")
        finally:
            # Re-enable the install button
            self.install_button.config(state='normal')
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    installer = VintlyInstaller()
    installer.run() 