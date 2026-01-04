# Makefile for protocols examples (i2c, spi, uart)
# Usage: make SIM=verilator MODULE=i2c_example
#        make SIM=verilator MODULE=spi_example  
#        make SIM=verilator MODULE=uart_example

# Default simulator
SIM ?= verilator

# Test module to run (must be set)
MODULE ?= i2c_example

# Python test file (based on MODULE)
PYTHON_FILES = $(MODULE).py

# Verilog files (uart uses uart.v, others use simple_dma.v)
ifeq ($(MODULE),uart_example)
    VERILOG_SOURCES = ../../dut/protocols/uart.v
    VERILOG_FILES = $(VERILOG_SOURCES)
    TOPLEVEL = uart
else
    VERILOG_SOURCES = ../../dut/dma/simple_dma.v
    VERILOG_FILES = $(VERILOG_SOURCES)
    TOPLEVEL = simple_dma
endif

# Cocotb variables - use COCOTB_TEST_MODULES instead of deprecated MODULE
COCOTB_TEST_MODULES = $(MODULE)
COCOTB_REDUCED_LOG_FMT = 1

# Include cocotb makefile
include $(shell cocotb-config --makefiles)/Makefile.sim

