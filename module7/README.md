# Module 7: Real-World Applications

This directory contains all examples, exercises, and test cases for Module 7.

## Directory Structure

```
module7/
├── examples/              # pyuvm examples for each topic
│   ├── dma/              # DMA verification examples
│   ├── protocols/        # Protocol verification examples (UART, SPI, I2C)
│   ├── vip/              # VIP development examples
│   └── best_practices/   # Best practices examples
├── dut/                   # Verilog Design Under Test modules
│   ├── dma/              # DMA controller
│   └── protocols/        # Protocol modules
├── tests/                 # Testbenches
│   └── pyuvm_tests/      # pyuvm testbenches
└── exercises/            # Exercise solutions
```

## Running Examples

Use the `module7.sh` script to run examples:

```bash
# Run all examples
./scripts/module7.sh

# Run specific examples
./scripts/module7.sh --dma
./scripts/module7.sh --uart
./scripts/module7.sh --spi
./scripts/module7.sh --i2c
./scripts/module7.sh --vip
./scripts/module7.sh --best-practices
./scripts/module7.sh --pyuvm-tests
```

## Topics Covered

1. **DMA Verification** - Complete DMA controller verification
2. **Protocol Verification** - UART, SPI, I2C verification
3. **Best Practices** - Code organization, reusability, documentation
4. **VIP Development** - Creating reusable verification IP
5. **System-Level Verification** - System and SoC verification
6. **Advanced Debugging** - Complex debugging techniques
7. **Test Planning** - Verification strategy and planning
8. **Industry Patterns** - Common verification patterns
9. **Performance Optimization** - Testbench optimization
10. **Coverage Closure** - Coverage strategies and closure

