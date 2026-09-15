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

SRCS = main.c parse.c init.c cleanup.c time.c heap.c heap_utils.c \
       arbitration.c

.PHONY: help all clean fclean re lint

$(NAME):
	@$(CC) $(CFLAGS) $(PTH) $(SRCS) -o $(NAME)
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

all: $(NAME)

clean:
	@echo "${RED}removing program.${RESET}"
	@rm ./codexion

fclean:


re: fclean

## helpers -----------------

lint:
	@echo "${YELLOW}running Norminette.${RESET}"
	@norminette
