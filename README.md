# Prometheus Alertmanager

This is a hack to get `alertmanager` into a container using `pack` so it can be deployed on Toolforge.

Runtime configuration is managed by `scripts/entrypoint.py`

## Production configuration

* `MONITORING_SEND_ALERTS_TO` - array of email addresses that alerts will be sent to
