import subprocess
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from marionette_driver.marionette import Marionette
import base64
import os

browser_mcp = FastMCP('browser')

running = False
client: Marionette
proc: subprocess.Popen

#lifecycle
@browser_mcp.tool()
def open_browser() -> str:
    global running, client, proc
    if running: return 'already open'
    client = Marionette('localhost', port=2828)
    proc = subprocess.Popen(['zen-browser', '--marionette', '--profile', os.path.expanduser('~/.zen/9y543uq4.Claude'), '--no-remote'])
    client.start_session()
    running = True
    return 'opened'

@browser_mcp.tool()
def close_browser() -> str:
    global running
    if not running: return 'already closed'
    # client.quit()
    proc.kill()
    running = False
    return 'closed'

# navigation
@browser_mcp.tool()
def navigate(url: str) -> str:
    client.navigate(url)
    return 'done'

@browser_mcp.tool()
def get_page() -> str:
    """Gets the tab title and URL"""
    return f'{client.title} ({client.get_url()})'

@browser_mcp.tool()
def go_back() -> str:
    client.go_back()
    return 'done'

@browser_mcp.tool()
def go_forward() -> str:
    client.go_forward()
    return 'done'

@browser_mcp.tool()
def refresh() -> str:
    client.refresh()
    return 'done'

#content
@browser_mcp.tool()
def get_screenshot() -> Image:
    raw = base64.b64decode(client.screenshot())
    return Image(data=raw)

@browser_mcp.tool()
def page_source() -> str:
    """WARNING: Very long output!"""
    return client.page_source

@browser_mcp.tool()
def dom_get_element_info(by: str, value: str) -> str:
    el = client.find_element(by, value)
    return f"tag={el.tag_name} text={el.text} attrs visible={el.is_displayed()}"

@browser_mcp.tool()
def dom_find_elements(by: str, value: str) -> str:
    """Find all matching elements. by: 'css selector', 'id', 'xpath', 'tag name', etc."""
    els = client.find_elements(by, value)
    return '\n'.join(f"[{i}] tag={el.tag_name} text={el.text!r} visible={el.is_displayed()}" for i, el in enumerate(els))

@browser_mcp.tool()
def dom_click(by: str, value: str) -> str:
    """Click an element"""
    client.find_element(by, value).click()
    return 'clicked'

@browser_mcp.tool()
def dom_type(by: str, value: str, text: str) -> str:
    """Type text into an element (clears first)"""
    el = client.find_element(by, value)
    el.clear()
    el.send_keys(text)
    return 'typed'

@browser_mcp.tool()
def execute_script(script: str) -> str:
    """Execute JavaScript in the current page context and return the result"""
    result = client.execute_script(script)
    return str(result)

# tabs
@browser_mcp.tool()
def get_tabs() -> str:
    """List all open tabs with their index, title, and URL"""
    current = client.current_window_handle
    lines = []
    for i, handle in enumerate(client.window_handles):
        client.switch_to_window(handle)
        marker = '*' if handle == current else ' '
        lines.append(f"[{i}]{marker} {client.title} ({client.get_url()})")
    client.switch_to_window(current)
    return '\n'.join(lines)

@browser_mcp.tool()
def switch_tab(index: int) -> str:
    """Switch to a tab by its index from get_tabs()"""
    handles = client.window_handles
    if index < 0 or index >= len(handles):
        return f'index out of range (0-{len(handles)-1})'
    client.switch_to_window(handles[index])
    return f'switched to tab {index}: {client.title}'

@browser_mcp.tool()
def open_tab(url: str = '') -> str:
    """Open a new tab, optionally navigating to url"""
    client.open()
    client.switch_to_window(client.window_handles[-1])
    if url:
        client.navigate(url)
    return f'opened tab {len(client.window_handles)-1}'

@browser_mcp.tool()
def close_tab() -> str:
    """Close the current tab"""
    handles = client.window_handles
    if len(handles) <= 1:
        return 'cannot close last tab'
    client.close()
    client.switch_to_window(client.window_handles[-1])
    return 'closed'
