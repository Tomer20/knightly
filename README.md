# KNIGHTLY

Knightly is a tool to scale all kubernetes deployments to 0 on a daily basis.

The application consists of 3 services:

- [Controller](#controller): Slack slash command

- [Zero-Scaler](#zero-scaler): Kubernetes cron job to scale down all deployments, and set "pause" annotation for [KEDA ScaledObjects](https://keda.sh/docs/2.8/concepts/scaling-deployments/)

- [Annotator](#annotator): Kubernetes cron job to edit namespaces' annotations

## Controller

Slack bot, based on bolt library.

The bot has the following commands:

- `/knightly-dev` with the following options:

    - `start namespace <NAME>`: will start a desired namespce. scale all replicas to 1 and enable keda

    - `stop  namespace <NAME>`: will stop a desired namespce. scale all replicas to 0 and disable keda

    - `keep  namespace <NAME> <NUM OF DAYS>`: will set a desired namespace to stay up for X days

## Zero-Scaler

A kubernetes cron job that executes every night.

The script will look for all namespaces with this label:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: true
```

then, it will scale all deployments in that namespace to 0.

If there are KEDA ScaledObjects, they will be paused by adding this annotation:

```yaml
metadata:
  annotations:
    autoscaling.keda.sh/paused-replicas: "0"
```

More inforemation about `autoscaling.keda.sh/paused-replicas` annotation can be found [here](https://keda.sh/docs/2.8/concepts/scaling-deployments/#pause-autoscaling).

## Annotator

A kubernetes cron job that executes every morning.

The annotator will work on all namespaces without knightly `excluded` or `true` labels:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: true
    knightly.everc.com/enabled: excluded
```

For each namespace found, it will check the value of the `keepmeup` annotation:

```yaml
metadata:
  annotations:
    knightly.everc.com/keepmeup: "4"
```

In this case, it will change the value to `3`, to count 3 more days.

Once reached `1`, it will set the label `knightly.everc.com/enabled=true`.

If no number of days, the label and annotation are probably not set, so we will add them to enable knightly:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: true
  annotations:
    knightly.everc.com/keepmeup: "0"
```
