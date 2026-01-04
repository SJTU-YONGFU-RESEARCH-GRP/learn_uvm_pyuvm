// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.axi4_lite_slave__DOT__ACLK = vlSelfRef.ACLK;
    vlSelfRef.axi4_lite_slave__DOT__ARESETn = vlSelfRef.ARESETn;
    vlSelfRef.axi4_lite_slave__DOT__AWVALID = vlSelfRef.AWVALID;
    vlSelfRef.axi4_lite_slave__DOT__AWADDR = vlSelfRef.AWADDR;
    vlSelfRef.axi4_lite_slave__DOT__AWPROT = vlSelfRef.AWPROT;
    vlSelfRef.axi4_lite_slave__DOT__WVALID = vlSelfRef.WVALID;
    vlSelfRef.axi4_lite_slave__DOT__WDATA = vlSelfRef.WDATA;
    vlSelfRef.axi4_lite_slave__DOT__WSTRB = vlSelfRef.WSTRB;
    vlSelfRef.axi4_lite_slave__DOT__BREADY = vlSelfRef.BREADY;
    vlSelfRef.axi4_lite_slave__DOT__ARVALID = vlSelfRef.ARVALID;
    vlSelfRef.axi4_lite_slave__DOT__ARADDR = vlSelfRef.ARADDR;
    vlSelfRef.axi4_lite_slave__DOT__ARPROT = vlSelfRef.ARPROT;
    vlSelfRef.axi4_lite_slave__DOT__RREADY = vlSelfRef.RREADY;
    vlSelfRef.AWREADY = vlSelfRef.axi4_lite_slave__DOT__AWREADY;
    vlSelfRef.WREADY = vlSelfRef.axi4_lite_slave__DOT__WREADY;
    vlSelfRef.BVALID = vlSelfRef.axi4_lite_slave__DOT__BVALID;
    vlSelfRef.BRESP = vlSelfRef.axi4_lite_slave__DOT__BRESP;
    vlSelfRef.ARREADY = vlSelfRef.axi4_lite_slave__DOT__ARREADY;
    vlSelfRef.RVALID = vlSelfRef.axi4_lite_slave__DOT__RVALID;
    vlSelfRef.RDATA = vlSelfRef.axi4_lite_slave__DOT__RDATA;
    vlSelfRef.RRESP = vlSelfRef.axi4_lite_slave__DOT__RRESP;
}

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __Vdly__axi4_lite_slave__DOT__write_state;
    __Vdly__axi4_lite_slave__DOT__write_state = 0;
    CData/*0:0*/ __Vdly__axi4_lite_slave__DOT__WREADY;
    __Vdly__axi4_lite_slave__DOT__WREADY = 0;
    CData/*0:0*/ __Vdly__axi4_lite_slave__DOT__BVALID;
    __Vdly__axi4_lite_slave__DOT__BVALID = 0;
    CData/*0:0*/ __Vdly__axi4_lite_slave__DOT__read_state;
    __Vdly__axi4_lite_slave__DOT__read_state = 0;
    CData/*0:0*/ __Vdly__axi4_lite_slave__DOT__RVALID;
    __Vdly__axi4_lite_slave__DOT__RVALID = 0;
    IData/*31:0*/ __VdlyVal__axi4_lite_slave__DOT__memory__v0;
    __VdlyVal__axi4_lite_slave__DOT__memory__v0 = 0;
    SData/*9:0*/ __VdlyDim0__axi4_lite_slave__DOT__memory__v0;
    __VdlyDim0__axi4_lite_slave__DOT__memory__v0 = 0;
    CData/*0:0*/ __VdlySet__axi4_lite_slave__DOT__memory__v0;
    __VdlySet__axi4_lite_slave__DOT__memory__v0 = 0;
    // Body
    __Vdly__axi4_lite_slave__DOT__RVALID = vlSelfRef.axi4_lite_slave__DOT__RVALID;
    __VdlySet__axi4_lite_slave__DOT__memory__v0 = 0U;
    __Vdly__axi4_lite_slave__DOT__WREADY = vlSelfRef.axi4_lite_slave__DOT__WREADY;
    __Vdly__axi4_lite_slave__DOT__BVALID = vlSelfRef.axi4_lite_slave__DOT__BVALID;
    __Vdly__axi4_lite_slave__DOT__read_state = vlSelfRef.axi4_lite_slave__DOT__read_state;
    __Vdly__axi4_lite_slave__DOT__write_state = vlSelfRef.axi4_lite_slave__DOT__write_state;
    if (vlSelfRef.ARESETn) {
        if (((IData)(vlSelfRef.ARVALID) & (~ (IData)(vlSelfRef.axi4_lite_slave__DOT__ARREADY)))) {
            vlSelfRef.axi4_lite_slave__DOT__ARREADY = 1U;
            __Vdly__axi4_lite_slave__DOT__read_state = 1U;
        } else {
            vlSelfRef.axi4_lite_slave__DOT__ARREADY = 0U;
        }
        if (((IData)(vlSelfRef.AWVALID) & (~ (IData)(vlSelfRef.axi4_lite_slave__DOT__AWREADY)))) {
            vlSelfRef.axi4_lite_slave__DOT__AWREADY = 1U;
            __Vdly__axi4_lite_slave__DOT__write_state = 1U;
        } else {
            vlSelfRef.axi4_lite_slave__DOT__AWREADY = 0U;
        }
        if (((IData)(vlSelfRef.axi4_lite_slave__DOT__read_state) 
             & (~ (IData)(vlSelfRef.axi4_lite_slave__DOT__RVALID)))) {
            __Vdly__axi4_lite_slave__DOT__RVALID = 1U;
            vlSelfRef.axi4_lite_slave__DOT__RDATA = 
                vlSelfRef.axi4_lite_slave__DOT__memory
                [(0x3ffU & (vlSelfRef.ARADDR >> 2U))];
            vlSelfRef.axi4_lite_slave__DOT__RRESP = 0U;
        } else if (((IData)(vlSelfRef.RREADY) & (IData)(vlSelfRef.axi4_lite_slave__DOT__RVALID))) {
            __Vdly__axi4_lite_slave__DOT__RVALID = 0U;
            __Vdly__axi4_lite_slave__DOT__read_state = 0U;
        }
        if ((((IData)(vlSelfRef.axi4_lite_slave__DOT__write_state) 
              & (IData)(vlSelfRef.WVALID)) & (~ (IData)(vlSelfRef.axi4_lite_slave__DOT__WREADY)))) {
            __Vdly__axi4_lite_slave__DOT__WREADY = 1U;
            __VdlyVal__axi4_lite_slave__DOT__memory__v0 
                = vlSelfRef.WDATA;
            __VdlyDim0__axi4_lite_slave__DOT__memory__v0 
                = (0x3ffU & (vlSelfRef.AWADDR >> 2U));
            __VdlySet__axi4_lite_slave__DOT__memory__v0 = 1U;
        } else {
            __Vdly__axi4_lite_slave__DOT__WREADY = 0U;
        }
        if (((IData)(vlSelfRef.axi4_lite_slave__DOT__WREADY) 
             & (IData)(vlSelfRef.WVALID))) {
            __Vdly__axi4_lite_slave__DOT__BVALID = 1U;
            vlSelfRef.axi4_lite_slave__DOT__BRESP = 0U;
        } else if (((IData)(vlSelfRef.BREADY) & (IData)(vlSelfRef.axi4_lite_slave__DOT__BVALID))) {
            __Vdly__axi4_lite_slave__DOT__BVALID = 0U;
            __Vdly__axi4_lite_slave__DOT__write_state = 0U;
        }
    } else {
        vlSelfRef.axi4_lite_slave__DOT__ARREADY = 0U;
        __Vdly__axi4_lite_slave__DOT__read_state = 0U;
        vlSelfRef.axi4_lite_slave__DOT__AWREADY = 0U;
        __Vdly__axi4_lite_slave__DOT__write_state = 0U;
        __Vdly__axi4_lite_slave__DOT__RVALID = 0U;
        vlSelfRef.axi4_lite_slave__DOT__RDATA = 0U;
        vlSelfRef.axi4_lite_slave__DOT__RRESP = 0U;
        __Vdly__axi4_lite_slave__DOT__WREADY = 0U;
        __Vdly__axi4_lite_slave__DOT__BVALID = 0U;
        vlSelfRef.axi4_lite_slave__DOT__BRESP = 0U;
    }
    vlSelfRef.axi4_lite_slave__DOT__read_state = __Vdly__axi4_lite_slave__DOT__read_state;
    vlSelfRef.axi4_lite_slave__DOT__RVALID = __Vdly__axi4_lite_slave__DOT__RVALID;
    vlSelfRef.axi4_lite_slave__DOT__write_state = __Vdly__axi4_lite_slave__DOT__write_state;
    if (__VdlySet__axi4_lite_slave__DOT__memory__v0) {
        vlSelfRef.axi4_lite_slave__DOT__memory[__VdlyDim0__axi4_lite_slave__DOT__memory__v0] 
            = __VdlyVal__axi4_lite_slave__DOT__memory__v0;
    }
    vlSelfRef.axi4_lite_slave__DOT__WREADY = __Vdly__axi4_lite_slave__DOT__WREADY;
    vlSelfRef.axi4_lite_slave__DOT__BVALID = __Vdly__axi4_lite_slave__DOT__BVALID;
    vlSelfRef.ARREADY = vlSelfRef.axi4_lite_slave__DOT__ARREADY;
    vlSelfRef.AWREADY = vlSelfRef.axi4_lite_slave__DOT__AWREADY;
    vlSelfRef.RVALID = vlSelfRef.axi4_lite_slave__DOT__RVALID;
    vlSelfRef.RDATA = vlSelfRef.axi4_lite_slave__DOT__RDATA;
    vlSelfRef.RRESP = vlSelfRef.axi4_lite_slave__DOT__RRESP;
    vlSelfRef.WREADY = vlSelfRef.axi4_lite_slave__DOT__WREADY;
    vlSelfRef.BVALID = vlSelfRef.axi4_lite_slave__DOT__BVALID;
    vlSelfRef.BRESP = vlSelfRef.axi4_lite_slave__DOT__BRESP;
}

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<2> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vtop___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY(((0x64U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("../../dut/protocols/axi4_lite_slave.v", 40, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vtop___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY(((0x64U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("../../dut/protocols/axi4_lite_slave.v", 40, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY(((0x64U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("../../dut/protocols/axi4_lite_slave.v", 40, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vtop___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vtop___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.ACLK & 0xfeU)))) {
        Verilated::overWidthError("ACLK");}
    if (VL_UNLIKELY(((vlSelfRef.ARESETn & 0xfeU)))) {
        Verilated::overWidthError("ARESETn");}
    if (VL_UNLIKELY(((vlSelfRef.AWVALID & 0xfeU)))) {
        Verilated::overWidthError("AWVALID");}
    if (VL_UNLIKELY(((vlSelfRef.AWPROT & 0xf8U)))) {
        Verilated::overWidthError("AWPROT");}
    if (VL_UNLIKELY(((vlSelfRef.WVALID & 0xfeU)))) {
        Verilated::overWidthError("WVALID");}
    if (VL_UNLIKELY(((vlSelfRef.WSTRB & 0xf0U)))) {
        Verilated::overWidthError("WSTRB");}
    if (VL_UNLIKELY(((vlSelfRef.BREADY & 0xfeU)))) {
        Verilated::overWidthError("BREADY");}
    if (VL_UNLIKELY(((vlSelfRef.ARVALID & 0xfeU)))) {
        Verilated::overWidthError("ARVALID");}
    if (VL_UNLIKELY(((vlSelfRef.ARPROT & 0xf8U)))) {
        Verilated::overWidthError("ARPROT");}
    if (VL_UNLIKELY(((vlSelfRef.RREADY & 0xfeU)))) {
        Verilated::overWidthError("RREADY");}
}
#endif  // VL_DEBUG
