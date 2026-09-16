/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   coder.c                                           :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/15 13:33:18 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/16 15:38:48 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	lone_compile_phase(t_table *table, t_coder *coder)
{
	pthread_mutex_lock(&table->lock);
	log_state(coder, "has taken a dongle");
	coder_wait(table, coder);
	pthread_mutex_unlock(&table->lock);
}

static int	compile_phase(t_table *table, t_coder *coder)
{
	pthread_mutex_lock(&table->lock);
	heap_push(table, coder);
	arbitration_pass(table);
	coder_wait(table, coder);
	if (table->stop)
	{
		pthread_mutex_unlock(&table->lock);
		return (1);
	}
	coder->granted = 0;
	log_state(coder, "has taken a dongle");
	log_state(coder, "has taken a dongle");
	log_state(coder, "is compiling");
	pthread_mutex_unlock(&table->lock);
	return (0);
}

static void	debug_phase(t_table *table, t_coder *coder)
{
	pthread_mutex_lock(&table->lock);
	coder->compile_count += 1;
	release_dongles(table, coder, sim_time(table->start_time));
	arbitration_pass(table);
	pthread_cond_broadcast(&table->cond);
	log_state(coder, "is debugging");
	pthread_mutex_unlock(&table->lock);
}

void	*coder_routine(void *arg)
{
	t_coder			*coder;
	t_table			*table;

	coder = (t_coder *)arg;
	table = coder->table;
	if (table->n_coders == 1)
		lone_compile_phase(table, coder);
	while (1)
	{
		if (compile_phase(table, coder))
			return (NULL);
		sim_sleep(table, table->t_compile);
		debug_phase(table, coder);
		sim_sleep(table, table->t_debug);
		pthread_mutex_lock(&table->lock);
		log_state(coder, "is refactoring");
		pthread_mutex_unlock(&table->lock);
		sim_sleep(table, table->t_refactor);
	}
}

void	coder_wait(t_table *table, t_coder *coder)
{
	long long		target_ms;
	struct timespec	abstime;

	while (!coder->granted && !table->stop)
	{
		target_ms = time_now() + 1;
		abstime.tv_sec = target_ms / 1000;
		abstime.tv_nsec = (target_ms % 1000) * 1000000;
		pthread_cond_timedwait(&table->cond, &table->lock, &abstime);
	}
}
