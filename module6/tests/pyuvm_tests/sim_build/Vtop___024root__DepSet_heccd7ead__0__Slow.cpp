// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

VL_ATTR_COLD void Vtop___024root___eval_static(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_static\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__ACLK__0 = vlSelfRef.ACLK;
    vlSelfRef.__Vtrigprevexpr___TOP__ARESETn__0 = vlSelfRef.ARESETn;
}

VL_ATTR_COLD void Vtop___024root___eval_initial(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_initial\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

VL_ATTR_COLD void Vtop___024root___eval_final(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_final\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_settle(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_settle\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VstlIterCount;
    CData/*0:0*/ __VstlContinue;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    __VstlContinue = 1U;
    while (__VstlContinue) {
        if (VL_UNLIKELY(((0x64U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__stl(vlSelf);
#endif
            VL_FATAL_MT("../../dut/protocols/axi4_lite_slave.v", 40, "", "Settle region did not converge.");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
        __VstlContinue = 0U;
        if (Vtop___024root___eval_phase__stl(vlSelf)) {
            __VstlContinue = 1U;
        }
        vlSelfRef.__VstlFirstIteration = 0U;
    }
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VstlTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        VL_DBG_MSGF("         'stl' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

VL_ATTR_COLD void Vtop___024root___eval_stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD void Vtop___024root___eval_triggers__stl(Vtop___024root* vlSelf);

VL_ATTR_COLD bool Vtop___024root___eval_phase__stl(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__stl\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VstlExecute;
    // Body
    Vtop___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = vlSelfRef.__VstlTriggered.any();
    if (__VstlExecute) {
        Vtop___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VicoTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        VL_DBG_MSGF("         'ico' region trigger index 0 is active: Internal 'ico' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VactTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge ACLK)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(negedge ARESETn)\n");
    }
}
#endif  // VL_DEBUG

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___dump_triggers__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1U & (~ vlSelfRef.__VnbaTriggered.any()))) {
        VL_DBG_MSGF("         No triggers active\n");
    }
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge ACLK)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(negedge ARESETn)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->ACLK = VL_RAND_RESET_I(1);
    vlSelf->ARESETn = VL_RAND_RESET_I(1);
    vlSelf->AWVALID = VL_RAND_RESET_I(1);
    vlSelf->AWREADY = VL_RAND_RESET_I(1);
    vlSelf->AWADDR = VL_RAND_RESET_I(32);
    vlSelf->AWPROT = VL_RAND_RESET_I(3);
    vlSelf->WVALID = VL_RAND_RESET_I(1);
    vlSelf->WREADY = VL_RAND_RESET_I(1);
    vlSelf->WDATA = VL_RAND_RESET_I(32);
    vlSelf->WSTRB = VL_RAND_RESET_I(4);
    vlSelf->BVALID = VL_RAND_RESET_I(1);
    vlSelf->BREADY = VL_RAND_RESET_I(1);
    vlSelf->BRESP = VL_RAND_RESET_I(2);
    vlSelf->ARVALID = VL_RAND_RESET_I(1);
    vlSelf->ARREADY = VL_RAND_RESET_I(1);
    vlSelf->ARADDR = VL_RAND_RESET_I(32);
    vlSelf->ARPROT = VL_RAND_RESET_I(3);
    vlSelf->RVALID = VL_RAND_RESET_I(1);
    vlSelf->RREADY = VL_RAND_RESET_I(1);
    vlSelf->RDATA = VL_RAND_RESET_I(32);
    vlSelf->RRESP = VL_RAND_RESET_I(2);
    vlSelf->axi4_lite_slave__DOT__ACLK = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__ARESETn = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__AWVALID = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__AWREADY = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__AWADDR = VL_RAND_RESET_I(32);
    vlSelf->axi4_lite_slave__DOT__AWPROT = VL_RAND_RESET_I(3);
    vlSelf->axi4_lite_slave__DOT__WVALID = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__WREADY = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__WDATA = VL_RAND_RESET_I(32);
    vlSelf->axi4_lite_slave__DOT__WSTRB = VL_RAND_RESET_I(4);
    vlSelf->axi4_lite_slave__DOT__BVALID = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__BREADY = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__BRESP = VL_RAND_RESET_I(2);
    vlSelf->axi4_lite_slave__DOT__ARVALID = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__ARREADY = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__ARADDR = VL_RAND_RESET_I(32);
    vlSelf->axi4_lite_slave__DOT__ARPROT = VL_RAND_RESET_I(3);
    vlSelf->axi4_lite_slave__DOT__RVALID = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__RREADY = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__RDATA = VL_RAND_RESET_I(32);
    vlSelf->axi4_lite_slave__DOT__RRESP = VL_RAND_RESET_I(2);
    for (int __Vi0 = 0; __Vi0 < 1024; ++__Vi0) {
        vlSelf->axi4_lite_slave__DOT__memory[__Vi0] = VL_RAND_RESET_I(32);
    }
    vlSelf->axi4_lite_slave__DOT__write_state = VL_RAND_RESET_I(1);
    vlSelf->axi4_lite_slave__DOT__read_state = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__ACLK__0 = VL_RAND_RESET_I(1);
    vlSelf->__Vtrigprevexpr___TOP__ARESETn__0 = VL_RAND_RESET_I(1);
}
