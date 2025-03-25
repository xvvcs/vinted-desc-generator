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
        
        # Add a flag to prevent multiple installations
        self.is_installing = False
        
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
        if self.is_installing:
            return
        self.is_installing = True
        self.install_button.config(state='disabled')
        
        try:
            install_dir = self.dir_entry.get()
            api_key = self.api_entry.get()
            
            if not api_key:
                messagebox.showerror("Error", "Please enter your Google API key")
                return
            
            # Get the base path for embedded files
            if getattr(sys, 'frozen', False):
                # Running as compiled executable
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            self.log_text.insert('end', f"Base path: {base_path}\n")
            
            # Create installation directory
            os.makedirs(install_dir, exist_ok=True)
            self.update_status("Creating installation directory...", 10)
            
            # Extract embedded files
            self.update_status("Extracting program files...", 20)
            try:
                files_to_copy = {
                    'app.py': 'file',
                    'requirements.txt': 'file',
                    'templates': 'dir',
                    'img': 'dir',
                    'config': 'dir',
                    'templates.json': 'file'
                }
                
                for file, file_type in files_to_copy.items():
                    src = os.path.join(base_path, file)
                    dst = os.path.join(install_dir, file)
                    self.log_text.insert('end', f"Copying from {src} to {dst}\n")
                    
                    try:
                        if file_type == 'dir':
                            if os.path.exists(dst):
                                shutil.rmtree(dst)
                            shutil.copytree(src, dst)
                        else:
                            shutil.copy2(src, dst)
                        self.log_text.insert('end', f"Successfully copied {file}\n")
                    except FileNotFoundError:
                        self.log_text.insert('end', f"Warning: Could not find {file}\n")
                        # Continue with installation even if some files are missing
                        continue
                    except Exception as e:
                        self.log_text.insert('end', f"Error copying {file}: {str(e)}\n")
                        raise
                
                # Create .env file
                self.update_status("Creating configuration file...", 40)
                env_path = os.path.join(install_dir, '.env')
                with open(env_path, 'w') as f:
                    f.write(f"GOOGLE_API_KEY={api_key}")
                
                # Instead of creating a virtual environment, use the bundled Python
                self.update_status("Setting up Python environment...", 60)
                python_dir = os.path.join(install_dir, 'python')
                os.makedirs(python_dir, exist_ok=True)
                
                # Install packages using bundled pip
                self.update_status("Installing required packages...", 80)
                pip_exe = os.path.join(python_dir, 'Scripts', 'pip.exe')
                requirements_path = os.path.join(install_dir, 'requirements.txt')
                
                try:
                    subprocess.run([pip_exe, 'install', '-r', requirements_path], 
                                 check=True,
                                 capture_output=True,
                                 text=True)
                except subprocess.CalledProcessError as e:
                    self.log_error(f"Failed to install requirements: {e.stdout}\n{e.stderr}")
                    raise
                
                # Update launcher script to use bundled Python
                self.update_status("Creating launcher...", 90)
                launcher_path = os.path.join(install_dir, 'launch_vintly.py')
                with open(launcher_path, 'w') as f:
                    f.write('''import os
import subprocess
import webbrowser
from pathlib import Path

def main():
    script_dir = Path(__file__).parent.absolute()
    python_exe = script_dir / 'python' / 'python.exe'
    app_path = script_dir / 'app.py'
    
    if not python_exe.exists():
        print("Error: Python runtime not found!")
        return
    
    if not app_path.exists():
        print("Error: Application not found!")
        return
    
    # Start the Flask application
    process = subprocess.Popen(
        [str(python_exe), str(app_path)],
        cwd=str(script_dir),
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
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
                self.log_error(f"Error during file extraction: {str(e)}")
                raise
            
        except Exception as e:
            self.log_error(f"Installation failed: {str(e)}")
            messagebox.showerror("Error", f"An error occurred during installation:\n{str(e)}")
        finally:
            self.is_installing = False
            self.install_button.config(state='normal')
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    installer = VintlyInstaller()
    installer.run() 