import os
import datetime
import config

def write_bindings(library_registry):
    linker_path = config.get_linker_path()
    if not os.path.exists(linker_path): os.makedirs(linker_path)

    for lib_name, classes in library_registry.items():
        filename = f"{config.BINDING_PREFIX}{lib_name}.cpp"
        output_file = os.path.join(linker_path, filename)
        print(f"[Emitter] Generating {filename}...")
        
        content = _build_cpp_content(lib_name, classes)
        with open(output_file, "w") as f: f.write(content)

def _build_cpp_content(lib_name, classes):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"// AUTO-GENERATED: {timestamp}",
        "#include <pybind11/pybind11.h>",
    ]
    
    # Includes
    included_files = sorted(list(set(c["file"] for c in classes)))
    for f in included_files:
        lines.append(f'#include "../{config.SRC_DIR_NAME}/{f}"')

    lines.append("\nnamespace py = pybind11;\n")
    lines.append(f"PYBIND11_MODULE({lib_name}, m) {{")
    
    for c in classes:
        cls_name = c["class_name"]
        data = c["data"] # The new struct from parser
        
        lines.append(f'    py::class_<{cls_name}>(m, "{cls_name}")')
        
        # --- NEW: CONSTRUCTOR GENERATION ---
        # If we found constructors, write them. If not, default to init<>()
        if data["constructors"]:
            for args in data["constructors"]:
                # args is a list like ["int", "float"]
                arg_str = ", ".join(args)
                lines.append(f'        .def(py::init<{arg_str}>())')
        else:
            # Fallback: Default Constructor
            lines.append(f'        .def(py::init<>())') 

        # Methods
        for method in data["methods"]:
            m_name = method["name"]
            if method["is_static"]:
                lines.append(f'        .def_static("{m_name}", &{cls_name}::{m_name})')
            else:
                lines.append(f'        .def("{m_name}", &{cls_name}::{m_name})')
        
        lines.append("    ;") 
    
    lines.append("}")
    return "\n".join(lines)