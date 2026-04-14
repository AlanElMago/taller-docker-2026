# Sección 2: Aplicación de Flask con plantilla HTML

Las plantillas HTML permiten separar la lógica de la aplicación de la presentación. En esta sección, agregaremos una plantilla HTML y archivo de estilos CSS a nuestra aplicación Flask y modificaremos nuestro código de Python para renderizar la plantilla.

## 1. Crear las carpetas `static` y `templates`

En el directorio base del proyecto, crea dos carpetas llamadas `static` y `templates`. La carpeta `static` se utilizará para almacenar archivos estáticos como CSS, mientras que la carpeta `templates` se utilizará para almacenar archivos de plantilla HTML.

## 2. Descargar los archivos de `index.html` y `styles.css`

Por motivos de simplicidad, se han proporcionado los archivos `index.html` y `styles.css` en el repositorio del taller. Estos archivos se encuentran en las siguientes carpetas:

- `02_Flask_Templates/static/styles.css`
- `02_Flask_Templates/templates/index.html`

Se le motiva al participante a realizar modificaciones en estos archivos para personalizar el contenido (y apariencia, si desea) de la aplicación a su gusto. Dentro de la carpeta `static`, se puede poner una imagen de perfil bajo el nombre `profile.png`. Ya existe una imágen de ejemplo en el repositorio en la carpeta `02_Flask_Templates/static/profile.png`. Sin embargo, se le anima al participante a utilizar una imagen de su elección.

## 3. Modificar el código de `app.py` para renderizar la plantilla

Abre el archivo `app.py` y modifica el código para importar `render_template` y renderizar la plantilla `index.html`. Las modificaciones señaladas se muestran a continuación:

```diff
-from flask import Flask
+from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
-def hola_mundo():
-    return '<p>Hola, Mundo!</p>'
+def index():
+    return render_template('index.html')
```

## 4. Ejecutar la aplicación Flask

Asegúrate de que tu entorno virtual esté activado y luego ejecuta el siguiente comando en la terminal:

```bash
flask --app app run
```

## 5. Acceso a la aplicación

Abre tu navegador web y navega a `http://localhost:5000` para ver la aplicación. Deberías ver el contenido de `index.html` con los estilos aplicados desde `styles.css`.

## Siguiente sección

Procedeer a la siguiente sección: [Construcción de una imagen y ejecución de un contenedor Docker](/03_Dockerfile/README.md)
