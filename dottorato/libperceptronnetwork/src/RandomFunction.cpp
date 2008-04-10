/* RandomFunction.cpp
 *
 * Copyright (C) 2002-2003 -- Sebastian Nowozin
 */

#include <sys/timeb.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <math.h>
#include <time.h>

#include <neuralnet/RandomFunction.h>


void
RandomFunctions::rand_init (void)
{
    struct timeb    tb;

    ftime (&tb);
    srandom (tb.millitm + tb.time);
//  srandom (time (NULL));
}


const double
RandomFunctions::rand_normal (RandomInterval *range)
{
    double  base;

    /* lose one bit precision here, too bad :-/
     */
    base = random ();
    if (base < 0.0)
        base *= -1.0;

    base /= (double) INT_MAX;
    base *= range->high - range->low;
    base += range->low;

    return (base);
}



