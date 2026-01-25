# Module 0: Installation and Setup

**Goal**: Set up development environment and verify installation

## Overview

This module covers the complete setup of your verification environment, including all required tools and dependencies. By the end of this module, you should have a working environment capable of running pyuvm testbenches.

### Automated Installation Scripts

This project includes automated installation scripts to simplify the setup process. You can use these scripts to install all tools automatically, or install them manually using the instructions in each section.

**Quick Start (All-in-One Installation)**:
```bash
# Make scripts executable (Linux/Mac/WSL)
chmod +x scripts/*.sh

# Install all tools with default settings
./scripts/module0.sh

# Or install with custom options
./scripts/module0.sh --verilator-mode submodule --cocotb-mode pip --pyuvm-mode pip
```

**Individual Tool Installation**:
- Verilator: `./scripts/install_verilator.sh [--from-submodule|--system|--source]`
- cocotb: `./scripts/install_cocotb.sh [--pip|--from-submodule] [--venv DIR]`
- pyuvm: `./scripts/install_pyuvm.sh [--pip|--from-submodule] [--venv DIR]`

**Uninstallation**:
- Uninstall all: Use individual uninstall scripts or remove tools manually
- Verilator: `./scripts/uninstall_verilator.sh [--system] [--keep-submodule]`
- cocotb: `./scripts/uninstall_cocotb.sh [--venv DIR] [--keep-submodule]`
- pyuvm: `./scripts/uninstall_pyuvm.sh [--venv DIR] [--keep-submodule]`

For detailed usage of each script, see the corresponding installation sections below.

## Topics Covered

### 1. System Requirements and Prerequisites

- **Operating System Support**
  - Linux (Ubuntu/Debian, CentOS/RHEL, Fedora)
  - macOS (Intel and Apple Silicon)
  - Windows (WSL2 recommended)
  
- **Hardware Requirements**
  - Minimum 4GB RAM (8GB+ recommended)
  - 10GB free disk space
  - Multi-core processor recommended

- **Software Prerequisites**
  - Python 3.8+ (3.10+ recommended)
  - Git
  - C/C++ compiler (GCC, Clang, or MSVC)
  - Make or Ninja build system

### 2. Python Environment Setup

- **Python Installation**
  - Installing Python 3.10+ on Linux
  - Installing Python 3.10+ on macOS
  - Installing Python 3.10+ on Windows/WSL2
  - Verifying Python installation

- **Virtual Environment Management**
  - Using `venv` (Python built-in)
  - Using `conda` (Anaconda/Miniconda)
  - Using `uv` or `rye` (modern Python package managers)
  - Best practices for virtual environments

- **Package Management**
  - pip basics
  - requirements.txt management
  - Dependency resolution

### 3. Verilator Installation

- **What is Verilator?**
  - Open-source Verilog/SystemVerilog simulator
  - Fast compilation and simulation
  - Integration with cocotb

- **Automated Installation (Recommended)**
  - **Using the installation script**:
    ```bash
    # Install from git submodule (default - builds from source)
    ./scripts/install_verilator.sh --from-submodule
    
    # Install from system package manager
    ./scripts/install_verilator.sh --system
    
    # Build from source (clones if submodule doesn't exist)
    ./scripts/install_verilator.sh --source
    ```
  - The script automatically:
    - Checks for existing installations
    - Installs system dependencies (build tools, libraries)
    - Sets up git submodule in `tools/verilator/`
    - Builds and installs Verilator
    - Verifies the installation

- **Manual Installation Methods**
  - **Linux Installation**
    - Ubuntu/Debian: `sudo apt-get install verilator`
    - CentOS/RHEL: `sudo yum install verilator` or `sudo dnf install verilator`
    - Fedora: `sudo dnf install verilator`
    - Building from source (latest features)
  
  - **macOS Installation**
    - Homebrew installation: `brew install verilator`
    - MacPorts installation (alternative)
    - Building from source
  
  - **Windows/WSL2 Installation**
    - Installing in WSL2 Ubuntu: `sudo apt-get install verilator`
    - Building from source in WSL2
    - Verifying installation

- **Uninstallation**
  ```bash
  # Uninstall and remove submodule
  ./scripts/uninstall_verilator.sh
  
  # Uninstall but keep git submodule
  ./scripts/uninstall_verilator.sh --keep-submodule
  
  # Also uninstall system package (if installed via package manager)
  ./scripts/uninstall_verilator.sh --system
  ```

- **Verification Steps**
  - Check Verilator version: `verilator --version`
  - Run simple Verilator test
  - Verify compilation works

### 4. cocotb Installation and Verification

- **What is cocotb?**
  - Coroutine-based testbench framework
  - Python testbenches for hardware
  - Simulator abstraction layer

- **Automated Installation (Recommended)**
  - **Using the installation script**:
    ```bash
    # Install via pip in virtual environment (default)
    ./scripts/install_cocotb.sh --pip --venv .venv
    
    # Install from git submodule (development/editable mode)
    ./scripts/install_cocotb.sh --from-submodule --editable --venv .venv
    
    # Install in system Python (not recommended)
    ./scripts/install_cocotb.sh --pip --no-venv
    ```
  - The script automatically:
    - Creates/uses virtual environment (default: `.venv`)
    - Sets up git submodule in `tools/cocotb/` (if using submodule mode)
    - Installs dependencies
    - Installs cocotb (via pip or from source)
    - Verifies the installation

- **Manual Installation Methods**
  - **pip installation (recommended)**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install cocotb
    ```
  - Development installation from source
  - Version pinning for stability: `pip install cocotb==2.0.0`

- **Uninstallation**
  ```bash
  # Uninstall from virtual environment (default)
  ./scripts/uninstall_cocotb.sh --venv .venv
  
  # Uninstall from system Python
  ./scripts/uninstall_cocotb.sh --no-venv
  
  # Keep git submodule
  ./scripts/uninstall_cocotb.sh --keep-submodule
  ```

- **Simulator Configuration**
  - Verilator configuration
  - Icarus Verilog configuration (alternative)
  - ModelSim/QuestaSim configuration (if available)
  - GHDL configuration (VHDL support)

- **Environment Variables**
  - `COCOTB_REDUCED_LOG_FMT`
  - `MODULE` and `TESTCASE`
  - `SIM` variable for simulator selection

- **Verification Steps**
  - Import cocotb successfully: `python3 -c "import cocotb; print(cocotb.__version__)"`
  - Run simple cocotb test
  - Verify simulator integration

### 5. pyuvm Installation and Verification

- **What is pyuvm?**
  - Python implementation of UVM 1.2
  - Works with cocotb
  - Full UVM methodology support

- **Automated Installation (Recommended)**
  - **Using the installation script**:
    ```bash
    # Install via pip in virtual environment (default)
    ./scripts/install_pyuvm.sh --pip --venv .venv
    
    # Install from git submodule (development/editable mode)
    ./scripts/install_pyuvm.sh --from-submodule --editable --venv .venv
    
    # Install in system Python (not recommended)
    ./scripts/install_pyuvm.sh --pip --no-venv
    ```
  - The script automatically:
    - Creates/uses virtual environment (default: `.venv`)
    - Sets up git submodule in `tools/pyuvm/` (if using submodule mode)
    - Installs dependencies
    - Installs pyuvm (via pip or from source)
    - Verifies the installation

- **Manual Installation Methods**
  - **pip installation**:
    ```bash
    source .venv/bin/activate  # Activate virtual environment
    pip install pyuvm
    ```
  - Installation from source (development)
  - Version selection and compatibility: `pip install pyuvm==2.9.0`

- **Uninstallation**
  ```bash
  # Uninstall from virtual environment (default)
  ./scripts/uninstall_pyuvm.sh --venv .venv
    
  # Uninstall from system Python
  ./scripts/uninstall_pyuvm.sh --no-venv
    
  # Keep git submodule
  ./scripts/uninstall_pyuvm.sh --keep-submodule
  ```

- **Dependencies**
  - Understanding pyuvm dependencies
  - Resolving dependency conflicts
  - Updating pyuvm

- **Verification Steps**
  - Import pyuvm successfully: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
  - Check pyuvm version
  - Run simple pyuvm test
  - Verify UVM classes available

### 6. IDE Setup and Configuration

- **Recommended IDEs**
  - VS Code with Python extension
  - PyCharm (Community or Professional)
  - Vim/Neovim with LSP
  - Emacs with Python support

- **VS Code Configuration**
  - Python extension setup
  - Pylance/Pyright configuration
  - Debugging configuration
  - Task runner setup for simulations
  - Extension recommendations

- **PyCharm Configuration**
  - Python interpreter setup
  - Virtual environment configuration
  - Run configurations for tests
  - Debugging setup

- **Editor Configuration**
  - Python formatting (Black, Ruff)
  - Linting (pylint, flake8, ruff)
  - Type checking (mypy, pyright)
  - Code formatting on save

### 7. Project Structure Setup

- **Directory Structure**
  - Source code organization
  - Test directory structure
  - DUT (Design Under Test) organization
  - Configuration files
  - `tools/` directory for git submodules (Verilator, cocotb, pyuvm)

- **Git Submodules Management**
  - Tools are managed as git submodules in the `tools/` directory
  - Initialize submodules: `./scripts/init_submodules.sh` or `git submodule update --init --recursive`
  - Update submodules: `./scripts/update_submodules.sh` or `git submodule update --remote`
  - Add new submodule: `./scripts/add_submodule.sh <repo_url> <path>`
  - Remove submodule: `./scripts/remove_submodule.sh <path>`

- **Makefile/Configuration**
  - Simple Makefile for running tests
  - pytest configuration
  - cocotb Makefile setup
  - Environment variable management

- **Version Control**
  - Git initialization
  - .gitignore for Python and simulation (include `.venv/`, `__pycache__/`, build artifacts)
  - Initial commit structure
  - Git submodules in `.gitmodules` file

### 8. First "Hello World" Verification Test

- **Prerequisites**
  - Ensure all tools are installed: `./scripts/module0.sh --verify-only`
  - Activate virtual environment: `source .venv/bin/activate` (if using venv)
  - Verify tools are accessible

- **Simple DUT Creation**
  - Basic Verilog module (e.g., AND gate)
  - Simple testbench structure

- **cocotb Test**
  - Basic cocotb test structure
  - Clock generation
  - Signal driving and reading
  - Running the test (requires Verilator and cocotb to be installed)

- **pyuvm Test**
  - First UVM test class
  - Basic UVM phases
  - Running pyuvm test (requires cocotb and pyuvm to be installed)
  - Understanding output

### 9. Troubleshooting Common Issues

- **Python Issues**
  - Python version conflicts
  - Virtual environment activation problems
  - Package installation failures

- **Verilator Issues**
  - Compilation errors
  - Missing dependencies
  - Version compatibility
  - Path issues

- **cocotb Issues**
  - Simulator not found
  - Import errors
  - Environment variable problems
  - Module loading issues

- **pyuvm Issues**
  - Import errors
  - Version compatibility
  - Dependency conflicts

- **IDE Issues**
  - Python interpreter not found
  - Import resolution problems
  - Debugging not working

### 10. Verification Checklist

- [ ] Python 3.10+ installed and working
- [ ] Virtual environment created and activated (or use `./scripts/module0.sh` which creates it automatically)
- [ ] Verilator installed and verified
  - Using script: `./scripts/install_verilator.sh --from-submodule`
  - Verify: `verilator --version`
- [ ] cocotb installed and verified
  - Using script: `./scripts/install_cocotb.sh --pip --venv .venv`
  - Verify: `python3 -c "import cocotb; print(cocotb.__version__)"`
- [ ] pyuvm installed and verified
  - Using script: `./scripts/install_pyuvm.sh --pip --venv .venv`
  - Verify: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
- [ ] All tools verified together: `./scripts/module0.sh --verify-only`
- [ ] IDE configured and working
- [ ] First test runs successfully
- [ ] Can create and run simple testbench
- [ ] Understand basic project structure
- [ ] Know how to get help when stuck

## Learning Outcomes

By the end of this module, you should be able to:

- Install and configure all required tools
- Set up a Python virtual environment
- Install and verify Verilator
- Install and verify cocotb
- Install and verify pyuvm
- Configure your IDE for verification work
- Create a basic project structure
- Run a simple verification test
- Troubleshoot common installation issues

## Exercises

1. **Installation Verification**
   - Use `./scripts/module0.sh --verify-only` to check all installations
   - Or verify each tool independently:
     - Verilator: `verilator --version`
     - cocotb: `python3 -c "import cocotb; print(cocotb.__version__)"`
     - pyuvm: `python3 -c "import pyuvm; print(pyuvm.__version__)"`
   - Document any issues encountered

2. **Environment Setup**
   - Option A (Automated): Run `./scripts/module0.sh` to install everything
   - Option B (Manual):
     - Create a virtual environment: `python3 -m venv .venv`
     - Activate it: `source .venv/bin/activate`
     - Install tools individually using the scripts or manually
   - Create a requirements.txt file with installed packages:
     ```bash
     source .venv/bin/activate
     pip freeze > requirements.txt
     ```

3. **First Test**
   - Create a simple Verilog module
   - Write a cocotb test for it
   - Run the test successfully

4. **IDE Configuration**
   - Set up your preferred IDE
   - Configure Python interpreter to use `.venv/bin/python`
   - Test debugging functionality

5. **Project Structure**
   - Create a well-organized project structure
   - Set up version control (git submodules for tools are already managed)
   - Create initial documentation
   - Understand the `tools/` directory structure (git submodules)

## Assessment

- [ ] Can install all required tools independently
- [ ] Can set up Python virtual environment
- [ ] Can verify Verilator installation
- [ ] Can verify cocotb installation
- [ ] Can verify pyuvm installation
- [ ] Can configure IDE for verification work
- [ ] Can create and run a simple test
- [ ] Can troubleshoot common issues
- [ ] Understands project structure best practices

## Next Steps

After completing this module, proceed to [Module 1: Python and Verification Basics](MODULE1.md) to learn the fundamental concepts needed for verification.

## Additional Resources

- **Installation Scripts**:
  - All scripts are located in the `scripts/` directory
  - Run `./scripts/module0.sh --help` for detailed usage
  - Individual script help: `./scripts/install_<tool>.sh --help`
  
- **Verilator Documentation**: https://verilator.org/
- **cocotb Installation Guide**: https://docs.cocotb.org/en/stable/install.html
- **pyuvm Installation Guide**: https://pyuvm.readthedocs.io/en/latest/installation.html
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html
- **Git Submodules**: https://git-scm.com/book/en/v2/Git-Tools-Submodules

