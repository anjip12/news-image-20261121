#!/usr/bin/env python3
"""Entrypoint: copy the shipped front page to the output directory.

The grader runs this with no network; the image in this repository is
the entry. The output directory is created if missing and is never
deleted (it may be a mount point); only entry.png is written into it.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
# Byte-for-byte copy only: two runs of this program always produce the
# same entry.png, because the source file in the repository never
# changes at run time and no timestamps or random values are involved.
