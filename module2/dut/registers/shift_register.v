/**
 * Module 2: Shift Register
 * 
 * A simple 8-bit shift register.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   shift:  Shift enable
 *   data_in: Serial data input
 *   data_out: Serial data output
 *   q:      Parallel output
 */

module shift_register (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       shift,
    input  wire       data_in,
    output reg        data_out,
    output reg  [7:0] q
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            q <= 8'h00;
            data_out <= 1'b0;
        end else if (shift) begin
            q <= {q[6:0], data_in};
            data_out <= q[7];
        end
    end

endmodule

