import os
import shutil
import sys

def sync_engine():
    # Resolve absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(base_dir, "shared", "engine")
    dst_dir = os.path.join(base_dir, "desktop", "engine")
    
    if not os.path.exists(src_dir):
        print(f"Error: Source directory {src_dir} does not exist.")
        sys.exit(1)
        
    print(f"Syncing engine: {src_dir} -> {dst_dir}")
    
    # Clean up localized directory
    if os.path.exists(dst_dir):
        # We preserve desktop/engine/worker.py because it is a PyQt6 worker class 
        # and doesn't belong in shared conversion engine!
        worker_path = os.path.join(dst_dir, "worker.py")
        has_worker = os.path.exists(worker_path)
        
        # Temp save worker.py
        temp_worker = None
        if has_worker:
            with open(worker_path, "r", encoding="utf-8") as f:
                temp_worker = f.read()
                
        shutil.rmtree(dst_dir)
        os.makedirs(dst_dir, exist_ok=True)
        
        # Re-write worker.py if saved
        if temp_worker:
            with open(worker_path, "w", encoding="utf-8") as f:
                f.write(temp_worker)
    else:
        os.makedirs(dst_dir, exist_ok=True)
        
    # Copy shared files to desktop
    for item in os.listdir(src_dir):
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
            
    print("Engine synchronization completed successfully!")

if __name__ == "__main__":
    sync_engine()
