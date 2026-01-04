/**
 * Module 7: UART Transmitter/Receiver
 * 
 * A simple UART for protocol verification.
 * 
 * Ports:
 *   clk:      Clock signal
 *   rst_n:    Active-low reset
 *   tx:       Transmit data line
 *   rx:       Receive data line
 *   tx_data:  Data to transmit
 *   tx_start: Start transmission
 *   tx_busy:  Transmission in progress
 *   rx_data:  Received data
 *   rx_ready: Received data ready
 */

module uart (
    input  wire       clk,
    input  wire       rst_n,
    output reg        tx,
    input  wire       rx,
    input  wire [7:0] tx_data,
    input  wire       tx_start,
    output reg        tx_busy,
    output reg  [7:0] rx_data,
    output reg        rx_ready
);

    // UART transmitter state machine
    reg [3:0] tx_state;
    reg [7:0] tx_shift;
    reg [3:0] tx_bit_count;
    
    localparam TX_IDLE = 4'h0;
    localparam TX_START = 4'h1;
    localparam TX_DATA = 4'h2;
    localparam TX_STOP = 4'h3;
    
    // UART receiver state machine
    reg [3:0] rx_state;
    reg [7:0] rx_shift;
    reg [3:0] rx_bit_count;
    
    localparam RX_IDLE = 4'h0;
    localparam RX_START = 4'h1;
    localparam RX_DATA = 4'h2;
    localparam RX_STOP = 4'h3;
    
    // Transmitter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx <= 1'b1;
            tx_busy <= 1'b0;
            tx_state <= TX_IDLE;
            tx_shift <= 8'h0;
            tx_bit_count <= 4'h0;
        end else begin
            case (tx_state)
                TX_IDLE: begin
                    if (tx_start) begin
                        tx_state <= TX_START;
                        tx_shift <= tx_data;
                        tx_busy <= 1'b1;
                    end
                end
                TX_START: begin
                    tx <= 1'b0;  // Start bit
                    tx_state <= TX_DATA;
                    tx_bit_count <= 4'h0;
                end
                TX_DATA: begin
                    tx <= tx_shift[0];
                    tx_shift <= {1'b0, tx_shift[7:1]};
                    if (tx_bit_count == 4'h7) begin
                        tx_state <= TX_STOP;
                    end else begin
                        tx_bit_count <= tx_bit_count + 1;
                    end
                end
                TX_STOP: begin
                    tx <= 1'b1;  // Stop bit
                    tx_state <= TX_IDLE;
                    tx_busy <= 1'b0;
                end
                default: begin
                    tx_state <= TX_IDLE;
                    tx_busy <= 1'b0;
                end
            endcase
        end
    end
    
    // Receiver (simplified - would need proper sampling in real implementation)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_data <= 8'h0;
            rx_ready <= 1'b0;
            rx_state <= RX_IDLE;
            rx_shift <= 8'h0;
            rx_bit_count <= 4'h0;
        end else begin
            case (rx_state)
                RX_IDLE: begin
                    if (!rx) begin  // Start bit detected
                        rx_state <= RX_START;
                        rx_ready <= 1'b0;
                    end
                end
                RX_START: begin
                    rx_state <= RX_DATA;
                    rx_bit_count <= 4'h0;
                end
                RX_DATA: begin
                    rx_shift <= {rx, rx_shift[7:1]};
                    if (rx_bit_count == 4'h7) begin
                        rx_state <= RX_STOP;
                    end else begin
                        rx_bit_count <= rx_bit_count + 1;
                    end
                end
                RX_STOP: begin
                    rx_data <= rx_shift;
                    rx_ready <= 1'b1;
                    rx_state <= RX_IDLE;
                end
                default: begin
                    rx_state <= RX_IDLE;
                    rx_ready <= 1'b0;
                end
            endcase
        end
    end

endmodule

