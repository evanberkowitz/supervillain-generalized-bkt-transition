#!/usr/bin/env python

from collections import deque
from itertools import product, chain
import numpy as np
import pandas as pd

ensembles = deque()

################################################################################
# STORAGE
# Where should we write things to disk?
################################################################################

storage = {
    'thermalization storage': 'scan-fine-thermalize.h5',
    'ensemble storage':  'scan-fine-data.h5',
    'bootstrap storage': 'scan-fine-bootstrap.h5',
}

################################################################################
# GENERATION
################################################################################
generate = {
    'thermalize': 1000,         # How many steps to take to measure τ?
    'thermalization cut': 10,   # Multiplies τ to cut and recompute τ.
    'configurations':   1000,   # How many configurations in production?
}

################################################################################
# ANALYSIS
################################################################################
analysis = {
    'bootstraps': 100,          # How many bootstrap samples?
}

################################################################################
# ACTION
# We will use two different actions to do this calculation; some ensembles use
# the original Villain frame and some use the dual Worldline frame.
################################################################################
defaults = storage | generate | analysis

worldline = defaults | {
    'action': 'Worldline',
    'start':  'cold',
}

villain = defaults | {
    'action': 'Villain',
    'start':  'cold',
}


################################################################################
W=2
NS=(5, 11, 21)
################################################################################

for N, kappa in product(NS, np.linspace(0.17, 0.20, 13)):
    ensembles.append(worldline | {'W': W, 'kappa': kappa, 'N':  N, })

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
    parser.add_argument('--pdf', default='', type=str)

    args = parser.parse_args()

    with pd.option_context(
            'display.max_rows', None,
            'display.max_columns', None,
            'display.width', None,
            ):
        print(ensembles)

    if args.figure or args.pdf:

        import matplotlib
        import matplotlib.pyplot as plt
        from results import collect
        from transition import visualize
        figs = visualize(collect(ensembles))

        if args.pdf:
            from matplotlib.backends.backend_pdf import PdfPages
            with PdfPages(args.pdf) as pdf:
                for fig in figs:
                    fig.savefig(pdf, format='pdf')

        if args.figure:
            plt.show()

