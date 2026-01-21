#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd "$PROJECT_ROOT" > /dev/null

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    log "Initializing Workspace Environment..."
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate
pip install toml pybind11 setuptools wheel --disable-pip-version-check --quiet

compile_generator() {
    log "Compiling C++ Overseer (Modular Agents)..."
    
    if [ ! -d "Generator" ]; then error "Generator directory missing!"; fi
    
    # Compile main.cpp AND all files in src/
    # -I Generator/Include adds the header path
    g++ -O3 -std=c++17 -I Generator/Include \
        Generator/Main.cpp \
        Generator/Src/*.cpp \
        -o Generator/overseer
    
    if [ $? -ne 0 ]; then
        error "Failed to compile Overseer."
    fi
}

build_engines() {
    log "Step 1/2: Fabricating C++ Bindings (Native Mode)..."
    if [ ! -f "Generator/overseer" ]; then
        compile_generator
    fi
    
    ./Generator/overseer
    if [ $? -ne 0 ]; then
        error "Generation failed. Aborting build."
    fi
    
    log "Step 2/2: Compiling Engines..."
    mkdir -p Engines
    python3 Builder/builder.py
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}>>> BUILD SUCCESSFUL. Engines are online.${NC}"
    else
        error "Build failed."
    fi
}

if [ "$1" == "--gen-bindings" ]; then
    log ">>> [Target: GENERATOR ONLY]"
    compile_generator
    log "Running Generator..."
    ./Generator/overseer

elif [ "$1" == "--shared-lib" ]; then
    log ">>> [Target: SHARED LIBRARY]"
    compile_generator
    log "Running Generator..."
    ./Generator/overseer
    build_engines
else
    echo ">>> [Error] Invalid Argument."
    echo "    Usage:"
    echo "      ./run.sh --shared-lib    (Generate + Compile for local dev)"
    echo "      ./run.sh --gen-bindings  (Generate C++ bindings only)"
    popd > /dev/null
    exit 1
fi

popd > /dev/null
