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
    parser = argparse.ArgumentParser(description='plot completion rates')
    parser.add_argument(
        'file',
        metavar='<path/to/file.{pdf,png,svg}>',
        help='path to output file'
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    sns.set(style='white')
    palette = sns.color_palette().as_hex()
    rates = pd.DataFrame(
        { 
            'Year': ('2018', '2019', '2020'),
            'Yes': (17.5, 44.4, 14.7),
            'Somewhat': (35, 88.8, 52.9),
            'No': (100, 100, 100),
        }
    )
    ax = sns.barplot(
        x='Year', y='No', data=rates, label='No', color=palette[3]
    )
    ax = sns.barplot(
        x='Year', y='Somewhat', data=rates, label='Somewhat', color=palette[1]
    )
    ax = sns.barplot(
        x='Year', y='Yes', data=rates, label='Yes', color=palette[0]
    )
    ax.set_title('Are you satisfied with the current administrative resources\nprovided by the program?')
    ax.legend(ncol=3, loc='upper center', frameon=True)
    ax.set(ylabel='', yticks=[], ylim=(0, 112))
    for p, percent in zip(ax.patches, (65.0, 11.1, 47.1, 17.5, 44.4, 38.2, 17.5, 44.4, 14.7)):
        height = p.get_height()
        ax.text(
            p.get_x()+p.get_width()/2.,
            height - 5,
            '{:1.1f}%'.format(percent),
            ha='center',
            color='w'
        )
    fig = ax.get_figure()
    fig.savefig(args.file, format=args.file.split('.')[1])





# Execute ======================================================================

if __name__ == '__main__':
    main()
