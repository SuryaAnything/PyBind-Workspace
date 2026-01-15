import os

# Define Directory Names
SRC_DIR_NAME = "src_cpp"
LINKER_DIR_NAME = "Binders"
BINDING_PREFIX = "bindings_"

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_src_path():
    return os.path.join(get_root_dir(), SRC_DIR_NAME)

def get_linker_path():
    return os.path.join(get_root_dir(), LINKER_DIR_NAME)