/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   parse.c                                           :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:28:38 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/11 11:50:06 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int is_valid_number(char *arg)
{
	int		i;
	t_table	table;

	i = 0;
	if (strlen(arg) == 0 || strlen(arg) > 9)
		return (0);
	while (arg[i] != '\0')
	{
		if (arg[i] < '0' || arg[i] > '9')
			return (0);
		i++;
	}
	return (1);
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
