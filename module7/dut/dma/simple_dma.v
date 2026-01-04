/**
 * Module 7: Simple DMA Controller
 * 
 * A simple DMA controller for verification.
 * 
 * Ports:
 *   clk:        Clock signal
 *   rst_n:      Active-low reset
 *   dma_start:  Start DMA transfer
 *   dma_done:   DMA transfer complete
 *   dma_src_addr: Source address
 *   dma_dst_addr: Destination address
 *   dma_length:  Transfer length
 *   dma_channel: DMA channel select
 */

module simple_dma (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        dma_start,
    output reg         dma_done,
    input  wire [31:0] dma_src_addr,
    input  wire [31:0] dma_dst_addr,
    input  wire [15:0] dma_length,
    input  wire [2:0]  dma_channel
);

    reg [31:0] src_addr_reg;
    reg [31:0] dst_addr_reg;
    reg [15:0] length_reg;
    reg [2:0]  channel_reg;
    reg [15:0] count;
    
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            dma_done <= 1'b0;
            src_addr_reg <= 32'h0;
            dst_addr_reg <= 32'h0;
            length_reg <= 16'h0;
            channel_reg <= 3'h0;
            count <= 16'h0;
        end else begin
            if (dma_start && !dma_done) begin
                src_addr_reg <= dma_src_addr;
                dst_addr_reg <= dma_dst_addr;
                length_reg <= dma_length;
                channel_reg <= dma_channel;
                count <= 16'h0;
            end else if (!dma_done) begin
                if (count < length_reg) begin
                    count <= count + 1;
                end else begin
                    dma_done <= 1'b1;
                end
            end else if (dma_done) begin
                dma_done <= 1'b0;
            end
        end
    end

endmodule

