import sys
import scanner
import compiler
import config

def main():
    print(f"Build System v2.0 initialized.")
    print(f"Root: {config.get_root_dir()}\n")

    # Step 1: Scan
    tasks = scanner.find_binding_files()
    
    if not tasks:
        print("[WRN] No binding files found in Binders/. Run generator first.")
        sys.exit(0)

    print(f"Detected {len(tasks)} build targets.\n")

    # Step 2: Compile
    success_count = 0
    for source, lib_name in tasks:
        if compiler.compile_task(source, lib_name):
            success_count += 1

    # Step 3: Summary
    if success_count == len(tasks):
        print(f"Build Complete. {success_count}/{len(tasks)} engines online.")
    else:
        print(f"Build Finished with Errors. {success_count}/{len(tasks)} targets succeeded.")
        sys.exit(1)

if __name__ == "__main__":
    main()