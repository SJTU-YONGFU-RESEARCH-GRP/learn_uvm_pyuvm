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
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(dma_start,0,0);
    VL_OUT8(dma_done,0,0);
    VL_IN8(dma_channel,2,0);
    CData/*0:0*/ simple_dma__DOT__clk;
    CData/*0:0*/ simple_dma__DOT__rst_n;
    CData/*0:0*/ simple_dma__DOT__dma_start;
    CData/*0:0*/ simple_dma__DOT__dma_done;
    CData/*2:0*/ simple_dma__DOT__dma_channel;
    CData/*2:0*/ simple_dma__DOT__channel_reg;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__rst_n__0;
    CData/*0:0*/ __VactContinue;
    VL_IN16(dma_length,15,0);
    SData/*15:0*/ simple_dma__DOT__dma_length;
    SData/*15:0*/ simple_dma__DOT__length_reg;
    SData/*15:0*/ simple_dma__DOT__count;
    VL_IN(dma_src_addr,31,0);
    VL_IN(dma_dst_addr,31,0);
    IData/*31:0*/ simple_dma__DOT__dma_src_addr;
    IData/*31:0*/ simple_dma__DOT__dma_dst_addr;
    IData/*31:0*/ simple_dma__DOT__src_addr_reg;
    IData/*31:0*/ simple_dma__DOT__dst_addr_reg;
    IData/*31:0*/ __VactIterCount;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<2> __VactTriggered;
    VlTriggerVec<2> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
