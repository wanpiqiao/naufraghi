/* PerceptronNeuron.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#ifndef	PERCEPTRONNEURON_H
#define	PERCEPTRONNEURON_H

#include <vector>

using namespace std;

/** Represent one neuron  within a layer of the neural network.
 */

class
PerceptronNeuron {
public:
	/** Counter within the current layer (top = 0) */
	unsigned int	num;

	/** Input signal level for this node, \f$net_{p,i}^{\lambda}\f$. */
	double	input;

	/** Output signal level for this node, \f$y_{p,i}^{\lambda}\f$. */
	double	output;

	/** Weightings to neurons in the next layer. Hence, the size of the
	 * vector must equal the number of neurons in the next layer
	 */
	vector<double>	weight;

	/** Delta-value for the individual weightings the node has to its
	 * successor nodes. Computed by the Processing algorithm
	 *
	 * Note this is within the public space due to the from-file
	 * constructor of PerceptronNetwork, which push_back's zeroes here.
	 */
	vector<double>	weight_diff;

	/* functions */

	/** Main constructor.
	 *
	 * @param in_layer_num number of neuron within its layer.
	 */
	PerceptronNeuron (unsigned int in_layer_num);

	/** Getter function for the delta variable.
	 */
	double getDelta (void) {
		return (delta);
	}

	/** Setter function for the delta variable.
	 *
	 * @param newval New value to be assigned to delta.
	 */
	void setDelta (double newval) {
		delta = newval;
	}

	/** Getter function for theta parameter.
	 */
	double getTheta (void) {
		return (theta);
	}

	/** Setter function for theta parameter.
	 */
	void setTheta (double newval) {
		theta = newval;
	}

	/** Getter for the difference calculated for the theta parameter.
	 */
	double getThetaDiff (void) {
		return (theta_diff);
	}

	/** Initialize the weightings vectors used for each neuron to zero.
	 *
	 * @param succ_count number of successor neurons to this neuron.
	 */
	void initializeWeightings (unsigned int succ_count);

	/** Reset all weightings to zero.
	 */
	void resetWeights (void);

	/** Reset all weight deltas to zero.
	 */
	void resetWeightDiffs (void);

	/** Reset all learned differences.
	 */
	void resetDiffs (void);

	/* ALGORITHMS */

	/** Weighting postprocess algorithm. Assign the weight differences to
	 * this neuron. Note that the assignment is done by adding the new
	 * delta value to the current one. Hence, both batch- and online
	 * learning can use this function. For online-learning the values must
	 * be resetted after each update using the resetWeightDiffs method.
	 * Also, only one weighting difference is calculated at a time. The
	 * computation of all differences is scheduled by
	 * PerceptronLayer::postprocess.
	 *
	 * @param succ Successor neuron to the current neuron.
	 * @param epsilon Learning parameter.
	 * @param weight_decay Weight decay factor.
	 * @param momterm Momentum term factor.
	 * @see resetWeightDiffs ()
	 */
	void postprocessWeight (PerceptronNeuron *succ, double epsilon,
		double weight_decay, double momterm);

	/** Theta postprocess algorithm. Assign the theta differences to this
	 * neuron.
	 *
	 * @param epsilon Learning parameter.
	 * @param weight_decay Weight decay factor.
	 * @param momterm Momentum term factor.
	 */
	void postprocessTheta (double epsilon, double weight_decay,
		double momterm);

	/** Update algorithm. Update weightings and theta parameter by the
	 * values calculated in the postprocess step.
	 */
	void update (void);

protected:
	/** Errorsignal, computed by the backpropagation algorithm. Used to
	 * compute the deltas for both the weightings and the sensitivity
	 * parameter
	 */
	double	delta;

	/** Sensitivity parameter to the activation function */
	double	theta;
	/** Delta-value for the sensitivity, calculated by the Processing
	 * algorithm, used to update theta within the Update algorithm
	 */
	double	theta_diff;

	/** The previous theta difference, used for momentum term calculation.
	 */
	double	theta_diff_last;

	/** The previous weight differences, used for momentum term.
	 */
	vector<double>	weight_diff_last;
};

#endif

