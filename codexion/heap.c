/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   heap.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/13 19:32:32 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/17 16:01:56 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	heap_push(t_table *table, t_coder *coder)
{
	t_request	*items;

	items = table->heap->items;
	items[table->heap->count].coder = coder;
	items[table->heap->count].arrival = sim_time(table->start_time);
	table->heap->count += 1;
	sift_up(table, table->heap->count - 1);
	return (0);
}

void	heap_delete(t_table *table, int pos)
{
	t_request	*items;

	items = table->heap->items;
	items[pos] = items[table->heap->count - 1];
	table->heap->count -= 1;
	if (pos >= table->heap->count)
		return ;
	if (pos > 0 && is_higher_priority(table, &items[pos], &items[(pos - 1) / 2]))
    	sift_up(table, pos);
	else
    	sift_down(table, pos);
}

t_coder	*heap_peek(t_table *table)
{
	if (table->heap->count == 0)
		return (NULL);
	return (table->heap->items[0].coder);
}
