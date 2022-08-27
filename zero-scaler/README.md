## Knightly Zero-Scaler

A Kubernetes cron job that executes every night.

The script will look for all namespaces with this label:

```yaml
metadata:
  labels:
    knightly.example.com/enabled: true
```

then, it will pause all KEDA ScaledObjects by adding `pause-replicas` annotation:

```yaml
metadata:
  annotations:
    autoscaling.keda.sh/paused-replicas: "0"
```

And will finish with scaling all deployments in that namespace to 0.

More information about `autoscaling.keda.sh/paused-replicas` annotation can be found [here](https://keda.sh/docs/2.8/concepts/scaling-deployments/#pause-autoscaling).
