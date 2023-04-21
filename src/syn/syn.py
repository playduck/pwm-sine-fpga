import argparse
import os
import subprocess
import sys
from ast import literal_eval as make_tuple
import time

from ..util import style as s

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
OUTPUT_PATH = f"{SCRIPT_PATH}/out"

PLUGIN_PATH = "/home/robin/share/lattice/ghdl-yosys-plugin"
LIB = f"{PLUGIN_PATH}/library"
VERILOG_WRAPPERS = (f"{LIB}/wrapper/primitives.v", f"{LIB}/wrapper/bram.v")

GHDL_FLAGS = "--std=08 -fsynopsys -fexplicit -frelaxed"
PACKAGE = "CABGA381"
NEXTPNR_FLAGS = "--45k --freq 100 --speed 6 --lpf-allow-unconstrained"
ECPPACK_FLAGS = "--compress"

GHDL = "ghdl"
YOSYS = "yosys"
NEXTPNR = "nextpnr-ecp5"
ECPPACK = "ecppack"

LPF = f"{SCRIPT_PATH}/sine.lpf"


def tuple_to_string(t: tuple) -> str:
    return " ".join(t)


# parsing args
parser = argparse.ArgumentParser("syn")
parser.add_argument("vhdl_sources", nargs='?',
                    help="VHDL source files in order")
parser.add_argument("verilog_sources", nargs='?',
                    help="Verilog source files in order")
parser.add_argument("top", nargs='?', help="top module")
parser.add_argument('-c', '--clean', dest="clean",
                    action='store_true', help="clean generated files")
args = parser.parse_args()

# clean env
subprocess.run(f"rm -rf {OUTPUT_PATH}", shell=True)
if (args.clean == True):
    exit(0)

os.mkdir(OUTPUT_PATH)

VHDL_SOURCES = make_tuple(args.vhdl_sources)
VERILOG_SOURCES = VERILOG_WRAPPERS + make_tuple(args.verilog_sources)

print(args)
TOP = args.top

s.printc(s.INFO, f"top = {s.BLUE}{TOP}")
s.printc(s.INFO, f"vhdl = {s.BLUE}{VHDL_SOURCES}")
s.printc(s.INFO, f"verilog = {s.BLUE}{VERILOG_SOURCES}")

JSON_OUT = f"{OUTPUT_PATH}/{TOP}.json"
CONFIG_OUT = f"{OUTPUT_PATH}/{TOP}.config"
SVF_OUT = f"{OUTPUT_PATH}/{TOP}.svf"
BIT_OUT = f"{OUTPUT_PATH}/{TOP}.bit"

s.printc(s.INFO, "running yosys")
try:
    cmd = f"{YOSYS} -m {GHDL} -p \" read_verilog {tuple_to_string(VERILOG_SOURCES)}; ghdl {GHDL_FLAGS} {tuple_to_string(VHDL_SOURCES)} -e {TOP}; synth_ecp5 -top {TOP} -json {JSON_OUT}\""

    print(cmd)

    result = subprocess.run(cmd, shell=True, check=True)
except subprocess.CalledProcessError as e:

    s.printc(s.ERROR, f"cannot synthesize with code {s.BLUE}{e.returncode}")
    s.printc(s.ERROR, e.cmd)
    exit(1)
else:
    s.printc(
        s.INFO, f"finished synthesis with code {s.BLUE}{result.returncode}")

s.printc(s.INFO, "running nextpnr")
try:
    cmd = f"{NEXTPNR} --json {JSON_OUT} --lpf {LPF} --textcfg {CONFIG_OUT} {NEXTPNR_FLAGS} --package {PACKAGE}"

    print(cmd)

    result = subprocess.run(cmd, shell=True, check=True)
except subprocess.CalledProcessError as e:

    s.printc(s.ERROR, f"cannot route with code {s.BLUE}{e.returncode}")
    s.printc(s.ERROR, e.cmd)
    exit(1)
else:
    s.printc(s.INFO, f"finished routing with code {s.BLUE}{result.returncode}")

s.printc(s.INFO, "running ecppack")
try:
    cmd = f"{ECPPACK} {ECPPACK_FLAGS} --svf {SVF_OUT} {CONFIG_OUT} {BIT_OUT}"

    print(cmd)

    result = subprocess.run(cmd, shell=True, check=True)
except subprocess.CalledProcessError as e:

    s.printc(s.ERROR, f"cannot pack with code {s.BLUE}{e.returncode}")
    s.printc(s.ERROR, e.cmd)
    exit(1)
else:
    s.printc(s.INFO, f"finished packing with code {s.BLUE}{result.returncode}")

s.printc(s.INFO, f"successfully created {s.BLUE}{BIT_OUT}")
