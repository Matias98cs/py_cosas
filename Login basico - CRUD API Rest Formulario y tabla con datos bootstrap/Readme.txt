Detalle de los archivos y funcionalidades del código proporcionado:

Introducción:
El código implementa una aplicación web con Flask que permite a los usuarios iniciar sesión, ver su panel de control, acerca de, contactar a través de un formulario, ver sus calificaciones y cerrar sesión. También proporciona una API para agregar y eliminar calificaciones, pero solo los usuarios autenticados tienen acceso a esta funcionalidad. El control de autenticación se logra mediante el uso de sesiones y decoradores personalizados.
El archivo `script.py` es un script JavaScript que interactúa con la API de calificaciones definida en el archivo `app.py`. Este script se encarga de mostrar las calificaciones en una lista y permite agregar y eliminar calificaciones a través de eventos DOM y solicitudes Fetch. 

1. app.py
Este archivo es el punto de entrada principal de la aplicación. Aquí se crea una instancia de Flask y se configura para utilizar el módulo Flask-RESTful y Flask-Session. Además, se registran las rutas y se define una API para manejar las calificaciones. A continuación, detallamos los componentes principales:

- Flask: Flask es un marco web ligero de Python utilizado para crear aplicaciones web. Se usa para crear la instancia de la aplicación (`app = Flask(__name__)`).
  
- Flask-RESTful: Es una extensión de Flask que simplifica la creación de APIs RESTful. Se utiliza para definir una API de recursos de calificaciones (`api = Api(app)`).

- Flask-Session: Es una extensión de Flask que agrega soporte para el manejo de sesiones en la aplicación. Se configura para utilizar el sistema de archivos para almacenar las sesiones (`app.config['SESSION_TYPE'] = 'filesystem'`). Además, se define un tiempo de vida para las sesiones de 15 minutos (`app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=15)`).

- Blueprints: Son una forma de organizar las rutas y vistas en una aplicación Flask. Se utilizan para separar las rutas en módulos reutilizables. En este caso, se registran dos blueprints: `auth_routes` y `main_routes`.

- Main Routes: Contiene las rutas principales de la aplicación, como el inicio, el panel de control, acerca de, contacto y calificaciones.

- Auth Routes: Contiene las rutas relacionadas con la autenticación, como el inicio de sesión (`/login`) y el cierre de sesión (`/logout`).

- API: Se define una clase `CalificacionesResource` que es un recurso de la API que maneja las operaciones GET, POST y DELETE para las calificaciones. Se utilizan decoradores para restringir el acceso a estas rutas, de manera que el usuario debe haber iniciado sesión para acceder a ellas.

2. routes.py
Este archivo contiene las rutas principales de la aplicación. Algunas rutas están protegidas y requieren que el usuario haya iniciado sesión (`@login_required`).

- ContactForm: Es una clase que define un formulario con campos de nombre, correo electrónico y mensaje para la página de contacto.

- Index: Redirige al usuario a la página de inicio, que a su vez redirige a la página de inicio de sesión (`/login`).

- Dashboard: Renderiza la plantilla del panel de control (`dashboard.html`) y requiere que el usuario haya iniciado sesión para acceder a esta página.

- About: Renderiza la plantilla de la página acerca de (`about.html`) y también requiere que el usuario haya iniciado sesión para acceder a esta página.

- Contact: Renderiza la plantilla de la página de contacto (`contact.html`) y permite enviar un formulario de contacto. Esta ruta también requiere que el usuario haya iniciado sesión.

- Calificaciones: Renderiza la plantilla de la página de calificaciones (`calificaciones.html`) y requiere que el usuario haya iniciado sesión.

3. auth.py
Este archivo contiene las rutas relacionadas con la autenticación de usuarios y algunas funciones auxiliares.

- Login: Maneja el inicio de sesión de los usuarios. Si se realiza una solicitud POST con el nombre de usuario y contraseña correctos, se establece una sesión para el usuario y se redirige al panel de control. Si ya se ha iniciado sesión, el usuario es redirigido directamente al panel de control.

- Logout: Maneja el cierre de sesión de los usuarios. Elimina la sesión actual del usuario y lo redirige a la página de inicio de sesión.

- find_user_by_username: Es una función auxiliar que busca un usuario en la lista de usuarios por su nombre de usuario y contraseña.

- is_logged_in: Es una función que comprueba si el usuario ha iniciado sesión o no. Si el usuario ha iniciado sesión, se establece un atributo `g.user` para que pueda ser utilizado por otras partes del código para determinar si el usuario está autenticado.

- login_required: Es un decorador personalizado que se aplica a ciertas rutas para asegurar que el usuario haya iniciado sesión antes de acceder a ellas.

- api_login_required: Es un decorador personalizado similar a `login_required`, pero se utiliza específicamente para proteger las rutas de la API (`CalificacionesResource`). Si un usuario no ha iniciado sesión, se devuelve un código de estado 401 (No autorizado) al intentar acceder a los endpoints de la API.

4. api.py
Este archivo contiene la API que maneja las calificaciones de los estudiantes. Utiliza el módulo Flask-RESTful para definir un recurso `CalificacionesResource`.

- calificaciones: Es una lista de diccionarios que representa las calificaciones de los estudiantes.

- post_parser: Es un analizador de argumentos que se utiliza para validar y analizar los datos enviados a través de una solicitud POST en la API.

- CalificacionesResource: Es una clase que maneja las solicitudes GET, POST y DELETE para las calificaciones. Esta clase tiene un decorador `api_login_required`, lo que significa que el usuario debe haber iniciado sesión para acceder a estas rutas de la API.

- GET: Devuelve la lista de calificaciones cuando se realiza una solicitud GET a `/api/calificaciones`.

- POST: Agrega una nueva calificación a la lista cuando se realiza una solicitud POST a `/api/calificaciones`. La solicitud debe incluir los campos "Nombre", "Clase", "Materia" y "Calificacion".

- DELETE: Elimina una calificación específica de la lista cuando se realiza una solicitud DELETE a `/api/calificaciones/<int:calificacion_id>`. El `calificacion_id` se pasa como parte de la URL.


El archivo `script.py`. A continuación, explicamos detalladamente cada componente y su funcionamiento:

1. DOMContentLoaded event:
Este evento se dispara cuando el contenido de la página web ha sido completamente cargado y analizado, incluyendo el DOM (Document Object Model). Esto garantiza que el código JavaScript se ejecute después de que la página esté completamente cargada, evitando problemas al intentar acceder a elementos HTML que aún no se han creado.

2. Fetch API:
La función `fetch()` es una API web de JavaScript que se utiliza para realizar solicitudes HTTP. En este caso, se utiliza para obtener la lista de calificaciones a través de una solicitud GET y para agregar y eliminar calificaciones a través de solicitudes POST y DELETE respectivamente.

3. mostrarcalificaciones():
Esta función recibe un arreglo de calificaciones en formato JSON y muestra las calificaciones en una lista HTML dentro del elemento con el ID `calificaciones-list`. Primero, limpia el contenido anterior de la lista (`calificacionesList.innerHTML = ''`) y luego crea elementos HTML para cada calificación, que se agregan a la lista.

4. agregarcalificacion():
Esta función se ejecuta cuando el formulario con el ID `nueva-calificacion-form` se envía. Obtiene los valores ingresados en el formulario y los envía al servidor a través de una solicitud POST para agregar una nueva calificación. Si la solicitud es exitosa, se muestra un mensaje de alerta y se actualiza la lista de calificaciones.

5. eliminarcalificacion():
Esta función se ejecuta cuando se hace clic en el botón "Eliminar" de una calificación específica. Muestra un mensaje de confirmación al usuario para asegurarse de que realmente desea eliminar la calificación. Si el usuario confirma la eliminación, se envía una solicitud DELETE al servidor para eliminar la calificación correspondiente. Si la solicitud es exitosa, se muestra un mensaje de alerta y se actualiza la lista de calificaciones.

En resumen, este último script interactúa con la API de calificaciones a través de solicitudes Fetch para obtener, agregar y eliminar calificaciones. También se encarga de mostrar las calificaciones en una lista en la página web. Las funciones `mostrarcalificaciones()`, `agregarcalificacion()` y `eliminarcalificacion()` se utilizan para manipular el DOM y comunicarse con el servidor. El script asegura que el usuario interactúe de manera segura con la aplicación web mediante el uso de eventos DOM y manejo de errores en caso de que las solicitudes al servidor no sean exitosas.