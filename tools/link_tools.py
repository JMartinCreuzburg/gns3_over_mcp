"""
Link management tools for GNS3 MCP Server.

This module contains all tools related to GNS3 link operations:
- Listing, creating, and deleting links between nodes
"""

from fastmcp import FastMCP
from config import Config
from gns3_client import GNS3Client, GNS3ClientError


def register_link_tools(mcp: FastMCP, config: Config):
    """Register all link-related tools with the MCP server."""

    @mcp.tool()
    async def list_links(project_id: str) -> dict:
        """
        List all links in a GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            List of all links in the project
        """
        async with GNS3Client(config) as client:
            try:
                links = await client.list_links(project_id)
                return {
                    "success": True,
                    "links": links,
                    "count": len(links),
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def create_link(
        project_id: str,
        node_a_id: str,
        node_a_port: int,
        node_b_id: str,
        node_b_port: int,
    ) -> dict:
        """
        Create a link between two nodes in a GNS3 project.

        Args:
            project_id: UUID of the project
            node_a_id: UUID of the first node
            node_a_port: Port number on the first node
            node_b_id: UUID of the second node
            node_b_port: Port number on the second node

        Returns:
            Created link details including link_id
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.create_link(
                    project_id, node_a_id, node_a_port, node_b_id, node_b_port
                )
                return {
                    "success": True,
                    "link": result,
                    "message": "Link created successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def delete_link(project_id: str, link_id: str) -> dict:
        """
        Delete a link from a GNS3 project.

        Args:
            project_id: UUID of the project
            link_id: UUID of the link to delete

        Returns:
            Deletion confirmation
        """
        async with GNS3Client(config) as client:
            try:
                await client.delete_link(project_id, link_id)
                return {
                    "success": True,
                    "message": f"Link {link_id} deleted successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}
