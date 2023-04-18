import os
from glob import glob

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
PLL_SOURCES = tuple(glob(f"{SCRIPT_PATH}/pll/*.v"))
