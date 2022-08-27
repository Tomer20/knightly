# Knightly Annotator

A Kubernetes cron job that executes every morning.

The annotator will work on all namespaces without knightly `excluded` or `true` labels:

```yaml
metadata:
  labels:
    knightly.example.com/enabled: excluded
```

```yaml
metadata:
  labels:
    knightly.example.com/enabled: true
```

For each namespace found, it will check the value of the `keepmeup` annotation:

```yaml
metadata:
  annotations:
    knightly.example.com/keepmeup: "4"
```

In this case, it will change the value to `3`, to count 3 more days.

Once reached `1`, it will set the label `knightly.example.com/enabled=true` and the namespace will be stopped on the following night.

If the label or the annotation are not set, it will add them to enable knightly:

```yaml
metadata:
  labels:
    knightly.example.com/enabled: true
  annotations:
    knightly.example.com/keepmeup: "0"
```

So make sure to label system namespaces (like `monitoring`, `kube-system`) with `knightly.example.com/enabled=excluded`.
