# GeoDiff

Sistema de detección de diferencias sobre superficies terrestres.

## Getting Started

A continuación definiremos las instrucciones para poder tener el proyecto corriendo de manera local. Ve a la sección **Instalación**.

### Prerequisitos

Para la instalación del proyecto es necesario descargar [Docker](https://docs.docker.com/desktop/)

También es necesario descargar los [TILES](https://app.box.com/s/pakte9wz7u0xfoitmktxsspbz01wsijc), que son las imagenes que conforman el mapa.

> Tip: El path donde extraigamos los resultados es conveniente asignarlo a una variable de entorno ya que luego lo utilizaremos `export TILES="/home/tiles"`

### Instalación - Docker

A continuación definiremos los pasos para correr el proyecto.

```
git clone https://github.com/mrgrassho/geo-diff
```

Una vez instalado docker es necesario activar el `swarm:mode`:

```bash
docker swarm init
```

Crear volumen, este será el medio donde se almacenarán los tiles, para ello utilizar en `device` el path de los TILES que descargamos en la etapa de Prerequisitos. Si asignaste el path a la variable `$TILES` directamente corre el siguiente comando, caso contrario reemplaza `$TILES` por la ubicación de los archivos **es necesario que el PATH sea absoluto**

```bash
docker volume create --driver local \
                    --opt type=none \
                    --opt device=$TILES \
                    --opt o=bind tiles-data
```

Buildear stack web y deployar a swarm, el script se encuentra en la folder `services`

```bash
./set_up_stack.sh docker-compose-web.yml geo-diff-web  
```

Buildear stack work y deployar a swarm

```bash
./set_up_stack.sh docker-compose-work.yml geo-diff-work  
```

### Stacks Web

| Aplicación     | Función     |
| :------------- | :------------- |
| MongoDB        | Base de Datos no relacional      |
| Mongo-Express  | Administrador de MongoDB  |
| Backend  | Tile Server (Flask) |
| Frontend  | UI Web (VueJS) |

### Stacks Work

| Aplicación     | Función     |
| :------------- | :------------- |
| RabbitMQ       | Servidor de Mesajeria   |
| Worker         | Procesador de tareas   |
| Updater        | Actualiza resultados procesados por los workers   |
| Dealer         | Repartidor de tareas a los workers   |
| Admin-Worker  | Administrador de workers, garantiza que esten activos y realiza autoscaling de workers  |

## Documentación

### Arquitectura del Sistema

![Arquitectura](diagrams/arquitecture.png)

### ¿Como funciona?

A continuación describiremos los pasos que realiza la aplicación para realizar una tarea.

> En desarrollo...

## Built With

* [RabbitMQ](https://www.rabbitmq.com/) - Message Broker
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Micro Web Server in Python
* [MongoDB](https://www.mongodb.com/es) - NoSQL Database
* [VueJS](https://vuejs.org/v2/guide/) - Frontend progressive framework
* [OpenLayers](https://openlayers.org/) - Used for Map render

## License

Este projecto esta bajo MIT License - vea el archivo [LICENSE.md](LICENSE.md) para mas detalles.