#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

NAME = fly_in

SRC	 = src

# Tools ----------

PY = python3
MAP = maps/easy/01_linear_path.txt

.PHONY: help install run debug clean lint lint-strict

# Commands -------

help:

install:

run:
	@echo "$(GREEN)Running program with $(MAP) file.$(RESET)"
	@$(PY) main.py $(MAP)

debug:
	@echo "$(YELLOW)Running program with $(MAP) file and debugger.$(RESET)"
	@$(PY) pdb main.py

clean:
	@echo "$(RED)Removing cache files.$(RESET)"
	@find . -path './.venv' -prune -o -type d -name '__pycache__' -print0 \
		| zargs -0 -r rm -rf
	@find . -path './.venv' -prune -o -type f -name '*.py[co]' -print0 \
		| xargs -0 -r rm -f
	@rm -rf .mypy_cache .pytest_cache .ruff_cache

lint:
	@run flake8 .
	@echo "flake8... $(GREEN)Success.$(RESET)"
	@run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
	@echo "mypy... $(GREEN)Success.$(RESET)"

lint-strict:
	@run mypy . --strict
	@echo "mypy --strict... $(GREEN)Success.$(RESET)"


