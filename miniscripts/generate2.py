#!/usr/bin/env python

template = """#!/bin/bash
#PBS -l walltime=72:00:00
#PBS -l nodes=1:ppn=1

cd /RQusagers/vanmerb/rnnencdec

export PYTHONPATH=/RQusagers/vanmerb/rnnencdec/groundhog-private/:$PYTHONPATH

python /RQusagers/vanmerb/rnnencdec/groundhog-private/scripts/RNN_Enc_Dec_Phrase.py \"{options}\" >{log} 2>&1"""

params = [
    ("dict(rec_gating=False)", "run6"),
    ("dict(rec_reseting=False)", "run7"),
    ("dict(rec_gating=False,rec_reseting=False)", "run8")
    ]

for options, name in params:
    with open("{}.sh".format(name), "w") as script:
        log = "{}.log".format(name)
        print >>script, template.format(**locals())

