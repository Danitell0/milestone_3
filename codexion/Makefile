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

OBJS_DIR = objs

HEADER = codexion.h

SRCS = main.c checkers.c init.c cleanup.c time.c heap.c heap_utils.c \
       arbitration.c monitor.c threads.c dongle_utils.c log.c coder.c

OBJS = $(SRCS:%.c=$(OBJS_DIR)/%.o)

.PHONY: help all clean fclean re lint

$(NAME): $(OBJS)
	@$(CC) $(CFLAGS) $(PTH) $(OBJS) -o $(NAME)
	@echo "${GREEN}program compiled.$(RESET)"

$(OBJS_DIR)/%.o: %.c $(HEADER)
	@mkdir -p $(dir $@)
	@$(CC) $(CFLAGS) $(PTH) -c $< -o $@
	@echo "$@ -> ${GREEN}compiled.${RESET}"

# Commands -----------------

## mandatory ---------------

help:
	@echo "${YELLOW}Available Commands:${RESET}"
	@echo "$(GREEN)	all	->${RESET}Compile the program."
	@echo "$(GREEN)	clean	->${RESET}Remove object directory."
	@echo "$(GREEN)	fclean	->${RESET}Remove program file and object directory."
	@echo "$(GREEN)	re	->${RESET}Rebuild from scratch."
	@echo "$(GREEN)	lint	->${RESET}Run Norminette."

all: $(NAME)

clean:
	@$(RM) $(OBJS_DIR)
	@echo "$(RED)objects removed.$(RESET)"

fclean: clean
	@$(RM) $(NAME)
	@echo "$(RED)program and object files removed$(RESET)"


re: fclean all

## helpers -----------------

lint:
	@echo "${YELLOW}running Norminette.${RESET}"
	@norminette
