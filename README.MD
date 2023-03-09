# IMAGE-VIEWER APP

## Description

This is simple web server to store and view images depening on user's tier. It was written in Python using Django and Django Rest Framework.

## Installation

Go into project's directory create your own enviroment (or just run it globally) and run to install all dependencies:

    pip install -r requirements.txt

Then to migrate database run:

    python manage.py migrate

And to start the server run:

    python manage.py runserver

## Available endpoints

### Auth

    POST /api/login-user/ - login user
    POST /api/auth/logout-user/ - logout user

### Images

    GET /image/<id>/<size> - get your image by id and size
    GET /image/<link> - get image by link
    GET /api/image-view/ - get all of your images
    POST /api/image-view/ - create new image
