/* ActivationFunction.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */
#include <stdio.h>
#include <string.h>
#include <math.h>

#ifndef ACTIVATIONFUNCTION_H
#define ACTIVATIONFUNCTION_H

/** Neural network activation function.
 *
 * Complete definition of a function and its derivate.
 */
typedef struct {
    /** The symbolic name of the function.
     */
    char *  name;
    /** Plain function itself. The first parameter gives the x-value,
     * the second one is the theta value, taken from the neuron.
     */
    double  (* normal)(double, double);
    /** The derivative function, used for the backpropagation algorithm.
     */
    double  (* derivate)(double, double);
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

static double
fact_tanh_normal (double in, double theta)
{
    return (tanh (in - theta));
}

static double
fact_tanh_derivate (double in, double theta)
{
    return (1.0 - pow (tanh (in - theta), 2.0));
}

static double
fact_log_normal (double in, double theta)
{
    return (1.0 / (1.0 + pow (M_E, theta - in)));
}

static double
fact_log_derivate (double in, double theta)
{
    double  e_val;

    e_val = pow (M_E, theta - in);

    return (e_val / pow (e_val + 1.0, 2.0));
}

static double
fact_linear_normal (double in, double theta)
{
    return (in - theta);
}

static double
fact_linear_derivate (double in, double theta)
{
    return (1.0);
}

static double
fact_binary_normal (double in, double theta)
{
    if (in >= theta)
        return (1.0);

    return (-1.0);
}

static double
fact_binary_derivate (double in, double theta)
{
    return (1.0);
}


const ActivationFunction
ActivationFunctions::fact_tanh = {
    "tanh",
    fact_tanh_normal,
    fact_tanh_derivate,
};

const ActivationFunction
ActivationFunctions::fact_log = {
    "log",
    fact_log_normal,
    fact_log_derivate,
};

const ActivationFunction
ActivationFunctions::fact_linear = {
    "linear",
    fact_linear_normal,
    fact_linear_derivate,
};

const ActivationFunction
ActivationFunctions::fact_binary = {
    "binary",
    fact_binary_normal,
    fact_binary_derivate,
};


const ActivationFunction *
ActivationFunctions::resolveByName (const char *name)
{
    if (strcmp (name, "tanh") == 0)
        return (&fact_tanh);
    if (strcmp (name, "log") == 0)
        return (&fact_log);
    if (strcmp (name, "linear") == 0)
        return (&fact_linear);
    if (strcmp (name, "binary") == 0)
        return (&fact_binary);

    return (NULL);
}

#endif

