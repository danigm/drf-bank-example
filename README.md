# drf-bank-example
Simple CRUD to manage bank accounts with social auth for admins

# Run in local

To run in local you'll need pipenv or you can install requierements using the requirements.txt

```
$ pipenv install
```

or

```
$ pip install -r requirements.txt
```

Then you can run tests with:

```
$ ./manage.py test
```

And to run the app follow the usual django commands:

```
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```

# How to run the docker container

```
$ docker-compose up
```

Then you should have the application available at http://localhost:8000

To run the tests inside the container you can run:

```
$ docker exec -ti iban_web ./manage.py test
```
