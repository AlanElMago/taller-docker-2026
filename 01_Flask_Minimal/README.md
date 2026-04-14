# Sección 1: Aplicación Mínima de Flask

Flask es un microframework de Python que permite crear aplicaciones web de manera sencilla y rápida. En esta sección, crearemos una aplicación mínima de Flask que mostrará un mensaje de "Hola, Mundo!" en el navegador.

## 1. Creación de la aplicación Flask

Crea un archivo llamado `app.py` en el directorio base del proyecto y agrega el siguiente código:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return '<p>Hola, Mundo!</p>'
```

## 2. Ejecución de la aplicación Flask

Para ejecutar la aplicación Flask, asegúrate de que tu entorno virtual esté activado y luego ejecuta el siguiente comando en la terminal:

```bash
flask --app app run
```

## 3. Acceso a la aplicación

Abre tu navegador web y navega a `http://localhost:5000` para ver la aplicación. Deberías ver un mensaje que dice "Hola, Mundo!".

## Siguiente sección

Procedeer a la siguiente sección: [Aplicación de Flask con plantilla HTML](/02_Flask_Templates/README.md)
