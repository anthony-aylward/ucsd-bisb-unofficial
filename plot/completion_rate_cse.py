#!/user/bin/env python3
#===============================================================================
# plot
#===============================================================================

# Imports ======================================================================

import argparse
import pandas as pd
import seaborn as sns




# Functions ====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='plot completion rates'
    )
    parser.add_argument(
        'file',
        metavar='<path/to/file.{pdf,png,svg}>',
        help='path to output file'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    sns.set(style='whitegrid')
    rates = pd.DataFrame(
        { 
            'Cohort': ('2000-02', '2003-05', '2006-08'),
            '<=6 Yrs': (41, 47, 48),
            '<=10 Yrs': (66, 75, 74),
        }
    )
    sns.set_color_codes('pastel')
    ax = sns.barplot(
        x='Cohort', y='<=10 Yrs', data=rates, label='<=10 Yrs', color='b'
    )
    sns.set_color_codes('muted')
    ax = sns.barplot(
        x='Cohort', y='<=6 Yrs', data=rates, label='<=6 Yrs', color='b'
    )
    ax.set_title('Computer Science & Engineering')
    ax.legend(ncol=2, loc='upper right', frameon=True)
    ax.set(ylabel='% Complete')
    fig = ax.get_figure()
    fig.savefig(args.file, format=args.file.split('.')[1])





# Execute ======================================================================

if __name__ == '__main__':
    main()
