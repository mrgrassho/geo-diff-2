# AWS - Análisis de Performance

A continuación describimos los experimentos realizados.

## Parámetros

Nuevamente, definimos los parametros importantes del cluster. En esta serie de experimentos se mantienen como objetivo los parametros propios del `admin_worker` adjuntando los propios del `dealer`.

Variable | Valor* | Descripción
|--|--|--|
`admin_worker.GREY_LIGHT` | 0.2 | Si LOAD es menor al Valor de la GREY_LIGHT quiere decir que la red esta ociosa por lo tanto hay workers demás -> eliminar nodo
`admin_worker.GREEN_LIGHT` | 0.5 | Si LOAD es menor al Valor de GREEN_LIGHT quiere decir que la carga esta bien, por lo tanto no hago nada
`admin_worker.YELLOW_LIGHT` | 0.7 | Si LOAD es menor al Valor de YELLOW_LIGHT quiere decir que la carga necesitamos mas nodos -> crear nodo
`admin_worker.RED_LIGHT` | 1 | Si LOAD es menor al Valor de RED_LIGHT quiere decir que la carga necesitamos mas nodos -> crear nodo (x2)
`admin_worker.QTY_TASK` | 100 | Cuantos mensajes puede procesar un worker si afectar el rendimiento (Este es un estimado, partiendo de la premisa que un worker tarda 900ms)
`admin_worker.MAX_SCALE` | 10 | Nro. workers máximo
`admin_worker.MIN_SCALE` | 1 | Nro. workers mínimo
`admin_worker.MAX_TIMEOUT` | 120 | Cuanto tiempo tiene que esperar el worker para eliminar un container que no responde
`admin_worker.REFRESH_RATE` | 10 | Cada cuanto pide data al RabbitMQ sobre los workers
`dealer.WAIT` | 2 | Intervalo de segundos que el dealer espera antes de encolar nuevas tareas.
`dealer.BATCH` | 300 | Cantidad de tareas que el dealer encola antes de esperar los segundos definidos en `dealer.WAIT`

> *El valor definido es el default, en esta serie de iteraciones variaran depende donde, que y como lo probemos.

En los siguientes experimentos nos focalizaremos en los primordialmente en estos atributos:

- `admin_worker.MAX_SCALE`
- `admin_worker.MIN_SCALE`

Además variaremos lijeramente los siguientes atributos para evaular el rendimiento con igual cantidad de workers

- `admin_worker.REFRESH_RATE`
- `admin_worker.QTY_TASK`
- `dealer.BATCH`
- `dealer.WAIT`

**¿Por qué se incluyó al `dealer` en este estudio?**

Este script es que determina la cantidad de mensajes por segundo que se encolaran en la `TASK_QUEUE`, aumentando y disminuyendo tanto `dealer.BATCH` como `dealer.WAIT` podemos incrementar el input al cluster y asi aumentar la velocidad de proceso, siempre y cuando no colapsemos la red y los nodos `workers`.

## Instancia Amazon EC2

Utilizamos las instancias `t2.micro` principalmente por su reducido costo. Para ver mas detalles del set-up utilizado ver [Guía AWS](../AWS.md)

Instancia  | CPU virtual*  | Créditos por hora de CPU | Memoria (GiB)  |  Almacenamiento | Rendimiento de red
|--|--|--|--|--|--|
`t2.micro`  | 1  | 6  | 1  | Solo EBS | De bajo a moderado

**¿Cómo funcionan los créditos?**

Las instancias T2 reciben créditos de CPU continuamente a un índice fijo en función del tamaño de la instancia, acumulando así créditos de CPU cuando están inactivas y consumiéndolos cuando están activas. Estos créditos se pueden aplicar a la factura. Sin embargo, si los créditos se agotan, es necesario pagar costos adicionales por los excesos.

### Tipos de Hardware para Servicios

Luego de llevarnos la sorpresa de que no se puede deployar todo el stack en un nodo (se colgo la instancia y tuvimos que empezar de cero), definimos tipo de hardware para evitar que el cluster colapse a la hora de deployar. 

```yaml
version: "3.2"
services:
    rabbitmq-server:
            ...       
            resources:
                limits:
                    cpus: "0.50"
                    memory: 512M
                reservations:
                    cpus: "0.25"
                    memory: 200M

    dealer:
            ...
            resources:
                limits:
                    cpus: "0.30"
                    memory: 200M
                reservations:
                    cpus: "0.05"
                    memory: 30M
    
    updater:
            ...
            resources:
                limits:
                    cpus: "0.30"
                    memory: 200M
                reservations:
                    cpus: "0.05"
                    memory: 20M

    worker:
            ...
            resources:
                limits:
                    cpus: "0.75"
                    memory: 400M
                reservations:
                    cpus: "0.3"
                    memory: 100M

    admin-worker:
            ...
            resources:
                limits:
                    cpus: "0.5"
                    memory: 400M
                reservations:
                    cpus: "0.1"
                    memory: 50M
```

Todos estos límites y reservas de hardware fueron definidos a partir de la ejecución en localhost ([VER ANÁLISIS](./workers-performance-comparison.pdf)). Pueden no ser exactos pero dan una idea de los recursos que minimamente deben estar presentes en el cluster.

### Dataset

Utilizamos los tiles provistos ([TILES](https://app.box.com/s/pakte9wz7u0xfoitmktxsspbz01wsijc)) que rondan en el ~1.5GB de tamaño. El mismo es una colección extraida de la API de la NASA que tiene tiles con periodicidad de un mes que van del 2016-01 al 2019-12. Cada tarea ejecutada por el worker genera 3 tiles asi que lo esperado es que los datos generados ronden los ~10GB (un poco más de 8GB por aplicar redimensión y otras operaciones sobre las imágenes).

---

## Experimentos

### Experimento 1

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 2
            BATCH: 300
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 1
            REFRESH_RATE: 5
            MIN_SCALE: 8
            MAX_SCALE: 8
```

### Objetivo

En este primera iteración es exploratoria, principalmente veremos si es posible ejecutar el cluster con parametros mínimos.

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

![CPU BIN](graphics/experiment_1/service%20worker/cpu-bin.png)

![RAM](graphics/experiment_1/service%20worker/ram.png)

Excelente! Logramos ejecutar toda la stack y con un rendimiento muy bueno. Todos los servicios estan dentro de los parámetros esperados de consumo de recursos.

Ahora veamos cuanto tardaron los workers en realizar el trabajo y cuanta data generaron.

![NET I](graphics/experiment_1/service%20worker/netin.png)

Bien! Vemos que estuvimos en el orden de los 20GB (5000MB por 4 nodos worker). Vease que el gráfico es la cantidad de bytes enviados en manera acumulativa, es decir en el instante 70 se habian enviado ~5000MB.

## Experimento 2.1

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 2
            BATCH: 300
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 1
            REFRESH_RATE: 2 #
            MIN_SCALE: 12 #
            MAX_SCALE: 12 #
```

### Objetivo

En esta segunda iteración evaluaremos el rendimiento del cluster escalando la cantidad de workers y la tasa de refresco (`REFRESH_RATE`). El objetivo principal es observar si 12 es un número acorde de `geo-diff-workers`.

### Experimento 2.1 - Workers

El 20% de CPU es razonable para la cantidad de nodos disponibles y los tiempos en los que se completó el proceso (demoró 20 minutos, en el gráfico desde el minuto 120 a 140). Podríamos haber aumentado un poco mas aún la cantidad de `workers`, pero peligramos de carecer de otras funcionalidades (ejemplo: poder ejecutar un ssh en el nodo para extraer información de la ejecución).

![CPU](graphics/experiment_2.1/service%20worker/cpu-bin.png)

> Nota: El gráfico anterior se ha suavizado aplicando un promedio por grupos de 5 muestras. Su alta variación hacía imposible su visualización.

![RAM](graphics/experiment_2.1/service%20worker/ram.png)

`![NET I](graphics/experiment_2.1/service%20worker/netin.png)`

Podemos observar como la cantidad de bytes aumenta completando los ~10GB (2.5 * 4) de tiles procesados que son el resultante del dataset ya segmentado.

![NET O](graphics/experiment_2.1/service%20worker/netout.png)

## Experimento 2.2

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 2
            BATCH: 600 #
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 1
            REFRESH_RATE: 2
            MIN_SCALE: 12
            MAX_SCALE: 12
```

### Objetivo

En esta iteración vamos a estudiar que sucede si modificamos el parametro `dealer.BATCH`, esperamos que la cantidad de tareas aumente y haya mucha mas carga en la red.

### Experimento 2.2 - Dealer

![NET O](graphics/experiment_2.2/service%20dealer/netout.png)

Como podemos obervar se dió el efecto totalmente contrario al esperado, la cantidad de paquetes enviados fue menor. Es muy posible que sea ligado a la restricciones que tenemos con las máquinas `t2.micro`. En definitiva para los próximos análisis volvemos al valor de `dealer.BATCH` de 300.

**Tráfico OUT del Dealer - Experimento anterior (2.1)**

![NET O](graphics/experiment_2.1/service%20dealer/netout.png)

## Experimento 2.3

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 2
            BATCH: 600
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 1
            REFRESH_RATE: 0.2 #
            MIN_SCALE: 12
            MAX_SCALE: 12
```

### Objetivo

En esta iteración vamos a estudiar como se comportando los nodos, sin input. Trataremos de averiguar cuanto CPU% se desperdicia si no se tiene carga en el cluster, es decir averiguaremos si es útil el uso del `admin-worker`.

### Experimento 2.3 - Workers

![CPU BIN](graphics/experiment_2.3/service%20worker/cpu-bin.png)

![CPU](graphics/experiment_2.3/service%20worker/cpu.png)

![RAM](graphics/experiment_2.3/service%20worker/ram.png)

Como dijimos anteriormente, observamos que el tráfico de red durante este periodo se mantiene casi nulo es decir observamos que efectívamente no hay tarea a realizar por parte de los nodos.

![NET IN](graphics/experiment_2.3/service%20worker/netin.png)

![NET OUT](graphics/experiment_2.3/service%20worker/netout.png)

Efectivamente estamos desperdiciando ciclos de CPU, no es mucho pero por momentos llega al 5% de Uso (y con picos que superan el 20%, lo podemos observar en la Figura de CPU sin aplicar bins).

#### Pero, ¿Cuánto estamos desperdiciando si no utilizamos el autoscaling de `geo-diff-worker` en casos que este ocioso el cluster?

![AWS CREDITS COST](graphics/experiment_2.3/service%20worker/aws-screen2.png)

Cuesta 0.1 créditos cada 5 minutos (0.1/6 = 1%) por cada instancia, puede ser un número insignificante pero hay que tener en cuenta que correr el cluster con carga cuesta ~1 crédito cada 5 minutos (1/6 = 1%), si consideramos que esta prueba se extendió por ~1hr, nos termino costando 5.1 (Ver Figura abajo) créditos por instancia, lo que casi excede los 6 créditos por instancia.

![AWS CREDITS TOTAL](graphics/experiment_2.3/service%20worker/aws-screen1.png)

## Experimento 3

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 2
            BATCH: 600
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 15 #
            REFRESH_RATE: 1 #
            MIN_SCALE: 8 #
            MAX_SCALE: 12
```

### Objetivo

En esta iteración evaluaremos el comportamiento de los `geo-diff-workers` bajo la configuración definida. Lo que esperamos es que el cluster crezca y descrezca a medida que la carga aumente o decremente.

### Experimento 3 - Dealer

Observamos un claro incremento en la entrega de mensajes, los cuales rondan los 60-100 por segundo. Estos datos son extraidos de la tasa de publicación promedio de la queue `TASK_QUEUE` que es de donde los workers consumen las tareas.

![TASK QUEUE](graphics/experiment_3/service%20dealer/rabbitmq.png)

### Experimento 3 - Admin Worker

Observamos la carga total del cluster a traves de los logs del admin worker. Además de la cantidad de replicas `geo-diff-worker` activas.

![LOAD](graphics/experiment_3/service%20admin_worker/load.png)

![REPLICAS](graphics/experiment_3/service%20admin_worker/replicas.png)

Podemos ver como sobre el final la carga de tareas disminuye y por lo tanto se eliminan workers. Si lo extrapolamos al consumo de memoria y CPU (Figuras en el proximo apartado), podemos observar como repentinamente cae el uso de RAM/CPU pero vuelve a subir rápidamente, esto sospechamos que es debido a que la carga restante es repartida en los nodos que quedaron activos por lo tanto hace que se incrementen ambos parámetros.

### Experimento 3 - Workers

![CPU BIN](graphics/experiment_3/service%20worker/cpu-bin.png)

![RAM](graphics/experiment_3/service%20worker/ram.png)

## Experimento 4

En este experimento estudiaremos como se comporta el cluster bajo los siguientes parametros:

```yaml
version: "3.2"
services:
    dealer:
        ...
        environment:
            ...
            WAIT: 600 # 10 min
            BATCH: 600
            ...

    admin-worker:
        ...
        environment:
            ...
            QTY_TASK: 15 #
            REFRESH_RATE: 5 #
            MIN_SCALE: 6 #
            MAX_SCALE: 12
```

### Objetivo

El objetivo de este última iteración es distinguir entre las replicas activas y las esperadas, algo que notamos durante el analisis anterior es que no estabamos contemplando las replicas que estaban efectivamente levantadas sino que veiamos solo las replicas que deberian estar corriendo, esto porque Swarm deja en esta `PENDING` aquellas replicas que no pudo levantar pero aun asi el contador sigue desactualizado por eso fue necesario modificar el `admin-worker` para tomar la cantidad de réplicas activas.

Luego de verificar que el contador de replicas funcione correctamente, realizaremos una última corrida utilizando 6 a 12 workers y aumentando el parametro `WAIT` a 10 min.

### Experimento 4 - Admin Worker

Efectivamente estamos viendo el número correcto de replicas, y podemos ver como tarda unos segundos en actualizar las replicas activas (Ver gráfico debajo).

![REPLICAS](graphics/experiment_4/service%20admin-worker/replicas.png)

### Experimento 4 - RabbitMQ

Podemos observar como cada 10 minutos crece la carga en la queue `TASK_QUEUE`.

![LOAD](graphics/experiment_4/service%20admin-worker/load.png)

![RABBITMQ](graphics/experiment_4/service%20admin-worker/rabbitmq.png)


### Experimento 4 - Workers

Ahora chequeamos que los workers hayan estado en funciomiento, y podemos ver que también hubo picos cada 10 min aprox, momento es los que la carga de tareas aumentó.

![CPU BIN](graphics/experiment_4/service%20worker/cpu-bin.png)

![CPU](graphics/experiment_4/service%20worker/cpu.png)

![RAM](graphics/experiment_4/service%20worker/ram.png)

## Conclusiones

- **El CPU es lo importante**. Aprendimos que 5 máquinas con 1GB de RAM y 1 core, rinden mejor que una máquina con 8GB y 2 cores.
- **El autoscaling de containers no es la panacea (pero algo nos ahorramos)**. Al fin y al cabo, lo que cobra AWS (y los distintos proveedores de cloud) es créditos por hora de CPU, es decir obvio que desplegar containers a demanda va a reducir la carga de CPU de aquellas máquinas ociosas, pero el costo de CPU de una máquina ociosa es mínimo, el verdadero ahorro se lograría escalando instancias de VM en la nube, pero para ello tenemos que trabajar mucho mas y migrar a otros administradores de clusters mas robustos como Kubernetes. Aún así, el porcentaje de CPU% de máquinas ociosas corriendo `geo-diff-2_worker` ahorrado es bastante alto, (~)
- **Dockerizar y distribuir procesos es clave**. Correr este proyecto sin Swarm en la nube hubiera sido casi imposible. Podemos decir que nos las ingeniamos para aprovechar al máximo los recursos más baratos de AWS (`t2.micro` – hay instancias un poco más baratas `t2.nano` pero son casi igual que las que usamos pero con menos RAM).
