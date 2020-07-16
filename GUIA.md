# GeoDiff2

## GUIA (Sin Docker)

1. Descargar repo:

    ```bash
    git clone https://github.com/mrgrassho/geo-diff
    ```

---

### DB - Instalación

1. Descargar mongoDB
1. Ejecutar BD con:

    ```bash
    mongod
    ```

1. Ejecutar cliente de BD para agregar usuarios e insertar colecciones (seeds)

    ```bash
    cd services/db/
    mongo
    ```

1. Luego en la consola de mongo ejecutar:

    ```js
    load('mongo-init.js')
    load('seeds/filters.js')
    load('seeds/users.js')
    ```

### DB - Ejecución

1. Cada vez que quieras ejecutar la BD debes correr:

    ```bash
    mongod
    ```

---

### Backend - Instalación

1. Descargar python
1. Instalar dependencias (pip o pip3 según su versión de python instalada):

    ```bash
    cd services/backend/
    pip install -r requirements.txt
    ```

1. Descargar [TILES](https://app.box.com/s/pakte9wz7u0xfoitmktxsspbz01wsijc) y descomprimir en `services/backend/`
1. Crear archivo `.env` basandose en `.env.example`:

    ```bash
    cp .env.example .env
    ```

    Dentro del `.env` reemplazar el `DIR_TILES` por la carpeta donde se encuentran las imagenes (usar PATH relativo, ejemplo `DIR_TILES=tiles-full`). Luego reemplazar el `MONGO_URI` por la string de conexión ( ejemplo `mongodb://admin:admin@localhost:27017/geo-mongo`) esta data va a ser la misma que esta en `services/db/mongo-init.js`

#### Utilizando miniconda

1. Instalar miniconda [(LINK)](https://docs.conda.io/en/latest/miniconda.html#linux-installers)

1. Ahora vamos a crear un virtual environment:

    ```bash
    conda create -n geodiff python=3.8
    ```

1. Activamos en virtual environment:

    ```bash
    conda activate geodiff
    ```

    Instalar la dependecias del paso 1.


#### Backend - Ejecución

1. Setear variable de entorno y luego ejecutar flask:

    ```bash
    export FLASK_APP="tile_server.py"
    flask run
    ```

---

### Frontend - Instalación

1. Descargar nodeJS.
1. Instalar dependencias:

    ```bash
    npm install
    ```

1. Crear archivo `.env` basandose en `.env.example`:

    ```bash
    cd /services/frontend
    cp .env.example .env
    ```

    En este caso solo es necesario modificar `VUE_APP_MAPTILER_API_TOKEN` que es el API_TOKEN de un servidor de mapas, este lo usamos solamente para darle mas relieve a las imagenes. Para ello se deben registrar en [MapTiler](https://cloud.maptiler.com/auth/widget) y luego buscar en `API_TOKEN` y pegarlo en `VUE_APP_MAPTILER_API_TOKEN=TU_TOKEN`

### Frontend - Ejecución

1. Ejecutar vue con:

    ```bash
    npm run serve
    ```
---

## GUIA (Con Docker) - 

### Geo Web

1. Crear volumen, este será el medio donde se almacenarán los tiles
```bash
docker volume create --driver local \
                    --opt type=none \
                    --opt device=./backend/tiles-full \
                    --opt o=bind tiles-data
```

2. Buildear stack web con

```bash
docker-compose -f docker-compose-web.yml build
```

3. Deployar stack a swarm con

```bash
docker stack deploy --compose-file docker-compose-web.yml geo-diff-web
```