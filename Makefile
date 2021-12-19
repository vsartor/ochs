
format:
	@black -l 100 ochs
	@isort ochs

checks:
	@black --check -l 100 ochs
	@mypy ochs
