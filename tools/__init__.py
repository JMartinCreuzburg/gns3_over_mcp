"""
GNS3 MCP Server Tools - Modular tool definitions.
"""

from .project_tools import register_project_tools
from .node_tools import register_node_tools
from .link_tools import register_link_tools
from .template_tools import register_template_tools

__all__ = [
    "register_project_tools",
    "register_node_tools",
    "register_link_tools",
    "register_template_tools",
]
