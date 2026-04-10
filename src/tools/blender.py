import subprocess
from fastmcp import FastMCP
from pathlib import Path
from time import sleep

blender_mcp = FastMCP('blender')

@blender_mcp.tool()
async def blender_exec(code: str) -> str:
    """Send Python code to Blender and return the output."""
    import socket

    try:
        s = socket.socket()
        s.settimeout(10)
        s.connect(('localhost', 5555))
        s.sendall(code.encode())
        s.shutdown(socket.SHUT_WR)

        chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)

        return b''.join(chunks).decode()
    except ConnectionRefusedError:
        return "ERROR: Blender not running or addon not enabled"
    except socket.timeout:
        return "ERROR: Timeout — Blender took too long to respond"
    finally:
        s.close()