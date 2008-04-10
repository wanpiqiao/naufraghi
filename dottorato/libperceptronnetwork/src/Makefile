
### compile wide definitions

# do runtime profiling (with gcov *.cpp)
#FLAGS_PROFILE=-fprofile-arcs -ftest-coverage -pg
#FLAGS_OPTIMIZE+=-fbranch-probabilities

DFLAGS=-g -ggdb
CPP=g++

CFLAGS+=-pedantic -Wall -I../ $(DFLAGS) $(FLAGS_OPTIMIZE) $(FLAGS_PROFILE)
CPPFLAGS=$(CFLAGS)

LIB_NN=-lperceptronnetwork -L.

### objects to be build
OBJS=	ActivationFunction.o RandomFunction.o \
	PerceptronNeuron.o PerceptronLayer.o PerceptronNetwork.o
LOBJS=	$(OBJS)

### targets
all:	libperceptronnetwork.a libtest libtest-classify

libperceptronnetwork.a:	$(LOBJS)
	ar rc libperceptronnetwork.a $(LOBJS)

libtest:	libtest.cpp libperceptronnetwork.a
	$(CPP) -o libtest libtest.cpp $(DFLAGS) $(CFLAGS) $(LIB_NN) -lm

libtest-classify:	libtest-classify.cpp libperceptronnetwork.a
	$(CPP) -o libtest-classify libtest-classify.cpp $(DFLAGS) $(CFLAGS) $(LIB_NN) -lm

%.o:	%.cpp
	$(CPP) -c $(CPPFLAGS) -o $@ $<

clean:	relclean
	rm -f libperceptronnetwork.a libtest libtest-classify

relclean:
	rm -f *.o
	rm -f out.* training.dat
	rm -f *.gcov *.bb *.bbg *.da gmon.out

