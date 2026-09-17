/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   arbitration.c                                     :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/15 11:10:57 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/17 16:41:59 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	can_grant(t_table *table, int id, long long now)
{
	int	left;
	int	right;

	if (table->n_coders == 1)
		return (0);
	left = id - 1;
	right = id % table->n_coders;
	return (is_dongle_ok(table, left, id, now)
		&& is_dongle_ok(table, right, id, now));
}

void	clear_reservations(t_table *table)
{
	int	i;

	i = 0;
	while (i < table->n_coders)
	{
		table->dongles[i].reserved_by = 0;
		i++;
	}
}

void	arbitration_pass(t_table *table)
{
	int			i;
	long long	now;
	t_coder		*head;
	t_request	*items;

	i = 0;
	now = sim_time(table->start_time);
	clear_reservations(table);
	head = heap_peek(table);
	items = table->heap->items;
	if (head && !can_grant(table, head->id, now))
		reserve_dongles(table, head);
	while (i < table->heap->count)
	{
		if (can_grant(table, items[i].coder->id, now))
		{
			items[i].coder->granted = 1;
			take_dongles(table, items[i].coder);
			items[i].coder->last_compile_start = now;
			heap_delete(table, i);
		}
		else
			i++;
	}
}
