/* RandomFunction.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#ifndef	RANDOMFUNCTION_H
#define	RANDOMFUNCTION_H

/** Random number generation function definition.
 */
typedef struct {
	/** The function that generates a random number. The first parameter
	 * is the user parameter.
	 */
	const double	(* func)(void *);
	/** The first parameter to the function.
	 */
	void *	user;	/* usedata to pass to the function */
} RandomFunction;

/** Range specification for random number generation.
 */
typedef struct {
	/** The low interval border.
	 */
	double	low;
	/** The high interval border.
	 */
	double	high;
} RandomInterval;


/** Multiple random generator functions and one common initialization
 * function.
 */
class
RandomFunctions
{
public:
	/** Initialize all random number generators.
	 */
	static void rand_init (void);

	/** The canonical random number generator.
	 *
	 * Generate one random floating point number within the given range.
	 *
	 * @param range Range of numbers where the random one will lie in.
	 */
	static const double rand_normal (RandomInterval *range);
};

#endif

