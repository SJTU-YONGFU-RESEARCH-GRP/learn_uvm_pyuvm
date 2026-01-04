# Makefile for Module 7 pyuvm tests
# Usage: make SIM=verilator TEST=test_real_world

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_real_world.py

# Verilog files
VERILOG_SOURCES = ../../dut/dma/simple_dma.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Test to run
TEST ?= test_real_world

# Cocotb variables - use COCOTB_TEST_MODULES instead of deprecated MODULE
COCOTB_TEST_MODULES = $(TEST)
TOPLEVEL = simple_dma
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

