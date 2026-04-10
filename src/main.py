from fastmcp import FastMCP
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import subprocess
import keyring

from tools.desktop import desktop_mcp
from tools.terminal import term_mcp
from tools.browser import browser_mcp
from tools.blender import blender_mcp

PASSWORD = keyring.get_password('homeclaude', 'mcp-password')

class QueryAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        token = request.query_params.get("token", "")
        if token == PASSWORD:
            return await call_next(request)
        return Response("Unauthorized", status_code=401)

mcp = FastMCP("home-claude")
mcp.mount(term_mcp, 'terminal')
mcp.mount(desktop_mcp, 'desktop')
mcp.mount(browser_mcp, 'browser')
mcp.mount(blender_mcp, 'blender')

app = mcp.http_app()
app.add_middleware(QueryAuthMiddleware)

@mcp.tool()
def send_notif(msg: str, title: str = 'Claude') -> str:
    """Sends a desktop notification via notify-send"""
    proc = subprocess.run(['notify-send', title, msg])
    return "ok" if proc.returncode == 0 else f"error: {proc.returncode}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)