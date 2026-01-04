/**
 * Module 2: Simple FIFO
 * 
 * A basic FIFO with read/write pointers.
 * 
 * Ports:
 *   clk:      Clock signal
 *   rst_n:    Active-low reset
 *   write_en: Write enable
 *   read_en:  Read enable
 *   data_in:  Write data
 *   data_out: Read data
 *   full:     FIFO full flag
 *   empty:    FIFO empty flag
 */

module simple_fifo (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       write_en,
    input  wire       read_en,
    input  wire [7:0] data_in,
    output reg  [7:0] data_out,
    output reg        full,
    output reg        empty
);

    reg [7:0] mem [0:15];  // 16-entry FIFO
    reg [4:0] write_ptr;
    reg [4:0] read_ptr;
    reg [4:0] count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            write_ptr <= 5'h0;
            read_ptr <= 5'h0;
            count <= 5'h0;
            full <= 1'b0;
            empty <= 1'b1;
        end else begin
            // Write operation
            if (write_en && !full) begin
                mem[write_ptr[3:0]] <= data_in;
                write_ptr <= write_ptr + 1;
                count <= count + 1;
            end
            
            // Read operation
            if (read_en && !empty) begin
                data_out <= mem[read_ptr[3:0]];
                read_ptr <= read_ptr + 1;
                count <= count - 1;
            end
            
            // Update flags
            full <= (count == 16);
            empty <= (count == 0);
        end
    end

endmodule

