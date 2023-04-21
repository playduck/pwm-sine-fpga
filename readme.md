# pwm-sine

A simple VHDL blinky for Lattice ECP5 FPGAs.
This pulses an LED in a sine-wave pattern.
The sine is generated with a quarter-wave look-up-table.

## building

```bash
python3 ./make.py sim # simulate
python3 ./make.py sym # synthesize
python3 ./make.py prog # program
```

This project uses ghdl, yosys, ghdl-yosys-plugin and nextpnr.
