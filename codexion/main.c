/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   main.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/08 15:31:56 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/14 15:11:17 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int argc, char *argv[])
{
	int		i;
	t_table	table;

	i = 0;
	if (argc != 9)
		return (print_error("Arguments should be exactly 8."));
	while (i++ < 7)
		if (!is_valid_number(argv[i]))
			return (print_error("Invalid numeric argument."));
	if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
		return (print_error("Invalid scheduler (ex: 'fifo'/'edf')."));
	setup(&table, argv);
	return (0);
}

int	print_error(char *msg)
{
	fprintf(stderr, "Error: %s\n", msg);
	return (1);
}

int	setup(t_table *table, char *argv[])
{
	memset(table, 0, sizeof(t_table));
	init_table(table, argv);
	if (init_sync(table))
		return (clean(table));
	table->init_step = STEP_SYNC;
	if (init_dongles(table))
		return (clean(table));
	table->init_step = STEP_DONGLES;
	if (init_coders(table))
		return (clean(table));
	table->init_step = STEP_CODERS;
	if (init_heap(table))
		return (clean(table));
	table->init_step = STEP_HEAP;
	table->start_time = time_now();
	return (0);
}
