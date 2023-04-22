import os
from glob import glob

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
VERILOG_SOURCES = tuple(glob(f"{SCRIPT_PATH}/pll/*.v"))

SYN_SOURCES = (
    f"{SCRIPT_PATH}/top_syn/top_syn.vhdl",
)

SYN_TOPFILE = "top_syn"
