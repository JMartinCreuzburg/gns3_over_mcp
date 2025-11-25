"""
Project management tools for GNS3 MCP Server.

This module contains all tools related to GNS3 project operations:
- Creating, listing, getting, opening, closing, and deleting projects
- Getting project statistics
"""

from typing import Optional
from fastmcp import FastMCP
from config import Config
from gns3_client import GNS3Client, GNS3ClientError


def register_project_tools(mcp: FastMCP, config: Config):
    """Register all project-related tools with the MCP server."""

    @mcp.tool()
    async def create_project(name: str, path: Optional[str] = None) -> dict:
        """
        Create a new GNS3 project.

        Args:
            name: Name for the new project
            path: Optional custom directory path for the project

        Returns:
            Project details including project_id
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.create_project(name, path)
                return {
                    "success": True,
                    "project": result,
                    "message": f"Project '{name}' created successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def list_projects() -> dict:
        """
        List all GNS3 projects.

        Returns:
            List of all projects with their details
        """
        async with GNS3Client(config) as client:
            try:
                projects = await client.list_projects()
                return {
                    "success": True,
                    "projects": projects,
                    "count": len(projects),
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def get_project(project_id: str) -> dict:
        """
        Get details of a specific GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            Project details
        """
        async with GNS3Client(config) as client:
            try:
                project = await client.get_project(project_id)
                return {
                    "success": True,
                    "project": project,
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def open_project(project_id: str) -> dict:
        """
        Open a GNS3 project.

        Args:
            project_id: UUID of the project to open

        Returns:
            Opened project details
        """
        async with GNS3Client(config) as client:
            try:
                result = await client.open_project(project_id)
                return {
                    "success": True,
                    "project": result,
                    "message": f"Project {project_id} opened successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def close_project(project_id: str) -> dict:
        """
        Close a GNS3 project.

        Args:
            project_id: UUID of the project to close

        Returns:
            Confirmation message
        """
        async with GNS3Client(config) as client:
            try:
                await client.close_project(project_id)
                return {
                    "success": True,
                    "message": f"Project {project_id} closed successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def delete_project(project_id: str) -> dict:
        """
        Delete a GNS3 project permanently.

        Args:
            project_id: UUID of the project to delete

        Returns:
            Deletion confirmation
        """
        async with GNS3Client(config) as client:
            try:
                await client.delete_project(project_id)
                return {
                    "success": True,
                    "message": f"Project {project_id} deleted successfully",
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}

    @mcp.tool()
    async def get_project_stats(project_id: str) -> dict:
        """
        Get statistics about a GNS3 project.

        Args:
            project_id: UUID of the project

        Returns:
            Statistics including node count, link count, and status information
        """
        async with GNS3Client(config) as client:
            try:
                stats = await client.get_project_stats(project_id)
                return {
                    "success": True,
                    "stats": stats,
                }
            except GNS3ClientError as e:
                return {"success": False, "error": str(e)}
