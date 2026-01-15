import scanner
import emitter

def main():
    print(">>> [Generator] Starting Sequence...")
    registry = scanner.scan_workspace()
    emitter.write_bindings(registry)
    print(">>> [Generator] Sequence Complete.")

if __name__ == "__main__":
    main()