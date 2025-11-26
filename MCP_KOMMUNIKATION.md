# MCP Kommunikationsablauf - Detaillierte Beschreibung

## Übersicht

Dieses Dokument beschreibt den genauen Kommunikationsablauf des Model Context Protocol (MCP) von der Benutzeranfrage bis zur Antwort.

## Beteiligte Komponenten

1. **MCP Host/Client** (z.B. Claude Desktop, Claude Code)
2. **LLM** (Large Language Model - z.B. Claude)
3. **MCP Server** (z.B. dein GNS3 MCP Server)
4. **Backend-Anwendung** (z.B. GNS3 Server)

## Architektur-Diagramm

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │         │             │
│  MCP Host   │◄───────►│     LLM     │         │ MCP Server  │◄───────►│   GNS3      │
│  (Claude)   │         │  (Claude)   │         │   (Python)  │         │   Server    │
│             │         │             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘         └─────────────┘
      │                       │                       │                       │
      │                       │                       │                       │
   stdio                   API Call              JSON-RPC 2.0            HTTP REST
```

## Phase 1: Initialisierung beim Start

### Schritt 1: MCP Host startet MCP Server

```
MCP Host (Claude Code)
   │
   ├─→ Liest Konfiguration (claude_code_config.json)
   │   {
   │     "mcpServers": {
   │       "gns3": {
   │         "command": "python3",
   │         "args": ["/home/mcj/repos/gns3_over_mcp/gns3_mcp_server.py"]
   │       }
   │     }
   │   }
   │
   ├─→ Startet Prozess: python3 gns3_mcp_server.py
   │
   └─→ Etabliert stdio-Verbindung (Standard Input/Output)
```

### Schritt 2: MCP Server initialisiert sich

```python
# gns3_mcp_server.py
config = load_config()  # Lädt gns3_config.json, .env

mcp = FastMCP(name="GNS3 MCP Server")

# Registriert alle Tools
register_project_tools(mcp, config)
register_node_tools(mcp, config)
register_link_tools(mcp, config)
register_template_tools(mcp, config)

mcp.run()  # Server läuft und wartet auf Requests
```

### Schritt 3: Initialize Handshake

**Host → Server:**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "Claude Code",
      "version": "1.0.0"
    }
  },
  "id": 0
}
```

**Server → Host:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "GNS3 MCP Server",
      "version": "0.2.0"
    }
  },
  "id": 0
}
```

### Schritt 4: Tools List Request

**Host → Server:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

**Server → Host:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "create_project",
        "description": "Create a new GNS3 project.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "path": {"type": "string"}
          },
          "required": ["name"]
        }
      },
      {
        "name": "list_projects",
        "description": "List all GNS3 projects.",
        "inputSchema": {
          "type": "object",
          "properties": {}
        }
      }
      // ... weitere 16 Tools
    ]
  },
  "id": 1
}
```

### Schritt 5: Server ist bereit

```
┌─────────────────────────────────────┐
│ MCP Server: READY                   │
│ - 18 Tools registriert              │
│ - Wartet auf Tool-Calls             │
│ - GNS3-Verbindung konfiguriert      │
└─────────────────────────────────────┘
```

## Phase 2: Benutzeranfrage

### Beispiel-Anfrage: "Liste alle GNS3 Projekte auf"

```
┌──────────────────────────────────────────────────┐
│ Benutzer gibt ein:                               │
│ "Liste alle GNS3 Projekte auf"                   │
└──────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────┐
│ 1. MCP Host empfängt User-Input                  │
│    - Speichert in Konversationshistorie          │
│    - Bereitet Anfrage an LLM vor                 │
└──────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────┐
│ 2. Host sendet an LLM (API Call):                │
│    {                                              │
│      "model": "claude-sonnet-4",                  │
│      "messages": [                                │
│        {                                          │
│          "role": "user",                          │
│          "content": "Liste alle GNS3 Projekte auf"│
│        }                                          │
│      ],                                           │
│      "tools": [                                   │
│        // Tool-Definitionen von MCP Server       │
│        {                                          │
│          "name": "list_projects",                 │
│          "description": "List all GNS3 projects." │
│        },                                         │
│        // ... weitere Tools                      │
│      ]                                            │
│    }                                              │
└──────────────────────────────────────────────────┘
```

## Phase 3: LLM Verarbeitung

```
┌──────────────────────────────────────────────────┐
│ 3. LLM (Claude) analysiert die Anfrage           │
│                                                   │
│    Input: "Liste alle GNS3 Projekte auf"         │
│           + Liste von 18 verfügbaren Tools       │
│                                                   │
│    Analyse:                                       │
│    ├─→ Benutzer möchte GNS3 Projekte auflisten   │
│    ├─→ Passendes Tool: "list_projects"           │
│    ├─→ Benötigte Parameter: keine                │
│    └─→ Tool-Call generieren                      │
└──────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────┐
│ 4. LLM generiert Tool-Call Response              │
│    {                                              │
│      "role": "assistant",                         │
│      "content": null,                             │
│      "tool_calls": [                              │
│        {                                          │
│          "id": "call_abc123",                     │
│          "type": "function",                      │
│          "function": {                            │
│            "name": "list_projects",               │
│            "arguments": "{}"                      │
│          }                                        │
│        }                                          │
│      ]                                            │
│    }                                              │
└──────────────────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────────────────┐
│ 5. Host empfängt Tool-Call vom LLM               │
│    - Extrahiert: Tool-Name "list_projects"       │
│    - Extrahiert: Argumente {}                    │
│    - Bereitet MCP-Request vor                    │
└──────────────────────────────────────────────────┘
```

## Phase 4: MCP Server Tool-Ausführung

### Schritt 6: Host sendet Tool-Call an MCP Server

**Host → Server (über stdio):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "list_projects",
    "arguments": {}
  },
  "id": 2
}
```

### Schritt 7: MCP Server empfängt und routet Request

```python
# FastMCP Framework empfängt JSON-RPC Request
# Routet zu registrierter Funktion

# In tools/project_tools.py:
@mcp.tool()
async def list_projects() -> dict:
    """List all GNS3 projects."""
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
```

### Schritt 8: Funktion wird ausgeführt

```python
# GNS3Client wird initialisiert
async with GNS3Client(config) as client:
    # config enthält:
    # - host: "localhost"
    # - port: 3080
    # - protocol: "http"
    # - auth: falls konfiguriert

    # client.list_projects() wird aufgerufen
    projects = await client.list_projects()
```

## Phase 5: Backend-Kommunikation (GNS3)

### Schritt 9: HTTP Request an GNS3 Server

```python
# In gns3_client.py
async def list_projects(self) -> List[dict]:
    url = f"{self.base_url}/v2/projects"

    # HTTP GET Request
    async with self.session.get(url) as response:
        response.raise_for_status()
        return await response.json()
```

**HTTP Request:**
```http
GET http://localhost:3080/v2/projects HTTP/1.1
Host: localhost:3080
User-Agent: Python/aiohttp
Accept: application/json
```

### Schritt 10: GNS3 Server verarbeitet Request

```
GNS3 Server:
   │
   ├─→ Empfängt GET /v2/projects
   ├─→ Authentifizierung prüfen (falls aktiviert)
   ├─→ Liest Projekt-Daten aus Datenbank
   ├─→ Scannt Projekt-Verzeichnisse
   ├─→ Sammelt Projekt-Metadaten
   └─→ Erstellt JSON Response
```

### Schritt 11: GNS3 Server sendet Response

**HTTP Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234

[
  {
    "auto_close": true,
    "auto_open": false,
    "auto_start": false,
    "drawing_grid_size": 25,
    "filename": "DemoLabor.gns3",
    "grid_size": 75,
    "name": "DemoLabor",
    "path": "/home/mcj/GNS3/projects/7c3bde8d-0d70-4314-b73d-99bc625edc80",
    "project_id": "7c3bde8d-0d70-4314-b73d-99bc625edc80",
    "scene_height": 1000,
    "scene_width": 2000,
    "show_grid": false,
    "show_interface_labels": false,
    "show_layers": false,
    "snap_to_grid": false,
    "status": "opened",
    "supplier": null,
    "variables": null,
    "zoom": 100
  },
  {
    "name": "Workshop_AOE_GNS3_MCP_Tutorial",
    "project_id": "0d1119db-e1fc-4ca2-bcc2-c380cb70881c",
    "status": "closed",
    // ... weitere Felder
  }
]
```

## Phase 6: Rückweg zum Benutzer

### Schritt 12: GNS3Client empfängt Response

```python
# In gns3_client.py
projects = await response.json()  # Parsed JSON
# projects ist jetzt eine Python-Liste mit Dictionaries
```

### Schritt 13: list_projects() formatiert Result

```python
# In tools/project_tools.py
return {
    "success": True,
    "projects": projects,  # Die empfangenen Projekte
    "count": len(projects)  # Anzahl: 2
}
```

### Schritt 14: MCP Server sendet JSON-RPC Response

**Server → Host (über stdio):**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "projects": [
      {
        "name": "DemoLabor",
        "project_id": "7c3bde8d-0d70-4314-b73d-99bc625edc80",
        "status": "opened",
        "path": "/home/mcj/GNS3/projects/7c3bde8d-0d70-4314-b73d-99bc625edc80"
      },
      {
        "name": "Workshop_AOE_GNS3_MCP_Tutorial",
        "project_id": "0d1119db-e1fc-4ca2-bcc2-c380cb70881c",
        "status": "closed",
        "path": "/home/mcj/GNS3/projects/0d1119db-e1fc-4ca2-bcc2-c380cb70881c"
      }
    ],
    "count": 2
  },
  "id": 2
}
```

### Schritt 15: Host empfängt Tool-Ergebnis

```
┌──────────────────────────────────────────────────┐
│ MCP Host (Claude Code):                          │
│ - Empfängt JSON-RPC Response                     │
│ - Matched ID 2 mit ursprünglichem Request        │
│ - Extrahiert "result" Feld                       │
│ - Bereitet für LLM auf                           │
└──────────────────────────────────────────────────┘
```

### Schritt 16: Host sendet Result zurück an LLM

**Host → LLM (API Call):**
```json
{
  "model": "claude-sonnet-4",
  "messages": [
    {
      "role": "user",
      "content": "Liste alle GNS3 Projekte auf"
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "list_projects",
            "arguments": "{}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_abc123",
      "content": "{\"success\":true,\"projects\":[...],\"count\":2}"
    }
  ]
}
```

### Schritt 17: LLM verarbeitet Result

```
┌──────────────────────────────────────────────────┐
│ LLM (Claude) analysiert Tool-Result:             │
│                                                   │
│ Input:                                            │
│ - Original User-Request                          │
│ - Tool-Call der ausgeführt wurde                 │
│ - Tool-Result (2 Projekte)                       │
│                                                   │
│ Verarbeitung:                                     │
│ ├─→ Tool-Call war erfolgreich (success: true)    │
│ ├─→ 2 Projekte gefunden                          │
│ ├─→ Projekt 1: "DemoLabor" (geöffnet)            │
│ ├─→ Projekt 2: "Workshop_AOE..." (geschlossen)   │
│ └─→ Generiere natürlichsprachige Antwort         │
└──────────────────────────────────────────────────┘
```

### Schritt 18: LLM generiert Antwort

**LLM → Host:**
```json
{
  "role": "assistant",
  "content": "Ich habe 2 GNS3 Projekte gefunden:\n\n1. **DemoLabor**\n   - Status: **geöffnet** (opened)\n   - Project ID: `7c3bde8d-0d70-4314-b73d-99bc625edc80`\n   - Pfad: `/home/mcj/GNS3/projects/7c3bde8d-0d70-4314-b73d-99bc625edc80`\n\n2. **Workshop_AOE_GNS3_MCP_Tutorial**\n   - Status: geschlossen (closed)\n   - Project ID: `0d1119db-e1fc-4ca2-bcc2-c380cb70881c`\n   - Pfad: `/home/mcj/GNS3/projects/0d1119db-e1fc-4ca2-bcc2-c380cb70881c`\n\nDas Projekt \"DemoLabor\" ist aktuell geöffnet."
}
```

### Schritt 19: Host zeigt Antwort dem Benutzer

```
┌──────────────────────────────────────────────────┐
│ Claude Code UI:                                  │
│                                                   │
│ 🤖 Ich habe 2 GNS3 Projekte gefunden:            │
│                                                   │
│ 1. DemoLabor                                      │
│    - Status: geöffnet (opened)                   │
│    - Project ID: 7c3bde8d-0d70-4314-b73d-...     │
│    - Pfad: /home/mcj/GNS3/projects/7c3b...       │
│                                                   │
│ 2. Workshop_AOE_GNS3_MCP_Tutorial                │
│    - Status: geschlossen (closed)                │
│    - Project ID: 0d1119db-e1fc-4ca2-bcc2-...     │
│    - Pfad: /home/mcj/GNS3/projects/0d11...       │
│                                                   │
│ Das Projekt "DemoLabor" ist aktuell geöffnet.    │
└──────────────────────────────────────────────────┘
```

## Vollständiger Datenfluss - Zusammenfassung

```
1. User Input
   "Liste alle GNS3 Projekte auf"
   ↓

2. MCP Host (Claude Code)
   Empfängt Input, bereitet LLM-Request vor
   ↓

3. LLM (Claude) - Erste Anfrage
   Analysiert Input + Tool-Liste
   ↓

4. LLM Response
   Tool-Call: list_projects()
   ↓

5. MCP Host
   Empfängt Tool-Call, sendet an MCP Server
   ↓

6. JSON-RPC Request
   {"method": "tools/call", "params": {"name": "list_projects"}}
   ↓ (stdio)

7. MCP Server (FastMCP)
   Empfängt Request, routet zu Funktion
   ↓

8. list_projects() Funktion
   async with GNS3Client(config) as client:
   ↓

9. GNS3Client
   HTTP GET /v2/projects
   ↓ (HTTP)

10. GNS3 Server
    Verarbeitet Request, sammelt Projekt-Daten
    ↓

11. GNS3 Response
    HTTP 200 OK + JSON Array mit Projekten
    ↑ (HTTP)

12. GNS3Client
    Parsed JSON Response
    ↑

13. list_projects()
    Formatiert Result {"success": true, "projects": [...]}
    ↑

14. MCP Server
    JSON-RPC Response mit Result
    ↑ (stdio)

15. MCP Host
    Empfängt Tool-Result
    ↑

16. LLM (Claude) - Zweite Anfrage
    Verarbeitet Tool-Result
    ↑

17. LLM Response
    Natürlichsprachige Antwort
    ↑

18. MCP Host
    Zeigt Antwort in UI
    ↑

19. User
    Sieht formatierte Projektliste
```

## Technische Details

### JSON-RPC 2.0 über stdio

MCP verwendet JSON-RPC 2.0 als Kommunikationsprotokoll über Standard Input/Output:

**Vorteile:**
- Einfache Prozess-zu-Prozess-Kommunikation
- Keine Netzwerk-Ports erforderlich
- Automatische Prozess-Lebenszyklusverwaltung
- Kein zusätzlicher HTTP-Server nötig

**Format:**
Jede Nachricht ist eine Zeile mit JSON-RPC 2.0 Format:
```
{"jsonrpc":"2.0","method":"tools/call","params":{...},"id":1}\n
```

### Asynchrone Verarbeitung

```python
# Alle GNS3Client-Operationen sind async
async with GNS3Client(config) as client:
    # Nicht-blockierende I/O
    projects = await client.list_projects()

    # Mehrere parallele Requests möglich
    projects, nodes, links = await asyncio.gather(
        client.list_projects(),
        client.list_nodes(project_id),
        client.list_links(project_id)
    )
```

### Error Handling

**Bei GNS3-Fehler:**
```python
try:
    projects = await client.list_projects()
except GNS3ClientError as e:
    return {"success": False, "error": str(e)}
```

**JSON-RPC Error Response:**
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Connection refused to GNS3 server"
  },
  "id": 2
}
```

### State Management

- **MCP Server**: Stateless - jeder Request ist unabhängig
- **LLM (Claude)**: Stateful - behält Konversationshistorie
- **MCP Host**: Vermittelt zwischen LLM und MCP Server
- **GNS3 Server**: Stateful - persistiert Projekt-Daten

### Sicherheit

1. **Lokale Kommunikation**: stdio nur innerhalb desselben Hosts
2. **Authentifizierung**: Zwischen MCP Server und GNS3 Server
3. **Keine direkte Internet-Exposition**: MCP Server läuft lokal
4. **Credential-Management**: Über .env-Dateien

## Erweiterte Szenarien

### Mehrere Tool-Calls in Serie

```
User: "Erstelle ein Projekt 'Lab1' und füge zwei Router hinzu"

1. LLM Tool-Call: create_project(name="Lab1")
   → Result: {"project_id": "abc-123"}

2. LLM Tool-Call: create_node(project_id="abc-123", name="Router1")
   → Result: {"node_id": "node-1"}

3. LLM Tool-Call: create_node(project_id="abc-123", name="Router2")
   → Result: {"node_id": "node-2"}

4. LLM generiert Zusammenfassung für User
```

### Parallele Tool-Calls

```
User: "Zeige mir alle Projekte, Nodes und Links"

LLM kann parallel aufrufen:
- list_projects()
- list_nodes(project_id)
- list_links(project_id)

Alle werden gleichzeitig ausgeführt (asyncio.gather)
```

### Error Recovery

```
1. Tool-Call schlägt fehl (z.B. GNS3 nicht erreichbar)
2. MCP Server sendet Error-Response
3. Host leitet Error an LLM weiter
4. LLM erklärt Problem dem User
5. LLM schlägt Lösung vor (z.B. "GNS3 starten")
```

## Zusammenfassung

Der MCP-Kommunikationsablauf ermöglicht eine nahtlose Integration zwischen:
- **Natürlicher Sprache** (Benutzer ↔ LLM)
- **Strukturierten Tool-Calls** (LLM ↔ MCP Server via JSON-RPC)
- **REST APIs** (MCP Server ↔ GNS3 Server via HTTP)

Dies schafft eine intuitive Schnittstelle für komplexe Netzwerk-Operationen, ohne dass der Benutzer die zugrunde liegenden APIs oder Protokolle verstehen muss.