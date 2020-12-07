# Stopwatch with Lap Timer Features

Stopwatches are digital clocks designed to measure the amount of time elapsed from the time when a start button is pressed and released to the current time or when the stop button is pressed and released. Short-term stopwatches usually omit hours in favour of displaying time intervals in increments of hundredths of seconds.

Using Quartus II Prime Software and the DE10-Standard FPGA-SoC Development Board, a digital stopwatch with lap view capabilities was created.

## Summary of Inputs and Outputs

The stopwatch has the following inputs:
* Pushbutton controlling start, stop, and reset features.
* Pushbutton controlling lap starter.
* Switch used to alternate between master stopwatch and lap stopwatch.

The stopwatch has the following outputs:
* Seven-segment display for the hundreths of seconds and tenths of seconds, for the seconds, and for the minutes.

## Future Improvements

In the future, a feature that could be added would perhaps be a display showing the lap count of the user. The pushbutton controlling reset features would also reset the number of laps back to zero.

Another feature that may be added in the future is the ability to display the decimal point separating the fractions of seconds from the rest of the time display. However, this would have to be done manually since the DE10-Standard FPGA-SoC Development Board does not have any wires to enable the decimal point.

## Verilog Implementation

The Verilog code used to develop the stopwatch are included in this directory for your viewing leisure.

## Implementation Demonstration

The demonstration of the stopwatch can viewed [here](https://youtu.be/5ri80YKdd5E) for your viewing leisure.
