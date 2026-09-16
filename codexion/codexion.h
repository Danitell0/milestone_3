/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   codexion.h                                        :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:08:20 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/16 12:59:13 by danmorei     ########   odam.nl          */
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
# define STEP_SYNC 0
# define STEP_DONGLES 2
# define STEP_CODERS 3
# define STEP_HEAP 4

typedef struct s_coder
{
	int				id;
	long long		last_compile_start;
	int				granted;
	int				compile_count;
	pthread_t		thread;
	struct s_table	*table;
}	t_coder;

typedef struct s_dongle
{
	int				held_by;
	int				reserved_by;
	long long		available_at;
}	t_dongle;

typedef struct s_request
{
	t_coder			*coder;
	long long		arrival;
}	t_request;

typedef struct s_heap
{
	t_request		*items;
	int				count;
	int				capacity;
}	t_heap;

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

	int				init_step;

	/* shared state */
	t_dongle		*dongles;
	t_coder			*coders;
	t_heap			*heap;
	int				stop;
	pthread_t		monitor;

	/* sync */
	pthread_mutex_t	lock;
	pthread_mutex_t	log_lock;
	pthread_cond_t	cond;

	/* timing */
	long long		start_time;
}	t_table;

//Init functions
int			setup(t_table *table, char *argv[]);
void		init_table(t_table *table, char *argv[]);
int			init_dongles(t_table *table);
int			init_coders(t_table *table);
int			init_sync(t_table *table);
int			init_heap(t_table *table);

//Heap functions
int			heap_push(t_table *table, t_coder *coder);
void		heap_delete(t_table *table, int pos);
t_coder		*heap_peek(t_table *table);
void		heap_swap(t_request *a, t_request *b);
void		sift_up(t_table *table, int pos);
void		sift_down(t_table *table, int pos);

//Coder
void		*coder_routine(void *arg);
void		coder_wait(t_table *table, t_coder *coder);

//Monitor
void		*monitor_routine(void *arg);

//Threads
int			create_threads(t_table *table);
void		join_coders(t_table *table, int count);

//Arbitration functions
int			can_grant(t_table *table, int id, long long now);

//Print errors
int			print_error(char *msg);

//Argument validation functions
int			is_valid_number(char *arg);
int			is_higher_priority(t_table *table, t_request *a, t_request *b);
int			is_dongle_ok(t_table *table, int d_id, int c_id, long long now);

//Time functions
long long	time_now(void);
long long	sim_time(long long start_time);

//Clean functions
int			clean(t_table *table);

#endif
