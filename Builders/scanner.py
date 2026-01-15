import os
import config

def find_binding_files():
    """
    Scans the Binders directory for valid C++ binding files.
    Returns a list of tuples: (full_source_path, library_name)
    """
    root = config.get_root_dir()
    binders_path = os.path.join(root, config.BINDERS_DIR_NAME)
    
    tasks = []

    if not os.path.exists(binders_path):
        print(f"FATAL: Source directory {binders_path} is missing.")
        return []

    for filename in os.listdir(binders_path):
        # We only look for files starting with 'bindings_'
        if not filename.endswith(".cpp") or not filename.startswith(config.BINDING_PREFIX):
            continue

        # Extract 'ws_math' from 'bindings_ws_math.cpp'
        lib_name = filename[len(config.BINDING_PREFIX):-4]
        full_path = os.path.join(binders_path, filename)
        
        tasks.append((full_path, lib_name))
    
    return tasks