/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   monitor.c                                         :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/15 16:58:34 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/15 19:56:28 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	check_burnout(t_table *table, long long now)
{
	int	i;

	i = 0;
	while (i < table->n_coders)
	{
		if (now - table->coders[i].last_compile_start >= table->t_burnout)
		{
			log_state(&table->coders[i], "burned out");
			return (1);
		}
		i++;
	}
	return (0);
}

static int	all_done(t_table *table)
{
	int	i;

	i = 0;
	while (i < table->n_coders)
	{
		if (table->coders[i].compile_count < table->compiles_required)
			return (0);
		i++;
	}
	return (1);
}

void	*monitor(void *arg)
{
	int			i;
	long long	now;
	t_table		*table;

	i = 0;
	table = (t_table *)arg;
	while (1)
	{
		pthread_mutex_lock(&table->lock);
		now = sim_time(table->start_time);
		if (check_burnout(table, now) || all_done(table))
		{
			table->stop = 1;
			pthread_cond_broadcast(&table->cond);
			pthread_mutex_unlock(&table->lock);
			return (NULL);
		}
		pthread_mutex_unlock(&table->lock);
		usleep(1000);
	}
}
