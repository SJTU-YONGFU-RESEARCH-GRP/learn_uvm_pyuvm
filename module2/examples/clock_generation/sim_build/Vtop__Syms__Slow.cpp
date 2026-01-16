// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup top module instance
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(250);
    // Setup sub module instances
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscopep_TOP = new VerilatedScope{this, "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER};
    __Vscopep_simple_register = new VerilatedScope{this, "simple_register", "simple_register", "simple_register", -9, VerilatedScope::SCOPE_MODULE};
    // Set up scope hierarchy
    __Vhier.add(0, __Vscopep_simple_register);
    // Setup export functions - final: 0
    // Setup export functions - final: 1
    // Setup public variables
    __Vscopep_TOP->varInsert("clk", &(TOP.clk), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("d", &(TOP.d), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 1 ,7,0);
    __Vscopep_TOP->varInsert("enable", &(TOP.enable), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_TOP->varInsert("q", &(TOP.q), false, VLVT_UINT8, VLVD_OUT|VLVF_PUB_RW, 0, 1 ,7,0);
    __Vscopep_TOP->varInsert("rst_n", &(TOP.rst_n), false, VLVT_UINT8, VLVD_IN|VLVF_PUB_RW, 0, 0);
    __Vscopep_simple_register->varInsert("clk", &(TOP.simple_register__DOT__clk), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_simple_register->varInsert("d", &(TOP.simple_register__DOT__d), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,7,0);
    __Vscopep_simple_register->varInsert("enable", &(TOP.simple_register__DOT__enable), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
    __Vscopep_simple_register->varInsert("q", &(TOP.simple_register__DOT__q), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 1 ,7,0);
    __Vscopep_simple_register->varInsert("rst_n", &(TOP.simple_register__DOT__rst_n), false, VLVT_UINT8, VLVD_NODIR|VLVF_PUB_RW, 0, 0);
}

Vtop__Syms::~Vtop__Syms() {
    // Tear down scope hierarchy
    __Vhier.remove(0, __Vscopep_simple_register);
    // Clear keys from hierarchy map after values have been removed
    __Vhier.clear();
    // Tear down scopes
    VL_DO_CLEAR(delete __Vscopep_TOP, __Vscopep_TOP = nullptr);
    VL_DO_CLEAR(delete __Vscopep_simple_register, __Vscopep_simple_register = nullptr);
    // Tear down sub module instances
}
