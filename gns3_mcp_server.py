#!/usr/bin/env python3
"""
GNS3 MCP Server - Model Context Protocol server for GNS3 automation.

This server provides MCP tools for managing GNS3 network topologies,
including projects, nodes, links, and topology operations.

The tools are organized into semantic modules:
- project_tools: Project management operations
- node_tools: Node creation and control operations
- link_tools: Link/connection management operations
- template_tools: Template listing and management operations
"""

from fastmcp import FastMCP
from config import load_config
from tools import (
    register_project_tools,
    register_node_tools,
    register_link_tools,
    register_template_tools,
)


# Load configuration
config = load_config()

# Initialize FastMCP server
mcp = FastMCP(
    name="GNS3 MCP Server",
)

# Register all tool modules
register_project_tools(mcp, config)
register_node_tools(mcp, config)
register_link_tools(mcp, config)
register_template_tools(mcp, config)


if __name__ == "__main__":
    mcp.run()
