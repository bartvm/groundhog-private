#!/usr/bin/env python

template = """#!/bin/bash
#PBS -l walltime=72:00:00
#PBS -l nodes=1:ppn=1

cd /RQusagers/vanmerb/rnnencdec

export PYTHONPATH=/RQusagers/vanmerb/rnnencdec/groundhog-private/:$PYTHONPATH

python /RQusagers/vanmerb/rnnencdec/groundhog-private/scripts/RNN_Enc_Dec_Phrase.py \"{options}\" >{log} 2>&1"""

params = [
    ("dict(dim=250, dim_mlp=250)", "run1"),
    ("dict(dim=500, dim_mlp=500)", "run2"),
    ("dict(rank_n_approx=200)", "run3"),
    ("dict(rank_n_approx=500)", "run4")
    ]

for options, name in params:
    with open("{}.sh".format(name), "w") as script:
        log = "{}.log".format(name)
        print >>script, template.format(**locals())

