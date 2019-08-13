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
    sns.set(style='whitegrid')
    sns.set_context('paper')
    ax = sns.barplot(
        x='Award year',
        y='Time to degree (years)',
        data=pd.DataFrame(
            { 
                'Award year': (
                    '2008-09', '2009-10', '2010-11', '2011-12', '2012-13',
                    '2013-14', '2014-15', '2015-16', '2016-17', '2017-18'
                ),
                'Time to degree (years)': (
                    5.8, 5.6, 6.3, 6.1, 6.0, 6.3, 5.6, 6.0, 6.1, 5.9
                )
            }
        ),
        palette='rocket_r'
    )
    ax.set_title('Computer Science & Engineering')
    ax.set(ylim=(4.5, 7))
    fig = ax.get_figure()
    fig.savefig(args.file, format=args.file.split('.')[1])





# Execute ======================================================================

if __name__ == '__main__':
    main()
