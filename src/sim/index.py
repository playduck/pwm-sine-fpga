import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

SIM_SOURCES = (
    f"{SCRIPT_PATH}/top_tb/top_tb.vhdl",
)

SIM_TOPFILE = "top_tb"
