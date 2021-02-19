# AWS - Análisis de Carga

A continuación describimos los experimentos realizados

## Experimento 1

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```txt
MIN_SCALE=8
MAX_SCALE=8
...
```

### Experimento 1 - Admin Worker

![CPU](graphics/experiment_1/service%20admin-worker/cpu.png)

![RAM](graphics/experiment_1/service%20admin-worker/ram.png)

### Experimento 1 - Dealer

![CPU](graphics/experiment_1/service%20dealer/cpu.png)

![RAM](graphics/experiment_1/service%20dealer/ram.png)

### Experimento 1 - RabbitMQ

![CPU](graphics/experiment_1/service%20rabbitmq-server/cpu.png)

![RAM](graphics/experiment_1/service%20rabbitmq-server/ram.png)

### Experimento 1 - Updater

![CPU](graphics/experiment_1/service%20updater/cpu.png)

![RAM](graphics/experiment_1/service%20updater/ram.png)

### Experimento 1 - Workers

![CPU](graphics/experiment_1/service%20worker/cpu.png)

![RAM](graphics/experiment_1/service%20worker/ram.png)

## Experimento 2

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```txt
MIN_SCALE=8
MAX_SCALE=8
...
```

### Experimento 2 - Workers

![CPU](graphics/experiment_2/service%20worker/cpu.png)

![RAM](graphics/experiment_2/service%20worker/ram.png)


## Experimento 3

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```txt
MIN_SCALE=8
MAX_SCALE=8
...
```

### Experimento 3 - Workers

![CPU](graphics/experiment_3/service%20worker/cpu.png)

![RAM](graphics/experiment_3/service%20worker/ram.png)

## Experimento 4

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```txt
MIN_SCALE=8
MAX_SCALE=8
...
```

### Experimento 4 - Workers

![CPU](graphics/experiment_4/service%20worker/cpu.png)

![RAM](graphics/experiment_4/service%20worker/ram.png)

### Conclusiones

...