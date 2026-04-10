import subprocess
# from fastmcp import FastMCP
from fastmcp.utilities.types import Image
import base64
import os

# I hate gi so much
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

desktop = Atspi.get_desktop(0)
for i in range(desktop.get_child_count()):
    app = desktop.get_child_at_index(i)
    print(app.get_name())

# qt_mcp = FastMCP('qt-at-spi2')
