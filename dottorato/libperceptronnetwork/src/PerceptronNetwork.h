/* PerceptronNetwork.h
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#ifndef PERCEPTRONNETWORK_H
#define PERCEPTRONNETWORK_H

#include <vector>
#include <fstream>

#include <neuralnet/ActivationFunction.h>
#include <neuralnet/RandomFunction.h>
#include <neuralnet/PerceptronLayer.h>

/** One multilayer perceptron network.
 */

class
PerceptronNetwork {
    /** The GUI visualization class is declared friend to allow access to
     * individual layers.
     */
    friend class WeightMatrix;

public:
    /** Symbolic name of the network. Never used by the methods
     * themselves, but convenient to use.
     */
    const char *    name;

    /** Input vector, fed into the first layer of the network. The number
     * of elements must equal the number of neurons within the input
     * layer.
     */
    vector<double>  input;

    /** Output vector, resulting from propagation through the entire
     * network. The number of elements equals the number of output neurons
     * within the network.
     */
    vector<double>  output;

    /** PerceptronNetwork constructor
     *
     * Construct a multilayer perceptron network by layer description
     * given through \a desc_layers. The vector size specifies the number
     * of layers, the individual elements the number of neurons within its
     * layer.
     *
     * @param desc_layers Number of neurons within each layer, given the
     * input layer as first and the output layer as last. Hence, the size
     * of the vector must be at least two.
     *
     * @param network_name Symbolic name of the network. Can be NULL. The
     * name is pointer-copied, so we steal a pointer here.
     *
     * @param fact Activation function to use for all neurons by default
     * within the network. By default, its the tangens-hyperbolicus
     * function. For individual layers, based one their type, the
     * activation function can be changed using the changeActivation
     * method.
     */
    PerceptronNetwork (vector<unsigned int> desc_layers,
                       const char *network_name = "unnamed",
                       const ActivationFunction *fact = &ActivationFunctions::fact_tanh);

    /* Default constructor. (To be used with the load method).
     */
    PerceptronNetwork (void);

    /** PerceptronNetwork destructor
     *
     * Remove all layers stored within the network.
     */
    ~PerceptronNetwork (void);

    /** Copy constructor.
     *
     * @param source Source object to be copied.
     */
    PerceptronNetwork (PerceptronNetwork& source);

    /** Set the activation function for layers, based on their type.
     *
     * @param type Type of layers that will use the new activation
     * function.
     * @param fact Activation function to use.
     */
    void setActivationFunction (PerceptronLayerType type,
                                const ActivationFunction *fact);

    /* LOAD/SAVE methods */
    /** Save the entire network as text into the stream \a fs.
     *
     * @param fs Stream (output) to save the network to.
     */
    void save (fstream& fs) const;

    /** Load the entire network from stream \a fs.
     *
     * @param fs Stream (input) to read the network from.
     *
     * @return True on success, false on failure.
     */
    bool load (fstream& fs);

    /* NETWORK operation methods */

    /** Randomize the variable network parameters, weightings and theta
     * values.
     *
     * @param weight_func Function to randomize weighting values.
     * @param theta_func Function to randomize theta parameters.
     */
    void randomizeParameters (const RandomFunction *weight_func,
                              const RandomFunction *theta_func);

    /** Setter for the entire network input.
     *
     * @param in Vector of input signal levels. The size must equal the
     * input layer neuron count.
     */
    void setInput (vector<double>& in);

    /** Setter for the requested network output.
     *
     * Must be used before any learning algorithm is called
     * (backpropagate).
     *
     * @param test Test network output for the current input.
     */
    void setTestOutput (vector<double>& test);

    /** Getter for the entire network output.
     */
    vector<double> getOutput (void) const;

    /** Calculate the errorterm for the network
     *
     * The error value for the current output is calculated. The current
     * test output must be given prior to calling this function.
     *
     * The formula used is \f$E = \frac{1}{2} \sum_{i} \left(t_{p,i} -
     * y_{p,i}^{\lambda,L}\right)^2\f$.
     */
    double errorTerm (void) const;

    /** Reset all learned parameters.
     *
     * Call after an update has been made.
     */
    void resetDiffs (void);

    /* ALGORITHMS */

    /** Propagation algorithm for the entire network.
     *
     * The input levels to the network have to be set using the setInput()
     * method, before. Afterwards the output of the network can be
     * obtained using the getOutput() method.
     */
    void propagate (void);

    /** Backpropagation algorithm for the entire network.
     *
     * Calculate all delta error signals in every layer and their neurons.
     * Every neuron must have a proper input/output signal assigned, and
     * the test_output training target result is used for calculation.
     */
    void backpropagate (void);

    /** Postprocess algorithm for the entire network.
     */
    void postprocess (void);

    /** Update algorithm for the entire network.
     */
    void update (void);

    /* DEBUG facilities */
    /** Dump whole neural network as graph file in the GraphViz file
     * format (www.graphviz.org).
     *
     * @param filename Name of the file to write the graph data to.
     */
    void dumpNetworkGraph (const char *filename) const;

    /** Getter for the epsilon parameter.
     */
    double getLearningParameter (void) const;

    /** Setter for the epsilon parameter.
     *
     * @param epsilon Learn parameter, in the range of 0.0 to 0.5.
     */
    void setLearningParameter (double epsilon);

    /** Getter for the test tolerance parameter.
     */
    double getTestTolerance (void) const;

    /** Setter for the test tolerance parameter.
     *
     * @param tolerance Value between 0.0 and 0.2.
     */
    void setTestTolerance (double tolerance);

    /** Getter for the weight decay parameter.
     */
    double getWeightDecayParameter (void) const;

    /** Setter for the weight decay parameter.
     *
     * @param factor Value in the range of 0.00005 to 0.0001.
     */
    void setWeightDecayParameter (double factor);

    /** Getter for the momentum term parameter.
     */
    double getMomentumTermParameter (void) const;

    /** Setter for the momentum term parameter.
     *
     * @param factor Value between 0.5 and 0.9.
     */
    void setMomentumTermParameter (double factor);

protected:
    /** Test expected output vector, used for the learning process. For
     * simple propagation it is not needed.
     */
    vector<double>  test_output;

    /** Left-to-right list of layers within the network. Must be at least
     * two (one input and one output layer), but can be arbitrary large.
     * More than four layers does not archive any improvement of the
     * network capabilities, though.
     */
    vector<PerceptronLayer *>   layers;

    /** Generic learn parameter epsilon, should be between 0.05 and 0.5.
     */
    double      epsilon;

    /** Test tolerance parameter, should be between 0.0 and 0.2.
     */
    double      test_tolerance;

    /** Weight decay parameter, should be between 0.005 and 0.03.
     */
    double      weight_decay;

    /** Momentum term parameter, should be between 0.5 and 0.9.
     */
    double      momentum_term;
};

#endif

