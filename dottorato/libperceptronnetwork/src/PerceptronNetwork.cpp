/* PerceptronNetwork.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#include <iostream>
#include <iomanip>
#include <fstream>

using namespace std;

#include <assert.h>
#include <string.h>

#include <neuralnet/PerceptronNetwork.h>
#include <neuralnet/PerceptronLayer.h>


PerceptronNetwork::PerceptronNetwork (vector<unsigned int> desc_layers,
                                      const char *network_name,
                                      const ActivationFunction *fact)
{
    unsigned int    n,
                    neuron;

    assert (desc_layers.size () >= 2);

    name = network_name;
    epsilon = test_tolerance = weight_decay = momentum_term = 0.0;

    /* create public input/output interface arrays
     */
    input = vector<double> (desc_layers[0]);
    output = vector<double> (desc_layers[desc_layers.size () - 1]);
    test_output = vector<double> (desc_layers[desc_layers.size () - 1]);

    /* create internal layer representation
     */
    layers = vector<PerceptronLayer *> (desc_layers.size ());

    for (n = 0 ; n < desc_layers.size () ; ++n) {
        layers[n] = new PerceptronLayer (desc_layers[n], fact);

        if (n == 0) {
            layers[n]->type = Input;
            continue;
        } else if (n == (desc_layers.size () - 1)) {
            layers[n]->type = Output;
        } else {
            layers[n]->type = Hidden;
        }

        /* link all neurons of the previous layer with this layer
         * leave the weightings untouched per-value, but reserve space
         */
        for (neuron = 0 ; neuron < layers[n - 1]->neurons.size () ;
            ++neuron)
        {
            PerceptronNeuron *  n_cur;

            n_cur = layers[n - 1]->neurons[neuron];
            n_cur->initializeWeightings (layers[n]->neurons.size ());
        }
    }
}


PerceptronNetwork::~PerceptronNetwork (void)
{
    unsigned int    n;

    for (n = 0 ; n < layers.size () ; ++n) {
        if (layers[n] != NULL)
            delete layers[n];
    }
}


PerceptronNetwork::PerceptronNetwork (PerceptronNetwork& source)
{
    name = source.name;
    input = source.input;
    output = source.output;
    test_output = source.test_output;
    epsilon = source.epsilon;
    test_tolerance = source.test_tolerance;
    weight_decay = source.weight_decay;
    momentum_term = source.momentum_term;

    for (unsigned int ln = 0 ; ln < source.layers.size () ; ++ln)
        layers.push_back (new PerceptronLayer (*source.layers[ln]));
}


PerceptronNetwork::PerceptronNetwork (void)
{
    name = NULL;
    epsilon = test_tolerance = weight_decay = momentum_term = 0.0;
}


void
PerceptronNetwork::setActivationFunction (PerceptronLayerType type, const ActivationFunction *fact)
{
    for (unsigned int ln = 0 ; ln < layers.size () ; ++ln) {
        if (layers[ln]->type != type)
            continue;

        layers[ln]->setActivationFunction (fact);
    }
}


bool
PerceptronNetwork::load (fstream &fs)
{
    char        act_str[16];
    unsigned int    layer_count,
                    neuron_count,
                    ln,     /* layer index */
                    nn,     /* neuron index */
                    sn;     /* successor neuron index */
    PerceptronLayer *   lay = NULL;
    const ActivationFunction *  fact;


    fs >> layer_count;
    layers = vector<PerceptronLayer *> (layer_count);
    for (ln = 0 ; ln < layer_count ; ++ln)
        layers[ln] = NULL;

    for (ln = 0 ; ln < layer_count ; ++ln) {
        fs >> neuron_count;

        /* read in activation function string and decode
         */
        fs.width (sizeof (act_str));
        fs >> act_str;
        act_str[sizeof (act_str) - 1] = '\0';

        if (strcmp (act_str, "tanh") == 0) {
            fact = &ActivationFunctions::fact_tanh;
        } else if (strcmp (act_str, "log") == 0) {
            fact = &ActivationFunctions::fact_log;
        } else if (strcmp (act_str, "linear") == 0) {
            fact = &ActivationFunctions::fact_linear;
        } else if (strcmp (act_str, "binary") == 0) {
            fact = &ActivationFunctions::fact_binary;
        } else {
            return (false);
        }
        assert (fact != NULL);

        lay = layers[ln] = new PerceptronLayer (neuron_count, fact);
        if (ln == 0)
            lay->type = Input;
        else if (ln == (layer_count - 1))
            lay->type = Output;
        else
            lay->type = Hidden;
    }

    for (ln = 0 ; ln < layer_count ; ++ln) {
        for (nn = 0 ; nn < layers[ln]->neurons.size () ; ++nn) {
            double  theta;

            lay = layers[ln];

            fs >> theta;
            lay->neurons[nn]->setTheta (theta);

            /* for the last layer, skip the weight assignment step
             */
            if (ln == (layer_count - 1))
                continue;

            lay->neurons[nn]->initializeWeightings
                (layers[ln+1]->neurons.size ());

            for (sn = 0 ; sn < layers[ln + 1]->neurons.size () ; ++sn)
            {
                fs >> lay->neurons[nn]->weight[sn];
            }
        }
    }

    input = vector<double> (layers[0]->neurons.size ());
    output = vector<double> (layers[layers.size () - 1]->neurons.size ());
    test_output = output;

    return (true);
}


void
PerceptronNetwork::save (fstream& fs) const
{
    unsigned int        ln, /* layer index */
                        nn, /* neuron index */
                        sn; /* succeeding neuron index */
    PerceptronLayer *   lay;

    /* an 80 bit double (ia32): 64 bit mantissa / 15 bit exponent, can
     * represent ~19.26 decimal digets, so with 32 we are on a pretty safe
     * bet. ;)
     */
    fs << setprecision (32);

    /* output according to doc/neural-network-textformat.txt
     */
    fs << layers.size () << endl;

    for (ln = 0 ; ln < layers.size () ; ++ln) {
        if (ln > 0)
            fs << " ";
        fs << layers[ln]->neurons.size ();
        fs << " " << layers[ln]->getActivationFunction ()->name;
    }
    fs << endl;

    for (ln = 0 ; ln < layers.size () ; ++ln) {
        lay = layers[ln];
        for (nn = 0 ; nn < lay->neurons.size () ; ++nn) {
            fs << "   " << lay->neurons[nn]->getTheta ();

            for (sn = 0 ; ln < (layers.size () - 1) &&
                sn < layers[ln+1]->neurons.size () ; ++sn)
            {
                fs << " ";
                fs << lay->neurons[nn]->weight[sn];
            }
            fs << endl;
        }
    }
}


void
PerceptronNetwork::randomizeParameters (const RandomFunction *weight_func,
                                        const RandomFunction *theta_func)
{
    unsigned int    ln;

    for (ln = 0 ; ln < (layers.size () - 1) ; ++ln) {
        layers[ln]->randomizeParameters (layers[ln + 1], weight_func, theta_func);
    }

    /* the last layer has no successor
     */
    layers[ln]->randomizeParameters (NULL, weight_func, theta_func);
}


void
PerceptronNetwork::setInput (vector<double>& in)
{
    input = in;
}


void
PerceptronNetwork::setTestOutput (vector<double>& test)
{
    test_output = test;
}


vector<double>
PerceptronNetwork::getOutput (void) const
{
    return (output);
}


double
PerceptronNetwork::errorTerm (void) const
{
    double          error,  /* overall error value */
                    suberr; /* error for one neuron */
    unsigned int        nn; /* neuron index */
    PerceptronLayer *   outlay; /* output layer */


    outlay = layers[layers.size () - 1];

    /* sum up the error using the errorterm formula
     */
    error = 0.0;
    for (nn = 0 ; nn < outlay->neurons.size () ; ++nn) {
        suberr = (test_output[nn] - outlay->neurons[nn]->output);
        error += suberr * suberr;
    }

    error /= 2.0;

    return (error);
}


void
PerceptronNetwork::resetDiffs (void)
{
    unsigned int    n;

    for (n = 0 ; n < layers.size () ; ++n)
        layers[n]->resetDiffs ();
}


void
PerceptronNetwork::propagate (void)
{
    unsigned int        nn, /* neuron index */
                        ln; /* layer index */
    PerceptronLayer *   prev = NULL;

    /* set output for the first layer from the network input
     */
    for (nn = 0 ; nn < layers[0]->neurons.size () ; ++nn) {
        layers[0]->neurons[nn]->input =
        layers[0]->neurons[nn]->output = input[nn];
    }

    prev = layers[0];
    for (ln = 1 ; ln < layers.size () ; ++ln) {
        layers[ln]->propagate (prev);
        prev = layers[ln];
    }

    /* set the output for the entire network from the output layer (prev)
     */
    for (nn = 0 ; nn < prev->neurons.size () ; ++nn)
        output[nn] = prev->neurons[nn]->output;
}


void
PerceptronNetwork::backpropagate (void)
{
    int         ln;
    PerceptronLayer *   succ = NULL;


    /* walk the layers, starting at the output layer
     */
    for (ln = (layers.size () - 1) ; ln > 0 ; --ln) {
        layers[ln]->backpropagate (succ, test_output, test_tolerance);
        succ = layers[ln];
    }
}


void
PerceptronNetwork::postprocess (void)
{
    unsigned int        n;
    PerceptronLayer *   succ;

    for (n = 0 ; n < layers.size () ; ++n) {
        /* in case of the last layer, we do not have a successor.
         */
        if (n == (layers.size () - 1))
            succ = NULL;
        else
            succ = layers[n + 1];

        layers[n]->postprocess (succ, epsilon, weight_decay, momentum_term);
    }
}


void
PerceptronNetwork::update (void)
{
    for (unsigned int n = 0 ; n < layers.size () ; ++n)
        layers[n]->update ();
}


void
PerceptronNetwork::dumpNetworkGraph (const char *filename) const
{
    unsigned int    ln, /* layer index */
                    nn, /* neuron index */
                    snn,    /* successor neuron index */
                    wd; /* neuron weight diff index */
    fstream dotf (filename, ios::out | ios::trunc);

    dotf << "digraph Network {" << endl;
    dotf << "\tgraph [" << endl << "\t\trankdir = \"LR\"" << endl;
    dotf << "\t];" << endl;
    dotf << endl;

    dotf << "\t\"legend\" [ label = \"{ Input | ";
    dotf << "{ lambda, neuron-index | Theta | Delta | Theta-Diff | Weight-Diffs }";
    dotf << " | Output }\"" << endl;
    dotf << "\t\tshape = \"record\"" << endl;
    dotf << "\t\tstyle = \"filled\" fillcolor = \"yellow\" ];" << endl;

    for (ln = 0 ; ln < layers.size () ; ++ln) {
        /*
        dotf << "\tsubgraph layer_" << ln << " {" << endl;
        dotf << "\t\tlabel = \"layer " << ln << "\";" << endl;
        dotf << "\t\tcolor = \"blue\";" << endl;
        */

        for (nn = 0 ; nn < layers[ln]->neurons.size () ; ++nn) {
            dotf << "\t\"neuron_" << ln << "_" << nn << "\" " <<
                "[ label = \"{ <fi> " <<
                layers[ln]->neurons[nn]->input
                << "| { " << ln << "," << nn
                << ": " << layers[ln]->getActivationFunction ()->name
                << "|" <<
                layers[ln]->neurons[nn]->getTheta () <<
                " | " << layers[ln]->neurons[nn]->getDelta ();
            dotf << " | " << layers[ln]->neurons[nn]->getThetaDiff ();
            dotf << " | ";
            for (wd = 0 ; wd < layers[ln]->neurons[nn]->weight_diff.size () ; ++wd) {
                dotf << layers[ln]->neurons[nn]->weight_diff[wd] << ", ";
            }
            dotf <<
                " } | <fo> " <<
                layers[ln]->neurons[nn]->output
                << "}\"" << endl;
            dotf << "\t\tshape = \"record\" ];" << endl;

            if (ln == (layers.size () - 1))
                continue;

            for (snn = 0 ; snn < layers[ln+1]->neurons.size () ; ++snn) {
                dotf << "\t";
                dotf << "\"neuron_" << ln << "_" << nn << "\":fo";
                dotf << " -> ";
                dotf << "\"neuron_" << (ln+1) << "_" << snn << "\":fi";

                dotf << " [ label=\"" << layers[ln]->neurons[nn]->weight[snn] <<
                    "\" ]";
                dotf << ";" << endl;
            }
        }

        /*
        dotf << "\t}" << endl;
        */
    }

    dotf << "}" << endl;
    dotf.close ();
}


double
PerceptronNetwork::getLearningParameter (void) const
{
    return (epsilon);
}


void
PerceptronNetwork::setLearningParameter (double epsilon)
{
    assert (epsilon >= 0.0 && epsilon <= 0.5);
    this->epsilon = epsilon;
}


double
PerceptronNetwork::getTestTolerance (void) const
{
    return (test_tolerance);
}


void
PerceptronNetwork::setTestTolerance (double tolerance)
{
    assert (tolerance >= 0.0 && tolerance <= 0.2);
    test_tolerance = tolerance;
}


double
PerceptronNetwork::getWeightDecayParameter (void) const
{
    return (weight_decay);
}


void
PerceptronNetwork::setWeightDecayParameter (double factor)
{
    weight_decay = factor;
}


double
PerceptronNetwork::getMomentumTermParameter (void) const
{
    return (momentum_term);
}


void
PerceptronNetwork::setMomentumTermParameter (double factor)
{
    momentum_term = factor;
}


