/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   log.c                                             :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/12 15:37:27 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/12 16:24:21 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void log_state(t_coder *coder, char *msg)
{
	long long	timer;

	if (coder->table->stop)
		return ;
	timer = sim_time(coder->table->start_time);
	pthread_mutex_lock(&coder->table->log_lock);
	printf("%lld %i %s\n", timer, coder->id, msg);
	pthread_mutex_unlock(&coder->table->log_lock);
}
