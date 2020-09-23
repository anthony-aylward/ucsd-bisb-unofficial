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

DEVELOPMENT_CONFIG_DATA = f'''
import os
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or {os.urandom(16)}
SQLALCHEMY_DATABASE_URI = (
    os.environ.get('DATABASE_URL')
    or 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
FTS_DATABASE = os.path.join(basedir, 'fts.db')
FTS_SOURCE_DATABASE = os.path.join(basedir, 'app.db')
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
POSTS_PER_PAGE = 3
UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads', 'img')
UPLOADED_DOCUMENTS_DEST = os.path.join(basedir, 'uploads', 'doc')
ROTATION_DATABASE_CSV = os.path.join(
    basedir,
    'protected',
    'bisb-cohort-rotation-database.csv'
)
ROTATION_DATABASE_JSON = {{
    'Proposal F18': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-f18.json'
    ),
    'Report F18': os.path.join(
        basedir,
        'protected',
        'rotation-report-f18.json'
    ),
    'Proposal W19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-w19.json'
    ),
    'Report W19': os.path.join(
        basedir,
        'protected',
        'rotation-report-w19.json'
    ),
    'Proposal S19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-s19.json'
    ),
    'Report S19': os.path.join(
        basedir,
        'protected',
        'rotation-report-s19.json'
    ),
    'Contact': os.path.join(
        basedir,
        'protected',
        'rotation-contact.json'
    )
}}
ROTATION_DATABASE_2019_CSV = os.path.join(
    basedir,
    'protected',
    'rotation-database-2019.csv'
)
ROTATION_DATABASE_2019_JSON = {{
    'Proposal F19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-f19.json'
    ),
    'Report F19': os.path.join(
        basedir,
        'protected',
        'rotation-report-f19.json'
    ),
    'Contact': os.path.join(
        basedir,
        'protected',
        'rotation-contact.json'
    )
}}
PROFS_CSV = {{
    'bio': os.path.join(basedir, 'protected', 'profs-bio.csv'),
    'bioe': os.path.join(basedir, 'protected', 'profs-bioe.csv'),
    'cse': os.path.join(basedir, 'protected', 'profs-cse.csv'),
}}
COMPANIES_CSV = os.path.join(basedir, 'protected', 'companies.csv')
ADMINS = []
GBIC_EMAILS = {{
    'president': 'dnachman@eng.ucsd.edu',
    'internal_affairs': 'mragsac@eng.ucsd.edu',
    'external_affairs': 'f5yuan@eng.ucsd.edu',
    'outreach': 'jhavens@eng.ucsd.edu',
    'development': 'ckmah@ucsd.edu',
    'student_wellness': 'jepekar@eng.ucsd.edu',
    'onboarding': 'ochapman@eng.ucsd.edu',
    'finance': 'cew003@ucsd.edu'
}}
APPROVED_EMAILS = []
'''

PRODUCTION_CONFIG_DATA = f"""
import os
import os.path
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY') or {os.urandom(16)}
SQLALCHEMY_DATABASE_URI = (
    os.environ.get('DATABASE_URL')
    or 'sqlite:///' + os.path.join(basedir, 'app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
FTS_DATABASE = os.path.join(basedir, 'fts.db')
FTS_SOURCE_DATABASE = os.path.join(basedir, 'app.db')
MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'mail.smtp2go.com'
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'ucsd.bisb.unofficial@ucsd-bisb.info'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
POSTS_PER_PAGE = 5
MAX_CONTENT_LENGTH = 64 * 1024 * 1024
UPLOADED_IMAGES_DEST = os.path.join(basedir, 'uploads', 'img')
UPLOADED_DOCUMENTS_DEST = os.path.join(basedir, 'uploads', 'doc')
ROTATION_DATABASE_CSV = os.path.join(
    basedir,
    'protected',
    'bisb-cohort-rotation-database.csv'
)
ROTATION_DATABASE_JSON = {{
    'Proposal F18': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-f18.json'
    ),
    'Report F18': os.path.join(
        basedir,
        'protected',
        'rotation-report-f18.json'
    ),
    'Proposal W19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-w19.json'
    ),
    'Report W19': os.path.join(
        basedir,
        'protected',
        'rotation-report-w19.json'
    ),
    'Proposal S19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-s19.json'
    ),
    'Report S19': os.path.join(
        basedir,
        'protected',
        'rotation-report-s19.json'
    ),
    'Contact': os.path.join(
        basedir,
        'protected',
        'rotation-contact.json'
    )
}}
ROTATION_DATABASE_2019_CSV = os.path.join(
    basedir,
    'protected',
    'rotation-database-2019.csv'
)
ROTATION_DATABASE_2019_JSON = {{
    'Proposal F19': os.path.join(
        basedir,
        'protected',
        'rotation-proposal-f19.json'
    ),
    'Report F19': os.path.join(
        basedir,
        'protected',
        'rotation-report-f19.json'
    ),
    'Contact': os.path.join(
        basedir,
        'protected',
        'rotation-contact.json'
    )
}}
PROFS_CSV = {{
    'bio': os.path.join(basedir, 'protected', 'profs-bio.csv'),
    'bioe': os.path.join(basedir, 'protected', 'profs-bioe.csv'),
    'cse': os.path.join(basedir, 'protected', 'profs-cse.csv'),
}}
COMPANIES_CSV = os.path.join(basedir, 'protected', 'companies.csv')
ADMINS = ['ucsd.bisb.unofficial@ucsd-bisb.info']
GBIC_EMAILS = {{
    'president': 'dnachman@eng.ucsd.edu',
    'internal_affairs': 'mragsac@eng.ucsd.edu',
    'external_affairs': 'f5yuan@eng.ucsd.edu',
    'outreach': 'jhavens@eng.ucsd.edu',
    'development': 'ckmah@ucsd.edu',
    'student_wellness': 'jepekar@eng.ucsd.edu',
    'onboarding': 'ochapman@eng.ucsd.edu',
    'finance': 'cew003@ucsd.edu'
}}
APPROVED_EMAILS = [
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
    'mragsac@eng.ucsd.edu',
    'solvason@eng.ucsd.edu',
    'earmingol@eng.ucsd.edu',
    'klchu@ucdavis.edu',
    'anp055@eng.ucsd.edu',
    'ileenamitra@eng.ucsd.edu',
    'grahman@eng.ucsd.edu',
    'joreyna@eng.ucsd.edu',
    'jnewsome@eng.ucsd.edu',
    'emkobaya@eng.ucsd.edu',
    'croy@eng.ucsd.edu',
    'aklie@eng.ucsd.edu',
    'b2jia@ucsd.edu',
    'pjaganna@eng.ucsd.edu',
    'xzwen@eng.ucsd.edu',
    'hsher@eng.ucsd.edu',
    'jepekar@eng.ucsd.edu',
    'f5yuan@eng.ucsd.edu',
    'cew003@ucsd.edu',
    'abbas22a@mtholyoke.edu',
    'fatemeh.amrollahi@emory.edu',
    'xiaomidu23@gmail.com',
    'b101102109@tmu.edu.tw',
    'pratibha.jagannatha@gmail.com',
    'aklie@ucsd.edu',
    'emikoifish@gmail.com',
    'ericrkofman@gmail.com',
    'roy.charlesalexandre@gmail.com',
    'domschenone@gmail.com',
    'jdtibochab@unal.edu.co',
    'xzwen.irene@gmail.com',
    'amabbasi@eng.ucsd.edu',
    'famrolla@eng.ucsd.edu',
    'xid032@eng.ucsd.edu',
    'b2jia@eng.ucsd.edu',
    'ekofman@eng.ucsd.edu',
    'dschenon@eng.ucsd.edu',
    'j1tiboch@eng.ucsd.edu',
    'jsnedeco@gmail.com',
    'jtsorren@eng.ucsd.edu',
    'jlz014@eng.ucsd.edu',
    'oshanta@eng.ucsd.edu',
    'andreabcastro@ucsd.edu',
    'olga.botvinnik@gmail.com',
    'jpnguyen@ucsd.edu',
    'jluebeck@eng.ucsd.edu',
    'pfiaux@ucsd.edu',
    'Nathaniel.P.DelosSantos@jacobs.ucsd.edu',
    'isshamie@eng.ucsd.edu',
    'lamaral@eng.ucsd.edu',
    'cag104@eng.ucsd.edu',
    'lfrancus@ucsd.edu',
    'amassara@ucsd.edu',
    'snwright@ucsd.edu',
    'lily.m.francus@gmail.com',
    'kpgodine@ucsd.edu',
    'mcuoco@ucsd.edu',
    'abegzati@ucsd.edu',
    'jjauregu@ucsd.edu',
    'hmummey@ucsd.edu',
    'j7lam@ucsd.edu',
    'cguccion@ucsd.edu',
    'yif064@ucsd.edu',
    'j5kim@ucsd.edu'
]
"""




# Functions ====================================================================

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


def main():
    args = parse_arguments()
    with open(os.path.join(args.instance, 'config.py'), 'w') as f:
        f.write(
            PRODUCTION_CONFIG_DATA if args.production
            else DEVELOPMENT_CONFIG_DATA
        )




# Execute ======================================================================

if __name__ == '__main__':
    main()
