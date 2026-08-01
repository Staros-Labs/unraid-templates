# Unraid Templates for Scrutiny

Official Unraid Community Applications templates for [Scrutiny](https://github.com/Starosdev/scrutiny), a hard drive S.M.A.R.T monitoring dashboard.

## Templates

| Template | Image | Description |
|----------|-------|-------------|
| scrutiny-omnibus | `ghcr.io/starosdev/scrutiny:latest-omnibus` | All-in-one: web dashboard, metrics collector, and InfluxDB |
| scrutiny-web | `ghcr.io/starosdev/scrutiny:latest-web` | Web dashboard and API only (hub/spoke mode) |
| scrutiny-collector | `ghcr.io/starosdev/scrutiny:latest-collector` | S.M.A.R.T metrics collector (hub/spoke mode) |
| scrutiny-collector-zfs | `ghcr.io/starosdev/scrutiny:latest-collector-zfs` | ZFS pool health collector (amd64 only) |
| scrutiny-collector-performance | `ghcr.io/starosdev/scrutiny:latest-collector-performance` | fio drive benchmarks for throughput/IOPS/latency |

## Getting Started

The **omnibus** template is the simplest way to run Scrutiny on Unraid. It bundles everything into a single container.

For distributed deployments with multiple hosts, use the **hub/spoke** templates (web + collector(s)).

## Device Passthrough

After installing a template that requires drive access (omnibus, collector, collector-performance), add your drives:

1. Edit the container in the Unraid Docker tab
2. Click "Add another Path, Port, Variable, Label or Device"
3. Select "Device" and enter the path to each drive (e.g. `/dev/sda`, `/dev/sdb`)
4. For NVMe drives, add both the controller (`/dev/nvme0`) and namespace (`/dev/nvme0n1`)

## Support

- Issues: https://github.com/Starosdev/scrutiny/issues
- Documentation: https://github.com/Starosdev/scrutiny/tree/master/docs

## GHAS-free security baseline

`.github/workflows/security-baseline.yml` runs report-only Gitleaks, OSV-Scanner, and Trivy
filesystem or IaC checks on pull requests, pushes to `main`, and a weekly schedule. Jobs call
reusable workflows in `Staros-Labs/infra` at one exact immutable 40-character commit and
produce private, short-retention artifacts for central inventory. Caller has no workflow-level
path filters, CodeQL, SARIF uploads, or `security-events`; it does not promote branch gates.
