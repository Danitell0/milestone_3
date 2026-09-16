/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   heap_utils.c                                      :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/14 20:20:27 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/16 15:06:38 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	heap_swap(t_request *a, t_request *b)
{
	t_request	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	sift_up(t_table *table, int pos)
{
	t_request	*items;
	int			parent;

	items = table->heap->items;
	while (pos > 0)
	{
		parent = (pos - 1) / 2;
		if (is_higher_priority(table, &items[pos], &items[parent]))
		{
			heap_swap(&items[pos], &items[parent]);
			pos = parent;
		}
		else
			break ;
	}
}

void	sift_down(t_table *table, int pos)
{
	t_request	*items;
	int			left;
	int			right;
	int			best;

	items = table->heap->items;
	left = 2 * pos + 1;
	right = 2 * pos + 2;
	while (left < table->heap->count)
	{
		best = left;
		if (right < table->heap->count
			&& is_higher_priority(table, &items[right], &items[left]))
			best = right;
		if (is_higher_priority(table, &items[best], &items[pos]))
		{
			heap_swap(&items[pos], &items[best]);
			pos = best;
			left = 2 * pos + 1;
			right = 2 * pos + 2;
		}
		else
			break ;
	}
}
