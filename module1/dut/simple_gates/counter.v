/**
 * Module 1: Simple Counter
 * 
 * A basic up-counter with reset for verification examples.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   enable: Counter enable
 *   count:  Counter output
 */

module counter (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       enable,
    output reg [7:0]  count
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 8'h00;
        end else if (enable) begin
            count <= count + 1;
        end
    end

endmodule

