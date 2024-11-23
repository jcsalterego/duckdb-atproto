.PHONY: all
all:

.PHONY: lint-fix
lint-fix:
	black *.py
	ruff --fix *.py
