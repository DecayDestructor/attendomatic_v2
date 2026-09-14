# Attendomatic Setup

## Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- Node.js 22.19.0 or newer for MCP Inspector

## 1. Install dependencies

From the project root, run:

```bash
uv sync
```

## 2. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name

METADATA_JSON_RESPONSE=

SCALEKIT_CLIENT_ID=
SCALEKIT_ENVIRONMENT_URL=
SCALEKIT_CLIENT_SECRET=

SCALEKIT_RESOURCE_METADATA_URL=
SCALEKIT_RESOURCE_NAME=
SCALEKIT_AUDIENCE_NAME=
```

`DATABASE_URL` should contain your PostgreSQL connection string.

The Scalekit variables are required for OAuth authentication and authorization when using Attendomatic through MCP.

## 3. Run the application

Start the FastAPI application with:

```bash
uv run fastapi dev src/attendomatic/main.py
```

The application will be available at:

```text
http://127.0.0.1:8000
```

The MCP endpoint is:

```text
http://127.0.0.1:8000/mcp
```

## 4. Debug locally with MCP Inspector

MCP Inspector can be used to connect to and debug the local MCP server.

With the FastAPI application running, open another terminal and run:

```bash
npx @modelcontextprotocol/inspector@latest
```

Then open the Inspector UI and connect it to:

```text
http://127.0.0.1:8000/mcp
```

You can use the Inspector to inspect the server, view available tools, and test tool calls during development.

## Architecture

Attendomatic follows a layered architecture:

```text
MCP Tools
    ↓
Services
    ↓
Repositories
    ↓
PostgreSQL
```

MCP tools expose functionality to the LLM, services contain the business logic, and repositories handle database interaction.

This keeps the core application logic decoupled from the MCP interface and makes the system easier to extend.
