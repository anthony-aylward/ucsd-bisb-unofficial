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
        x='Cohort',
        y='Median Time to degree (years)',
        data=pd.DataFrame(
            { 
                'Cohort': ('2000-02', '2001-03', '2003-05', '2004-06', '2006-08', '2007-09'),
                'Median Time to degree (years)': (6.0, 6.0, 5.75, 6.0, 5.75, 5.38)
            }
        ),
        palette='rocket_r'
    )
    ax.set_title('Bioinformatics & Systems Biology')
    ax.set(ylim=(4.5, 7))
    fig = ax.get_figure()
    fig.savefig(args.file, format=args.file.split('.')[1])





# Execute ======================================================================

if __name__ == '__main__':
    main()
