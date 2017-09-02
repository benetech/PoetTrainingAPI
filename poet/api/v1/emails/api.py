# -*- coding: utf-8 -*-
"""The API module for emails."""
import boto3
from flask import current_app, jsonify, render_template
from webargs import fields
from webargs.flaskparser import use_args

from poet.api.v1.annotations.api import get_annotation_by_id
from poet.locales import Errors, Success
from poet.utils import RESTBlueprint


blueprint = RESTBlueprint('emails', __name__, version='v1')


send_email_args = {
    'to_email': fields.Email(required=True),
    'annotation_id': fields.UUID(required=True)
}


def generate_email_body(annotation):
    """Generate an email body from an annotation.

    :param annotation Annotation: the annotation from which the email body
        should be generated
    :return string: An HTML formatted string for the email body
    """
    return render_template('annotation-email.html', annotation=annotation)


def send_email(annotation, email):
    """Send an email with the annotation.

    :param annotation Annotation: the annotation from which the body of the
        email should be created.
    :param email string: the email to send to
    :return bool: whether or not the email could be sent
    """
    body = generate_email_body(annotation)
    if current_app.config['SEND_EMAILS']:
        return send_ses_email(body, email)
    else:
        return simulate_email_server()


def simulate_email_server():
    """Simulate sending an email.

    There could be many things that go wrong with sending an email. Let's
    pretend that sending an email have a 5% failure rate.
    """
    import random
    # 5% chance of failure
    if random.random() < 0.05:
        return False
    else:
        return True


def send_ses_email(body, dest_email):
    """Send an email via AWS SES.

    :param body string: the formatted HTML body of the email
    :param dest_email string: the destination email address
    :return bool: whether or not the email could be sent
    """
    try:
        ses_client = boto3.client('ses', region_name='us-east-1')
        ses_client.send_email(
            Source=current_app.config['FROM_EMAIL'],
            Destination={
                'ToAddresses': [dest_email],
            },
            Message={
                'Subject': {
                    'Data': current_app.config['EMAIL_SUBJECT']
                },
                'Body': {
                    'Html': {
                        'Data': body
                    }
                }
            }
        )
        return True
    except:
        raise


@blueprint.create()
@use_args(send_email_args)
def create_email(args):
    """Send an email with an annotation based."""
    annotation = get_annotation_by_id(args['annotation_id'])
    if send_email(annotation=annotation, email=args['to_email']):
        return jsonify(message=Success.EMAIL_SENT), 200
    else:
        return jsonify(message=Errors.UNKNOWN_ERROR), 500
