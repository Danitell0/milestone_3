/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   time.c                                            :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/12 11:06:50 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/12 15:26:46 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long long time_now(void)
{
	struct	timeval	tv;

	gettimeofday(&tv, NULL);
	return (((long long)tv.tv_sec * 1000) + ((long long)tv.tv_usec / 1000));
}

long long sim_time(long long start_time)
{
	return (time_now() - start_time);
}
