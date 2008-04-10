/* libtest-classify.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 *
 * howto use:
 * $ ./libtest | grep gnuplot > out.dat
 * $ gnuplot
 * gnuplot> plot "out.dat" using 1:2, "training.dat" using 1:2
 *
 * the example classifies among three functions: sin, cos and linear absolute.
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
	RandomInterval	ival = { -1.0, 1.0 };
	RandomFunction	rf =
		{ (const double (*)(void *)) RandomFunctions::rand_normal, &ival };


	RandomFunctions::rand_init ();

	gen.push_back (2);
	gen.push_back (5);
	gen.push_back (5);
	gen.push_back (3);

	net = new PerceptronNetwork (gen);
	net->randomizeParameters (&rf, &rf);
	net->setLearningParameter (0.2);
//	net->setWeightDecayParameter (0.00008);
#if 0
	if (argc == 2) {
		net->setMomentumTermParameter (atof (argv[1]));
	} else
		net->setMomentumTermParameter (0.2);
#endif

	testNetwork (net);

	delete net;
}


static void
testNetwork (PerceptronNetwork *net)
{
	unsigned int	n,
					on;
	vector<double>	input = vector<double> (2);
	vector<double>	output;
	vector<double>	test = vector<double> (3);
#define	TRAIN_LOW	(-3.14)
#define	TRAIN_HIGH	(3.14)
	RandomInterval	ival = { TRAIN_LOW, TRAIN_HIGH };
#define	TRAIN_SIZE	100
	vector<int>	train_type = vector<int> (TRAIN_SIZE);
	vector<double>	train_input = vector<double> (TRAIN_SIZE);
	vector<double>	train_output = vector<double> (TRAIN_SIZE);
#define	TRAIN_EPOCHS	300
#define	TRAIN_LENGTH	(TRAIN_EPOCHS * TRAIN_SIZE)

	fstream train ("training.dat", ios::out | ios::trunc);
	for (n = 0 ; n < train_input.size () ; ++n) {
		train_input[n] = n * ((TRAIN_HIGH - TRAIN_LOW) / TRAIN_SIZE) + TRAIN_LOW;

		switch (n % 3) {
		case (0):
			train_output[n] = sin (train_input[n]);
			train_type[n] = 0;
			break;
		case (1):
			train_output[n] = cos (train_input[n]);
			train_type[n] = 1;
			break;
		case (2):
			train_output[n] = 0.25 * fabs (train_input[n]);
			train_type[n] = 2;
			break;
		}
		train << n << "\t" <<
			train_input[n] << "\t" << train_output[n] << endl;
	}
	train.close ();

	for (n = 0 ; n < TRAIN_LENGTH ; ++n) {
		on = n % TRAIN_SIZE;
		input[0] = train_input[on];
		input[1] = train_output[on];

		switch (train_type[on]) {
		case (0):
			test[0] = 1;
			test[1] = test[2] = 0;
			break;
		case (1):
			test[0] = test[2] = 0;
			test[1] = 1;
			break;
		case (2):
			test[0] = test[1] = 0;
			test[2] = 1;
			break;
		}

		cout << "input = { ";
		for (on = 0 ; on < input.size () ; ++on)
			cout << input[on] << ", ";
		cout << "};" << endl;

		net->setInput (input);
		net->propagate ();

		output = net->getOutput ();
		for (on = 0 ; on < output.size () ; ++on)
			cout << "out: " << on << "\t" << output[on] << endl;

		net->setTestOutput (test);
		cout << n << "\t" << net->errorTerm () << "\t# errorterm" << endl;

		net->backpropagate ();
		net->postprocess ();
		net->update ();
		net->resetDiffs ();
	}

	/* dump network to file
	 */
	fstream netfile ("out.net.txt", ios::out | ios::trunc);
	net->save (netfile);
	netfile.close ();

	int	g_correct = 0,
		g_incorrect = 0,
		cur_type = 0;

	for (n = 0 ; n < TRAIN_SIZE ; ++n) {
#ifdef	ONLY_TRAINED
		input[0] = train_input[n];
		input[1] = train_output[n];
		cur_type = train_type[n];
#else
		input[0] = RandomFunctions::rand_normal (&ival);

		switch (n % 3) {
		case (0):
			input[1] = sin (train_input[n]);
			cur_type = 0;
			break;
		case (1):
			input[1] = cos (train_input[n]);
			cur_type = 1;
			break;
		case (2):
			input[1] = 0.25 * fabs (train_input[n]);
			cur_type = 2;
			break;
		}
#endif
		net->setInput (input);
		net->propagate ();
		output = net->getOutput ();

		cout << cur_type << "\t"
			<< output[0] << "\t"
			<< output[1] << "\t"
			<< output[2] << "\t# gnuplot" << endl;

		int type;
		type = -1;
		if (output[0] >= output[1] && output[0] >= output[2])
			type = 0;
		else if (output[1] >= output[0] && output[1] >= output[2])
			type = 1;
		else if (output[2] >= output[0] && output[2] >= output[1])
			type = 2;
		cout << "guessed type:\t" << type << "\tcorrect: " <<
			cur_type << endl;
		if (type == cur_type)
			g_correct++;
		else
			g_incorrect++;
	}
	cout << "correct: " << g_correct << endl;
	cout << "incorrect: " << g_incorrect << endl;

	net->dumpNetworkGraph ("out.dot");
	system ("dot -Tps -o out.ps out.dot && gv out.ps");
}


