# Makefile for dma example
# Usage: make SIM=verilator

# Default simulator
SIM ?= verilator

# Python test file
PYTHON_FILES = dma_example.py

# Verilog files (using simple DUT for UVM pattern demonstration)
VERILOG_SOURCES = ../../dut/dma/simple_dma.v
VERILOG_FILES = $(VERILOG_SOURCES)

# Cocotb variables - use COCOTB_TEST_MODULES instead of deprecated MODULE
COCOTB_TEST_MODULES = dma_example
TOPLEVEL = simple_dma
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

