/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   init.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 20:56:45 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/11 17:50:14 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	setup(t_table *table, char *argv[])
{
	init_table(table, argv);
	if (init_dongles(table))
		return (1);
	if (init_coders(table))
		return (1);// clean partial
	return (0);
}

void init_table(t_table *table, char *argv[])
{
	table->n_coders = atoi(argv[1]);
	table->t_burnout = atoi(argv[2]);
	table->t_compile = atoi(argv[3]);
	table->t_debug = atoi(argv[4]);
	table->t_refactor = atoi(argv[5]);
	table->compiles_required = atoi(argv[6]);
	table->cooldown = atoi(argv[7]);
	if (strcmp(argv[8], "fifo") == 0)
		table->scheduler = FIFO;
	else
		table->scheduler = EDF;
}

int init_dongles(t_table *table)
{
	table->dongles = malloc(table->n_coders * sizeof(t_dongle));
	if (!table->dongles)
		return (print_error("Failing allocating malloc for dongles."));
	memset(table->dongles, 0, table->n_coders * sizeof(t_dongle));
	return (0);
}

int init_coders(t_table *table)
{
	int	i;

	i = 0;
	table->coders = malloc(table->n_coders * sizeof(t_coder));
	if (!table->coders)
		return (print_error("Failling allocating malloc for coders."));
	memset(table->coders, 0, table->n_coders * sizeof(t_coder));
	while (i < table->n_coders)
	{
		table->coders[i].id = i + 1;
		table->coders[i].table = table;
		i++;
	}
	return (0);
}
