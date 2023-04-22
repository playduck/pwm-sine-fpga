import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

COMMON_SOURCES = (
    f"{SCRIPT_PATH}/pwm/pwm_generator.vhdl",
    f"{SCRIPT_PATH}/sine-generator/sine_lut_pkg.vhdl",
    f"{SCRIPT_PATH}/sine-generator/sine_wave_generator.vhdl",
    f"{SCRIPT_PATH}/top/top.vhdl",
)
