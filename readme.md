# pwm-sine-fpga

A simple VHDL blinky for Lattice ECP5 FPGAs.
This pulses a LED using PWM in a sine-wave pattern.
The sine is generated using a quarter-wave look-up-table.
The sine wave is fully modular with regard to bit-depth and amount of samples.

## building

```bash
python3 ./make.py sim # simulate
python3 ./make.py pll sym # synthesize
python3 ./make.py prog # program
```

This project uses ghdl, yosys, ghdl-yosys-plugin, prj-trellis, nextpnr and ecpdap.
The Python scripts require python >= **3.10**!
