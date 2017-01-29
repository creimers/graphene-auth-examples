# django graphene authentiation example - work in progress

In this repo, I'm trying to figure out how to do authentication and authorization with graphql and [graphene-django](https://github.com/graphql-python/graphene-django).

When I started, I was especially interested in mutation examples for user registration, account activation, login etc.

Should anyone stumble upon this, I'd be very happy to receive some feedback.

## what's inside.
* python3
* Django 1.10
* graphene
* docker-compose
* py.test

## main commands

### development
* `docker-compose build`
* `docker-compose run django python ./src/manage.py migrate`
* `docker-compose run -p 8000:8000 django python ./src/manage.py runserver 0.0.0.0:8000`

### test
`docker-compose run django py.test -s ./src`
