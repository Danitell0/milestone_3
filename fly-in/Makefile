#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

# Tools ----------
UV = uv
PY = $(UV) run python3
MAP = maps/easy/01_linear_path.txt

.PHONY: help install run debug clean fclean lint lint-strict visual

# Commands -------

help:
	@echo "$(YELLOW)Available Commands:$(RESET)"
	@echo "$(GREEN)  install	->$(RESET) Sync the virtual environment from uv.lock"
	@echo "$(GREEN)  run		->$(RESET) Run the pipeline (Default easy map)"
	@echo "$(GREEN)  debug		->$(RESET) Run the pipeline with pdb"
	@echo "$(GREEN)  clean		->$(RESET) Remove caches and ignored files"
	@echo "$(GREEN)  fclean	->$(RESET) Remove caches, ignored files and virtual environment"
	@echo "$(GREEN)  lint		->$(RESET) Run flake8 + mypy with required flags"
	@echo "$(GREEN)  lint-strict	->$(RESET) Run mypy --strict"
	@echo "$(GREEN)  visual	->$(RESET) Run the program with pygame visuals"

install:
	$(UV) sync

run:
	@echo "$(GREEN)Running program with $(MAP) file.$(RESET)"
	@$(PY) main.py $(MAP)

debug:
	@echo "$(YELLOW)Running program with $(MAP) file and debugger.$(RESET)"
	@$(PY) -m pdb main.py $(MAP)

clean:
	@echo "$(RED)Removing cache files.$(RESET)"
	@find . -path './.venv' -prune -o -type d -name '__pycache__' -print0 \
		| xargs -0 -r rm -rf
	@find . -path './.venv' -prune -o -type f -name '*.py[co]' -print0 \
		| xargs -0 -r rm -f
	@rm -rf .mypy_cache .pytest_cache .ruff_cache

fclean: clean
	@echo "$(RED)Removing virtual environment.$(RESET)"
	@rm -rf .venv

lint:
	@$(UV) run flake8 . --exclude=venv,.venv 
	@echo "flake8... $(GREEN)Success.$(RESET)"
	@$(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
	@echo "mypy... $(GREEN)Success.$(RESET)"

lint-strict:
	@$(UV) run mypy . --strict
	@echo "mypy --strict... $(GREEN)Success.$(RESET)"

visual:
	@echo "$(GREEN)Running program in Visual Mode.$(RESET)"
	@$(PY) main.py $(MAP) --visual
