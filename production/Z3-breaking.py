#!/usr/bin/env python

from collections import deque
from itertools import product, chain
import pandas as pd

ensembles = deque()

################################################################################
# STORAGE
# Where should we write things to disk?
################################################################################

storage = {
    'thermalization storage': 'Z3-breaking/thermalize.h5',
    'ensemble storage':  'Z3-breaking/ensemble.h5',
    'bootstrap storage': 'Z3-breaking/bootstrap.h5',
}

################################################################################
# GENERATION
################################################################################
generate = {
    'thermalization cut': 10,   # Multiplies τ to cut and recompute τ.
    'configurations':   10000,   # How many configurations in production?
}

################################################################################
# ANALYSIS
################################################################################
analysis = {
    'bootstraps': 100,          # How many bootstrap samples?
}

################################################################################
# ACTION
# To see the Z_3 breaking it is simplest to exclusively use the Worldline frame.
# We'll construct histograms of exp(2πi v/W), which requires acces to v.
################################################################################
defaults = storage | generate | analysis

worldline = defaults | {
    'action': 'Worldline',
    'start':  'cold',
}

################################################################################
W=3
N=7
################################################################################

# Production most of these ensembles is relatively quick; lower kappa is slower.
# The reason is physical: lower kappa has larger autocorrelation times because it rejects more in the worldline frame.
# We therefore increase the number of thermalization steps as kappa goes down.
# The worst was thermalizing kappa=0.08, took about an hour and a half on my machine.
#                                                                                       # Autocorrelation times
#                                                                                       # during thermalization
ensembles.append(worldline | {'W': W, 'kappa': 0.08, 'N':  N, 'thermalize': 1000000, 
                              'configurations': 1000                               })   # τ =  313
ensembles.append(worldline | {'W': W, 'kappa': 0.09, 'N':  N, 'thermalize': 100000})    # τ =  109
ensembles.append(worldline | {'W': W, 'kappa': 0.12, 'N':  N, 'thermalize': 10000})     # τ =   16
ensembles.append(worldline | {'W': W, 'kappa': 0.15, 'N':  N, 'thermalize': 1000})      # τ =    4
ensembles.append(worldline | {'W': W, 'kappa': 0.18, 'N':  N, 'thermalize': 1000})      # τ =    4
#                                                                                       # (EXAMPLES, your run may differ in details)


################################################################################
# MAKE A DATAFRAME
################################################################################
ensembles = pd.DataFrame(ensembles)

################################################################################
# AND ADD ANY OBVIOUS PROCESSING
################################################################################
ensembles['path'] = ensembles.apply(lambda row:
    f"W={row['W']}/kappa={row['kappa']:0.5f}/N={row['N']}/{row['action']}",
    axis=1, raw=False
    )

################################################################################
# HUMAN INTERFACE
################################################################################
if __name__ == '__main__':
    import supervillain
    parser = supervillain.cli.ArgumentParser()
    parser.add_argument('--figure', default=False, action='store_true')
    parser.add_argument('--parallel', default=False, action='store_true')
    parser.add_argument('--pdf', default='', type=str)

    args = parser.parse_args()

    if args.parallel:
        import parallel
        ensembles = ensembles.apply(parallel.io_prep, axis=1)

    with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', None,
            ):
        print(ensembles)

    if args.figure or args.pdf:

        import results
        import breaking

        figs = breaking.visualize(results.collect(ensembles))

        if args.pdf:
            results.pdf(args.pdf, figs)
        if args.figure:
            import matplotlib.pyplot as plt
            plt.show()
 
