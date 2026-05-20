import os
import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from server import mcp  # your FastMCP app

app = FastAPI(title="OpenGov MCP API")

TOOLS = [
    {
        "name": "search_datasets",
        "description": "Search for datasets on the Government of Canada Open Data portal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"},
                "limit": {"type": "integer", "description": "Maximum results", "default": 5}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_dataset_metadata",
        "description": "Get detailed metadata for a specific dataset by its ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dataset_id": {"type": "string", "description": "The dataset's unique identifier"}
            },
            "required": ["dataset_id"]
        }
    },
    {
        "name": "download_dataset",
        "description": "Get a downloadable URL for a dataset resource.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "resource_id": {"type": "string", "description": "The resource (file) ID"}
            },
            "required": ["resource_id"]
        }
    }
]

class ToolCall(BaseModel):
    name: str
    arguments: dict

@app.get("/tools")
async def list_tools():
    return TOOLS

@app.post("/call")
async def call_tool(call: ToolCall):
    try:
        # FastMCP provides a built-in call_tool method
        result = await mcp.call_tool(call.name, call.arguments)
        # result is a CallToolResult, extract the text content
        if hasattr(result, "content") and result.content:
            # Return the first content item as plain text
            content_item = result.content[0]
            # If it's a TextContent, return its text
            if hasattr(content_item, "text"):
                return content_item.text
            return str(content_item)
        return str(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)