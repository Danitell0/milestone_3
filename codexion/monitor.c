/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   monitor.c                                         :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/15 16:58:34 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/15 17:16:40 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*monitor(void *arg)
{
	int			i;
	long long	now;
	t_table		*table;

	i = 0;
	table = (t_table *)arg;
	now = sim_time(table->start_time);
	pthread_mutex_lock(&table->lock);
	while (i < table->n_coders)
	{
		if (now - table->coders[i].last_compile_start >= table->t_burnout)
		{
			pthread_cond_broadcast(&table->cond);
			log_state(table->coders[i], "burned out");
			table->stop = 1;
		}
		i++;
	}
}
