#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

NAME = codexion

# Tools --------------------

CC = cc
CFLAGS = -Wall -Werror -Wextra
PTH = -pthread
RM = rm -rf

SRCS = main.c

.PHONY: help all clean fclean re lint

$(NAME):
	@$(CC) $(CFLAGS) $(PTH) $(SRCS)
	@echo "${GREEN}program compiled.$(RESET)"

# Commands -----------------

## mandatory ---------------

help:
	@echo "${YELLOW}Available Commands:${RESET}"
	@echo "$(GREEN)	all	->${RESET}"
	@echo "$(GREEN)	clean	->${RESET}"
	@echo "$(GREEN)	fclean	->${RESET}"
	@echo "$(GREEN)	re	->${RESET}"
	@echo "$(GREEN)	lint	->${RESET}"



all:

clean:

fclean:

re: fclean

## helpers -----------------

lint:


