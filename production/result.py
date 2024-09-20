#!/usr/bin/env python

import supervillain

import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = "Computer Modern Roman"
import matplotlib.pyplot as plt

import numpy as np

import gvar as gv
import gvarplot as gvp

import sys
import importlib.util

import logging
logger = logging.getLogger(__name__)

def load_input(module_name, file_name):
    spec = importlib.util.spec_from_file_location(module_name, file_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def estimate(bracket):
    mean = bracket[1]
    diff = np.array([bracket[0], bracket[-1]]) - mean
    err  = np.sqrt((diff**2).mean())
    return gv.gvar(mean, err)

if __name__ == '__main__':

    parser = supervillain.cli.ArgumentParser()
    parser.add_argument('--pdf', default='', type=str)

    args = parser.parse_args()

    one = load_input('one', 'scaling/W=1.py')
    logger.info(f'W=1 bracket {one.brackets_critical}')
    two = load_input('two', 'scaling/W=2.py')
    logger.info(f'W=2 bracket {two.brackets_critical}')
    three = load_input('three', 'scaling/W=3.py')
    logger.info(f'W=3 bracket {three.brackets_critical}')

    W = np.array([1, 2, 3])
    results = np.array([estimate(ensemble.brackets_critical) for ensemble in (one, two, three)])
    logger.info(f'Results {results}')

    fig, ax = plt.subplots(1,1, figsize=(10, 6))
    orange = '#F96928'
    green  = '#4C8945'
    blue   = '#34A5DA'

    # W^-2 scaling of κ critical
    x = np.linspace(1/16, 1.1, 100)
    gvp.errorband(ax, x, results[0]*x, color='black', sigma=(1,))

    # W=1 benchmark
    gvp.errorbar(ax, 1/(W**2)[[0]], results[[0]], linestyle='none', marker='o', color='black', markerfacecolor='none')
    # W=2, 3 data
    gvp.errorbar(ax, 1/(W**2)[1:], results[1:], linestyle='none', marker='o', color=orange, markerfacecolor='none', elinewidth=5)

    # CFT / ZW breaking phase
    (hi, lo) = (0.06, 1.1)
    ax.vlines((1/1**2, 1/1**2), (0.74,lo), (hi,0.74), color=(blue, green), zorder=-1, linewidth=5)
    ax.vlines((1/2**2, 1/2**2), (0.185,lo), (hi,0.185), color=(blue, green), zorder=-1, linewidth=5)
    ax.vlines((1/3**2, 1/3**2), (0.08,lo), (hi,0.08), color=(blue, green), zorder=-1, linewidth=5)

    # pretty
    ax.set_xlim((1/16, 1.1))
    ax.set_ylim((hi, lo))
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xticks((1/1**2, 1/2**2, 1/3**2), labels=[f'1/{each_n}'+r'${}^2$' for each_n in (1,2,3)], minor=False)
    ax.minorticks_off()
    ax.set_xlabel(r'$1/W^2$', fontsize=18)
    ax.set_ylabel(r'$\kappa_{*}$', fontsize=18)

    fig.tight_layout()

    if args.pdf:
        fig.savefig(args.pdf)
    else:
        plt.show()

