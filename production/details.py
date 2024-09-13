#!/usr/bin/env python

import pandas as pd
import supervillain
from supervillain.performance import Timer
from steps import Possible, Ensemble, Thermalization

import logging
logger = logging.getLogger(__name__)

def length(row):
    if E:=Possible(Ensemble).of(row):
        return len(E)
    return 0

def tau(step):
    def curry(row):
        if S:=Possible(step).of(row):
            return S.tau
        return float('inf')
    return curry

if __name__ == '__main__':

    parser = supervillain.cli.ArgumentParser()
    parser.add_argument('input_file', type=supervillain.cli.input_file('input'), default='input.py')
    parser.add_argument('--parallel', default=False, action='store_true')
    parser.add_argument('--W', default=None, type=int)
    parser.add_argument('--N', default=None, type=int)
    parser.add_argument('--kappa', default=None, type=float)
    parser.add_argument('--cfgs-less-than', default=float('inf'), type=float)
    parser.add_argument('--cfgs-more-than', default=-1, type=float)
    parser.add_argument('--delete', default=False, action='store_true')

    args = parser.parse_args()

    ensembles = args.input_file.ensembles
    if args.parallel:
        from parallel import io_prep
        ensembles = ensembles.apply(io_prep, axis=1)

    if args.W:
        ensembles = ensembles[ensembles['W'] == args.W]
    if args.N:
        ensembles = ensembles[ensembles['N'] == args.N]
    if args.kappa:
        ensembles = ensembles[ensembles['kappa'] == args.kappa]

    ensembles['length'] = ensembles.apply(length, axis=1)
    ensembles['tau (t)']    = ensembles.apply(tau(Thermalization), axis=1)
    ensembles['tau (e)']    = ensembles.apply(tau(Ensemble), axis=1)

    ensembles = ensembles[(ensembles['length'] < args.cfgs_less_than) & (ensembles['length'] > args.cfgs_more_than)]

    ensembles = ensembles.sort_values(by=['W', 'kappa', 'N'], ascending=True)

    with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', 1000,
            ):
        print(ensembles[['W', 'kappa', 'N', 'action', 'length', 'tau (t)', 'tau (e)']])

    if args.delete:
        from pathlib import Path
        
        for idx, row in ensembles.iterrows():
            Path(row['ensemble storage']).unlink()
            Path(row['bootstrap storage']).unlink()
