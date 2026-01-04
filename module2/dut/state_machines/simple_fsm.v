/**
 * Module 2: Simple Finite State Machine
 * 
 * A basic state machine with 4 states.
 * 
 * Ports:
 *   clk:    Clock signal
 *   rst_n:  Active-low reset
 *   start:  Start signal
 *   done:   Done signal
 *   state:  Current state output
 */

module simple_fsm (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       start,
    output reg        done,
    output reg  [1:0] state
);

    // State encoding
    localparam IDLE  = 2'b00;
    localparam START = 2'b01;
    localparam WORK  = 2'b10;
    localparam DONE  = 2'b11;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            done <= 1'b0;
        end else begin
            case (state)
                IDLE: begin
                    if (start) begin
                        state <= START;
                        done <= 1'b0;
                    end
                end
                START: begin
                    state <= WORK;
                    done <= 1'b0;
                end
                WORK: begin
                    state <= DONE;
                    done <= 1'b0;
                end
                DONE: begin
                    state <= IDLE;
                    done <= 1'b1;
                end
                default: begin
                    state <= IDLE;
                    done <= 1'b0;
                end
            endcase
        end
    end

endmodule

