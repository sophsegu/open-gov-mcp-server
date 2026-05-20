import os
from server import mcp
import uvicorn
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

async def health(request):
    return PlainTextResponse("ok")

app = Starlette(routes=[
    Route("/health", health),
    Mount("/", app=mcp.sse_app()),   # This serves /sse and /messages
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)