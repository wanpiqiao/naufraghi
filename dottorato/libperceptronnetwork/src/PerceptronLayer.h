/* PerceptronLayer.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#ifndef	PERCEPTRONLAYER_H
#define	PERCEPTRONLAYER_H

#include <vector>

using namespace std;

#include <neuralnet/ActivationFunction.h>
#include <neuralnet/RandomFunction.h>
#include <neuralnet/PerceptronNeuron.h>

/** Represent one layer within the neural network.
 */
enum PerceptronLayerType { Input, Hidden, Output };

/** One layer within the perceptron network.
 *
 * Most algorithm related calculation is done at the layer level.
 */
class
PerceptronLayer {
public:
	/** Type of the layer within the network. The input layer is always
	 * the first, the output layer the last layer in the network. Every
	 * other layer must be a hidden layer.
	 */
	PerceptronLayerType	type;

	/** Every layer contains at least one neuron. This is the list of
	 * neurons within this layer.
	 */
	vector<PerceptronNeuron *>	neurons;

	/** PerceptronLayer constructor, creating a layer with \a neuron_count
	 * number of neurons.
	 *
	 * @param neuron_count Number of neurons within this layer.
	 * @param fact Activation function to use for this layer.
	 */
	PerceptronLayer (unsigned int neuron_count,
		const ActivationFunction *fact);

	/** PerceptronLayer destructor, mainly removing all the subneurons
	 * within this layer.
	 */
	~PerceptronLayer (void);

	/** Copy constructor.
	 *
	 * @param source Source object to be copied.
	 */
	PerceptronLayer (PerceptronLayer& source);

	/** Network randomization functions.
	 *
	 * Randomize variable network parameters: weightings and theta values.
	 * Use individual functions for greater customizeability.
	 *
	 * @param succ Succeeding layer in network. Must be non-NULL.
	 * @param weight_func Function to generate weighting parameters.
	 * @param theta_func Function to generate theta values.
	 */
	void randomizeParameters (PerceptronLayer *succ,
		const RandomFunction *weight_func,
		const RandomFunction *theta_func);

	/** Reset functions for learned differences.
	 *
	 * This function resets all parameters that are learned by the
	 * backpropagation and postprocess algorithms. It has to be called
	 * after an update has been made. This way, both online- and
	 * batch-learning can be implemented.
	 */
	void resetDiffs (void);

	/** Setter for the activation function.
	 *
	 * @param fact Activation function to use for this layer.
	 */
	void setActivationFunction (const ActivationFunction *fact);

	/** Getter for the activation function.
	 */
	const ActivationFunction * getActivationFunction (void) const;

	/* ALGORITHMS */

	/** Forward propagation algorithm. The input and output signals of
	 * this layer is calculated from the output signals of the \a pred
	 * layer.
	 *
	 * @param pred the layer before this one, can be NULL.
	 */
	void propagate (PerceptronLayer *pred);

	/** Backpropagation algorithm.
	 *
	 * Compute the delta value for all neurons within this layer.
	 *
	 * @param succ Succeeding layer to this one, can be NULL.
	 * @param test_output Test expected output for the last layer
	 * (output).
	 * @param test_tolerance The test difference tolerance parameter.
	 */
	void backpropagate (PerceptronLayer *succ,
		vector<double> &test_output, double test_tolerance);

	/** Postprocess algorithm for a single layer.
	 *
	 * @param succ Successor layer to this one, or NULL if it is the
	 * last.
	 * @param epsilon Learning parameter.
	 * @param weight_decay Weight decay factor.
	 * @param momterm Momentum term factor.
	 */
	void postprocess (PerceptronLayer *succ, double epsilon,
		              double weight_decay, double momterm);

	/** Update algorithm for a single layer.
	 */
	void update (void);

protected:
	/** Activation function and its derivate. Used for both propagation
	 * and backpropagation. Must be set and can be different for each
	 * layer.
	 */
	const ActivationFunction *	fact;
};

#endif

