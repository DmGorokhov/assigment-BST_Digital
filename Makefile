MANAGE := poetry run python manage.py

install:
		@poetry install

make-migration:
		@$(MANAGE) makemigrations

migrate: make-migration
		@$(MANAGE) migrate

build: install migrate

run-celery:
	 celery -A R4C worker --loglevel=info & celery -A R4C flower

start-dev:
		@$(MANAGE) runserver

lint:
		poetry run flake8 .

test:
		poetry run ./manage.py test

.PHONY: shell
shell:
		@$(MANAGE) shell_plus --ipython