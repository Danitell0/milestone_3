/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   parse.c                                           :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/10 18:28:38 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/14 15:05:10 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_valid_number(char	*arg)
{
	int		i;

	i = 0;
	if (strlen(arg) == 0 || strlen(arg) > 9)
		return (0);
	while (arg[i] != '\0')
	{
		if (arg[i] < '0' || arg[i] > '9')
			return (0);
		i++;
	}
	return (1);
}
