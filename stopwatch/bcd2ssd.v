module bcd2ssd(
    bcd,
    HEX
);

    // define inputs and outputs
    input       [3:0] bcd;
    output reg  [6:0] HEX;

    // perform display logic using case statement
    always @ (bcd) begin
        case (bcd)
            //           GFEDCBA
            00: HEX = 7'b1000000;
            01: HEX = 7'b1111001;
            02: HEX = 7'b0100100;
            03: HEX = 7'b0110000;
            04: HEX = 7'b0011001;
            05: HEX = 7'b0010010;
            06: HEX = 7'b0000010;
            07: HEX = 7'b1111000;
            08: HEX = 7'b0000000;
            09: HEX = 7'b0010000;
            10: HEX = 7'b0000110;
            11: HEX = 7'b0000110;
            12: HEX = 7'b0000110;
            13: HEX = 7'b0000110;
            14: HEX = 7'b0000110;
            15: HEX = 7'b0000110;
            default: HEX = 7'b0000110;
        endcase
    end

endmodule
