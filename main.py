"""Entrypoint: draw the 21 November 2026 front page to /output/entry.png.

The picture is generated, not copied: gen.py renders the broadsheet
from the verified numbers baked into it. Runs with the standard
library plus Pillow, which the kit ships for this competition; no
network, no clock, no randomness, so both grader runs write the
same bytes.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gen  # noqa: E402


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    gen.build(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
# Note: gen.build asserts the layout fits 1024x1024, so a silent
# overflow can never ship as a truncated page.
