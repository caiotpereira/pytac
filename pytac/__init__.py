# Copyright (c) 2025-2026 Qualcomm Technologies, Inc. and/or its subsidiaries.
# SPDX-License-Identifier: BSD-3-Clause

import os

__version__ = "1.4.0"

# Configs shipped with the package; used as the default --tac-config-path.
DEFAULT_TAC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tac_configs")
