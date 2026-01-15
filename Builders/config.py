import os
import sysconfig
import pybind11

# Directory constants
SRC_DIR_NAME = "src_cpp"
BINDERS_DIR_NAME = "Binders"
ENGINES_DIR_NAME = "Engines"
BINDING_PREFIX = "bindings_"

# Compiler Settings
COMPILER = "g++"
STD_VERSION = "-std=c++17"
OPTIMIZATION = "-O3"

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_base_flags():
    """Returns the standard compilation flags."""
    return [OPTIMIZATION, "-Wall", "-shared", STD_VERSION, "-fPIC"]

def get_include_paths():
    """Returns the list of include directories required for compilation."""
    root = get_root_dir()
    src_include = os.path.join(root, SRC_DIR_NAME)
    
    paths = [
        sysconfig.get_path("include"),    # Python Headers
        pybind11.get_include(),           # Pybind11 Headers
        src_include                       # User Source Headers
    ]
    return paths

def get_extension_suffix():
    """Returns the OS-specific shared library suffix (e.g., .so, .pyd)."""
    return sysconfig.get_config_var("EXT_SUFFIX") or ".so"