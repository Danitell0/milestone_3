/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   codexion.h                                        :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:08:20 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/12 16:24:26 by danmorei     ########   odam.nl          */
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

// defines
# define FIFO 1
# define EDF 2

# define STEP_NONE 0
# define STEP_SYNC 1
# define STEP_DONGLES 2
# define STEP_CODERS 3
# define STEP_HEAP 4

typedef struct s_coder
{
	int				id;
	long long		last_compile_start;
	int				compile_count;
	pthread_t 		thread;
	struct	s_table	*table;
}	t_coder;

typedef struct s_dongle
{
	int				held_by;
	int				reserved_by;
	long long		available_at;
}	t_dongle;

typedef struct s_heap
{

}

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

	int 			init_step;

	/* shared state */
	t_dongle		*dongles;
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

//Init functions
int setup(t_table *table, char *argv[]);
void init_table(t_table *table, char *argv[]);
int init_dongles(t_table *table);
int init_coders(t_table *table);
int init_sync(t_table *table);

//Print errors
int print_error(char *msg);

//Argument valudation functions
int	is_valid_number(char *arg);

//Time functions
long long time_now(void);
long long sim_time(long long start_time);

//Clean functions
int	clean(t_table *table);

#endif
