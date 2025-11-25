"""
Configuration management for GNS3 MCP Server.
Handles loading from environment variables and config files.
"""

import json
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class GNS3Config:
    """GNS3 server connection configuration."""
    host: str = "localhost"
    port: int = 3080
    protocol: str = "http"
    verify_ssl: bool = True
    timeout: int = 30
    auth_required: bool = False
    username: Optional[str] = None
    password: Optional[str] = None

    @property
    def base_url(self) -> str:
        """Construct the base URL for GNS3 API."""
        return f"{self.protocol}://{self.host}:{self.port}/v2"


def load_config() -> GNS3Config:
    """
    Load configuration with precedence:
    1. Environment variables (highest)
    2. gns3_config.json file
    3. Defaults (lowest)
    """
    load_dotenv()

    config_path = os.getenv("GNS3_CONFIG_PATH", "gns3_config.json")
    config_data = {}

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_data = json.load(f).get("gns3", {})

    return GNS3Config(
        host=os.getenv("GNS3_HOST", config_data.get("host", "localhost")),
        port=int(os.getenv("GNS3_PORT", config_data.get("port", 3080))),
        protocol=os.getenv("GNS3_PROTOCOL", config_data.get("protocol", "http")),
        verify_ssl=os.getenv("GNS3_VERIFY_SSL",
                           str(config_data.get("verify_ssl", True))).lower() == "true",
        timeout=int(os.getenv("GNS3_TIMEOUT", config_data.get("timeout", 30))),
        auth_required=os.getenv("GNS3_AUTH_REQUIRED",
                              str(config_data.get("auth_required", False))).lower() == "true",
        username=os.getenv("GNS3_USERNAME"),
        password=os.getenv("GNS3_PASSWORD"),
    )
