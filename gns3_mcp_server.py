#!/usr/bin/env python3
"""
GNS3 MCP Server - Model Context Protocol server for GNS3 automation.

This server provides MCP tools for managing GNS3 network topologies,
including projects, nodes, links, and topology operations.
"""

from typing import Optional
from fastmcp import FastMCP
from config import load_config
from gns3_client import GNS3Client, GNS3ClientError


config = load_config()

mcp = FastMCP(
    name="GNS3 MCP Server",
    version="0.1.0",
    description="Control GNS3 network topologies via Model Context Protocol",
)


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


if __name__ == "__main__":
    mcp.run()
