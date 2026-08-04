#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

NAME = call_me_maybe

SRC	 	:= src
DATA_IN  	:= data/input
DATA_OUT 	:= data/output

FUNCTIONS	:= $(DATA_IN)/functions_definition.json
INPUT		:= $(DATA_IN)/function_calling_tests.json
OUTPUT		:= $(DATA_OUT)/function_calling_results.json

# Tools --------------------
UV 		:= uv
PY 		:= $(UV) run python
MYPY_FLAGS	:= --warn-return-any \
		   --warn-unused-ignores \
	           --ignore-missing-imports \
	           --disallow-untyped-defs \
	           --check-untyped-defs
STD_ARGS	:= --functions_definition $(FUNCTIONS) \
		   --input $(INPUT) \
		   --output $(OUTPUT)

.PHONY: help install run debug lint lint-strict test clean fclean

# Commands --------------------

help:
	@echo "${YELLOW}Available Commands:${RESET}"
	@echo "${GREEN}  install      ->${RESET} Sync the virtual environment from uv.lock"
	@echo "${GREEN}  run          ->${RESET} Run the pipeline (ARGS=... for extra flags)"
	@echo "${GREEN}  debug        ->${RESET} Run the pipeline with pdb"
	@echo "${GREEN}  lint         ->${RESET} flake8 + mypy with required flags"
	@echo "${GREEN}  lint-strict  ->${RESET} flake8 + mypy --strict"
	@echo "${GREEN}  test         ->${RESET} Run the pytest suite"
	@echo "${GREEN}  clean        ->${RESET} Remove caches and ignore files"
	@echo "${GREEN}  fclean       ->${RESET} clean + remove generated output"


install:
	$(UV) sync
 
run: | $(DATA_OUT)
	@echo "Running main program"
	@$(PY) -m $(SRC) $(STD_ARGS)

debug: | $(DATA_OUT)
	@echo "Running main program with debugger"
	@$(PY) -m pdb -m $(SRC) $(STD_ARGS)

lint:
	@$(UV) run flake8 --exclude=llm_sdk,venv,.venv
	@echo "flake8... ${GREEN}Success${RESET}"
	@$(UV) run mypy . $(MYPY_FLAGS)
	@echo "mypy... ${GREEN}Success${RESET}"

lint-strict:
	@$(UV) run flake8 --exclude=llm_sdk,venv,.venv
	@echo "flake8... ${GREEN}Success${RESET}"
	@$(UV) run mypy . --strict
	@echo "mypy --strict... ${GREEN}Success${RESET}"

$(DATA_OUT):
	mkdir -p $@

test:
	@echo "${GREEN}Running pytest suite${RESET}"
	@$(UV) run pytest -q

clean:
	find . -path './.venv' -prune -o -type d -name '__pycache__' -print0 \
		| xargs -0 -r rm -rf
	find . -path './.venv' -prune -o -type f -name '*.py[co]' -print0 \
		| xargs -0 -r rm -f
	rm -rf .mypy_cache .pytest_cache .ruff_cache

fclean:
	@echo "$(RED)Removing output$(RESET)"
	@rm -rf $(DATA_OUT)

