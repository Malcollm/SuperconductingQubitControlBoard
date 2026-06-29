`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: N/A
// Engineer: Malcolm Mohr
// 
// Create Date: 05/30/2026 01:13:37 PM
// Design Name: 
// Module Name: Main
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module Main(
    output [3:0] led,
    input ck_io26,
    input ck_io27,
    input CLK100MHZ
    );
    
    wire [3:0] loaded_data;
    
    serial_to_reg_4bit my_loader (
    .clk(CLK100MHZ),
    .serial_clk(ck_io26),
    .reset(1'b0),
    .serial_in(ck_io27),
    .shift_enable1(1'b1),
    .data_out(loaded_data)
);
    
    assign led = loaded_data;
 
endmodule

module serial_to_reg_4bit (
    input wire clk,
    input wire serial_clk,
    input wire reset,
    input wire serial_in,
    input wire shift_enable1,
    output reg [3:0] data_out
);

    wire serial_clk_rising;
    reg serial_clk_last;
    wire shift_enable2 ;

always @(posedge clk) begin
    serial_clk_last <= serial_clk;
    if (reset) begin
        data_out <= 4'b0000;
    end else if (shift_enable2) begin
        data_out <= {data_out[2:0], serial_in};
    end
end
    
    assign serial_clk_rising = serial_clk & ~serial_clk_last;
    assign shift_enable2 = shift_enable1 & serial_clk_rising;

endmodule
