# KNIGHTLY

Knightly is a tool to scale all Kubernetes deployments to 0 on a daily basis.

The application consists of 3 services:

- [Commander](./commander/README.md): Slack slash command to listen to users' requests.

- [Zero-Scaler](./zero-scaler/README.md): Kubernetes cron job to scale down all deployments, and to set "pause" annotation for [KEDA ScaledObjects](https://keda.sh/docs/2.8/concepts/scaling-deployments/).

- [Annotator](./annotator/README.md): Kubernetes cron job to edit namespaces' annotations and to track number of days to keep.
