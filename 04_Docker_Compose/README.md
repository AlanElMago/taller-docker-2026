# Sección 4: Uso de Docker Compose para orquestar múltiples contenedores

Imagine que desea conectar su aplicación de Flask a una base de datos para mantener el conteo de visitas a la página. Una solución sería instalar una base de datos en su máquina local y configurar la aplicación Flask para conectarse a esa base de datos. Sin embargo, ¿qué sucede si deseo desplegar mi aplicación a un servidor en la nube o compartir mi aplicación con otros desarrolladores? En ese caso, será necesario que el servidor y las máquinas de los desarrolladores tengan la misma instalación y configuración de la base de datos, lo cuál puede provocar dolores de cabeza.

Para resolver este problema, podemos usar Docker para crear una imágen de Docker para la base de datos y ejecutar un contenedor con esa imagen. Tal contenedor se puede compartir fácilmente con otros desarrolladores o desplegar a un servidor en la nube. Sin embargo, administrar múltiples contenedores de Docker puede volverse complicado rápidamente. Para esto, Docker Compose es una herramienta que nos permite definir y administrar múltiples contenedores de Docker utilizando un archivo de configuración YAML. Esta administración de contenedores con Docker Compose se conoce como **orquestación**.

En esta sección, utilizaremos Docker Compose para orquestar dos contenedores de Docker: uno para la aplicación Flask y otro para la base de datos Redis. La aplicación Flask se conectará a la base de datos Redis para mantener y mostrar el conteo de visitas a la página.

Para evitar construir una imágen para un gestor de base de datos (DBMS) desde cero, se hará uso de una imágen de Docker del DBMS de Redis. Esta imagen ya existe en un repositorio público de imágenes Docker llamado Docker Hub, y lo único que se necesita hacer es descargarla y ejecutar un contenedor con esa imagen.

## 1. Mover el contenido del proyecto a la carpeta `webapp`

Cuando se comienza a trabajar en proyectos con múltiples contenedores, es una buena práctica organizar el contenido del proyecto en carpetas, donde cada carpeta corresponde a un contenedor. Para esto, crea una carpeta llamada `webapp` en el directorio base del proyecto y mueve el contenido del proyecto (archivos `app.py`, `requirements.txt`, `Dockerfile`, carpetas `static` y `templates`) a la carpeta `webapp`.

## 2. Crear el archivo `docker-compose.yml`

Crea un archivo llamado `docker-compose.yml` en el directorio base del proyecto y agrega el siguiente contenido:

```yaml
services:
  webapp:
    build: ./webapp
    image: mi-webapp:latest
    container_name: mi-webapp
    ports:
      - 80:5000

  redis:
    image: redis:7-alpine
    container_name: mi-redis
```

Antes de continuar, es importante entender cada una de las secciones en el archivo `docker-compose.yml`:

- `services`: Es la sección principal del archivo `docker-compose.yml` donde se definen los servicios (contenedores) que forman parte del sistema, conocido como **stack**.
- `webapp` y `redis`: Son los nombres de los servicios que se están definiendo. Estos nombres se pueden usar para referenciar los servicios dentro del archivo `docker-compose.yml` y también se utilizan para nombrar los contenedores cuando se ejecutan. Se puede definir cualquier nombre para los servicios, pero es recomendable usar nombres descriptivos que reflejen la función del servicio.
- `build`: Especifica la ruta al directorio donde se encuentra el `Dockerfile` para construir la imagen del servicio. En este caso, se indica que el `Dockerfile` para el servicio `webapp` se encuentra en la carpeta `./webapp`.
- `container_name`: Especifica el nombre que se asignará al contenedor cuando se ejecute. Esto es útil para identificar fácilmente a los contenedores.
- `ports`: Especifica las reglas de mapeo de puertos entre el contenedor y la máquina host. En este caso, el puerto 5000 del contenedor `webapp` se mapea al puerto 80 de la máquina host. No se le asigna un puerto a `redis` (esto se explicará más adelante).

Una vez creado el archivo, la organización del proyecto debería verse de la siguiente manera:

```
.
├── .venv/
├── docker-compose.yml
├── webapp/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── static/
│   │   └── styles.css
│   └── templates/
│       └── index.html
```

## 3. Construcción de las imágenes y ejecución de los contenedores usando Docker Compose

Para construir las imágenes y ejecutar los contenedores definidos en el archivo `docker-compose.yml`, ejecuta el siguiente comando en la terminal:

```bash
docker compose up --build
```

El comando `docker compose up` levanta los servicios definidos en el archivo `docker-compose.yml`. La opción `--build` indica que se deben construir las imágenes antes de levantar los contenedores. Si las imágenes ya han sido construidas previamente y no se han realizado cambios en el código, se puede omitir la opción `--build` para acelerar el proceso.

Cuando se ejecuta este comando, ocurren dos cosas:

1. Docker Compose construye la imagen para el servicio `webapp` utilizando el `Dockerfile` ubicado en `./webapp`.
2. Docker Compose descarga la imagen `redis:7-alpine` para el servicio `redis` desde Docker Hub.

Posteriormente, Docker Compose levanta dos contenedores: uno para la aplicación Flask (`webapp`) y otro para la base de datos Redis (`redis`). En el terminal se mostrarán los logs de ambos contenedores, lo que permite monitorear el estado de cada servicio. Para salir de los logs de los contenedores, presionen la tecla `d` en el terminal. Los contenedores seguirán ejecutándose en segundo plano después de salir de los logs. Pueden usar `docker ps` para verificar que ambos contenedores todavía están en ejecución.

Se logró levantar la aplicación de Flask y la base de datos Redis utilizando Docker Compose. Sin embargo, todavía falta conectar el contenedor de `mi-webapp` con el contenedor de `mi-redis` para que la aplicación Flask pueda interactuar con la base de datos Redis. Para esto, se debe realizar dos cosas:

1. Crear una red de Docker para que ambos contenedores puedan comunicarse entre sí.
2. Modificar el código de la aplicación Flask para que se conecte a la base de datos Redis para posteriormente mostrar y actualizar el conteo de visitas a la página.

Antes de continuar, detendremos la ejecución de los contenedores dentro del stack y los eliminaremos con el siguiente comando:

```bash
docker compose down
```

> [!NOTE]
> Para detener los contenedores sin eliminarlos, se puede usar el siguiente comando:
> ```bash
> docker compose stop
> ```
> y se puede volver a levantar los contenedores detenidos con el siguiente comando:
> ```bash
> docker compose start
> ```

## 4. Definir una red de Docker para la comunicación entre contenedores

Las redes de Docker utilizan un controlador de red para gestionar la comunicación entre contenedores. Los tres controladores más comunes que se puede aplicar a un contenedor son:

- `none`: El contenedor esta completamente aislado del host y de otros contenedores.
- `host`: El contenedor comparte la red del host. El aislamiento entre el contenedor y el host se pierde.
- `bridge`: El contenedor se conecta a una red virtual creada por Docker. Esta red está aislada del host y de otras redes virtuales. Esta es la opción predeterminada para los contenedores de Docker.

En este paso, se creará una red de Docker `bridge` para que los contenedores `mi-webapp` y `mi-redis` puedan comunicarse entre sí. Para esto, agrega la siguiente sección al archivo `docker-compose.yml`:

```diff
services:
  webapp:
    build: ./webapp
    image: mi-webapp:latest
    container_name: mi-webapp
    ports:
      - 80:5000
+   networks:
+     - mi-red

  redis:
    image: redis:7-alpine
    container_name: mi-redis
+   networks:
+     - mi-red

+networks:
+  mi-red:
+    driver: bridge
```

La sección `networks` (el que está al mismo nivel que `services`) define la red de Docker llamada `mi-red` utilizando el controlador `bridge`. Luego, en cada servicio (`webapp` y `redis`), se especifica que el servicio se conecta a la red `mi-red`. Esto permite que ambos contenedores puedan comunicarse entre sí.

## 5. Modificar `index.html` para mostrar el conteo de visitas a la página

Agregarmos el siguiente comentario y elemento HTML a `index.html` para mostrar el conteo de visitas a la página:

```diff
...
      <!-- Lenguaje de programación favorito -->
      <section class="about-box">
        <h2>Mi Lenguaje de Programación Favorito</h2>
        <p>
          <strong>C</strong> es mi lenguaje de programación favorito. Es un
          lenguaje de bajo nivel que me permite entender cómo funcionan las
          cosas a nivel de hardware. Además, sirve como buen fundamento para
          aprender otros lenguajes de programación.
        </p>
      </section>
+
+     <!-- Contador de visitas -->
+     <!-- <p>Esta página ha sido visitada <strong>{{ visits }}</strong> veces.</p> -->
    </main>
...
```

La variable `{{ visits }}` es una variable de plantilla que se renderizará con el conteo de visitas a la página. Por ahora, esta variable no tiene ningún valor asignado, pero se le asignará un valor en el siguiente paso al modificar el código de `app.py`.

## 6. Modificar `app.py` para conectarse a Redis, consultar y actualizar el conteo de visitas a la página

Agregaremos el siguiente código a `app.py` para conectarnos a Redis, consultar y actualizar el conteo de visitas a la página:

```diff
from flask import Flask, render_template
+import redis

app = Flask(__name__)

+# Conectarse a Redis
+redis_host = 'redis'
+redis_port = 6379
+redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.route('/')
def index():
+   # Incrementar el contador de visitas a la página
+   visits = redis_client.incr('visits')
-   return render_template('index.html')
+   return render_template('index.html', visits=visits)
```

El código que se añadió hace tres cosas principales:
1. Importa el módulo `redis` para poder interactuar con la base de datos Redis.
2. Se crea un cliente de Redis utilizando la clase `Redis` del módulo `redis`. Se especifica el host y el puerto de Redis para establecer la conexión.
3. Se inicializa la variable `visits` con el resultado de la función `incr` del cliente de Redis, la cual incrementa el valor almacenado en la clave `visits` y devuelve el nuevo valor. Luego, se pasa la variable `visits` a la plantilla `index.html` para que se pueda mostrar el contador de visitas a la página.

> [!NOTE]
> **¿Por qué se usa `redis` como el nombre del host en vez de `localhost`?**
> Esto se debe a que el contenedor `mi-webapp` (bajo el nombre de servicio `webapp`) no puede comunicarse con el contenedor `mi-redis` (bajo el nombre de servicio `redis`) usando `localhost`, ya que `localhost` se refiere a la propia máquina anfitriona y el controlador `bridge` de Docker crea una red virtual aislada para los contenedores. Dentro de esta red virtual, cada contenedor se comunica con otros contenedores utilizando el nombre del servicio definido en el archivo `docker-compose.yml` como el nombre del host.

> [!NOTE]
> **¡Oye, pero todavía no hemos mapeado un puerto al servicio de `redis` en el `docker-compose.yml`!**
> No hay necesidad de hacerlo. Esto se debe a que el servicio `webapp` se conecta a `redis` utilizando la red virtual creada por Docker. El puerto por defecto de Redis es el 6379, y como ambos contenedores están en la misma red virtual, `webapp` puede conectarse a `redis` utilizando el nombre del servicio `redis` y el puerto 6379 sin necesidad de exponer el puerto al host (el no exponer puertos de más al host es una buena práctica de seguridad).

## 7. Agregar condición de `depends_on` al servicio de `webapp`

Pareciera que ya se puede levantar el stack con `docker compose up --build`. Sin embargo, al intentar esto, puede ocurrir la posibilidad de que el contenedor `mi-webapp` intente conectarse a `mi-redis` antes de esté disponible, lo que provocaría que el servicio `webapp` falle. Para evitar esto, se agregarán estas dos líneas al servicio `webapp` en el archivo `docker-compose.yml`:

```diff
services:
  webapp:
    build: ./webapp
    image: mi-webapp:latest
    container_name: mi-webapp
    ports:
      - 80:5000
    networks:
      - mi-red
+   depends_on:
+     - redis

  redis:
    image: redis:7-alpine
    container_name: mi-redis
    networks:
      - mi-red

networks:
  mi-red:
    driver: bridge
```

La sección `depends_on` indica que el servicio `webapp` depende del servicio `redis`, lo que significa que Docker Compose se asegurará de que el contenedor `mi-redis` esté en ejecución antes de iniciar el contenedor `mi-webapp`.

## 8. Volver a construir y levantar los contenedores usando Docker Compose

Ahora sí, se puede volver a construir y levantar los contenedores con el siguiente comando:

```bash
docker compose up -d
```

> [!NOTE]
> Se agregó el parámetro `-d` (alias de `--detach`) para levantar los contenedores en segundo plano (así como `docker run -d`), lo que permite seguir usando la terminal para correr otros comandos.

> [!CAUTION]
> Verifiquen que ambos contenedores estén en ejecución con `docker ps`. Si alguno de los contenedores no están presentes en la lista, es probable que haya ocurrido un error al iniciar el contenedor. En ese caso, pueden revisar los logs del contenedor con `docker logs <nombre_del_contenedor>` para identificar el error. Debuggea y vuelve a intentar levantar los contenedores.

## 9. Acceso a la aplicación de Flask actualizada

Abre tu navegador web y navega a `http://localhost` para ver la aplicación. Deberías ver el contenido de `index.html` con los estilos aplicados desde `styles.css`, así como el contador de visitas a la página que se actualiza cada vez que recargas la página.

Los siguientes pasos son opcionales, pero se recomienda seguirlos para aprender más sobre Docker Compose.

## 10. Definir volúmenes (EXTRA)

## 11. Definir monturas (EXTRA)

## 12. Definir variables de entorno (EXTRA)

## Conclusión del Taller

¡Felicidades por completar el taller de introducción a la virtualización con Docker! En este taller, aprendiste a crear una aplicación sencilla con Flask, a construir una imagen de Docker para esa aplicación y a ejecutar un contenedor con esa imagen. Además, aprendiste cómo usar Docker Compose para orquestar múltiples contenedores, lo que te permitió crear un pequeño sistema web.
