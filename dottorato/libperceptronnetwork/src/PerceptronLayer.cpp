/* PerceptronLayer.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#include <iostream>

using namespace std;

#include <assert.h>

#include <neuralnet/PerceptronLayer.h>


PerceptronLayer::PerceptronLayer (unsigned int neuron_count,
	const ActivationFunction *fact)
{
	this->fact = fact;
	neurons = vector<PerceptronNeuron *> (neuron_count);

	for (unsigned int n = 0 ; n < neuron_count ; ++n)
		neurons[n] = new PerceptronNeuron (n);
}


PerceptronLayer::~PerceptronLayer (void)
{
	unsigned int	n;

	for (n = 0 ; n < neurons.size () ; ++n)
		delete neurons[n];
}


PerceptronLayer::PerceptronLayer (PerceptronLayer& source)
{
	type = source.type;
	fact = source.fact;

	for (unsigned int nn = 0 ; nn < source.neurons.size () ; ++nn)
		neurons.push_back (new PerceptronNeuron (*source.neurons[nn]));
}


void
PerceptronLayer::randomizeParameters (PerceptronLayer *succ,
	const RandomFunction *weight_func, const RandomFunction *theta_func)
{
	unsigned int	n,
			wn;

	for (n = 0 ; n < neurons.size () ; ++n) {
		/* initialize theta value accordingly
		 * note that Input type layers do not have a theta value.
		 */
		if (type != Input)
			neurons[n]->setTheta (theta_func->func
				(theta_func->user));

		/* if there is no succeeding layer, skip weight assignment
		 */
		if (succ == NULL)
			continue;

		/* now all weighted connections to neurons in the succeeding
		 * layer
		 */
		for (wn = 0 ; wn < succ->neurons.size () ; ++wn) {
			neurons[n]->weight[wn] =
				weight_func->func (weight_func->user);
		}
	}
}


void
PerceptronLayer::resetDiffs (void)
{
	for (unsigned int n = 0 ; n < neurons.size () ; ++n)
		neurons[n]->resetDiffs ();
}


void
PerceptronLayer::setActivationFunction (const ActivationFunction *fact)
{
	this->fact = fact;
}


const ActivationFunction *
PerceptronLayer::getActivationFunction (void) const
{
	return (fact);
}


void
PerceptronLayer::propagate (PerceptronLayer *pred)
{
	double		input_sum;
	unsigned int	nidx;

	/* first calculate all the inputs of this layer, then the neuron
	 * activation. note that we never propagate an Input type layer.
	 */
	assert (type != Input);

	for (nidx = 0 ; nidx < neurons.size () ; ++nidx) {
		input_sum = 0.0;

		/* sum up all (weight * output) products from the previous
		 * layer
		 */
		for (unsigned int pn = 0 ; pn < pred->neurons.size () ; ++pn) {
			input_sum += pred->neurons[pn]->weight[nidx] *
				pred->neurons[pn]->output;
		}

		neurons[nidx]->input = input_sum;
	}

	/* now calculate the output of each neuron
	 */
	for (nidx = 0 ; nidx < neurons.size () ; ++nidx) {
		neurons[nidx]->output = fact->normal (neurons[nidx]->input,
			neurons[nidx]->getTheta ());
	}
}


void
PerceptronLayer::backpropagate (PerceptronLayer *succ,
	vector<double>& output_optimal, double opt_tolerance)
{
	unsigned int	nidx,
			sn;
	double		delta,
			opt_diff;

	for (nidx = 0 ; nidx < neurons.size () ; ++nidx) {
		/* an output-layer neuron
		 */
		if (type == Output) {
			delta = fact->derivate (neurons[nidx]->input,
				neurons[nidx]->getTheta ());

			opt_diff = (output_optimal[nidx] - neurons[nidx]->output);

			/* when the difference is below the tolerance
			 * treshhold, we just set it to zero.
			 */
			if (opt_tolerance != 0.0 &&
				opt_diff >= (-1.0 * opt_tolerance) &&
				opt_diff <= opt_tolerance)
			{
				opt_diff = 0.0;
			}

			delta *= opt_diff;
			delta *= -1.0;
			neurons[nidx]->setDelta (delta);

			continue;
		}

		/* a normal (non-output-layer) neuron
		 *
		 * sum up all weighted delta values of the successor neurons
		 */
		delta = 0.0;
		for (sn = 0 ; sn < succ->neurons.size () ; ++sn) {
			delta += neurons[nidx]->weight[sn] *
				succ->neurons[sn]->getDelta ();
		}
		delta *= fact->derivate (neurons[nidx]->input,
			neurons[nidx]->getTheta ());

		neurons[nidx]->setDelta (delta);
	}
}


void
PerceptronLayer::postprocess (PerceptronLayer *succ, double epsilon,
	double weight_decay, double momterm)
{
	unsigned int	n,
			succ_n;

	for (n = 0 ; n < neurons.size () ; ++n) {
		neurons[n]->postprocessTheta (epsilon, weight_decay, momterm);

		/* for each successor neuron, postprocess the weighting
		 * differences.
		 */
		for (succ_n = 0 ; succ != NULL &&
			succ_n < succ->neurons.size () ; ++succ_n)
		{
			neurons[n]->postprocessWeight (succ->neurons[succ_n],
				epsilon, weight_decay, momterm);
		}
	}
}


void
PerceptronLayer::update (void)
{
	for (unsigned int n = 0 ; n < neurons.size () ; ++n)
		neurons[n]->update ();
}


