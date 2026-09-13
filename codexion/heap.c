/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   heap.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/13 19:32:32 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/13 21:08:55 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int heap_push(t_table *table, t_coder *coder)
{
	t_request	*items;

	items = table->heap->items;
	items[table->heap->count].coder = coder;
	items[table->heap->count].arrival = sim_time(table->start_time);
	table->heap->count += 1;
	sift_up(table, table->heap->count - 1);
	return (0);
}

void heap_swap(t_request *a, t_request *b)
{
	t_request	tmp;
	
	tmp = *a;
	*a = *b;
	*b = tmp;
}

void sift_up(t_table *table, int pos)
{
	t_request	*items;
	int			parent;

	items = table->heap->items;
	while (pos > 0)
	{
		parent = (pos - 1) / 2;
		if (is_higher_priority(items[pos], items[parent]))
		{
			heap_swap(&items[pos], &items[parent]);
			pos = parent;
		}
		else
			break;
	}
}

void heap_delete(t_table *table, int pos)
{
	t_request	*items;

	items = table->heap->items;
	items[pos] = items[table->heap->count - 1];

}

t_coder *heap_peek(t_table *table)
{
	if (table->heap->count == 0)
		return (NULL);
	return (table->heap->items[0].coder); 
}
