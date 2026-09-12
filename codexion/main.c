/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   main.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/08 15:31:56 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/12 15:21:26 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int main(int argc, char *argv[])
{
	int		i;
	t_table	table;

	i = 0;
	if (argc != 9)
		return(print_error("Arguments should be exactly 8."));
	while (i++ < 7)
		if (!is_valid_number(argv[i]))
			return(print_error("Invalid numeric argument."));
	if (strcmp(argv[8], "fifo") != 0 && strcmp(argv[8], "edf") != 0)
		return(print_error("Invalid scheduler (ex: 'fifo'/'edf')."));
	setup(&table, argv);
	return (0);
}

int	print_error(char *msg)
{
	fprintf(stderr, "Error: %s\n", msg);
	return (1);
}
