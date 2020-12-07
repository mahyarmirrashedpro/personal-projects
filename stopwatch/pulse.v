module pulse(
    clk,
    out
);

    // define constants
    parameter   FREQUENCY = 500_000;

    // define inputs and outputs
    input       clk;
    output reg  out;

    // define variables
    integer     cycles = 0;

    // execute logic every clock tick
    always @ (posedge clk) begin
        if (cycles >= FREQUENCY) begin
            cycles <= 0;
            out <= 1;
        end else begin
            out <= 0;
            cycles <= cycles + 1;
        end
    end

endmodule
