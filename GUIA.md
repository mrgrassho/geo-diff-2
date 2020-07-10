# GeoDiff2

## GUIA PROVISORIA (Sin Docker)

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
1. Instalar dependencias:

    ```bash
    cd services/backend/
    pip install -r requirements
    ```

1. Descargar [TILES](https://app.box.com/s/pakte9wz7u0xfoitmktxsspbz01wsijc) y descomprimir en `services/backend/`
1. Crear archivo `.env` basandose en `.env.example`:

    ```bash
    cp .env.example .env
    ```

    Dentro del `.env` reemplazar el `DIR_TILES` por la carpeta donde se encuentran las imagenes (usar PATH relativo, ejemplo `DIR_TILES=tiles-full`). Luego reemplazar el `MONGO_URI` por la string de conexión ( ejemplo `mongodb://admin:admin@localhost:27017/geo-mongo`) esta data va a ser la misma que esta en `services/db/mongo-init.js`

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