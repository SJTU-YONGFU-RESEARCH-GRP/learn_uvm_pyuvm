/**
 * Module 4: Simple Interface
 * 
 * A simple interface for UVM component testing.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   valid:  Valid signal
 *   ready:  Ready signal
 *   data:   Data bus
 *   address: Address bus
 */

module simple_interface (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       valid,
    output reg        ready,
    input  wire [7:0] data,
    input  wire [15:0] address,
    output reg  [7:0] result
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ready <= 1'b0;
            result <= 8'h00;
        end else begin
            if (valid) begin
                ready <= 1'b1;
                // Simple operation: result = data + 1
                result <= data + 1;
            end else begin
                ready <= 1'b0;
            end
        end
    end

endmodule

