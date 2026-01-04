# Learn UVM with pyuvm

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![UVM](https://img.shields.io/badge/UVM-1.2-orange.svg)](https://www.accellera.org/)
[![pyuvm](https://img.shields.io/badge/pyuvm-Latest-green.svg)](https://pyuvm.readthedocs.io/)
[![cocotb](https://img.shields.io/badge/cocotb-Latest-blue.svg)](https://docs.cocotb.org/)
[![Verilator](https://img.shields.io/badge/Verilator-Latest-red.svg)](https://www.veripool.org/verilator/)

A comprehensive, modular learning path for mastering **UVM (Universal Verification Methodology)** and **pyuvm** (Python UVM implementation) with progressive complexity levels. This project provides a complete educational resource with examples, testbenches, and documentation covering all aspects of UVM verification.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Modules](#modules)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

This project is a complete educational resource for learning UVM verification methodology using pyuvm, a Python implementation of UVM 1.2. It provides:

- **8 Progressive Modules**: From Python basics to real-world applications
- **Comprehensive Examples**: Over 50+ working examples with detailed explanations
- **Complete Testbenches**: cocotb and pyuvm testbenches for each module
- **Automated Scripts**: Installation and orchestration scripts for easy setup
- **Full Documentation**: Detailed guides covering all concepts and usage
- **IEEE 1800.2 Coverage**: Complete coverage of the UVM standard

### Why pyuvm?

- **Open Source**: Free and accessible to everyone
- **Python Syntax**: Easier to learn and read than SystemVerilog
- **Full UVM 1.2**: Complete implementation of the IEEE 1800.2 standard
- **Works with Verilator**: Fast, open-source simulation
- **Better Tooling**: Python IDE support, debugging, testing frameworks
- **Modern Development**: Async/await, type hints, comprehensive error handling

## ✨ Features

- ✅ **Complete UVM Coverage**: All 12 sections of IEEE 1800.2 standard
- ✅ **Progressive Learning**: 8 modules from beginner to advanced
- ✅ **Practical Examples**: Real-world verification scenarios
- ✅ **Automated Setup**: One-command installation scripts
- ✅ **Multiple Simulators**: Support for Verilator and other open-source simulators
- ✅ **Virtual Environment Support**: Isolated Python environments
- ✅ **Git Submodules**: Easy tool management
- ✅ **Comprehensive Documentation**: Detailed guides for every concept
- ✅ **Production Quality**: Best practices and industry patterns
- ✅ **Exercises**: Hands-on practice for each module

## 📚 Prerequisites

### Required Knowledge

- **Hardware Description Languages**: Basic understanding of Verilog/SystemVerilog
- **Python Programming**: Intermediate level (classes, decorators, async/await)
- **Digital Design Concepts**: Flip-flops, state machines, buses
- **Verification Basics**: Testbenches, assertions, coverage (helpful but not required)

### System Requirements

- **Operating System**: Linux, macOS, or Windows (WSL2 recommended)
- **Python**: 3.10 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended)
- **Disk Space**: ~2GB for tools and dependencies

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd learn_uvm_pyuvm
```

### 2. Install All Tools (Automated)

```bash
# Make scripts executable (Linux/Mac/WSL)
chmod +x scripts/*.sh

# Install all tools with default settings
./scripts/module0.sh
```

### 3. Run Your First Example

```bash
# Run Module 1 examples
./scripts/module1.sh

# Or run specific examples
./scripts/module1.sh --python-basics
./scripts/module1.sh --cocotb-tests
```

### 4. Start Learning

Begin with [Module 0: Installation and Setup](docs/MODULE0.md) and follow the modules sequentially.

## 📁 Project Structure

```
learn_uvm_pyuvm/
├── docs/                      # Comprehensive documentation
│   ├── MODULE0.md            # Installation and setup guide
│   ├── MODULE1.md            # Python and verification basics
│   ├── MODULE2.md            # cocotb fundamentals
│   ├── MODULE3.md            # UVM basics
│   ├── MODULE4.md            # UVM components
│   ├── MODULE5.md            # Advanced UVM concepts
│   ├── MODULE6.md            # Complex testbenches
│   ├── MODULE7.md            # Real-world applications
│   ├── MODULE8.md            # UVM miscellaneous utilities
│   ├── STUDY.md              # Complete study plan
│   ├── PYTHON_VERILOG_INTERACTION.md  # Python-Verilog interaction guide
│   ├── COVERAGE_CHECKLIST.md # Coverage verification
│   ├── IEEE_1800_2_COVERAGE.md # IEEE standard coverage
│   └── GLOSSARY.md           # UVM terminology
│
├── module0/                   # Installation scripts and tools
├── module1/                   # Python basics and verification fundamentals
│   ├── examples/             # Python examples
│   ├── dut/                   # Design Under Test (Verilog)
│   └── tests/                 # Testbenches (cocotb and pyuvm)
├── module2/                   # cocotb fundamentals
├── module3/                   # UVM basics
├── module4/                   # UVM components
├── module5/                   # Advanced UVM concepts
├── module6/                   # Complex testbenches
├── module7/                   # Real-world applications
├── module8/                   # UVM utilities
│
├── scripts/                   # Automation scripts
│   ├── module0.sh            # Install all tools
│   ├── module1.sh            # Run Module 1 examples
│   ├── ...                    # Module orchestrators
│   ├── install_*.sh          # Individual tool installers
│   └── uninstall_*.sh        # Tool uninstallers
│
├── tools/                     # Git submodules for tools
│   ├── verilator/            # Verilator simulator
│   ├── cocotb/               # cocotb framework
│   └── pyuvm/                # pyuvm library
│
└── README.md                  # This file
```

## 📖 Documentation

The `docs/` directory contains comprehensive documentation for the entire learning path:

### Core Documentation

- **[STUDY.md](docs/STUDY.md)**: Complete study plan with learning path, schedule, and resources
- **[PYTHON_VERILOG_INTERACTION.md](docs/PYTHON_VERILOG_INTERACTION.md)**: Detailed guide on Python-Verilog interaction using cocotb

### Module Documentation

Each module has a dedicated guide with examples, exercises, and detailed explanations:

- **[MODULE0.md](docs/MODULE0.md)**: Installation and Setup
  - System requirements, tool installation, environment setup
  - Automated installation scripts usage
  - Verification checklist

- **[MODULE1.md](docs/MODULE1.md)**: Python and Verification Basics
  - Python OOP, decorators, async/await
  - Data structures for verification
  - Error handling and logging
  - Basic testbenches

- **[MODULE2.md](docs/MODULE2.md)**: cocotb Fundamentals
  - Signal access, clock generation, triggers
  - Reset patterns, common verification patterns
  - cocotb testbenches for registers, FIFOs, state machines

- **[MODULE3.md](docs/MODULE3.md)**: UVM Basics
  - UVM class hierarchy, phases, reporting
  - ConfigDB, factory pattern, objections
  - Basic UVM testbenches

- **[MODULE4.md](docs/MODULE4.md)**: UVM Components
  - Drivers, monitors, sequencers, sequences
  - TLM (Transaction-Level Modeling)
  - Scoreboards, agents, complete testbenches

- **[MODULE5.md](docs/MODULE5.md)**: Advanced UVM Concepts
  - Virtual sequences, coverage models
  - Configuration, callbacks, register models
  - Advanced testbench patterns

- **[MODULE6.md](docs/MODULE6.md)**: Complex Testbenches
  - Multi-agent environments, protocol verification
  - Protocol checkers, multi-channel scoreboards
  - System-level testbench architecture

- **[MODULE7.md](docs/MODULE7.md)**: Real-World Applications
  - DMA verification, protocol verification (UART, SPI, I2C)
  - VIP development, best practices
  - System-level verification

- **[MODULE8.md](docs/MODULE8.md)**: UVM Miscellaneous Utilities
  - Command Line Processor, comparators, recorders
  - Pools, queues, string/math/random utilities
  - Utility integration patterns

### Reference Documentation

- **[COVERAGE_CHECKLIST.md](docs/COVERAGE_CHECKLIST.md)**: Verification checklist for all IEEE 1800.2 sections
- **[IEEE_1800_2_COVERAGE.md](docs/IEEE_1800_2_COVERAGE.md)**: Detailed mapping of IEEE standard to modules
- **[GLOSSARY.md](docs/GLOSSARY.md)**: Comprehensive glossary of UVM terms and concepts

## 🎓 Modules

### Module 0: Installation and Setup
**Duration**: 1 week | **Complexity**: Beginner

Set up your verification environment with all required tools:
- Verilator (simulator)
- cocotb (coroutine-based testbench framework)
- pyuvm (Python UVM implementation)

**Quick Start**: `./scripts/module0.sh`

### Module 1: Python and Verification Basics
**Duration**: 2 weeks | **Complexity**: Beginner

Learn Python concepts essential for verification:
- Python OOP (classes, inheritance)
- Decorators and context managers
- Async/await for simulation
- Data structures for verification
- Error handling and logging

**Quick Start**: `./scripts/module1.sh`

### Module 2: cocotb Fundamentals
**Duration**: 2 weeks | **Complexity**: Intermediate

Master cocotb for hardware verification:
- Signal access and manipulation
- Clock generation and triggers
- Reset patterns
- Common verification patterns
- Testbenches for registers, FIFOs, state machines

**Quick Start**: `./scripts/module2.sh`

### Module 3: UVM Basics
**Duration**: 2 weeks | **Complexity**: Intermediate

Introduction to UVM methodology:
- UVM class hierarchy
- Phases (build, connect, run, check, report)
- Reporting and logging
- ConfigDB for configuration
- Factory pattern
- Objections

**Quick Start**: `./scripts/module3.sh`

### Module 4: UVM Components
**Duration**: 3 weeks | **Complexity**: Intermediate-Advanced

Build complete UVM testbenches:
- Drivers, monitors, sequencers
- Sequences and sequence items
- TLM (Transaction-Level Modeling)
- Scoreboards
- Agents and environments

**Quick Start**: `./scripts/module4.sh`

### Module 5: Advanced UVM Concepts
**Duration**: 3 weeks | **Complexity**: Advanced

Advanced UVM features:
- Virtual sequences and sequencers
- Coverage models
- Configuration and callbacks
- Register models
- Multi-channel environments

**Quick Start**: `./scripts/module5.sh`

### Module 6: Complex Testbenches
**Duration**: 3 weeks | **Complexity**: Advanced

Build production-quality testbenches:
- Multi-agent environments
- Protocol verification
- Protocol checkers
- Multi-channel scoreboards
- System-level architecture

**Quick Start**: `./scripts/module6.sh`

### Module 7: Real-World Applications
**Duration**: 3 weeks | **Complexity**: Advanced

Apply UVM to real-world scenarios:
- DMA verification
- Protocol verification (UART, SPI, I2C)
- VIP development
- Best practices and patterns
- System-level verification

**Quick Start**: `./scripts/module7.sh`

### Module 8: UVM Miscellaneous Utilities
**Duration**: 2 weeks | **Complexity**: Intermediate-Advanced

Master UVM utility classes:
- Command Line Processor
- Comparators
- Recorders
- Pools and queues
- String, math, and random utilities

**Quick Start**: `./scripts/module8.sh`

## 🔧 Installation

### Automated Installation (Recommended)

```bash
# Install all tools
./scripts/module0.sh

# Or install with custom options
./scripts/module0.sh --verilator-mode submodule --cocotb-mode pip --pyuvm-mode pip
```

### Individual Tool Installation

```bash
# Verilator
./scripts/install_verilator.sh [--from-submodule|--system|--source]

# cocotb
./scripts/install_cocotb.sh [--pip|--from-submodule] [--venv DIR]

# pyuvm
./scripts/install_pyuvm.sh [--pip|--from-submodule] [--venv DIR]
```

### Manual Installation

See [MODULE0.md](docs/MODULE0.md) for detailed manual installation instructions.

## 💻 Usage

### Running Examples

Each module has an orchestrator script to run examples and tests:

```bash
# Run all examples for a module
./scripts/module1.sh
./scripts/module2.sh
# ... etc

# Run specific examples
./scripts/module1.sh --python-basics --decorators
./scripts/module2.sh --signal-access --clock-generation

# Run tests
./scripts/module1.sh --cocotb-tests --pyuvm-tests
```

### Running Individual Examples

```bash
# Activate virtual environment
source .venv/bin/activate

# Run Python example
cd module1/examples/python_basics
python3 transaction.py

# Run cocotb test
cd module1/tests/cocotb_tests
make SIM=verilator TEST=test_and_gate

# Run pyuvm test
cd module1/tests/pyuvm_tests
make SIM=verilator TEST=test_and_gate_uvm
```

### Using Command-Line Arguments

```bash
# Module 8: CLP example
cd module8/examples/clp
python3 clp_example.py +test_mode=stress +num_transactions=20 +seed=42
```

## 🤝 Contributing

Contributions are welcome! This project follows best practices for educational resources:

1. **Code Quality**: All code follows Python best practices with type hints and docstrings
2. **Documentation**: Comprehensive docstrings and comments
3. **Testing**: Examples are tested and verified
4. **Consistency**: Follow existing patterns and structure

### Contribution Guidelines

- Follow the existing code style and structure
- Add comprehensive docstrings to all functions and classes
- Include type hints for all code
- Update relevant documentation
- Test your changes thoroughly
- Follow the module structure for new examples

## 📄 License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

[![CC BY 4.0](https://i.creativecommons.org/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

### What this means:

- ✅ **You are free to:**
  - Share — copy and redistribute the material in any medium or format
  - Adapt — remix, transform, and build upon the material for any purpose, even commercially

- 📝 **Under the following terms:**
  - **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

### Attribution

When using this material, please include:

```
Based on "Learn UVM with pyuvm" by [Your Name/Organization]
Licensed under CC BY 4.0
https://creativecommons.org/licenses/by/4.0/
```

## 🙏 Acknowledgments

This project is built on the excellent work of:

- **pyuvm**: Python implementation of UVM 1.2 by Ray Salemi
  - Website: https://pyuvm.readthedocs.io/
  - GitHub: https://github.com/pyuvm/pyuvm

- **cocotb**: Coroutine-based testbench framework
  - Website: https://docs.cocotb.org/
  - GitHub: https://github.com/cocotb/cocotb

- **Verilator**: Fast Verilog/SystemVerilog simulator
  - Website: https://www.veripool.org/verilator/
  - GitHub: https://github.com/verilator/verilator

- **UVM**: Universal Verification Methodology
  - Standard: IEEE 1800.2-2020
  - Accellera Systems Initiative

### Educational Resources

- UVM 1.2 User's Guide (Accellera Systems Initiative)
- Verification Academy: https://verificationacademy.com/
- IEEE Design & Test publications
- DVCon proceedings

## 📞 Support

For questions, issues, or contributions:

1. Check the [documentation](docs/) first
2. Review the [GLOSSARY.md](docs/GLOSSARY.md) for terminology
3. Check [COVERAGE_CHECKLIST.md](docs/COVERAGE_CHECKLIST.md) for module coverage
4. Open an issue for bugs or feature requests

## 🎯 Learning Path

Recommended learning path:

1. **Week 1**: Module 0 (Installation)
2. **Weeks 2-3**: Module 1 (Python Basics)
3. **Weeks 4-5**: Module 2 (cocotb)
4. **Weeks 6-7**: Module 3 (UVM Basics)
5. **Weeks 8-10**: Module 4 (UVM Components)
6. **Weeks 11-13**: Module 5 (Advanced UVM)
7. **Weeks 14-16**: Module 6 (Complex Testbenches)
8. **Weeks 17-19**: Module 7 (Real-World Applications)
9. **Weeks 20-21**: Module 8 (Utilities)

**Total Duration**: ~21 weeks (5 months) for complete mastery

## 📊 Project Statistics

- **8 Modules**: Complete learning path
- **50+ Examples**: Working code examples
- **20+ Testbenches**: cocotb and pyuvm testbenches
- **15+ Scripts**: Automation and orchestration
- **13 Documentation Files**: Comprehensive guides
- **100% IEEE 1800.2 Coverage**: All standard sections covered

---

**Happy Learning! 🚀**

Start your UVM journey today with Module 0: [Installation and Setup](docs/MODULE0.md)

