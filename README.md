# cattler
backend challenge

### Tecnología usada
Desarrollado con python 3.10.6 + django 4.1.2. Para el desarrollo de API's se
usó django rest framework 3.14.0.

## Instalación en entorno local
Clonar el repositorio y posicionarse en el directorio descargado.
~~~
$ git clone https://github.com/wilmays10/cattler
$ cd cattler
~~~

### En un entorno virtual
Ejecutar el script 'init_local.sh'
~~~
$ ./init_local.sh
~~~

### Con docker
Se necesita tener instalado Docker.
Ejecutar el script 'init_docker.sh'
~~~
$ ./init_docker.sh
~~~

### Consideraciones
En el API de registro, consideré que los datos pueden estar bien parcialmente.
Es decir, puede ocurrir que un corral no exista o no esté vacío por lo que no se
cargaran los datos de ese corral, pero si cargará los demás datos anteriores en
caso de que sean correctos.
Se aclara esto ya que puede romper el principio de atomicidad que tiene el API.

### API's
- Animales: http://localhost:8000/feedlots/api/animales/
- Tropas: http://localhost:8000/feedlots/api/tropas/
- Lotes: http://localhost:8000/feedlots/api/lotes/
- Corrales: http://localhost:8000/feedlots/api/corrales/
- Ingreso: http://localhost:8000/feedlots/api/registro