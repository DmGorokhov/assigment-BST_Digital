MANAGE := poetry run python manage.py

install:
		@poetry install

make-migration:
		@$(MANAGE) makemigrations

migrate: make-migration
		@$(MANAGE) migrate

build: install migrate

setup: migrate
	echo Create a super user
	poetry run python manage.py createsuperuser

run-celery:
	 celery -A R4C worker --loglevel=info & celery -A R4C flower

run-redis:
	 redis-server --daemonize yes

start-server:
		poetry run python manage.py runserver 0.0.0.0:8000

start: run-redis start-server

lint:
		poetry run flake8 .

test:
		poetry run ./manage.py test

test-coverage:
		poetry run coverage run  manage.py test .
		poetry run coverage html

.PHONY: shell
shell:
		@$(MANAGE) shell_plus --ipython