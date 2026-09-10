/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   codexion.h                                        :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:08:20 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/10 20:37:09 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <stdio.h>
# include <string.h>
# include <stdlib.h>
# include <unistd.h>
# include <pthread.h>
# include <sys/time.h>

# define FIFO 1
# define EDF 2

typedef struct s_coder
{
	int				id;
	long long		last_compile_start;
	int				compile_count;
	pthread_t 		thread;
	struct	s_table	*table;
}	t_coder;

typedef struct s_table
{
	/* config */
	int				n_coders;
	long long		t_burnout;
	long long		t_compile;
	long long		t_debug;
	long long		t_refactor;
	int				compiles_required;
	long long		cooldown;
	int				scheduler;

	/* shared state */
//	t_dongle		*dongles;
	t_coder			*coders;
//	t_heap			*queue;
	int				stop;

	/* sync */
	pthread_mutex_t	lock;
	pthread_mutex_t	log_lock;
	pthread_cond_t	cond;

	/* timing */
	long long		start_time;
}	t_table;

//Print errors
int print_error(char *msg);

//Argument valudation functions
int	is_valid_number(char *arg);

#endif
