import argparse
import os
import sys

from .platform.colorlight_5a_75b_v82 import Colorlight_5A75B_R82Platform
from .test.blinky import *
from .pll_timer import PllTimer

def main():
    Colorlight_5A75B_R82Platform().build(PllTimer(), do_program=True, verbose=True)
    # plat.build(PllTimer(), do_program=False)
    # plat.build(FT600_Test(), do_program=False)

    # # Create the parser
    # my_parser = argparse.ArgumentParser(
    #     description='List the content of a folder')

    # my_parser.add_argument('Path',
    #                        metavar='path',
    #                        type=str,
    #                        help='the path to list')

    # # Execute the parse_args() method
    # args = my_parser.parse_args()

    # input_path = args.Path

    # if not os.path.isdir(input_path):
    #     print('The path specified does not exist')
    #     sys.exit()

    # print('\n'.join(os.listdir(input_path)))


if __name__ == "__main__":
    main()
