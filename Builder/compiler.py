import os
import subprocess
import config

def compile_task(source_file, lib_name):
    """
    Compiles a single binding file into a shared object (.so).
    Returns True if successful, False otherwise.
    """
    root = config.get_root_dir()
    engines_dir = os.path.join(root, config.ENGINES_DIR_NAME)
    
    # Ensure Engines dir exists (Self-Healing)
    if not os.path.exists(engines_dir):
        os.makedirs(engines_dir)

    # 1. Prepare Output Path
    output_filename = f"{lib_name}{config.get_extension_suffix()}"
    output_path = os.path.join(engines_dir, output_filename)

    # 2. Construct Command
    cmd = [config.COMPILER]
    
    # Flags
    cmd += config.get_base_flags()
    
    # Includes (-I)
    for inc in config.get_include_paths():
        cmd.append(f"-I{inc}")
    
    # Source Input
    cmd.append(source_file)
    
    # Output (-o)
    cmd.append("-o")
    cmd.append(output_path)
    
    # Linker Libraries (Must go last)
    cmd += config.get_libs()

    # 3. Execute
    # We strip the full path for cleaner logging
    short_src = os.path.basename(source_file)
    print(f"[CXX] Building Target: {lib_name} ({short_src})")
    
    try:
        subprocess.check_call(cmd)
        print(f"  -> [LNK] Linked: {output_filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  -> [ERR] Failed {lib_name} (Exit Code: {e.returncode})")
        return False