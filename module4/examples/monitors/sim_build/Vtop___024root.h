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
    CData/*0:0*/ simple_interface__DOT__clk;
    CData/*0:0*/ simple_interface__DOT__rst_n;
    VL_IN8(clk,0,0);
    VL_IN8(rst_n,0,0);
    VL_IN8(valid,0,0);
    VL_OUT8(ready,0,0);
    VL_IN8(data,7,0);
    VL_OUT8(result,7,0);
    CData/*0:0*/ simple_interface__DOT__valid;
    CData/*0:0*/ simple_interface__DOT__ready;
    CData/*7:0*/ simple_interface__DOT__data;
    CData/*7:0*/ simple_interface__DOT__result;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__simple_interface__DOT__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__simple_interface__DOT__rst_n__0;
    CData/*0:0*/ __VactContinue;
    VL_IN16(address,15,0);
    SData/*15:0*/ simple_interface__DOT__address;
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
