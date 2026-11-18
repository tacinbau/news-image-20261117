"""Copy the finished newspaper image into make.fun's requested output folder."""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).with_name("entry.png")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    if source.stat().st_size != destination.stat().st_size:
        raise RuntimeError("The copied image size does not match the source.")


if __name__ == "__main__":
    main()
