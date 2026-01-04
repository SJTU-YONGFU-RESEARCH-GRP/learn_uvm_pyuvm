/**
 * Module 3: Simple Adder
 * 
 * A basic 8-bit adder for UVM testing.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   a:      Operand A
 *   b:      Operand B
 *   sum:    Sum output
 *   carry:  Carry output
 */

module adder (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] a,
    input  wire [7:0] b,
    output reg  [7:0] sum,
    output reg        carry
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum <= 8'h00;
            carry <= 1'b0;
        end else begin
            {carry, sum} <= a + b;
        end
    end

endmodule

