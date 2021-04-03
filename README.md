# Musikilla-bot

## Qué es
Un bot de telegram.

## Qué hace
Cosas, como los catalanes.

## Cómo las hace
1. Necesitas rellenar un fichero `.env` con la información relevante, 
como el `TELEGRAM_BOT_TOKEN` o las distintas variables de Spotify.

2. Se recomienda instalar un entorno virtual de Python para gestionar las dependencias del proyecto, las cuales se pueden instalar mediante:
    ```
    pip install -r requirements.txt
    ```

    2.1. Para añadir un paquete nuevo se debe añadir primero a
    `requirements.in`, posteriormente ejecutar
    ```
    pip-compile
    ```
    Y posteriormente instalarlo de manera habitual con `pip`.

3. Una vez está todo preparado se puede ejecutar el bot en local
    ```
    python3 bot.py --local
    ```

## Cosas de Heroku
Para que esta vaina funcione se necesita tener un entorno cloud, en este caso la version gratuita de Heroku ofrece todo lo necesario.

### Variables de entorno
Es necesario configurar de nuevo las variables de entorno que se usan en
local y **NO ESTÁN** bajo control de versiones por motivos de
seguridad mediante las [herramientas que ofrece Heroku](https://devcenter.heroku.com/articles/config-vars), 
tanto por CLI como por interfaz web.

### Buildpacks
Son scripts que se ejecutan cuando se realiza el despliegue de 
la aplicación, para este proyecto se han utilizado:
1. https://github.com/heroku/heroku-buildpack-chromedriver
2. https://github.com/heroku/heroku-buildpack-google-chrome

Son necesarios para el testeo automático de Selenium a la hora
de obtener el token OAuth2 de Spotify.
### Aplicaciones
Hay un addon instalado que realiza ping 2 veces cada minuto para
mantener viva la instancia del bot pero no sé si está funcionando. 
1. https://elements.heroku.com/addons/newrelic

### Plugins
Se ha instalado el plugin heroku-repo para reiniciar el desarrollo
y que el código se pueda publicar en GitHub.

## TODO's
Para una lista de las tareas pendientes, consultar https://github.com/javisenberg/spoti-bot/projects/1 y https://github.com/javisenberg/spoti-bot/issues/.
 