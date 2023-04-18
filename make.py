#!/usr/bin/python3

import argparse
import importlib
import os
import subprocess
import sys

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
PLL_SCRIPT = f"{SCRIPT_PATH}/src/syn/pll/gen-pll.sh"

SIM_GHDL_SCRIPT = f"{SCRIPT_PATH}/src/sim/ghdl/ghdl-sim.py"

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

COMMON_SOURCES = hdl_index.SOURCES
SIM_SOURCES = sim_index.SOURCES
PLL_SOURCES = syn_index.PLL_SOURCES

parser = argparse.ArgumentParser("pwm-sine make")
parser.add_argument("action", help="Action to perform")
args = parser.parse_args()

match args.action:
    case "clean":
        print("Clean")
        subprocess.run([PLL_SCRIPT, "clean"])
        subprocess.run([SIM_GHDL_SCRIPT, "--clean"])

    case "sim":
        print("Sim")
        SOURCES = COMMON_SOURCES + SIM_SOURCES
        subprocess.run([SIM_GHDL_SCRIPT, "--stop-time=1ms", str(SOURCES)])

    case "pll":
        print("Generating PLLs")
        subprocess.run([PLL_SCRIPT, "generate"])

    case "syn":
        SOURCES = COMMON_SOURCES
        print("Synthesis")

    case "prog":
        print("Programm")

    case "flash":
        print("Flash")

    case other:
        print(f"no action for target '{args.action}'")
