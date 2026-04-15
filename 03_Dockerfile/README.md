# Sección 3: Construcción de una imagen y ejecución de un contenedor Docker

En Docker, una imagen es una plantilla de solo lectura que contiene las instrucciones para crear un contenedor. Un contenedor es una instancia en ejecución de una imagen. En esta sección, aprenderemos a construir una imagen de Docker para nuestra aplicación Flask y a ejecutar un contenedor con esa imagen.

## 1. Crear el archivo `requirements.txt`

Para que el contenedor cuente con las dependencias necesarias para ejecutar nuestra aplicación Flask, es necesario crear un archivo llamado `requirements.txt` en el directorio base del proyecto. El archivo `requirements.txt` es un archivo de texto que lista las dependencias de Python necesarias para ejecutar la aplicación. Para crear el archivo `requirements.txt`, ejecuta el siguiente comando en la terminal:

```bash
pip freeze > requirements.txt
```
## 2. Crear el archivo `Dockerfile`

Un archivo `Dockerfile` es un archivo de texto que contiene las instrucciones para construir una imagen de Docker. Crea un archivo llamado `Dockerfile` en el directorio base del proyecto y agrega el siguiente contenido:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]
```

Antes de continuar, es importante entender cada una de las instrucciones en el `Dockerfile`:

- `FROM python:3.12-slim`: Especifica la imagen base que se utilizará para construir nuestra imagen. Es una imagen que ya está preconfigurada con Python 3.12 y es una versión ligera (slim) para reducir el tamaño de la imagen final. Las siguientes instrucciones añadirán capas adicionales a esta imagen base.

- `WORKDIR /app`: Establece el directorio de trabajo dentro del contenedor. Esto significa que todas las instrucciones posteriores se ejecutarán desde este directorio.

- `COPY requirements.txt .`: Copia el archivo `requirements.txt` desde el directorio actual de tu máquina al directorio de trabajo (`/app`) dentro del contenedor.

- `RUN pip install --no-cache-dir -r requirements.txt`: Ejecuta el comando para instalar las dependencias listadas en `requirements.txt` utilizando pip. La opción `--no-cache-dir` se utiliza para evitar que pip almacene en caché los paquetes descargados, lo que ayuda a reducir el tamaño de la imagen final.

- `COPY . .`: Copia todos los archivos y carpetas desde el directorio actual donde se encuentra situado el `Dockerfile` a la raíz del directorio de trabajo (`/app`) dentro del contenedor.

- `EXPOSE 5000`: Indica que el contenedor debe tener expuesto el puerto 5000, que es el puerto donde la aplicación Flask escuchá las peticiones entrantes desde el exterior del contenedor.

- `CMD ["flask", "--app", "app", "run", "--host=0.0.0.0"]`: Especifica el comando que se ejecutará cuando el contenedor se inicie. En este caso, se ejecutará el comando para iniciar la aplicación Flask, indicando que escuche en todas las interfaces de red (`--host=0.0.0.0`) para que sea accesible desde fuera del contenedor.

## 3. Construir la imagen de Docker

Una vez creada el archivo `Dockerfile`, se puede construir la imagen de Docker utilizando el siguiente comando en la terminal:

```bash
docker build -t mi-webapp .
```

Este comando construirá la imagen de Docker utilizando el `Dockerfile` en el directorio actual (indicado por `.`) y le asignará el nombre `mi-webapp` a la imagen.

> [!TIP]
> La opción `-t` (alias de `--tag`) es un parámetro opcional que se utiliza para etiquetar la imagen con un nombre específico. Si bien no es obligatorio, es una buena práctica etiquetar las imágenes para identificarlas fácilmente.

Para verificar que la imagen se ha construido correctamente, ejecuta el siguiente comando:

```bash
docker images
```

Les debería aparecer una lista de imágenes de Docker en su máquina, incluyendo la imagen `mi-webapp` que se acaba de construir. Aquí se muestra un ejemplo de cómo debería verse la salida del comando:

```
IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
hello-world:latest   85404b3c5395       25.9kB         9.52kB
mi-webapp:latest     22895f3589c4        197MB         48.2MB
```

Como podrán observar, al nombre de la imagen `mi-webapp` se le añade la etiqueta `latest` de manera predeterminada. Esto indica que esta es la última versión de la imagen. Si se construye una nueva imagen con el mismo nombre, la etiqueta `latest` se actualizará automáticamente para apuntar a la nueva imagen.

> [!TIP]
> Puede asignar etiquetas adicionales a la imagen utilizando el formato `nombre:etiqueta`. Por ejemplo, si desea etiquetar la imagen como `v1`, puede usar el siguiente comando:
> ```bash
> docker build -t mi-webapp:v1 .
> ```
> Esto es útil para mantener un control de versiones de las imágenes.

## 4. Ejecutar un contenedor con la imagen de Docker creada

Una obtenida la imagen de Docker, se puede crear una instancia en ejecución de esa imagen, conocida como **contenedor**, utilizando el siguiente comando:

```bash
docker run -p 5000:5000 --name mi-webapp mi-webapp:latest
```
Este comando crea un contenedor a partir de la imagen `mi-webapp:latest` y se le asigna el nombre mismo nombre de la imágen (`mi-webapp`). La opción `-p 5000:5000` se utiliza para mapear el puerto 5000 del contenedor al puerto 5000 de la máquina host, lo que permite acceder a la aplicación Flask extenamente desde un navegador web.

> [!TIP]
> La opción `--name` es un parámetro opcional que se utiliza para asignar un nombre específico al contenedor. Si no se proporciona un nombre, Docker asignará un nombre aleatorio al contenedor. Por esta razón (como asignar etiquetas a las imágenes), es una buena práctica asignar un nombre significativo a los contenedores para identificarlos fácilmente.

Cuando ejecuten el comando `docker run`, deberían ver una salida similar a la siguiente en la terminal:

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```
> [!NOTE]
> La advertencia que nos aparece indica que el servidor de desarrollo de Flask no es adecuado para entornos de producción por cuestiones de rendimiento y seguridad. Sin embargo, para fines de este taller, lo ignoraremos.

Para verificar que el contenedor está corriendo, pueden abrir una nueva terminal y ejecutar el siguiente comando:

```bash
docker ps
```

Les debería aparecer una lista con un solo contenedor en ejecución parecido al siguiente:

```
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS              PORTS                                         NAMES
058cf7f573bd   mi-webapp:latest   "flask --app app run…"   11 minutes ago   Up About a minute   0.0.0.0:5000->5000/tcp, [::]:5000->5000/tcp   mi-webapp
```

La información que muestra el comando nos propociona la siguiente información:

- `CONTAINER ID`: Es un identificador único para el contenedor en ejecución.
- `IMAGE`: Indica la imagen de Docker que se está utilizando para ejecutar el contenedor.
- `COMMAND`: Muestra el comando que se está ejecutando dentro del contenedor.
- `CREATED`: Indica cuánto tiempo ha pasado desde que se creó el contenedor.
- `STATUS`: Muestra el estado actual del contenedor.
- `PORTS`: Indica los puertos que están siendo mapeados entre el contenedor y la máquina host.
- `NAMES`: Muestra el nombre asignado al contenedor.

## 5. Acceso a la aplicación Flask en el contenedor

Abre tu navegador web y navega a `http://localhost:5000` para ver la aplicación Flask en ejecución. Deberías ver el mismo contenido que antes, pero ahora la aplicación está siendo ejecutada dentro de un contenedor de Docker.

Antes de continuar con el siguiente paso, cierre la aplicación Flask en ejecución dentro del contenedor utilizando la combinación de teclas `CTRL+C` en la terminal donde se está ejecutando el contenedor. Si se encuentra en Windows, es posible que necesite presionar `CTRL+C` dos veces para detener el contenedor correctamente.

## 6. Cambiar el mapeo de puertos

Imagine que desea acceder a la aplicación Flask sin necesidad de especificar el puerto en la URL (es decir, acceder a `http://localhost` en lugar de `http://localhost:5000`). Para lograr esto, puede cambiar el mapeo de puertos al ejecutar el contenedor. Para lograr esto, detendremos la ejecución del contenedor usando la combinación de teclas `CTRL+C` en la terminal.

Cuando un contenedor se detiene, el contenedor sigue existiendo en el sistema, pero no está en ejecución. Para verificar que el contenedor se ha detenido, pueden ejecutar el siguiente comando:

```bash
docker ps -a
```

La opción `-a` (alias de `--all`) se utiliza para mostrar todos los contenedores, tanto los que están en ejecución como los que están detenidos. Deberían el contenedor `mi-webapp` con un estado de "Exited".

Una vez detenida la ejecución del contenedor, hay que eliminar el contenedor existente utilizando el siguiente comando:

```bash
docker rm mi-webapp
```

Ahora podemos volver a ejecutar el contenedor con un nuevo mapeo de puertos utilizando el siguiente comando:

```bash
docker run -d -p 80:5000 --name mi-webapp mi-webapp:latest
```

> [!NOTE]
> Se agregó el parámetro `-d` (alias de `--detach`) para ejecutar el contenedor en segundo plano (detached mode), lo que permite que la terminal quede libre para correr otros comandos.

Se eligió el puerto 80 para el mapeo del puerto del host porque es el puerto predeterminado para el tráfico HTTP.

## 7. Acceso a la aplicación Flask sin especificar el puerto

Abre tu navegador web y navega a `http://localhost` para ver la aplicación Flask en ejecución. Ahora deberías poder acceder a la aplicación sin necesidad de especificar el puerto en la URL, gracias al nuevo mapeo de puertos que se configuró al ejecutar el contenedor.

## 8. Detención de la un contenedor en ejecución en segundo plano

Para detener el contenedor `mi-webapp` que se está ejecutando en segundo plano, puedes usar el siguiente comando:

```bash
docker stop mi-webapp
```

Este comando envía una señal de terminación al contenedor, lo que hace que el proceso dentro del contenedor se detenga de manera ordenada. Para verificar que el contenedor se ha detenido, puedes ejecutar el comando `docker ps` nuevamente y no debería aparecer en la lista de contenedores en ejecución.

## Siguiente Sección

Proceder a la siguiente sección: [Uso de Docker Compose para orquestar múltiples contenedores](/04_Docker_Compose/README.md)
