/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   time.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/12 11:06:50 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/17 16:24:10 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long long	time_now(void)
{
	struct timeval	tv;

	gettimeofday(&tv, NULL);
	return (((long long)tv.tv_sec * 1000) + ((long long)tv.tv_usec / 1000));
}

long long	sim_time(long long start_time)
{
	return (time_now() - start_time);
}

int	sim_sleep(t_table *table, long long ms)
{
	long long	target;
	int			stop;

	target = sim_time(table->start_time) + ms;
	while (sim_time(table->start_time) < target)
	{
		pthread_mutex_lock(&table->lock);
		stop = table->stop;
		pthread_mutex_unlock(&table->lock);
		if (stop)
		{
			break ;
			return (1);
		}
		usleep(100);
	}
	return (0);
}
