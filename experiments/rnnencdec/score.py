#!/usr/bin/env python

import argparse
import cPickle
import traceback
import logging
import time
import math

import numpy

from experiments.rnnencdec import\
        RNNEncoderDecoder,\
        prototype_state,\
        parse_input,\
        get_batch_iterator

logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", help="State to use")
    parser.add_argument("--src", help="Source phrases")
    parser.add_argument("--trg", help="Target phrases")
    parser.add_argument("--scores", default="scores.txt", help="Save scores to")
    parser.add_argument("model_path", help="Path to the model")
    parser.add_argument("changes",  nargs="?", help="Changes to state", default="")
    return parser.parse_args()

def main():
    args = parse_args()

    state = prototype_state()
    if hasattr(args, 'state'):
        with open(args.state) as src:
            state.update(cPickle.load(src))
    state.update(eval("dict({})".format(args.changes)))

    logging.basicConfig(level=getattr(logging, state['level']), format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

    rng = numpy.random.RandomState(state['seed'])
    enc_dec = RNNEncoderDecoder(state, rng)
    enc_dec.build()
    lm_model = enc_dec.create_lm_model()
    lm_model.load(args.model_path)

    if args.src and args.trg:
        state['source'] = [args.src]
        state['target'] = [args.trg]
        state['shuffle'] = False

        data_iter = get_batch_iterator(state, rng)
        score_file = open(state["score_file"], "w")

        scorer = enc_dec.create_scorer(batch=True)

        count = 0
        n_samples = 0
        logger.info('Scoring phrases')
        for batch in data_iter:
            if batch == None:
                continue
            st = time.time()
            [scores] = scorer(batch['x'], batch['y'],
                    batch['x_mask'], batch['y_mask'])
            up_time = time.time() - st
            for s in scores:
                print >>score_file, "{:.5f}".format(float(s))

            n_samples += batch['x'].shape[1]
            count += 1

            if count % 1000 == 0:
                score_file.flush()
                logger.debug("Scores flushed")
            logger.debug("{} batches, {} samples, {} per sample; example scores: {}".format(
                count, n_samples, up_time/scores.shape[0], scores[:5]))

        logger.info("Done")
        score_file.flush()
        score_file.close()
    else:
        scorer = enc_dec.create_scorer()
        indx_word_src = cPickle.load(open(state['word_indx'],'rb'))
        indx_word_trgt = cPickle.load(open(state['word_indx_trgt'], 'rb'))
        while True:
            try:
                compute_probs = enc_dec.create_probs_computer()
                src_line = raw_input('Source sequence: ')
                trgt_line = raw_input('Target sequence: ')
                src_seq = parse_input(state, indx_word_src, src_line, raise_unk=True)
                trgt_seq = parse_input(state, indx_word_trgt, trgt_line, raise_unk=True)
                print "Binarized source: ", src_seq
                print "Binarized target: ", trgt_seq
                probs = compute_probs(src_seq, trgt_seq)
                print "Probs: {}, cost: {}".format(probs, -numpy.sum(numpy.log(probs)))
            except Exception:
                traceback.print_exc()


if __name__ == "__main__":
    main()