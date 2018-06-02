#!/user/bin/env python3
#===============================================================================
# configure_secret_key.py
#===============================================================================

"""Configure the secret key for a flask instance"""




# Imports ======================================================================

import argparse
import os
import os.path




# Functions ====================================================================

def main(args):
    with open(os.path.join(args.instance, 'config.py'), 'w') as f:
        f.write('SECRET_KEY = {}\n'.format(os.urandom(16)))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='configure the secret key for a flask instance'
    )
    parser.add_argument(
        'instance',
        metavar='/path/to/instance-folder/',
        help='Path to instance folder'
    )
    return parser.parse_args()




# Execute ======================================================================

if __name__ == '__main__':
    args = parse_arguments()
    main(args)

