import subprocess
from fastmcp import FastMCP
from pathlib import Path
from time import sleep

term_mcp = FastMCP('terminal')

def is_term_open() -> bool:
    return Path('/tmp/homeclaude-kitty').exists()

@term_mcp.tool()
def term_open() -> str:
    """Opens a Clade terminal if it's not already open"""
    if is_term_open(): return 'terminal already open'
    subprocess.Popen([
        'kitty', '--listen-on', 'unix:/tmp/homeclaude-kitty', '-d', '/home/wojtmic/claude-corner', '--title', "Claude's Private Terminal"
    ])
    sleep(0.5)
    subprocess.run(['kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty', 'send-text', '/home/wojtmic/claude-corner/.clauderc\n'])
    return term_read()

@term_mcp.tool()
def term_kill() -> str:
    """Kills/closes the Claude terminal"""
    if not is_term_open(): return 'terminal not open'
    subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'close-window',
    ])
    return "closed"

@term_mcp.tool()
def term_switch_tab(tab_id: int) -> str:
    """Switches the active term tab"""
    if not is_term_open(): return 'terminal not open'

    proc = subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'focus-tab', '--match', f'id:{str(tab_id)}'
    ], capture_output=True, text=True)
    return proc.stdout

@term_mcp.tool()
def term_open_tab(change_focus: bool = True, cmd: str = 'zsh') -> str:
    """Opens a new term tab"""
    if not is_term_open(): return 'terminal not open'

    if change_focus:
        proc = subprocess.run([
            'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
            'launch', '--type=tab', cmd
        ], capture_output=True, text=True)
    else:
        proc = subprocess.run([
            'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
            'launch', '--type=tab', '--keep-focus', cmd
        ], capture_output=True, text=True)
    return proc.stdout

@term_mcp.tool()
def term_kill_tab(tab_id: int) -> str:
    """Kills/closes a term tab"""
    if not is_term_open(): return 'terminal not open'

    proc = subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'close-tab', '--match', f'id:{str(tab_id)}'
    ], capture_output=True, text=True)
    return proc.stdout

@term_mcp.tool()
def term_get_tabs() -> str:
    """Get list of all tabs"""
    if not is_term_open(): return 'terminal not open'

    proc = subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'ls'
    ], capture_output=True, text=True)
    return proc.stdout

@term_mcp.tool()
def term_send(cmd: str, newline: bool=True) -> str:
    """Send a command to the Claude terminal"""
    if not is_term_open(): return 'terminal not open'
    if newline:
        subprocess.run([
            'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
            'send-text',
            cmd + '\n'
        ])
    else:
        subprocess.run([
            'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
            'send-text',
            cmd
        ])
    return "sent"

@term_mcp.tool()
def term_key(key_combo: str) -> str:
    """Sends a key combo, use + to separate keys"""
    if not is_term_open(): return 'terminal not open'
    subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'send-key',
        key_combo
    ])
    return "send"

@term_mcp.tool()
def term_read() -> str:
    """Read current terminal screen contents"""
    if not is_term_open(): return 'terminal not open'
    proc = subprocess.run([
        'kitten', '@', '--to', 'unix:/tmp/homeclaude-kitty',
        'get-text'
    ], capture_output=True, text=True)
    return proc.stdout
