#!/bin/bash
# Reapply the selected shared palette without quitting KiwiDesk.
exec /usr/bin/python3 -c 'import runpy; from pathlib import Path; d=runpy.run_path(str(Path.home()/".config/appearance/appearance.py")); s=d["state"](); d["apply"](s.get("theme","Gruvbox"),s.get("accent"))'
