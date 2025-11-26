# GNS3 MCP Server

Model Context Protocol (MCP) server for controlling GNS3 network topologies through Claude Code and Claude Desktop.

## Features

- **Project Management**: Create, open, close, delete GNS3 projects
- **Node Operations**: Add, remove, start, stop network nodes (VMs, routers, switches)
- **Link Management**: Create and delete connections between nodes

## Requirements

- Python 3.12.3+
- GNS3 Server 2.2.55 (local or remote)
- FastMCP 2.0+
- Claude Code or Claude Desktop

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/JMartinCreuzburg/gns3_over_mcp.git
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GNS3 Connection

Create `gns3_config.json` (already exists with default localhost settings):

```json
{
  "gns3": {
    "host": "localhost",
    "port": 3080,
    "protocol": "http",
    "verify_ssl": true,
    "timeout": 30,
    "auth_required": false
  }
}
```

For remote servers with authentication, create `.env`:

```bash
cp .env.example .env
# Edit .env and add your credentials:
# GNS3_USERNAME=your_username
# GNS3_PASSWORD=your_password
# GNS3_AUTH_REQUIRED=true
```

## Integration with Claude

### Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gns3": {
      "command": "python3",
      "args": [
        "/<<path>>/gns3_over_mcp/gns3_mcp_server.py"
      ]
    }
  }
}
```

Restart Claude Desktop after updating the configuration.

### Claude Code

The server will be auto-discovered by Claude Code if you configure it via:

```bash
# Add to Claude Code MCP configuration
# The examples/claude_code_config.json shows the format
```

## Available Tools

The MCP server provides 18 tools:

### Project Management (6 tools)
- `create_project` - Create a new GNS3 project
- `list_projects` - List all projects
- `get_project` - Get project details by ID
- `open_project` - Open a closed project
- `close_project` - Close an open project
- `delete_project` - Permanently delete a project

### Node Management (5 tools)
- `list_nodes` - List all nodes in a project
- `create_node` - Create a new node (VM, router, switch, etc.)
- `delete_node` - Delete a node from project
- `start_node` - Start a specific node
- `stop_node` - Stop a specific node

### Link Management (3 tools)
- `list_links` - List all links in a project
- `create_link` - Create a link between two nodes
- `delete_link` - Delete a link

### Topology Operations (4 tools)
- `start_all_nodes` - Start all nodes in a project
- `stop_all_nodes` - Stop all nodes in a project
- `get_project_stats` - Get statistics (node count, link count, status)
- `list_templates` - List available node templates

## Usage Examples

### Via Claude Code or Claude Desktop

Once configured, you can interact with GNS3 through natural language:

```
Create a new GNS3 project called "NetworkLab"
```

```
List all available templates
```

```
Add two VPCS nodes named PC1 and PC2 to the project
```

```
Create a link between PC1 port 0 and PC2 port 0
```

```
Start all nodes in the project
```

```
Get statistics for the current project
```

```
Stop all nodes and close the project
```

## Architecture

### File Structure

```
gns3_over_mcp/
├── gns3_mcp_server.py      # Main MCP server entry point
├── gns3_client.py          # GNS3 REST API client wrapper
├── config.py               # Configuration management
├── tools/                  # Modular tool definitions
│   ├── __init__.py         # Tool module exports
│   ├── project_tools.py    # Project management (7 tools)
│   ├── node_tools.py       # Node operations (7 tools)
│   ├── link_tools.py       # Link management (3 tools)
│   └── template_tools.py   # Template operations (1 tool)
├── gns3_config.json        # GNS3 connection settings
├── .env                    # Environment variables (sensitive data)
├── .env.example            # Template for .env
├── requirements.txt        # Python dependencies
├── examples/               # Example configurations
│   ├── claude_desktop_config.json
│   └── claude_code_config.json
└── README.md               # This file
```

### Configuration Precedence

The server uses a three-layer configuration system:

1. **Environment variables** (highest priority)
2. **gns3_config.json** file
3. **Default values** (lowest priority)

This allows you to:
- Store connection settings in `gns3_config.json`
- Override with environment variables for different environments
- Keep sensitive data (passwords) in `.env` file

## Troubleshooting

### Connection Issues

**Problem**: Cannot connect to GNS3 server

**Solutions**:
1. Verify GNS3 server is running:
   ```bash
   curl http://localhost:3080/v2/version
   ```

2. Check `gns3_config.json` settings match your GNS3 server configuration

3. For remote servers, ensure authentication is configured in `.env`

### Tool Errors

**Problem**: Tools return error messages

**Solutions**:
1. Check Claude logs:
   - Linux: `~/.config/Claude/logs/`
   - Check for connection errors or API response issues

2. Verify project IDs and node IDs are correct:
   ```
   List all projects first to get valid project IDs
   ```

3. Ensure GNS3 server has necessary permissions and resources

### Template Issues

**Problem**: Cannot create nodes with specific templates

**Solutions**:
1. List available templates first:
   ```
   List all available templates
   ```

2. Use the correct `template_id` from the templates list

3. Verify the template is properly installed in GNS3

### Adding New Tools

1. Add method to `GNS3Client` in [gns3_client.py](gns3_client.py)
2. Add `@mcp.tool()` decorated function to the appropriate tool module:
   - [tools/project_tools.py](tools/project_tools.py) for project operations
   - [tools/node_tools.py](tools/node_tools.py) for node operations
   - [tools/link_tools.py](tools/link_tools.py) for link operations
   - [tools/template_tools.py](tools/template_tools.py) for template operations
   - Or create a new module in `tools/` for new categories
3. Register the new tool in the module's `register_*_tools()` function
4. Update this README with the new tool documentation

## Future Enhancements

Potential features for future versions:

- Snapshot management (create, restore, delete snapshots)
- Console access streaming
- Packet capture integration
- Node configuration import/export
- Multi-project batch operations
- Real-time status notifications
- Network diagram export
- Support for GNS3 compute nodes

## License

MIT License

## Support

For issues or questions:
- Check GNS3 documentation: https://docs.gns3.com/
- Check FastMCP documentation: https://gofastmcp.com/
- GNS3 API documentation: https://gns3-server.readthedocs.io/

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Version History

### v0.2.0 (Current)

- Refactored server into modular architecture
- Tools organized into semantic modules (project, node, link, template)
- Improved maintainability and extensibility
- Reduced main server file from 459 to 42 lines

### v0.1.0 (Initial Release)

- 18 MCP tools for GNS3 control
- Support for projects, nodes, links, and topology operations
- Configuration management with environment variables
- Claude Code and Claude Desktop integration
- Comprehensive error handling
