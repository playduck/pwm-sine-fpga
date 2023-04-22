#!/usr/bin/python3

import argparse
import importlib
import os
import subprocess
import sys

from src.util import style as s

os.system("")

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
PLL_SCRIPT = f"{SCRIPT_PATH}/src/syn/pll/gen-pll.sh"
PROG_SCRIPT = f"{SCRIPT_PATH}/src/syn/prog.sh"
FLASH_SCRIPT = f"{SCRIPT_PATH}/src/syn/flash.sh"

SIM_GHDL_SCRIPT = f"src.sim.ghdl.ghdl-sim"
SYN_SCRIPT = f"src.syn.syn"

HDL_INDEX_PATH = f"{SCRIPT_PATH}/src/hdl/index.py"
SIM_INDEX_PATH = f"{SCRIPT_PATH}/src/sim/index.py"
SYN_INDEX_PATH = f"{SCRIPT_PATH}/src/syn/index.py"


def import_module(name, path):
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


hdl_index = import_module("index", HDL_INDEX_PATH)
sim_index = import_module("index", SIM_INDEX_PATH)
syn_index = import_module("index", SYN_INDEX_PATH)

COMMON_SOURCES = hdl_index.COMMON_SOURCES
SIM_SOURCES = sim_index.SIM_SOURCES
SYN_SOURCES = syn_index.SYN_SOURCES
VERILOG_SOURCES = syn_index.VERILOG_SOURCES


parser = argparse.ArgumentParser("pwm-sine make")
parser.add_argument("action", nargs='*', help="Actions to perform")
args = parser.parse_args()

for action in args.action:
    match action:
        case "clean":
            s.printc(s.INFO, s.GREEN + "Clean")
            subprocess.run([PLL_SCRIPT, "clean"])
            subprocess.run(["python3", "-m", SIM_GHDL_SCRIPT, "--clean"])
            subprocess.run(["python3", "-m", SYN_SCRIPT, "--clean"])

        case "sim":
            s.printc(s.INFO, s.GREEN + "Sim")
            SOURCES = COMMON_SOURCES + SIM_SOURCES
            for TOPLEVEL in sim_index.SIM_TOPFILES:
                s.printc(s.INFO, s.GREEN + "Simulating " + s.BLUE + TOPLEVEL)
                subprocess.run(["python3", "-m", SIM_GHDL_SCRIPT, "--stop-time=2ms", str(SOURCES), str(TOPLEVEL)])

        case "pll":
            s.printc(s.INFO, s.GREEN + "Pll")
            subprocess.run([PLL_SCRIPT, "generate"])

        case "syn":
            s.printc(s.INFO, s.GREEN + "Syn")
            SOURCES = COMMON_SOURCES + SYN_SOURCES
            TOPLEVEL = syn_index.SYN_TOPFILE
            subprocess.run(["python3", "-m", SYN_SCRIPT, str(SOURCES), str(VERILOG_SOURCES), str(TOPLEVEL)])

        case "prog":
            s.printc(s.INFO, s.GREEN + "Prog")
            subprocess.run([PROG_SCRIPT, syn_index.SYN_TOPFILE])

        case "flash":
            s.printc(s.INFO, s.GREEN + "Flash")
            subprocess.run([FLASH_SCRIPT, syn_index.SYN_TOPFILE])

        case other:
            s.printc(s.ERROR, f"no action for target '{args.action}'")
