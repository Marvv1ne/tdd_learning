test:
	cd superlists && uv run manage.py test

functional_tests:
	cd superlists && uv run manage.py test functional_tests

runserver:
	cd superlists && uv run manage.py runserver

migrations:
	cd superlists && uv run manage.py makemigrations

migrate:
	cd superlists && uv run manage.py migrate
