#!/bin/bash

# --- CONFIGURATION ---
# Define colors for professional output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper for logging with timestamp
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Ensure we are in project root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
pushd "$PROJECT_ROOT" > /dev/null

VENV_DIR=".venv"

# --- 1. SYSTEM CHECK ---
if [ ! -d "$VENV_DIR" ]; then
    log "Initializing Workspace Environment..."
    python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

# Check dependencies quietly
pip install toml pybind11 setuptools wheel --disable-pip-version-check --quiet

# --- 2. PIPELINE LOGIC ---

if [ "$1" == "--gen-bindings" ]; then
    log ">>> [Target: GENERATOR ONLY]"
    python3 Generators/assembler.py

elif [ "$1" == "--shared-lib" ]; then
    log ">>> [Target: SHARED LIBRARY]"
    
    # STEP 1: GENERATE
    log "Step 1/2: Fabricating C++ Bindings..."
    python3 Generators/assembler.py
    
    # Check if generator succeeded
    if [ $? -ne 0 ]; then
        error "Generation failed. Aborting build."
    fi
    
    # STEP 2: COMPILE
    log "Step 2/2: Compiling Engines..."
    mkdir -p Engines
    python3 Builders/builder.py
    
    # Check if builder succeeded
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}>>> BUILD SUCCESSFUL. Engines are online.${NC}"
    else
        error "Build failed."
    fi
    
else
    echo ">>> [Error] Invalid Argument."
    echo "    Usage:"
    echo "      ./run.sh --shared-lib    (Generate + Compile for local dev)"
    echo "      ./run.sh --gen-bindings  (Generate C++ bindings only)"
    popd > /dev/null
    exit 1
fi

popd > /dev/null