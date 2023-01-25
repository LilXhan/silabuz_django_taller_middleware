# Taller middleware

Para este taller, crearemos una nueva aplicación de Django, si no recuerdas los pasos, no te preocupes:

Aquí los comandos necesarios para ejecutar:

```shell
python -m venv env
```

Entramos a nuestro entorno virtual y ejecutamos.

```shell
pip install django
```

Creamos nuestro proyecto Django

```shell
django-admin startproject middleTutorial .
```

Creamos nuestra aplicación

```shell
python manage.py startapp posts
```

Y añadimos nuestra aplicación a `settings.py`.

```python
INSTALLED_APPS = [
    ...,
    'posts',
]
```

Dentro de nuestro archivo de `urls.py` de `middleTutorial`, deberíamos tenerlo de la siguiente forma.

```python
# ...
from posts.views import index

urlpatterns = [
    path('', index, name='index'),
     ...
]
```

Y en nuestro archivo de vistas de `posts`, añadimos la siguiente vista.

```python
# ....
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hola mundo desde PyWomabt.")
```

Para este tutorial tendremos una vista básica, luego de confirmar de que nuestro proyecto funciona vamos a crear nuestro middleware.

Ahora crearemos nuestro propio Middleware.

Creamos el archivo `middleware.py` dentro de la aplicación `posts`.

```python
def ip_is_valid(get_response):

    def middleware(request):
        # Código que se ejecutará antes del llamado a la vista.
        print('Hola mundo desde un Middleware!!!')
        response = get_response(request)
        # Código que se ejecutará después del llamado a la vista.
        return response

    return middleware
```

Cómo vemos, básicamente es un decorador, en este caso nos va a servir para verificar que la IP de un cliente sea válida.

Ahora para regostar nuestro middleware, dentro de `settings.py` modificamos el listado de middlewares.

```python
MIDDLEWARE = [
    #...
    'post.middleware.ip_is_valid',
]
```

Aquí debemos tener algunas cosas en cuenta.

1.  Tenemos acceso a la petición a través del objeto request.
    
2.  La función `get_reponse` será la que se encarge de ejecutar nuestra vista.
    
3.  Mediante la función del middleware, tendremos la capacidad de extender la funcionalidad que tenga nuestra vista.
    

Ahora procederemos a obtener la ip.

Instalamos `django-ipware`

```shell
pip install django-ipware
```

Una vez instalado, nuestro middleware debería quedar de la siguiente forma.

```python
from ipware import get_client_ip

def ip_is_valid(get_response):

    def middleware(request):

        ip, is_routable = get_client_ip(request)

        print(ip)
        print(is_routable)

        return get_response(request)

    return middleware
```

Si volvemos a ejecutar deberíamos obtener lo siguiente:

```shell
127.0.0.1
False
```

Con esto, ¡ya tenemos creado nuestro propio middleware!, por ejemplo podemos banearnos de la página.

```python
from ipware import get_client_ip
from django.http import HttpResponse

BLACK_LIST = [
    '127.0.0.1'
]

def ip_is_valid(get_response):

    def middleware(request):

        ip, is_routable = get_client_ip(request)

        if ip in BLACK_LIST:
            return HttpResponse('Bad request', status=404)
        else:
            return get_response(request)

    return middleware
```

## Ejemplo con clases

Un middleware también podemos tenerlo con clases, por ejemplo:

```python
from ipware import get_client_ip
from django.http import HttpResponse

BLACK_LIST = [
    '127.0.0.1'
]

class IPIsValid():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)

        if ip in BLACK_LIST:
            return HttpResponse('Bad request', status=404)
        else:
            return get_response(request)
```

Este middleware funciona de la misma forma que el anterior, ahora solo lo agregamos a nuestra lista de middlewares en `settings.py`.

```python
MIDDLEWARE = [
    #...
    'post.middleware.IPIsValid',
]
```

## Tarea

Crea un middleware que en el caso de estar baneada la ip del servidor, retorne una nueva vista basada en un template con un 404.

Links:

[Diapositivas](https://docs.google.com/presentation/d/e/2PACX-1vTr-r7MmaNDeCMS7q2Agis76OqehZSvWYVv6jakwkPpdyT-oXF-K2tMhwpeVBMTyZbI2hwtR8ilPzgX/embed?start=false&loop=false&delayms=3000#slide=id.g143f30675af_0_0)

Videos:

[Teoria](https://www.youtube.com/watch?v=euSU-9nGhPs&list=PLxI5H7lUXWhjV-yCSEuJXxsDmNESrvbw3&index=17&ab_channel=Silabuz)

[Practica](https://www.youtube.com/watch?v=BrKyN-_tDO4&list=PLxI5H7lUXWhjV-yCSEuJXxsDmNESrvbw3&index=18&ab_channel=Silabuz)