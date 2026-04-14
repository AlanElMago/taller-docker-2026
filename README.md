# Taller de Introducción a la Virtualización con Docker

Este taller está diseñado para introducir a los participantes a la virtualización utilizando Docker. En este taller, los participantes aprenderán a crear una apliación sencilla con Flask, a construir una imagen de Docker para esa aplicación y a ejecutar un contenedor con esa imagen. Además, se cubrirá cómo usar Docker Compose para orquestar múltiples contenedores.

## Prerequisitos

- Conocimientos básicos de Python y HTML/CSS
- Tener Python instalado en su máquina (puede descargarlo desde [aquí](https://www.python.org/downloads/))
- Tener Docker instalado en su máquina (puede descargarlo desde [aquí](https://www.docker.com/get-started))

## Antes de comenzar

Se recomienda realizar este curso en una carpeta por separado y no trabajar directamente sobre este repositorio.

Otra recomendación es trabajar dentro un entorno virtual de Python para evitar conflictos con otras dependencias. Puede crear un entorno virtual utilizando `venv`. Sitúase en el directorio base del proyecto y ejecute el siguiente comando:

```bash
python -m venv .venv
```

Una vez creado el entorno virtual, actívelo con el siguiente comando:

- En Windows:

```bash
.venv\Scripts\activate
```

- En macOS/Linux:

```bash
source .venv/bin/activate
```

Por último, hay que instalar el módulo Flask dentro del entorno virtual con el siguiente comando:

```bash
pip install Flask
```

## Secciones del taller

1. [Aplicación mínima de Flask](/01_Flask_Minimal/README.md)
2. [Aplicación de Flask con plantilla HTML](/02_Flask_Templates/README.md)
3. [Construcción de una imagen y ejecución de un contenedor Docker](/03_Dockerfile/README.md)
4. [Uso de Docker Compose para orquestar múltiples contenedores](/04_Docker_Compose/README.md)

## Documentación recomendada

- [Docker Documentation](https://docs.docker.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
