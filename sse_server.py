import os
from server import mcp  # Your FastMCP instance
import uvicorn

# Get the SSE-compatible ASGI app
app = mcp.sse_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)