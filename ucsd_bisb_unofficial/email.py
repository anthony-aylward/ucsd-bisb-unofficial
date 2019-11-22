#===============================================================================
# email.py
#===============================================================================

"""Instantiation of the Mail object, along with helper functions for email
handling

Attributes
----------
mail : Mail
    A Mail object (see Flask-Mail: https://pythonhosted.org/Flask-Mail/ )
"""




# Imports ======================================================================

from flask import render_template, current_app
from flask_mail import Mail, Message
from threading import Thread

from ucsd_bisb_unofficial import create_app



# Constants ====================================================================

TAG_DICT = {
    'career': 'Career',
    'committee': 'Doctoral Committee',
    'fellowships': 'Fellowships',
    'lab': 'Lab',
    'mental_health': 'Mental Health',
    'news': 'News',
    'residency': 'Residency',
    'seminars': 'Seminars',
    'stats': 'Program Statistics',
    'ta': 'TAships',
    'tech': 'Technology',
    'townhall': 'Town Hall & SC',
    'blog': 'Test blog'
}





# Initialization ===============================================================

mail = Mail()




# Functions ====================================================================

def send_async_email(app, msg):
    """Send an email asynchronously

    An application context is pushed so that the mail operation can use its own
    thread. See the Flask documentation for more on application contexts:

    http://flask.pocoo.org/docs/1.0/appcontext/

    Parameters
    ----------
    app : Flask
        The application from which to push a context
    msg : Message
        The message to be sent
    """

    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """Send an email

    A Message object is instantiated using the provided subject, sender and
    recippients, then filled using the provided text/html data. A new app is
    created to support sending mail asynchrounously, and finally
    send_async_email is called with its own thread.

    Parameters
    ----------
    subject
        The subject of the email
    sender
        The sender of the email
    recipients
        The recipients of the email
    text_body
        The body of the email (text version)
    html_body
        The body of the email (html version)
    """

    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    app = create_app()
    Thread(target=send_async_email, args=(app, msg)).start()


# def send_password_reset_email(user):
#     """Send a password reset email

#     A JSON web token is created, then included in an email to the account for
#     which a password reset has been requested.

#     Parameters
#     ----------
#     user : User
#         User whose password is to be reset
#     """

#     token = user.get_reset_password_token()
#     send_email(
#         '[ucsd-bisb-unofficial] Reset Your Password',
#         sender=current_app.config['ADMINS'][0],
#         recipients=[user.email],
#         text_body=render_template(
#             'email/reset_password.txt',
#             user=user,
#             token=token
#         ),
#         html_body=render_template(
#             'email/reset_password.html',
#             user=user,
#             token=token
#         )
#     )


def send_confirmation_email(user):
    """Send a confirmation email

    A JSON web token is created, then included in an email to the account for
    which the email is to be confirmed

    Parameters
    ----------
    user : User
        The user whose email is to be confirmed
    """

    token = user.get_confirm_email_token()
    send_email(
        '[ucsd-bisb-unofficial] Confirm Your Email Address',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/email_confirmation.txt',
            user=user,
            token=token
        ),
        html_body=render_template(
            'email/email_confirmation.html',
            user=user,
            token=token
        )
    )


def send_whisper_email(user):
    """Send a whisper email

    A JSON web token is created, then included in an email to the account for
    which the email is to be confirmed

    Parameters
    ----------
    user : User
        The user whose email is to be confirmed for whisper
    """

    token = user.get_whisper_token()
    send_email(
        '[ucsd-bisb-unofficial] Whisper',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/whisper.txt',
            user=user,
            token=token
        ),
        html_body=render_template(
            'email/whisper.html',
            user=user,
            token=token
        )
    )


def send_new_post_email(user, tag, index_route, detail_route, post_id):
    send_email(
        f'[ucsd-bisb-unofficial] New {TAG_DICT[tag]} content',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'email/new_post.txt',
            tag=TAG_DICT[tag],
            detail_route=detail_route,
            post_id=post_id
        ),
        html_body=render_template(
            'email/new_post.html',
            tag=TAG_DICT[tag],
            index_route=index_route,
            detail_route=detail_route,
            post_id=post_id
        )
    )