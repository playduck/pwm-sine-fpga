import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

SIM_SOURCES = (
    f"{SCRIPT_PATH}/hdl/top_tb/top_tb.vhdl",
    f"{SCRIPT_PATH}/hdl/sine_generator_tb/sine_generator_tb.vhdl",
)

SIM_TOPFILES = ("top_tb", "sine_generator_tb",)
