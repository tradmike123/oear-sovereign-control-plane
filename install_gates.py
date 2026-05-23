import os
import shutil
import sys
from pathlib import Path

def install_hooks():
    print("=== OEAR Quality Gate Installer ===")
    
    # Target directory is the .git/hooks of the project hosting this system
    # We look for .git starting from parent directories
    current_dir = Path(os.getcwd())
    git_dir = None
    
    # Search upwards for .git
    temp_dir = current_dir
    while temp_dir != temp_dir.parent:
        if (temp_dir / ".git").exists():
            git_dir = temp_dir / ".git"
            break
        temp_dir = temp_dir.parent
        
    if not git_dir:
        print("ERROR: No .git directory found in parent tree. OEAR Gates require a Git repository.")
        sys.exit(1)
        
    hooks_src = current_dir / "hooks"
    hooks_dst = git_dir / "hooks"
    
    if not hooks_src.exists():
        print(f"ERROR: Source hooks directory not found at {hooks_src}")
        sys.exit(1)
        
    print(f"Installing OEAR Gates into: {hooks_dst.absolute()}")
    
    for hook_file in ["pre-commit", "pre-push"]:
        src_path = hooks_src / hook_file
        dst_path = hooks_dst / hook_file
        
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            # On Linux/MacOS we would need chmod +x, on Windows it's handled by git-bash
            print(f"  [OK] Installed {hook_file}")
        else:
            print(f"  [SKIP] {hook_file} not found in source")

    print("\nGovernance gates successfully active. OEAR is now guarding your commits.")

if __name__ == "__main__":
    install_hooks()
