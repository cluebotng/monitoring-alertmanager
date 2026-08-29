#!/usr/bin/env python3
import os
import subprocess
from pathlib import PosixPath

WORKSPACE_DIR = PosixPath("/workspace")
TARGET_RELEASE = "0.33.0"


def download_release():
    bin_path = WORKSPACE_DIR / "bin"
    bin_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--fail",
            "-L",
            "-o",
            f"/tmp/alertmanager-{TARGET_RELEASE}.linux-amd64.tar.gz",
            (
                f"https://github.com/prometheus/alertmanager/releases/download/v{TARGET_RELEASE}/"
                f"alertmanager-{TARGET_RELEASE}.linux-amd64.tar.gz"
            ),
        ],
        check=True,
    )
    subprocess.run(
        [
            "tar",
            "-C",
            bin_path.as_posix(),
            "-xf",
            f"/tmp/alertmanager-{TARGET_RELEASE}.linux-amd64.tar.gz",
            "--strip-components=1",
            f"alertmanager-{TARGET_RELEASE}.linux-amd64/alertmanager",
        ],
        check=True,
    )
    os.remove(f"/tmp/alertmanager-{TARGET_RELEASE}.linux-amd64.tar.gz")


def main():
    if not WORKSPACE_DIR.is_dir():
        print(f"Skipping setup, workspace does not exist: {WORKSPACE_DIR}")
        return

    download_release()


if __name__ == "__main__":
    main()
