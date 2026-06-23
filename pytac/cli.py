#!/usr/bin/env python3

# Copyright (c) 2025-2026 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause

import logging
import sys
from argparse import ArgumentParser

from . import DEFAULT_TAC_CONFIG_PATH, __version__

logger = logging.getLogger()


def _setup_logging(level):
    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def build_parser():
    parser = ArgumentParser(
        prog="pytac",
        description="Test Automation Controller (TAC/Alpaca) for Qualcomm debug boards.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    # Options shared by every subcommand.
    common = ArgumentParser(add_help=False)
    common.add_argument(
        "--serial",
        nargs="+",
        help="Debug board serial number(s)",
    )
    common.add_argument(
        "--tac-config-path",
        default=DEFAULT_TAC_CONFIG_PATH,
        help="Path to directory with TAC configs (devicelist.json + .tcnf "
        "files). Required for FTDI/PSOC boards; Bughopper boards need no configs.",
    )
    common.add_argument(
        "--log-level", default="DEBUG", help="Log level (default: DEBUG)"
    )

    subparsers = parser.add_subparsers(dest="mode", required=True, metavar="COMMAND")

    shell = subparsers.add_parser(
        "shell", parents=[common], help="Run the interactive shell"
    )
    shell.add_argument(
        "--config-file-path",
        help="Path to a single config file; use for debugging the config file syntax.",
    )

    oneshot = subparsers.add_parser(
        "oneshot", parents=[common], help="Run a single command and exit"
    )
    oneshot.add_argument("command", help="Command to run, e.g. bootToEDL")
    oneshot.add_argument(
        "value",
        nargs="?",
        help="Optional integer value for pin commands, e.g. 1",
    )
    oneshot.add_argument(
        "--config-file-path",
        help="Path to a single config file; use for debugging the config file syntax.",
    )

    service = subparsers.add_parser(
        "service", parents=[common], help="Run the REST API service"
    )
    service.add_argument(
        "--hostname",
        default="0.0.0.0",
        help="Host name the server attaches to (default: 0.0.0.0)",
    )
    service.add_argument(
        "--port",
        default=5000,
        type=int,
        help="Port on the host to attach to (default: 5000)",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    _setup_logging(args.log_level)

    if args.mode == "service":
        if not args.serial:
            parser.error("service requires --serial")
        from .service import run_service

        run_service(args.serial, args.tac_config_path, args.hostname, args.port)
    elif args.mode == "oneshot":
        if not args.serial and not args.config_file_path:
            parser.error("oneshot requires --serial or --config-file-path")
        from .shell import run_oneshot

        serial = args.serial[0] if args.serial else None
        run_oneshot(
            args.command,
            serial,
            args.config_file_path,
            args.tac_config_path,
            args.value,
        )
    else:  # shell
        if not args.serial and not args.config_file_path:
            parser.error("shell requires --serial or --config-file-path")
        from .shell import run_shell

        serial = args.serial[0] if args.serial else None
        run_shell(serial, args.config_file_path, args.tac_config_path)


if __name__ == "__main__":
    main()
