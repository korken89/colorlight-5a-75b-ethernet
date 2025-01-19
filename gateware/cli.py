import argparse
import os
import sys

from .platform.colorlight_5a_75b_v82 import Colorlight_5A75B_R82Platform
from .test.blinky import *
from .pll_timer import PllTimer

def main():
    Colorlight_5A75B_R82Platform().build(PllTimer(), do_program=True, verbose=True)


if __name__ == "__main__":
    main()
