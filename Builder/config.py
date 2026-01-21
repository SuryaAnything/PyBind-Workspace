import os
import sysconfig
import pybind11

# Matches what the C++ Overseer expects
SRC_DIR_NAME = "src_cpp"
BINDERS_DIR_NAME = "Binders"
ENGINES_DIR_NAME = "Engines"
BINDING_PREFIX = "bindings_"

COMPILER = "g++"
STD_VERSION = "-std=c++17"
OPTIMIZATION = "-O3"

LIBS = ["-lm", "-lpthread"] 

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_base_flags():
    """Returns the standard high-performance compilation flags."""
    return [OPTIMIZATION, "-Wall", "-shared", STD_VERSION, "-fPIC"]

def get_libs():
    """Returns the external libraries to link against."""
    return LIBS

def get_include_paths():
    """Automatically finds Python, Pybind11, and your Source headers."""
    root = get_root_dir()
    src_include = os.path.join(root, SRC_DIR_NAME)
    
    paths = [
        sysconfig.get_path("include"),    # Python Headers (e.g., Python.h)
        pybind11.get_include(),           # Pybind11 Headers
        src_include                       # Your C++ Headers
    ]
    return paths

def get_extension_suffix():
    """Returns the OS-specific shared lib extension (e.g., .cpython-310-x86_64-linux-gnu.so)."""
    return sysconfig.get_config_var("EXT_SUFFIX") or ".so"