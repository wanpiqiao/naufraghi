/* libtest.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 *
 * howto use:
 * $ ./libtest | grep gnuplot > out.dat
 * $ gnuplot
 * gnuplot> plot "out.dat" using 1:2, "training.dat" using 1:2
 */

#include <iostream>
#include <fstream>
#include <math.h>

#include "ActivationFunction.h"
#include "RandomFunction.h"
#include "PerceptronNetwork.h"


static void testNetwork (PerceptronNetwork *net);


int
main (int argc, char *argv[])
{
	vector<unsigned int>	gen;
	PerceptronNetwork *	net;

	RandomFunctions::rand_init ();

#if	0
	fstream netfile ("sinus-net.txt", ios::in);
//	fstream netfile ("out.net.txt", ios::in);
	net = new PerceptronNetwork ();
	if (net->load (netfile) == false) {
		cerr << "load of network failed." << endl;
		exit (EXIT_FAILURE);
	}
	netfile.close ();

	net->dumpNetworkGraph ("out.dot");
	system ("dot -Tps -o out.rec.ps out.dot && gv out.rec.ps");

	testNetwork (net);

	return (0);
#endif

	gen.push_back (1);
	gen.push_back (5);
	gen.push_back (4);
	gen.push_back (1);

	net = new PerceptronNetwork (gen);

	RandomInterval	ival = { -1.0, 1.0 };
	RandomFunction	rf = { (const double (*)(void *)) RandomFunctions::rand_normal, &ival };

	net->randomizeParameters (&rf, &rf);
	/*
	net->setActivationFunction (Input, &ActivationFunctions::fact_binary);
	net->setActivationFunction (Hidden, &ActivationFunctions::fact_binary);
	net->setActivationFunction (Output, &ActivationFunctions::fact_tanh);
	*/
	net->setLearningParameter (0.2);
/*
	if (argc == 2) {
		net->setMomentumTermParameter (atof (argv[1]));
	} else
		net->setMomentumTermParameter (0.2);
*/
	if (argc == 2)
		net->setWeightDecayParameter (atof (argv[1]));
//	net->setTestTolerance (0.05);
//	net->setWeightDecayParameter (0.00004);

	testNetwork (net);

	delete net;
}


static void
testNetwork (PerceptronNetwork *net)
{
	unsigned int	n,
					on;
	vector<double>	input = vector<double> (1);
	vector<double>	output;
	vector<double>	test = vector<double> (1);
#define	TRAIN_LOW	(-3.14)
#define	TRAIN_HIGH	(3.14)
//	RandomInterval	ival = { TRAIN_LOW, TRAIN_HIGH };
#define	TRAIN_SIZE	100
	vector<double>	train_input = vector<double> (TRAIN_SIZE);
	vector<double>	train_output = vector<double> (TRAIN_SIZE);
#define	TRAIN_EPOCHS	1500
#define	TRAIN_LENGTH	(TRAIN_EPOCHS * TRAIN_SIZE)

	fstream train ("training.dat", ios::out | ios::trunc);
	for (n = 0 ; n < train_input.size () ; ++n) {
		train_input[n] = n * ((TRAIN_HIGH - TRAIN_LOW) / TRAIN_SIZE) +
			TRAIN_LOW;
		/* XXX: trained function here: sin (in) */
		train_output[n] = sin (train_input[n]);
		train << train_input[n] << "\t" << train_output[n] << endl;
	}
	train.close ();

#if 1
	for (n = 0 ; n < TRAIN_LENGTH ; ++n) {
		on = n % TRAIN_SIZE;
		input[0] = train_input[on];
		test[0] = train_output[on];
		/* alternative: random on each case
		 */
//		input[0] = RandomFunctions::rand_normal (&ival);
//		test[0] = sin (input[0]);

/*		cout << "input = { ";
		for (on = 0 ; on < input.size () ; ++on)
			cout << input[on] << ", ";
		cout << "};" << endl;
*/
		net->setInput (input);
		net->propagate ();

		output = net->getOutput ();
/*		for (on = 0 ; on < output.size () ; ++on)
			cout << "out: " << on << "\t" << output[on] << endl;
*/
//		cout << "test: " << test[0] << endl;
		net->setTestOutput (test);
//		cout << n << "\t" << net->errorTerm () << "\t# errorterm" << endl;

		net->backpropagate ();
		net->postprocess ();
		net->update ();
		net->resetDiffs ();
	}
#endif

	/* dump network to file
	 */
	fstream netfile ("out.net.txt", ios::out | ios::trunc);
	net->save (netfile);
	netfile.close ();

	double error_sum = 0.0;

	for (n = 0 ; n < TRAIN_SIZE ; ++n) {
		/* input[0] = RandomFunctions::rand_normal (&ival); */
		input[0] = train_input[n];
		net->setInput (input);
		net->propagate ();
		output = net->getOutput ();

		cout << input[0] << "\t"
			<< output[0] << "\t# gnuplot" << endl;

		test[0] = train_output[on];
		net->setTestOutput (test);
		error_sum += net->errorTerm ();
	}
	error_sum /= TRAIN_SIZE;
	cout << error_sum << "\t# overall errorterm of testset" << endl;

	net->dumpNetworkGraph ("out.dot");
	system ("dot -Tps -o out.ps out.dot && gv out.ps");
}


