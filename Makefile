MANAGE := poetry run python manage.py

install:
		@poetry install

make-migration:
		@$(MANAGE) makemigrations

migrate: make-migration
		@$(MANAGE) migrate

build: install migrate

start-dev:
		@$(MANAGE) runserver

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