/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   cleanup.c                                         :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/12 12:14:01 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/14 15:03:31 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	clean(t_table	*table)
{
	if (table->init_step >= STEP_CODERS)
		free(table->coders);
	if (table->init_step >= STEP_DONGLES)
		free(table->dongles);
	if (table->init_step >= STEP_SYNC)
	{
		pthread_mutex_destroy(&table->lock);
		pthread_mutex_destroy(&table->log_lock);
		pthread_cond_destroy(&table->cond);
	}
	if (table->init_step >= STEP_HEAP)
	{
		free(table->heap->items);
		free(table->heap);
	}
	return (1);
}
