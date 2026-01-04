/**
 * Module 6: AXI4-Lite Slave
 * 
 * A simplified AXI4-Lite slave for protocol verification.
 * 
 * Ports:
 *   ACLK:     Clock signal
 *   ARESETn:  Active-low reset
 *   
 *   Write Address Channel:
 *   AWVALID:  Write address valid
 *   AWREADY:  Write address ready
 *   AWADDR:   Write address
 *   AWPROT:   Write protection type
 *   
 *   Write Data Channel:
 *   WVALID:   Write data valid
 *   WREADY:   Write data ready
 *   WDATA:    Write data
 *   WSTRB:    Write strobe
 *   
 *   Write Response Channel:
 *   BVALID:   Write response valid
 *   BREADY:   Write response ready
 *   BRESP:    Write response
 *   
 *   Read Address Channel:
 *   ARVALID:  Read address valid
 *   ARREADY:  Read address ready
 *   ARADDR:   Read address
 *   ARPROT:   Read protection type
 *   
 *   Read Data Channel:
 *   RVALID:   Read data valid
 *   RREADY:   Read data ready
 *   RDATA:    Read data
 *   RRESP:    Read response
 */

module axi4_lite_slave (
    input  wire        ACLK,
    input  wire        ARESETn,
    
    // Write Address Channel
    input  wire        AWVALID,
    output reg         AWREADY,
    input  wire [31:0] AWADDR,
    input  wire [2:0]  AWPROT,
    
    // Write Data Channel
    input  wire        WVALID,
    output reg         WREADY,
    input  wire [31:0] WDATA,
    input  wire [3:0]  WSTRB,
    
    // Write Response Channel
    output reg         BVALID,
    input  wire        BREADY,
    output reg  [1:0] BRESP,
    
    // Read Address Channel
    input  wire        ARVALID,
    output reg         ARREADY,
    input  wire [31:0] ARADDR,
    input  wire [2:0]  ARPROT,
    
    // Read Data Channel
    output reg         RVALID,
    input  wire        RREADY,
    output reg  [31:0] RDATA,
    output reg  [1:0] RRESP
);

    // Simple memory for AXI4-Lite slave
    reg [31:0] memory [0:1023];
    
    // Write state machine
    reg write_state;
    localparam WRITE_IDLE = 1'b0;
    localparam WRITE_DATA = 1'b1;
    
    // Read state machine
    reg read_state;
    localparam READ_IDLE = 1'b0;
    localparam READ_DATA = 1'b1;
    
    // Write Address Channel
    always @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            AWREADY <= 1'b0;
            write_state <= WRITE_IDLE;
        end else begin
            if (AWVALID && !AWREADY) begin
                AWREADY <= 1'b1;
                write_state <= WRITE_DATA;
            end else begin
                AWREADY <= 1'b0;
            end
        end
    end
    
    // Write Data Channel
    always @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            WREADY <= 1'b0;
            BVALID <= 1'b0;
            BRESP <= 2'b00;
        end else begin
            if (write_state == WRITE_DATA && WVALID && !WREADY) begin
                WREADY <= 1'b1;
                // Write to memory
                memory[AWADDR[11:2]] <= WDATA;
            end else begin
                WREADY <= 1'b0;
            end
            
            if (WREADY && WVALID) begin
                BVALID <= 1'b1;
                BRESP <= 2'b00; // OKAY
            end else if (BREADY && BVALID) begin
                BVALID <= 1'b0;
                write_state <= WRITE_IDLE;
            end
        end
    end
    
    // Read Address Channel
    always @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            ARREADY <= 1'b0;
            read_state <= READ_IDLE;
        end else begin
            if (ARVALID && !ARREADY) begin
                ARREADY <= 1'b1;
                read_state <= READ_DATA;
            end else begin
                ARREADY <= 1'b0;
            end
        end
    end
    
    // Read Data Channel
    always @(posedge ACLK or negedge ARESETn) begin
        if (!ARESETn) begin
            RVALID <= 1'b0;
            RDATA <= 32'h0;
            RRESP <= 2'b00;
        end else begin
            if (read_state == READ_DATA && !RVALID) begin
                RVALID <= 1'b1;
                RDATA <= memory[ARADDR[11:2]];
                RRESP <= 2'b00; // OKAY
            end else if (RREADY && RVALID) begin
                RVALID <= 1'b0;
                read_state <= READ_IDLE;
            end
        end
    end

endmodule

