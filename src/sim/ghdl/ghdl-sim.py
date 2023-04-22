import argparse
import os
import subprocess
import sys
from ast import literal_eval as make_tuple
import time
from timeit import default_timer as timer

from ...util import style as s

os.system("")

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
VCD_OUTPUT = f"{SCRIPT_PATH}/wave"
OUTPUT_PATH = f"{SCRIPT_PATH}/out"
CFLAGS = "-v --std=08 -frelaxed -Wno-binding -Wno-shared"
GHDL = "ghdl"


def generate_cmd(cmd):
    # prepend output directory to the command
    cmd = f"cd {OUTPUT_PATH}; "+" ".join(cmd)
    print(cmd)
    return cmd


# parsing args
parser = argparse.ArgumentParser("ghdl-sim")
parser.add_argument("sources", nargs='?', help="source files in order")
parser.add_argument("top", nargs='?', help="top module")
parser.add_argument('-c', '--clean', dest="clean",
                    action='store_true', help="clean generated files")
parser.add_argument('-u', '--unique', dest="unique",
                    action='store_true', help="generate a unique VCD file")
parser.add_argument("--stop-time", dest="stop_time", type=str,
                    default="100us", help="simulation stop time")
args = parser.parse_args()

# clean env
subprocess.run(generate_cmd([GHDL, "--clean"]), shell=True)
subprocess.run(generate_cmd(["rm -rf", "./*"]), shell=True)
subprocess.run(generate_cmd(["rm -rf", "./../wave/*"]), shell=True)
if (args.clean == True):
    exit(0)

# create constants from args
if (args.unique == True):
    TIME_FORMAT = "%Y-%m-%d-%H-%M-%S"
    VCD_FILE = f"{VCD_OUTPUT}/wave-{time.strftime(TIME_FORMAT, time.localtime())}.vcd"
else:
    VCD_FILE = f"{VCD_OUTPUT}/wave.vcd"

SIMFLAGS = f"--stop-time={args.stop_time} --stop-delta=10000 --vcd={VCD_FILE}"
SOURCES = make_tuple(args.sources)

t = timer()

# analyzing files
s.printc(s.INFO, "running analysis")
for source in SOURCES:
    s.printc(s.INFO, f"analyzing {source}")
    try:
        result = subprocess.run(generate_cmd(
            [GHDL, "-a", CFLAGS, source]), check=True, shell=True)
    except subprocess.CalledProcessError as e:

        s.printc(s.ERROR, f"cannot analyze {source} with code {s.BLUE}{e.returncode}")
        s.printc(s.ERROR, e.cmd)
        exit(1)

# finding top file
if (args.top):
    TOP = args.top
else:
    s.printc(s.INFO, "finding top")
    try:
        result = subprocess.run(generate_cmd(
            [GHDL, "--find-top", CFLAGS]), shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        s.printc(s.ERROR, f"failed while finding top with code {s.BLUE}{e.returncode}")
        s.printc(s.ERROR, e.cmd)
        exit(1)
    else:
        if (result.stdout == None):
            s.printc(s.ERROR, result)
            s.printc(s.ERROR, f"failed to find top {s.BLUE}{result.stdout}")
            exit(1)
        else:
            TOP = result.stdout.decode('utf-8').rstrip()

s.printc(s.INFO, f"top = {s.BLUE}{TOP}")

# elaborating top
s.printc(s.INFO, "running elaboration")
try:
    result = subprocess.run(generate_cmd(
        [GHDL, "-e", CFLAGS, TOP]), check=True, shell=True)
except subprocess.CalledProcessError as e:
    s.printc(s.ERROR, f"cannot elaborate {TOP} with code {s.BLUE}{e.returncode}")
    s.printc(s.ERROR, e.cmd)
    exit(1)

# simulating
s.printc(s.INFO, "running simulation")
try:
    result = subprocess.run(generate_cmd(
        [GHDL, "-r", CFLAGS, TOP, SIMFLAGS]), check=True, shell=True)
except subprocess.CalledProcessError as e:
    s.printc(s.ERROR, f"cannot simulate {TOP} with code {s.BLUE}{e.returncode}")
    s.printc(s.ERROR, e.cmd)
    exit(1)
else:
    elapsed_time = timer() - t
    s.printc(s.INFO, f"finished simulation with code {s.BLUE}{result.returncode}")
    s.printc(s.INFO, f"simulation took {s.BLUE}{elapsed_time}s")
