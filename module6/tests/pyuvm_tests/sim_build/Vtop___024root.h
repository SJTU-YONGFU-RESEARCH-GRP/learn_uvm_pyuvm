// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(ACLK,0,0);
    VL_IN8(ARESETn,0,0);
    VL_IN8(AWVALID,0,0);
    VL_OUT8(AWREADY,0,0);
    VL_IN8(AWPROT,2,0);
    VL_IN8(WVALID,0,0);
    VL_OUT8(WREADY,0,0);
    VL_IN8(WSTRB,3,0);
    VL_OUT8(BVALID,0,0);
    VL_IN8(BREADY,0,0);
    VL_OUT8(BRESP,1,0);
    VL_IN8(ARVALID,0,0);
    VL_OUT8(ARREADY,0,0);
    VL_IN8(ARPROT,2,0);
    VL_OUT8(RVALID,0,0);
    VL_IN8(RREADY,0,0);
    VL_OUT8(RRESP,1,0);
    CData/*0:0*/ axi4_lite_slave__DOT__ACLK;
    CData/*0:0*/ axi4_lite_slave__DOT__ARESETn;
    CData/*0:0*/ axi4_lite_slave__DOT__AWVALID;
    CData/*0:0*/ axi4_lite_slave__DOT__AWREADY;
    CData/*2:0*/ axi4_lite_slave__DOT__AWPROT;
    CData/*0:0*/ axi4_lite_slave__DOT__WVALID;
    CData/*0:0*/ axi4_lite_slave__DOT__WREADY;
    CData/*3:0*/ axi4_lite_slave__DOT__WSTRB;
    CData/*0:0*/ axi4_lite_slave__DOT__BVALID;
    CData/*0:0*/ axi4_lite_slave__DOT__BREADY;
    CData/*1:0*/ axi4_lite_slave__DOT__BRESP;
    CData/*0:0*/ axi4_lite_slave__DOT__ARVALID;
    CData/*0:0*/ axi4_lite_slave__DOT__ARREADY;
    CData/*2:0*/ axi4_lite_slave__DOT__ARPROT;
    CData/*0:0*/ axi4_lite_slave__DOT__RVALID;
    CData/*0:0*/ axi4_lite_slave__DOT__RREADY;
    CData/*1:0*/ axi4_lite_slave__DOT__RRESP;
    CData/*0:0*/ axi4_lite_slave__DOT__write_state;
    CData/*0:0*/ axi4_lite_slave__DOT__read_state;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__ACLK__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__ARESETn__0;
    CData/*0:0*/ __VactContinue;
    VL_IN(AWADDR,31,0);
    VL_IN(WDATA,31,0);
    VL_IN(ARADDR,31,0);
    VL_OUT(RDATA,31,0);
    IData/*31:0*/ axi4_lite_slave__DOT__AWADDR;
    IData/*31:0*/ axi4_lite_slave__DOT__WDATA;
    IData/*31:0*/ axi4_lite_slave__DOT__ARADDR;
    IData/*31:0*/ axi4_lite_slave__DOT__RDATA;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<IData/*31:0*/, 1024> axi4_lite_slave__DOT__memory;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // PARAMETERS
    static constexpr CData/*0:0*/ axi4_lite_slave__DOT__WRITE_IDLE = 0U;
    static constexpr CData/*0:0*/ axi4_lite_slave__DOT__WRITE_DATA = 1U;
    static constexpr CData/*0:0*/ axi4_lite_slave__DOT__READ_IDLE = 0U;
    static constexpr CData/*0:0*/ axi4_lite_slave__DOT__READ_DATA = 1U;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
