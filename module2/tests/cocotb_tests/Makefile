# Makefile for Module 2 cocotb tests
# Usage: make SIM=verilator test_simple_register

# Default simulator
SIM ?= verilator

# Python files
PYTHON_FILES = test_simple_register.py test_shift_register.py

# Test to run
TEST ?= test_simple_register

# Cocotb variables
MODULE = $(TEST)
TOPLEVEL = $(shell echo $(TEST) | sed 's/test_//')
COCOTB_REDUCED_LOG_FMT = 1

# Verilog files - select based on test
ifeq ($(TEST),test_simple_register)
VERILOG_SOURCES = ../../dut/registers/simple_register.v
else ifeq ($(TEST),test_shift_register)
VERILOG_SOURCES = ../../dut/registers/shift_register.v
else
VERILOG_SOURCES = ../../dut/registers/simple_register.v ../../dut/registers/shift_register.v
endif
VERILOG_FILES = $(VERILOG_SOURCES)

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

# Helper targets
.PHONY: test_all
test_all:
	$(MAKE) TEST=test_simple_register
	$(MAKE) TEST=test_shift_register

.PHONY: clean
clean::
	rm -rf __pycache__
	rm -rf sim_build
	rm -rf results.xml
	rm -rf *.vcd
	rm -rf *.log

