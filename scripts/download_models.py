#!/usr/bin/env python3
"""
Downloads models listed in models.toml into data/models/.
Run manually from the project root: python scripts/download_models.py

Requires Python 3.11+ (uses stdlib tomllib).
"""

import sys
import tomllib
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MODELS_FILE = SCRIPT_DIR.parent / "models.toml"
MODELS_DIR = SCRIPT_DIR.parent / "data" / "models"


def progress_hook(count: int, block_size: int, total_size: int) -> None:
    if total_size <= 0:
        print(f"\r  {count * block_size / 1_048_576:.1f} MB downloaded...", end="", flush=True)
        return
    pct = min(count * block_size / total_size * 100, 100)
    downloaded = min(count * block_size, total_size) / 1_048_576
    total = total_size / 1_048_576
    bar = "=" * int(pct / 2) + ">" + " " * (50 - int(pct / 2))
    print(f"\r  [{bar}] {pct:5.1f}%  {downloaded:.1f}/{total:.1f} MB", end="", flush=True)


def download(url: str, dest: Path) -> None:
    print(f"[download_models] Downloading {dest.name} -> {dest.parent.name}/")
    urllib.request.urlretrieve(url, dest, reporthook=progress_hook)
    print()  # newline after progress bar


def main() -> None:
    if not MODELS_FILE.exists():
        print("[download_models] No models.toml found.")
        sys.exit(1)

    with open(MODELS_FILE, "rb") as f:
        config = tomllib.load(f)

    models = config.get("model", [])
    if not models:
        print("[download_models] No models defined.")
        return

    for model in models:
        url = model["url"]
        destination = model["destination"]
        filename = model.get("filename") or url.rstrip("/").split("/")[-1]

        dest_dir = MODELS_DIR / destination
        dest_file = dest_dir / filename

        dest_dir.mkdir(parents=True, exist_ok=True)

        if dest_file.exists():
            print(f"[download_models] Already exists: {destination}/{filename}")
        else:
            download(url, dest_file)

    print("[download_models] Done.")


if __name__ == "__main__":
    main()
