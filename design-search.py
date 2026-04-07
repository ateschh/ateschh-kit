"""
ATESCHH KIT — Design Engine
Wrapper script for the bundled design engine.

Usage (from project root):
  python3 design-search.py "<query>" --design-system [-p "Project Name"]
  python3 design-search.py "<query>" --domain <domain>
  python3 design-search.py "<query>" --stack <stack>

Domains: style, color, typography, ux, product, landing, chart
Stacks: react, nextjs, vue, svelte, react-native, flutter, swiftui, shadcn, ...
"""

import sys
import os

# Add the scripts directory to path so relative imports work
_engine_scripts = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "design-engine", "src", "ui-ux-pro-max", "scripts"
)
sys.path.insert(0, _engine_scripts)

# search.py uses --persist which saves files relative to cwd.
# We keep cwd as the project directory (wherever the user runs from).
# Override sys.argv[0] so argparse shows clean usage.
sys.argv[0] = "design-search.py"

# Run the search script in-process
exec(open(os.path.join(_engine_scripts, "search.py")).read(), {"__name__": "__main__"})
