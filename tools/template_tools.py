"""
Template management tools for GNS3 MCP Server.

This module contains all tools related to GNS3 template operations:
- Listing available node templates
"""

from fastmcp import FastMCP
from config import Config
from gns3_client import GNS3Client, GNS3ClientError


def register_template_tools(mcp: FastMCP, config: Config):
    """Register all template-related tools with the MCP server."""

    @mcp.tool()
    async def list_templates() -> dict:
        """
        List all available node templates in GNS3.

        Returns:
            List of available templates for creating nodes
        """
        async with GNS3Client(config) as client:
            try:
                templates = await client.list_templates()
                return {
                    "success": True,
                    "templates": templates,
                    "count": len(templates),
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}
