#!/usr/bin/env python

import numpy
import sys

tm = numpy.load(sys.argv[1])
steps = numpy.where(tm['cost'] == 0.0)[0][0]
start = max(0, steps - 10000)
print "After {} steps perplexity is {}".format(steps, numpy.mean(tm['cost'][start:steps]))
