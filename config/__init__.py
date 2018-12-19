#!/user/bin/env python3
#===============================================================================
# config
#===============================================================================

"""Create a config file"""




# Imports ======================================================================

import argparse
import os
import os.path




# Constants ====================================================================

DEVELOPMENT_CONFIG_DATA = '''
import os
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or {}
SQLALCHEMY_DATABASE_URI = (
    os.environ.get('DATABASE_URL')
    or 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
POSTS_PER_PAGE = 3
ADMINS = []
APPROVED_EMAILS = []
'''.format(os.urandom(16))

PRODUCTION_CONFIG_DATA = '''
import os
import os.path

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY') or {}
SQLALCHEMY_DATABASE_URI = (
    os.environ.get('DATABASE_URL')
    or 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'ucsd.bisb.unofficial'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
POSTS_PER_PAGE = 5
ADMINS = ['ucsd.bisb.unofficial@gmail.com']
APPROVED_EMAILS = [
    'ucsd.bisb.unofficial@gmail.com',
    'aaylward@eng.ucsd.edu',
    'amraman@ucsd.edu',
    'bkellman@eng.ucsd.edu',
    'bbehsaz@eng.ucsd.edu',
    'billgreenwald@eng.ucsd.edu',
    'dnachman@eng.ucsd.edu',
    'jenhantao@gmail.com',
    'jensluebeck@gmail.com',
    'jeyuan@eng.ucsd.edu',
    'jil340@eng.ucsd.edu',
    'jmccorri@eng.ucsd.edu',
    'jsauls@eng.ucsd.edu',
    'justin.k.huang@gmail.com',
    'kasthana@eng.ucsd.edu',
    'mdow@eng.ucsd.edu',
    'mkrdonovan@gmail.com',
    'najami@eng.ucsd.edu',
    'niemamoshiri@gmail.com',
    'ochapman@eng.ucsd.edu',
    'ramarty@eng.ucsd.edu',
    'sjroth@eng.ucsd.edu',
    'r3fang@eng.ucsd.edu',
    'yuq003@eng.ucsd.edu',
    'smollah@eng.ucsd.edu',
    'akhandek@eng.ucsd.edu',
    'cmartino@eng.ucsd.edu',
    'jhavens@eng.ucsd.edu',
    'ckmah@ucsd.edu',
    'craylward@gmail.com',
    'mragsac@eng.ucsd.edu',
    'solvason@eng.ucsd.edu'
]
'''.format(os.urandom(16))




# Functions ====================================================================

def main(args):
    with open(os.path.join(args.instance, 'config.py'), 'w') as f:
        f.write(
            PRODUCTION_CONFIG_DATA
            if args.production
            else DEVELOPMENT_CONFIG_DATA
        )


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='write configuration file'
    )
    parser.add_argument(
        'instance',
        metavar='<path/to/instance-folder/>',
        help='path to instance folder'
    )
    parser.add_argument(
        '--production',
        action='store_true',
        help='write a production config file'
    )
    return parser.parse_args()




# Execute ======================================================================

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
