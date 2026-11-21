"""Copy the pre-rendered front page into the grader output directory.

The image is rendered at build time by gen.py and shipped in this
repository as entry.png. Grade time does no rendering at all: it only
copies that shipped file with the standard library, so the run cannot
fail on a missing system font or a missing imaging package.
"""
import os
import shutil
from pathlib import Path


def shipped_image():
    return Path(__file__).resolve().parent / "entry.png"


def output_dir():
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    src = shipped_image()
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(src, dest)
    if dest.stat().st_size != src.stat().st_size:
        raise SystemExit("copied entry.png size mismatch")
    print("wrote", dest, dest.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
