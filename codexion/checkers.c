/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   checkers.c                                        :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:28:38 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/14 20:51:20 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_valid_number(char	*arg)
{
	int		i;

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

int is_higher_priority(t_table *table, t_request *a, t_request *b)
{
	long long	deadline_a;
	long long	deadline_b;

	deadline_a = a->coder->last_compile_start + table->t_burnout;
	deadline_b = b->coder->last_compile_start + table->t_burnout;
	if (table->scheduler == FIFO)
	{
		if (a->arrival != b->arrival)
			return (a->arrival < b->arrival);
		return (a->coder->id < b->coder->id);
	}
	else
	{
		if (deadline_a != deadline_b)
			return (deadline_a < deadline_b);
		return (a->coder->id < b->coder->id);
	}
}
