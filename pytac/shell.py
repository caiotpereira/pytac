# Copyright (c)i 2025-2026 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause

import logging
import sys
from cmd import Cmd

from .debugboard import Board

logger = logging.getLogger()


def make_h(name, comment=None):
    def h(cls, *args):
        print("Set GPIO value to HIGH (1) or LOW (0)")
        print("When called without parameters, GPIO is set to LOW")
        if comment:
            print(comment)

    return h


def make_f(quick_method):
    def f(cls, *args):
        quick_method.call()

    return f


class AlpacaCmd(Cmd):

    def do_quit(self, line):
        print("Quitting")
        return True

    do_EOF = do_quit


def run_shell(serial=None, config_file_path=None, tac_config_path=None):
    board = None
    if serial:
        board = Board.create_board(serial, tac_config_path)
    if config_file_path:
        board = Board.create_from_config(config_file_path)

    if board is None:
        logger.error(f"Failed to create board with serial {serial}, board not found")
        sys.exit(1)

    for pin in board.pins.values():
        method_name = f"do_{pin.command}"
        help_name = f"help_{pin.command}"
        logger.debug(f"Adding {method_name}")
        method = pin.set
        help_f = make_h(pin.command, pin.get("help_hint"))
        setattr(AlpacaCmd, method_name, method)
        setattr(AlpacaCmd, help_name, help_f)

    for name, method in board.quick_methods.items():
        method_name = f"do_{name}"
        logger.debug(f"Adding {method_name}")
        setattr(AlpacaCmd, method_name, make_f(method))

    cmd = AlpacaCmd()
    cmd.cmdloop()
