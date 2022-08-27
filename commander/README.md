# Knightly Commander

This is not an actual commander, it just listens to Slack slash commands.

The commander accepts one slash command - `/knightly`.

With this command you can perform the following actions:

## Start namespace

`/knightly start namespace <NAME>`

It applies knightly label and annotation on the namespace:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: true
  annotations:
    knightly.everc.com/keepmeup: "0"
```

Then it removes KEDA's `paused-replicas` annotation (that is being set when stopping a namespace).

And finally scales all deployments in the namespace to 1.

## Stop namespace

`/knightly stop namespace <NAME>`

It applies knightly label and annotation on the namespace:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: true
  annotations:
    knightly.everc.com/keepmeup: "0"
```

Then it applies KEDA's `paused-replicas` [annotation](https://keda.sh/docs/2.8/concepts/scaling-deployments/#pause-autoscaling):

```yaml
metadata:
  annotations:
    autoscaling.keda.sh/paused-replicas: "0"
```

And finally scales all deployments in the namespace to 0.

## Keep namespace

`/knightly keep  namespace <NAME> <NUM OF DAYS>`

Marks a desired namespace to stay up for X days (so the zero-scaler won't stop it) by setting `keepmeup` annotation with the desired number of days and changing the label `knightly.everc.com/enabled` to `false`:

```yaml
metadata:
  labels:
    knightly.everc.com/enabled: false
  annotations:
    knightly.everc.com/keepmeup: "0"
```

# Slack integration

To start the commander slack bot, you'll need to create new slack application and deploy it to your workspace.

Once done, create a slash command and keep the following keys: `SLACK_APP_TOKEN`, `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`.
