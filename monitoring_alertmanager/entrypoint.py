#!/usr/bin/env python3
import json
import os
from pathlib import PosixPath
import yaml


def generate_configuration() -> str:
    send_alerts_to = json.loads(os.environ.get("MONITORING_SEND_ALERTS_TO", "[]"))

    config = {
        "templates": [],
        "global": {
            "smtp_from": "ClueBot Monitoring <tools.cluebotng-monitoring@toolforge.org>",
            "smtp_smarthost": "mail.tools.wmcloud.org:25",
        },
        "route": {
            "group_by": ["alertname", "cluster", "service"],
            "group_wait": "30s",
            "group_interval": "5m",
            "repeat_interval": "12h",
            "receiver": "email_contacts",
            "routes": [
                {
                    "receiver": "wiki-updater",
                    "group_wait": "1m",
                    "matchers": [
                        "update_wiki_host=~.+",
                        "update_wiki_page=~.+",
                    ],
                }
            ],
        },
        "receivers": [],
    }

    # Calculate receivers
    email_contacts = {
        "name": "email_contacts",
    }
    wiki_updater = {
        "name": "wiki-updater",
        "webhook_configs": [
            {
                "send_resolved": True,
                "url": "http://wiki-update-receiver:8900/alertmanager",
            }
        ],
    }

    if send_alerts_to:
        # Email
        email_configs = [{"send_resolved": True, "to": email_address} for email_address in send_alerts_to]
        email_contacts["email_configs"] = email_configs
        wiki_updater["email_configs"] = email_configs
    else:
        # Placeholder
        email_contacts["webhook_configs"] = [{"send_resolved": False, "url": "http://invalid.host"}]

    config["receivers"] = [email_contacts, wiki_updater]

    return yaml.dump(config)


def main():
    persistent_path = PosixPath(os.environ.get("TOOL_DATA_DIR")) / "persistent-data" / "alert-manager"
    persistent_path.mkdir(parents=True, exist_ok=True)

    with open("/tmp/alertmanager.yml", "w") as fh:
        fh.write(generate_configuration())

    return os.execv(
        "/workspace/bin/alertmanager",
        [
            "/workspace/bin/alertmanager",
            "--config.file",
            "/tmp/alertmanager.yml",
            "--storage.path",
            persistent_path.absolute().as_posix(),
            "--log.level=debug",
        ],
    )


if __name__ == "__main__":
    main()
