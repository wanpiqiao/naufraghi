/* ActivationFunction.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#ifndef	ACTIVATIONFUNCTION_H
#define	ACTIVATIONFUNCTION_H

/** Neural network activation function.
 *
 * Complete definition of a function and its derivate.
 */
typedef struct {
	/** The symbolic name of the function.
	 */
	char *	name;
	/** Plain function itself. The first parameter gives the x-value,
	 * the second one is the theta value, taken from the neuron.
	 */
	double	(* normal)(double, double);
	/** The derivative function, used for the backpropagation algorithm.
	 */
	double	(* derivate)(double, double);
} ActivationFunction;


/** List of activation functions that are available to the perceptron network.
 */
class
ActivationFunctions
{
public:
	/** Resolve an activation function by symbolic name.
	 *
	 * @param name The function name, as given in the function structure.
	 *
	 * @return NULL on failure, pointer to structure on success.
	 */
	static const ActivationFunction * resolveByName (const char *name);

	/** \f$f_{act} (x, \Theta) = tanh (x - \Theta)\f$
	 */
	static const ActivationFunction fact_tanh;
	/** \f$f_{act} (x, \Theta) = \frac{1}{1 + e^{-(x - \Theta)}}\f$
	 */
	static const ActivationFunction fact_log;
	/** \f$f_{act} (x, \Theta) = x - \Theta\f$
	 */
	static const ActivationFunction fact_linear;
	/** \f$f_{act} (x, \Theta) = \left\{\begin{array}{cl}1.0 & x \geq
	 * \Theta\\-1.0 & x < \Theta\end{array}\right.\f$
	 */
	static const ActivationFunction fact_binary;
};

#endif

