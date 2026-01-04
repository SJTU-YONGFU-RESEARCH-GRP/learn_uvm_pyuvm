// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_axi4_lite_slave);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(49);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_axi4_lite_slave.configure(this, name(), "axi4_lite_slave", "axi4_lite_slave", "axi4_lite_slave", -9, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_axi4_lite_slave);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"ACLK", &(TOP.ACLK), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"ARADDR", &(TOP.ARADDR), false, VLVT_UINT32,VLVD_IN|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_TOP.varInsert(__Vfinal,"ARESETn", &(TOP.ARESETn), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"ARPROT", &(TOP.ARPROT), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"ARREADY", &(TOP.ARREADY), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"ARVALID", &(TOP.ARVALID), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"AWADDR", &(TOP.AWADDR), false, VLVT_UINT32,VLVD_IN|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_TOP.varInsert(__Vfinal,"AWPROT", &(TOP.AWPROT), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_TOP.varInsert(__Vfinal,"AWREADY", &(TOP.AWREADY), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"AWVALID", &(TOP.AWVALID), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"BREADY", &(TOP.BREADY), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"BRESP", &(TOP.BRESP), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_TOP.varInsert(__Vfinal,"BVALID", &(TOP.BVALID), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"RDATA", &(TOP.RDATA), false, VLVT_UINT32,VLVD_OUT|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_TOP.varInsert(__Vfinal,"RREADY", &(TOP.RREADY), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"RRESP", &(TOP.RRESP), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_TOP.varInsert(__Vfinal,"RVALID", &(TOP.RVALID), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"WDATA", &(TOP.WDATA), false, VLVT_UINT32,VLVD_IN|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_TOP.varInsert(__Vfinal,"WREADY", &(TOP.WREADY), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"WSTRB", &(TOP.WSTRB), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_TOP.varInsert(__Vfinal,"WVALID", &(TOP.WVALID), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ACLK", &(TOP.axi4_lite_slave__DOT__ACLK), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ARADDR", &(TOP.axi4_lite_slave__DOT__ARADDR), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ARESETn", &(TOP.axi4_lite_slave__DOT__ARESETn), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ARPROT", &(TOP.axi4_lite_slave__DOT__ARPROT), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ARREADY", &(TOP.axi4_lite_slave__DOT__ARREADY), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"ARVALID", &(TOP.axi4_lite_slave__DOT__ARVALID), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"AWADDR", &(TOP.axi4_lite_slave__DOT__AWADDR), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"AWPROT", &(TOP.axi4_lite_slave__DOT__AWPROT), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"AWREADY", &(TOP.axi4_lite_slave__DOT__AWREADY), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"AWVALID", &(TOP.axi4_lite_slave__DOT__AWVALID), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"BREADY", &(TOP.axi4_lite_slave__DOT__BREADY), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"BRESP", &(TOP.axi4_lite_slave__DOT__BRESP), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"BVALID", &(TOP.axi4_lite_slave__DOT__BVALID), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"RDATA", &(TOP.axi4_lite_slave__DOT__RDATA), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"READ_DATA", const_cast<void*>(static_cast<const void*>(&(TOP.axi4_lite_slave__DOT__READ_DATA))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"READ_IDLE", const_cast<void*>(static_cast<const void*>(&(TOP.axi4_lite_slave__DOT__READ_IDLE))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"RREADY", &(TOP.axi4_lite_slave__DOT__RREADY), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"RRESP", &(TOP.axi4_lite_slave__DOT__RRESP), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"RVALID", &(TOP.axi4_lite_slave__DOT__RVALID), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WDATA", &(TOP.axi4_lite_slave__DOT__WDATA), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WREADY", &(TOP.axi4_lite_slave__DOT__WREADY), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WRITE_DATA", const_cast<void*>(static_cast<const void*>(&(TOP.axi4_lite_slave__DOT__WRITE_DATA))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WRITE_IDLE", const_cast<void*>(static_cast<const void*>(&(TOP.axi4_lite_slave__DOT__WRITE_IDLE))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WSTRB", &(TOP.axi4_lite_slave__DOT__WSTRB), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"WVALID", &(TOP.axi4_lite_slave__DOT__WVALID), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"memory", &(TOP.axi4_lite_slave__DOT__memory), false, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,1,1 ,0,1023 ,31,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"read_state", &(TOP.axi4_lite_slave__DOT__read_state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_axi4_lite_slave.varInsert(__Vfinal,"write_state", &(TOP.axi4_lite_slave__DOT__write_state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
    }
}
