
format:
	@black -l 100 ochs tests
	@isort ochs

checks:
	@black --check -l 100 ochs
	@mypy ochs tests
	@tox
