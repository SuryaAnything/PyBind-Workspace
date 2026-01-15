import os
import subprocess
import config

def compile_task(source_file, lib_name):
    """
    Compiles a single binding file into a shared object engine.
    """
    root = config.get_root_dir()
    engines_dir = os.path.join(root, config.ENGINES_DIR_NAME)
    
    # Ensure Engines dir exists
    if not os.path.exists(engines_dir):
        os.makedirs(engines_dir)

    # Prepare Output Path
    output_filename = f"{lib_name}{config.get_extension_suffix()}"
    output_path = os.path.join(engines_dir, output_filename)

    # 1. Build Command
    cmd = [config.COMPILER]
    cmd += config.get_base_flags()
    
    # Add Includes
    includes = config.get_include_paths()
    for inc in includes:
        cmd.append(f"-I{inc}")
    
    cmd.append(source_file)
    cmd.append("-o")
    cmd.append(output_path)

    # 2. Technical Logging
    print(f"[CXX] Target: {lib_name}")
    print(f"      Input:  {os.path.basename(source_file)}")
    print(f"      Output: {os.path.basename(output_path)}")
    print(f"      Flags:  {' '.join(config.get_base_flags())}")
    print(f"      Inc:    {[os.path.basename(p) for p in includes]}")

    # 3. Execution
    try:
        subprocess.check_call(cmd)
        print(f"[LNK] Linking successful: {output_filename}")
        print("") # Empty line for spacing between tasks
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERR] Compilation failed with exit code {e.returncode}")
        return False