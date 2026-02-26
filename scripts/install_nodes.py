#!/usr/bin/env python3
"""
Clones custom nodes listed in nodes.toml into data/custom_nodes/.
Called automatically at container startup via entrypoint.sh.
"""

import subprocess
import sys
import tomllib
from pathlib import Path

NODES_FILE = Path("/app/nodes.toml")
NODES_DIR = Path("/app/custom_nodes")
PIP = Path("/app/venv/bin/pip")


def clone_node(url: str, dest: Path) -> None:
    subprocess.run(["git", "clone", "--depth=1", url, str(dest)], check=True)


def install_requirements(node_dir: Path) -> None:
    req = node_dir / "requirements.txt"
    if req.exists():
        print(f"[install_nodes] Installing requirements for {node_dir.name}")
        subprocess.run([str(PIP), "install", "-r", str(req)], check=True)


def main() -> None:
    if not NODES_FILE.exists():
        print("[install_nodes] No nodes.toml found, skipping.")
        return

    with open(NODES_FILE, "rb") as f:
        config = tomllib.load(f)

    nodes = config.get("node", [])
    if not nodes:
        print("[install_nodes] No nodes defined, skipping.")
        return

    NODES_DIR.mkdir(parents=True, exist_ok=True)

    for node in nodes:
        url = node["url"]
        name = url.rstrip("/").split("/")[-1].removesuffix(".git")
        dest = NODES_DIR / name

        if dest.exists():
            print(f"[install_nodes] Already installed: {name}")
        else:
            print(f"[install_nodes] Cloning: {url}")
            clone_node(url, dest)
            install_requirements(dest)

    print("[install_nodes] Done.")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"[install_nodes] Error: {e}", file=sys.stderr)
        sys.exit(1)
