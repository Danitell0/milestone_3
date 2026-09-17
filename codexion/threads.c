/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   threads.c                                         :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/16 12:51:06 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/17 19:28:19 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	stop_and_join(t_table *table, int count)
{
	pthread_mutex_lock(&table->lock);
	table->stop = 1;
	pthread_cond_broadcast(&table->cond);
	pthread_mutex_unlock(&table->lock);
	join_coders(table, count);
	return (1);
}

void	join_coders(t_table *table, int count)
{
	while (count)
		pthread_join(table->coders[--count].thread, NULL);
}

int	create_threads(t_table *table)
{
	int		i;
	t_coder	*coders;

	i = 0;
	coders = table->coders;
	while (i < table->n_coders)
	{
		if (pthread_create(&coders[i].thread, NULL, coder_routine, &coders[i]))
			return (stop_and_join(table, i));
		i++;
	}
	if (pthread_create(&table->monitor, NULL, monitor_routine, table))
	{
		stop_and_join(table, table->n_coders);
		pthread_join(table->monitor, NULL);
		return (1);
	}
	return (0);
}
