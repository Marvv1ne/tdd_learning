test:
	cd superlists && uv run manage.py test

functional_tests:
	cd superlists && uv run function_tests.py

runserver:
	cd superlists && uv run manage.py runserver
