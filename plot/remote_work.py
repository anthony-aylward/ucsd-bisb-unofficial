#!/user/bin/env python3
#===============================================================================
# plot remote work data
#===============================================================================

# Imports ======================================================================

import argparse
import pandas as pd
import seaborn as sns
import numpy as np




# Functions ====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='plot time to degree'
    )
    parser.add_argument(
        'file',
        metavar='<path/to/file.{pdf,png,svg}>',
        help='path to output file'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    sns.set(style='white')
    sns.set_context('talk')
    ax = sns.distplot(
        [1,8]+[9]*2+[12]*2+[13]*3+[14]+[15]*2+[16]*12+[17]*5+[20,21,23],
        hist_kws={'cumulative': True},
        kde_kws={'cumulative': True}
    )
    ax.set_title('Computational staff WFH date')
    ax.set(xlim=(1, 23))
    fig = ax.get_figure()
    fig.savefig(args.file, format=args.file.split('.')[1])





# Execute ======================================================================

if __name__ == '__main__':
    main()
