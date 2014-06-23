#!/usr/bin/env python

import sys
import numpy
import gzip
import logging

def moses_format(fields, new_features):
    fields[2] = " ".join(map(str, new_features))
    return " ||| ".join(fields)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
            format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

    options = eval("dict({})".format(", ".join(sys.argv[1:])))

    paths = options['features']
    if not isinstance(paths, list):
        paths = [paths]
    iters = map(iter, map(open, paths))

    mask = options.get('mask', Ellipsis)

    dest = gzip.open(options['dest'], 'w')

    for line_num, line in enumerate(gzip.open(options['table'])):
        fields = map(str.strip, list(line.split("|||")))
        features = map(float, fields[2].strip().split(" "))
        for it in iters:
            features.append(float(next(it).strip()))
        features = numpy.array(features)
        features[-1] = numpy.exp(features[-1])
        print >>dest, moses_format(fields, features[mask])
        if line_num % 10000 == 0:
            logging.debug(line_num)


    dest.close()
