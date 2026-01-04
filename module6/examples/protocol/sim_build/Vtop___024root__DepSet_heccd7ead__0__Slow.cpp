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
    vlSelfRef.__Vtrigprevexpr___TOP__axi4_lite_slave__DOT__ACLK__0 
        = vlSelfRef.axi4_lite_slave__DOT__ACLK;
    vlSelfRef.__Vtrigprevexpr___TOP__axi4_lite_slave__DOT__ARESETn__0 
        = vlSelfRef.axi4_lite_slave__DOT__ARESETn;
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
        VL_DBG_MSGF("         'act' region trigger index 0 is active: @(posedge axi4_lite_slave.ACLK)\n");
    }
    if ((2ULL & vlSelfRef.__VactTriggered.word(0U))) {
        VL_DBG_MSGF("         'act' region trigger index 1 is active: @(negedge axi4_lite_slave.ARESETn)\n");
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
        VL_DBG_MSGF("         'nba' region trigger index 0 is active: @(posedge axi4_lite_slave.ACLK)\n");
    }
    if ((2ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        VL_DBG_MSGF("         'nba' region trigger index 1 is active: @(negedge axi4_lite_slave.ARESETn)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vtop___024root___ctor_var_reset(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ctor_var_reset\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->name());
    vlSelf->ACLK = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3034660589080906099ull);
    vlSelf->ARESETn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11625642876178449192ull);
    vlSelf->AWVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11750918698781911943ull);
    vlSelf->AWREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17297234574184235162ull);
    vlSelf->AWADDR = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3704207311081907456ull);
    vlSelf->AWPROT = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 7076923066334087385ull);
    vlSelf->WVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9495255681580949789ull);
    vlSelf->WREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 17076114656213402080ull);
    vlSelf->WDATA = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13545846466767745629ull);
    vlSelf->WSTRB = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17384056636743468383ull);
    vlSelf->BVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8367422369656964262ull);
    vlSelf->BREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18149121645282540317ull);
    vlSelf->BRESP = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 12793087776628502554ull);
    vlSelf->ARVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1896485211029909696ull);
    vlSelf->ARREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 11936612248788037190ull);
    vlSelf->ARADDR = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 17761954141230437835ull);
    vlSelf->ARPROT = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 4622094218666349735ull);
    vlSelf->RVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5829902753712117520ull);
    vlSelf->RREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2085817933989443683ull);
    vlSelf->RDATA = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 4866321451055619796ull);
    vlSelf->RRESP = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 17082317525515500324ull);
    vlSelf->axi4_lite_slave__DOT__ACLK = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3064556554388272116ull);
    vlSelf->axi4_lite_slave__DOT__ARESETn = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9288383414069408872ull);
    vlSelf->axi4_lite_slave__DOT__AWVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 6258793095501765650ull);
    vlSelf->axi4_lite_slave__DOT__AWREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16281233134493343396ull);
    vlSelf->axi4_lite_slave__DOT__AWADDR = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8972882985743065186ull);
    vlSelf->axi4_lite_slave__DOT__AWPROT = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9869756506787959736ull);
    vlSelf->axi4_lite_slave__DOT__WVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 18168352935381733502ull);
    vlSelf->axi4_lite_slave__DOT__WREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 3016007778758478713ull);
    vlSelf->axi4_lite_slave__DOT__WDATA = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10529316179120149992ull);
    vlSelf->axi4_lite_slave__DOT__WSTRB = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 8808500256834480651ull);
    vlSelf->axi4_lite_slave__DOT__BVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9284935256251554695ull);
    vlSelf->axi4_lite_slave__DOT__BREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5054486302197025292ull);
    vlSelf->axi4_lite_slave__DOT__BRESP = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 9087902711421585238ull);
    vlSelf->axi4_lite_slave__DOT__ARVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14306260012427034008ull);
    vlSelf->axi4_lite_slave__DOT__ARREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12983612923460393443ull);
    vlSelf->axi4_lite_slave__DOT__ARADDR = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 5376445607231156176ull);
    vlSelf->axi4_lite_slave__DOT__ARPROT = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 18043364310262677454ull);
    vlSelf->axi4_lite_slave__DOT__RVALID = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12995728839675915735ull);
    vlSelf->axi4_lite_slave__DOT__RREADY = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9024601422434617660ull);
    vlSelf->axi4_lite_slave__DOT__RDATA = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 14931538133589772657ull);
    vlSelf->axi4_lite_slave__DOT__RRESP = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 8891484909249726633ull);
    for (int __Vi0 = 0; __Vi0 < 1024; ++__Vi0) {
        vlSelf->axi4_lite_slave__DOT__memory[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 13574519678020883956ull);
    }
    vlSelf->axi4_lite_slave__DOT__write_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13974991232865775285ull);
    vlSelf->axi4_lite_slave__DOT__read_state = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14633322551774103212ull);
    vlSelf->__Vtrigprevexpr___TOP__axi4_lite_slave__DOT__ACLK__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 2757000064968680478ull);
    vlSelf->__Vtrigprevexpr___TOP__axi4_lite_slave__DOT__ARESETn__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5994356815771381140ull);
}
