import os
import sys
import subprocess
import platform

def create_venv():
    venv_dir = "venv"
    
    # 1. Create Virtual Environment
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    else:
        print(f"Virtual environment already exists in {venv_dir}.")

    # 2. Determine pip executable path based on OS
    if platform.system() == "Windows":
        pip_exe = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_exe = os.path.join(venv_dir, "bin", "pip")

    # 3. Upgrade pip and install requirements
    print("Installing dependencies...")
    subprocess.check_call([pip_exe, "install", "--upgrade", "pip"])
    subprocess.check_call([pip_exe, "install", "-r", "requirements.txt"])
    
    print("\n✅ Setup complete.")
    print("To activate the environment, run:")
    if platform.system() == "Windows":
        print(f"   {venv_dir}\\Scripts\\activate")
    else:
        print(f"   source {venv_dir}/bin/activate")

if __name__ == "__main__":
    create_venv()