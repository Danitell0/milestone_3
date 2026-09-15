/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   dongle_utils.c                                    :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/15 13:01:20 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/15 13:31:02 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	reserve_dongles(t_table *table, t_coder *coder)
{
	table->dongles[coder->id - 1].reserved_by = coder->id;
	table->dongles[coder->id % table->n_coders].reserved_by = coder->id;
}

void	take_dongles(t_table *table, t_coder *coder)
{
	table->dongles[coder->id - 1].held_by = coder->id;
	table->dongles[coder->id % table->n_coders].held_by = coder->id;
}

void	release_dongles(t_table *table, t_coder *coder, long long now)
{
	long long	new_cooldown;

	new_cooldown = now + table->cooldown;
	table->dongles[coder->id - 1].held_by = 0;
	table->dongles[coder->id % table->n_coders].held_by = 0;
	table->dongles[coder->id - 1].available_at = new_cooldown;
	table->dongles[coder->id % table->n_coders].available_at = new_cooldown;
}
