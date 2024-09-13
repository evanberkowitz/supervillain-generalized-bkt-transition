#!/usr/bin/env python

import h5py as h5
import supervillain
import steps

import logging
logger = logging.getLogger(__name__)

def reset(steps, row):
    for step in steps:
        logger.info(f"Resetting W={row['W']} κ={row['kappa']} N={row['N']} {row['action']}")
    
if __name__ == '__main__':
    
    parser = supervillain.cli.ArgumentParser()
    parser.add_argument('input_file', type=supervillain.cli.input_file('input'))
    parser.add_argument('row', type=int, nargs='+')
    parser.add_argument('--thermalization', default=False, action='store_true')
    parser.add_argument('--ensemble', default=False, action='store_true')
    parser.add_argument('--bootstrap', default=False, action='store_true')
    parser.add_argument('--force', default=False, action='store_true')
    args = parser.parse_args()

    rows = args.input_file.ensembles.iloc[args.row]

    if args.thermalization:
        to_reset = (steps.Bootstrap, steps.Ensemble, steps.Thermalization, )
    elif args.ensemble:
        to_reset = (steps.Bootstrap, steps.Ensemble, )
    elif args.bootstrap:
        to_reset = (steps.Bootstrap, )

    if not args.force:
        names = ' '.join((c.__name__ for c in to_reset))
        print(rows)
        print(f'\nReally reset the {names} for these rows?\n')



