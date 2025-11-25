"""
GNS3 REST API client wrapper using httpx.
Provides async methods for all GNS3 operations.
"""

import httpx
from typing import Optional, Dict, Any, List
from config import GNS3Config


class GNS3ClientError(Exception):
    """Custom exception for GNS3 API errors."""
    pass


class GNS3Client:
    """Async client for GNS3 REST API v2."""

    def __init__(self, config: GNS3Config):
        self.config = config
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        auth = None
        if self.config.auth_required and self.config.username:
            auth = (self.config.username, self.config.password)

        self.client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            verify=self.config.verify_ssl,
            auth=auth,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to GNS3 API with error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for httpx request

        Returns:
            Response JSON as dictionary

        Raises:
            GNS3ClientError: On API errors
        """
        if not self.client:
            raise GNS3ClientError("Client not initialized. Use async context manager.")

        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()

            if response.status_code == 204 or not response.content:
                return {"success": True}

            return response.json()

        except httpx.HTTPStatusError as e:
            error_msg = f"GNS3 API error: {e.response.status_code}"
            try:
                error_detail = e.response.json()
                error_msg += f" - {error_detail.get('message', str(error_detail))}"
            except:
                error_msg += f" - {e.response.text}"
            raise GNS3ClientError(error_msg) from e

        except httpx.RequestError as e:
            raise GNS3ClientError(f"Connection error: {str(e)}") from e

    async def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        return await self._request("GET", "/projects")

    async def create_project(
        self,
        name: str,
        path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new project."""
        data = {"name": name}
        if path:
            data["path"] = path
        return await self._request("POST", "/projects", json=data)

    async def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details."""
        return await self._request("GET", f"/projects/{project_id}")

    async def open_project(self, project_id: str) -> Dict[str, Any]:
        """Open a project."""
        return await self._request("POST", f"/projects/{project_id}/open")

    async def close_project(self, project_id: str) -> Dict[str, Any]:
        """Close a project."""
        return await self._request("POST", f"/projects/{project_id}/close")

    async def delete_project(self, project_id: str) -> Dict[str, Any]:
        """Delete a project."""
        return await self._request("DELETE", f"/projects/{project_id}")

    async def list_nodes(self, project_id: str) -> List[Dict[str, Any]]:
        """List all nodes in a project."""
        return await self._request("GET", f"/projects/{project_id}/nodes")

    async def create_node(
        self,
        project_id: str,
        name: str,
        node_type: str,
        template_id: Optional[str] = None,
        x: int = 0,
        y: int = 0,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new node in a project."""
        data = {
            "name": name,
            "node_type": node_type,
            "x": x,
            "y": y,
        }
        if template_id:
            data["compute_id"] = "local"
            data["template_id"] = template_id
        if properties:
            data["properties"] = properties

        return await self._request("POST", f"/projects/{project_id}/nodes", json=data)

    async def delete_node(self, project_id: str, node_id: str) -> Dict[str, Any]:
        """Delete a node from a project."""
        return await self._request("DELETE", f"/projects/{project_id}/nodes/{node_id}")

    async def start_node(self, project_id: str, node_id: str) -> Dict[str, Any]:
        """Start a node."""
        return await self._request("POST", f"/projects/{project_id}/nodes/{node_id}/start")

    async def stop_node(self, project_id: str, node_id: str) -> Dict[str, Any]:
        """Stop a node."""
        return await self._request("POST", f"/projects/{project_id}/nodes/{node_id}/stop")

    async def start_all_nodes(self, project_id: str) -> Dict[str, Any]:
        """Start all nodes in a project."""
        return await self._request("POST", f"/projects/{project_id}/nodes/start")

    async def stop_all_nodes(self, project_id: str) -> Dict[str, Any]:
        """Stop all nodes in a project."""
        return await self._request("POST", f"/projects/{project_id}/nodes/stop")

    async def list_links(self, project_id: str) -> List[Dict[str, Any]]:
        """List all links in a project."""
        return await self._request("GET", f"/projects/{project_id}/links")

    async def create_link(
        self,
        project_id: str,
        node_a_id: str,
        node_a_port: int,
        node_b_id: str,
        node_b_port: int,
    ) -> Dict[str, Any]:
        """Create a link between two nodes."""
        nodes = await self.list_nodes(project_id)
        node_a = next((n for n in nodes if n["node_id"] == node_a_id), None)
        node_b = next((n for n in nodes if n["node_id"] == node_b_id), None)

        if not node_a or not node_b:
            raise GNS3ClientError("One or both nodes not found")

        data = {
            "nodes": [
                {
                    "node_id": node_a_id,
                    "adapter_number": 0,
                    "port_number": node_a_port,
                },
                {
                    "node_id": node_b_id,
                    "adapter_number": 0,
                    "port_number": node_b_port,
                },
            ]
        }
        return await self._request("POST", f"/projects/{project_id}/links", json=data)

    async def delete_link(self, project_id: str, link_id: str) -> Dict[str, Any]:
        """Delete a link from a project."""
        return await self._request("DELETE", f"/projects/{project_id}/links/{link_id}")

    async def list_templates(self) -> List[Dict[str, Any]]:
        """List all available templates."""
        return await self._request("GET", "/templates")

    async def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        """Get project statistics."""
        project = await self.get_project(project_id)
        nodes = await self.list_nodes(project_id)
        links = await self.list_links(project_id)

        node_status = {}
        for node in nodes:
            status = node.get("status", "unknown")
            node_status[status] = node_status.get(status, 0) + 1

        return {
            "project_id": project_id,
            "project_name": project.get("name"),
            "status": project.get("status"),
            "total_nodes": len(nodes),
            "total_links": len(links),
            "node_status": node_status,
        }
