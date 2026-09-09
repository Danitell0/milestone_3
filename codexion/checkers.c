/* ************************************************************************** */
/*                                                                            */
/*                                                       ::::::::             */
/*   checkers.c                                        :+:    :+:             */
/*                                                    +:+                     */
/*   By: danmorei <danmorei@student.codam.nl>        +#+                      */
/*                                                  +#+                       */
/*   Created: 2026/09/09 17:18:46 by danmorei     #+#    #+#                  */
/*   Updated: 2026/09/09 17:55:33 by danmorei     ########   odam.nl          */
/*                                                                            */
/* ************************************************************************** */

dongle_ok(d, coder) = !d.held
				&& now >= dongle.cooldown_until
				&& (dongle.reserved_for == NONE ||
						dongle.reserved_for == coder)

can_grant(coder) = dongle_ok(L, coder) && dongle_ok(R, coder)
