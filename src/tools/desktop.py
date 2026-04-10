import subprocess
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from time import sleep
import os

desktop_mcp = FastMCP('desktop')

@desktop_mcp.tool()
def take_screenshot() -> Image:
    """Take a screenshot and return it"""
    subprocess.run(['spectacle', '-f', '-o', '/tmp/screenshot.png', '-b', '-n'])
    return Image(path='/tmp/screenshot.png')

@desktop_mcp.tool()
def take_screenshot_window() -> Image:
    """Take a screenshot of a single user-selected winand return it"""
    subprocess.run(['spectacle', '-u', '-p', '-b', '-o', '/tmp/screenshot.png', '--nonotify'])
    return Image(path='/tmp/screenshot.png')

@desktop_mcp.tool()
def view(path: str) -> Image:
    """Sends you an image"""
    if not os.path.exists(path):
        raise ValueError(f'Path {path} does not exist')

    return Image(path=path)

@desktop_mcp.tool()
def run_kwin_script(script: str) -> str:
    """Run a KWin script and return output"""
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script)
        path = f.name

    script_id = subprocess.run([
        'qdbus6', 'org.kde.KWin', '/Scripting',
        'org.kde.kwin.Scripting.loadScript', path
    ], capture_output=True, text=True).stdout.strip()

    subprocess.run([
        'qdbus6', 'org.kde.KWin', '/Scripting',
        'org.kde.kwin.Scripting.start'
    ])

    os.unlink(path)
    sleep(1)
    journal = subprocess.run([
        'journalctl', '--user', '-n', '20', '--no-pager', '--since', '-2s'
    ], capture_output=True, text=True).stdout
    return f"ran script (id: {script_id})\n{journal}"

@desktop_mcp.tool()
def list_processes(filter: str = "") -> str:
    """List running processes, optionally filtered by name"""
    result = subprocess.run(
        ["ps", "-eo", "pid,ppid,user,%cpu,%mem,stat,comm", "--sort=-%cpu"],
        capture_output=True, text=True
    )
    lines = result.stdout.splitlines()
    if filter:
        lines = [l for l in lines if filter.lower() in l.lower()]
    return "\n".join(lines)
