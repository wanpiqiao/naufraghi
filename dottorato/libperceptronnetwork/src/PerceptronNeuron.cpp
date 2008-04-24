/* PerceptronNeuron.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#include <iostream>

#include <neuralnet/PerceptronNeuron.h>


PerceptronNeuron::PerceptronNeuron (unsigned int in_layer_num)
{
    num = in_layer_num;
    delta = 0.0;
    theta = theta_diff = theta_diff_last = 0.0;
}


void
PerceptronNeuron::initializeWeightings (unsigned int succ_count)
{
    weight = vector<double> (succ_count);
    weight_diff = vector<double> (succ_count);
    weight_diff_last = vector<double> (succ_count);

    resetWeights ();
    resetWeightDiffs ();
}


void
PerceptronNeuron::resetWeights (void)
{
    for (unsigned int n = 0 ; n < weight.size () ; ++n)
        weight[n] = 0.0;
}


void
PerceptronNeuron::resetWeightDiffs (void)
{
    for (unsigned int n = 0 ; n < weight_diff.size () ; ++n)
        weight_diff[n] = 0.0;
}


void
PerceptronNeuron::resetDiffs (void)
{
    resetWeightDiffs ();
    theta_diff = 0.0;
}


void
PerceptronNeuron::postprocessWeight (PerceptronNeuron *succ, double epsilon,
    double weight_decay, double momterm)
{
    weight_diff[succ->num] +=
        /* standard backpropagation */
        (-1.0) * epsilon * succ->getDelta () * output -
        /* weight decay term */
        weight_decay * weight[succ->num] +
        /* momentum term */
        momterm * weight_diff_last[succ->num];
}


void
PerceptronNeuron::postprocessTheta (double epsilon, double weight_decay,
    double momterm)
{
    theta_diff += epsilon * delta -
        /* weight decay term */
        weight_decay * theta +
        /* momentum term */
        momterm * theta_diff_last;

//  cout << theta_diff_last << endl;
}


void
PerceptronNeuron::update (void)
{
    theta += theta_diff;
    theta_diff_last = theta_diff;

//  cout << "updated: " << theta_diff_last << endl;

    for (unsigned int n = 0 ; n < weight.size () ; ++n) {
        weight[n] += weight_diff[n];
        weight_diff_last[n] = weight_diff[n];
    }
}


