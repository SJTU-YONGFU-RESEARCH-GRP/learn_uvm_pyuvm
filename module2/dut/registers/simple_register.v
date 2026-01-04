/**
 * Module 2: Simple Register
 * 
 * A basic register with clock, reset, and enable.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   enable: Register enable
 *   d:      Data input
 *   q:      Data output
 */

module simple_register (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       enable,
    input  wire [7:0] d,
    output reg  [7:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q <= 8'h00;
        end else if (enable) begin
            q <= d;
        end
    end

endmodule

