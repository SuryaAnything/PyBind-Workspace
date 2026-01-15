import os
import re
import config
import parser

def scan_workspace():
    src_path = config.get_src_path()
    library_registry = {}

    print(f"[Scanner] analyzing {config.SRC_DIR_NAME}...")

    if not os.path.exists(src_path):
        return {}

    for filename in os.listdir(src_path):
        if not filename.endswith(".cpp"): continue
        
        filepath = os.path.join(src_path, filename)
        with open(filepath, "r") as f:
            content = f.read()

        matches = re.findall(r'extern_py_lib\s*\((.*?)\)', content, re.DOTALL)
        
        for match_str in matches:
            parts = [p.strip() for p in match_str.split(',') if p.strip()]
            if len(parts) < 2: continue

            lib_name = parts[0]
            class_names = parts[1:]

            if lib_name not in library_registry:
                library_registry[lib_name] = []

            for cls in class_names:
                print(f"  -> Found Target: {cls} (Lib: {lib_name}) in {filename}")
                
                # [CHANGED] Now returns a dict with 'constructors' and 'methods'
                cls_data = parser.extract_methods(content, cls)
                
                library_registry[lib_name].append({
                    "class_name": cls,
                    "file": filename,
                    "data": cls_data # Store the whole dict
                })
    
    return library_registry