"""
Node management tools for GNS3 MCP Server.

This module contains all tools related to GNS3 node operations:
- Listing, creating, and deleting nodes
- Starting and stopping individual nodes or all nodes in a project
"""

from typing import Optional
from fastmcp import FastMCP
from config import GNS3Config
from gns3_client import GNS3Client, GNS3ClientError


def register_node_tools(mcp: FastMCP, config: GNS3Config):
    """Register all node-related tools with the MCP server."""

    @mcp.tool()
    async def list_nodes(project_id: str) -> dict:
        """
        List all nodes in a GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            List of all nodes in the project
        """
        async with GNS3Client(config) as client:
            try:
                nodes = await client.list_nodes(project_id)
                return {
                    "success": True,
                    "nodes": nodes,
                    "count": len(nodes),
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def create_node(
        project_id: str,
        name: str,
        node_type: str,
        template_id: Optional[str] = None,
        x: int = 0,
        y: int = 0,
    ) -> dict:
        """
        Create a new node in a GNS3 project.

        Args:
            project_id: UUID of the project
            name: Name for the node
            node_type: Type of node (qemu, vpcs, docker, dynamips, iou)
            template_id: Optional UUID of a template to use
            x: X position in topology (default: 0)
            y: Y position in topology (default: 0)

        Returns:
            Created node details including node_id
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.create_node(
                    project_id, name, node_type, template_id, x, y
                )
                return {
                    "success": True,
                    "node": result,
                    "message": f"Node '{name}' created successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def delete_node(project_id: str, node_id: str) -> dict:
        """
        Delete a node from a GNS3 project.

        Args:
            project_id: UUID of the project
            node_id: UUID of the node to delete

        Returns:
            Deletion confirmation
        """
        async with GNS3Client(config) as client:
            try:
                await client.delete_node(project_id, node_id)
                return {
                    "success": True,
                    "message": f"Node {node_id} deleted successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def start_node(project_id: str, node_id: str) -> dict:
        """
        Start a node in a GNS3 project.

        Args:
            project_id: UUID of the project
            node_id: UUID of the node to start

        Returns:
            Node status after starting
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.start_node(project_id, node_id)
                return {
                    "success": True,
                    "node": result,
                    "message": f"Node {node_id} started successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def stop_node(project_id: str, node_id: str) -> dict:
        """
        Stop a node in a GNS3 project.

        Args:
            project_id: UUID of the project
            node_id: UUID of the node to stop

        Returns:
            Node status after stopping
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.stop_node(project_id, node_id)
                return {
                    "success": True,
                    "node": result,
                    "message": f"Node {node_id} stopped successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def start_all_nodes(project_id: str) -> dict:
        """
        Start all nodes in a GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            Status of all nodes after starting
        """
        async with GNS3Client(config) as client:
            try:
                await client.start_all_nodes(project_id)
                nodes = await client.list_nodes(project_id)
                return {
                    "success": True,
                    "message": "All nodes started successfully",
                    "nodes": nodes,
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def stop_all_nodes(project_id: str) -> dict:
        """
        Stop all nodes in a GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            Status of all nodes after stopping
        """
        async with GNS3Client(config) as client:
            try:
                await client.stop_all_nodes(project_id)
                nodes = await client.list_nodes(project_id)
                return {
                    "success": True,
                    "message": "All nodes stopped successfully",
                    "nodes": nodes,
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}
