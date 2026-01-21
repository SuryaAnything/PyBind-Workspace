import os
import concurrent.futures
import time
import config
import compiler

def main():
    root = config.get_root_dir()
    binders_dir = os.path.join(root, config.BINDERS_DIR_NAME)
    
    print(f"Build System v2.1 (Parallelized)")
    print(f"Root: {root}")

    # 1. Scan for Binding Files
    # The C++ Generator creates files like 'bindings_mylib.cpp'
    tasks = []
    if os.path.exists(binders_dir):
        for filename in os.listdir(binders_dir):
            if filename.startswith(config.BINDING_PREFIX) and filename.endswith(".cpp"):
                # Extract lib name: "bindings_chaos_lib.cpp" -> "chaos_lib"
                lib_name = filename[len(config.BINDING_PREFIX):-4]
                full_path = os.path.join(binders_dir, filename)
                tasks.append((full_path, lib_name))

    total_tasks = len(tasks)
    print(f"Detected {total_tasks} build targets.\n")
    if total_tasks == 0:
        return

    # 2. Parallel Compilation
    start_time = time.time()
    
    # ProcessPoolExecutor is safer for heavy CPU tasks like compilation
    success_count = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit all tasks
        futures = {executor.submit(compiler.compile_task, t[0], t[1]): t[1] for t in tasks}
        
        for future in concurrent.futures.as_completed(futures):
            lib_name = futures[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as exc:
                print(f"[ERR] {lib_name} generated an exception: {exc}")

    end_time = time.time()
    duration = end_time - start_time

    # 3. Summary
    print(f"\nBuild Finished: {success_count}/{total_tasks} succeeded in {duration:.2f}s")
    
    if success_count < total_tasks:
        exit(1) # Signal failure to run.sh

if __name__ == "__main__":
    main()