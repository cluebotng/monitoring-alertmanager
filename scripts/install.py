#!/usr/bin/env python3
import os
import subprocess
from pathlib import PosixPath


def main():
    release_version = "0.29.0"

    target_path = PosixPath("/workspace/bin")
    target_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "curl",
            "--silent",
            "--show-error",
            "--fail",
            "-L",
            "-o",
            f"/tmp/alertmanager-{release_version}.linux-amd64.tar.gz",
            f"https://github.com/prometheus/alertmanager/releases/download/v{release_version}/"
            f"alertmanager-{release_version}.linux-amd64.tar.gz",
        ],
        check=True,
    )
    subprocess.run(
        [
            "tar",
            "-C",
            target_path.as_posix(),
            "-xf",
            f"/tmp/alertmanager-{release_version}.linux-amd64.tar.gz",
            "--strip-components=1",
            f"alertmanager-{release_version}.linux-amd64/alertmanager",
        ],
        check=True,
    )
    os.remove(f"/tmp/alertmanager-{release_version}.linux-amd64.tar.gz")


if __name__ == "__main__":
    main()
