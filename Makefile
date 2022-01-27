
format:
	@black -l 100 ochs
	@isort -l 100 ochs

checks:
	@black --check -l 100 ochs
	@mypy ochs
