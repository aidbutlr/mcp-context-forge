# -*- coding: utf-8 -*-
"""Location: ./mcpgateway/__init__.py
Copyright 2025
SPDX-License-Identifier: Apache-2.0
Authors: Mihai Criveti

MCP Gateway - A flexible feature-rich FastAPI-based gateway for the Model Context Protocol (MCP).
"""

__author__ = "Mihai Criveti"
__copyright__ = "Copyright 2025"
__license__ = "Apache 2.0"
__version__ = "1.0.0-RC-1"
__description__ = "IBM Consulting Assistants - Extensions API Library"
__url__ = "https://ibm.github.io/mcp-context-forge/"
__download_url__ = "https://github.com/IBM/mcp-context-forge"
__packages__ = ["mcpgateway"]

import os
from pathlib import Path
import sys

from jwcrypto import jwe, jwk

project_root = Path(__file__).resolve().parents[1]  # adjust as needed
sys.path.insert(0, str(project_root)+"/cyberfraud")
import protected_secrets

protected_secrets.get_config()
_real_getenv = os.environ.get


def custom_getenv(key, default=None):
    # Intercept read semantics here
    if key.find("PG")!=-1:
        print(f">>>>>>. getting key {key}")
    return _real_getenv(key, default)

os.environ.get = custom_getenv
