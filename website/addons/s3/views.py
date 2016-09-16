import httplib

from boto import exception
from flask import request
from modularodm import Q
from modularodm.storage.base import KeyExistsException

from framework.exceptions import HTTPError
from framework.auth.decorators import must_be_logged_in

from website.addons.base import generic_views
from website.addons.s3 import utils
from website.addons.s3.serializer import S3Serializer
from website.oauth.models import ExternalAccount
from website.project.decorators import (
    must_have_addon, must_have_permission,
    must_be_addon_authorizer,
)

SHORT_NAME = 's3'
FULL_NAME = 'Amazon S3'

s3_account_list = generic_views.account_list(
    SHORT_NAME,
    S3Serializer
)

s3_import_auth = generic_views.import_auth(
    SHORT_NAME,
    S3Serializer
)

s3_deauthorize_node = generic_views.deauthorize_node(
    SHORT_NAME
)

s3_get_config = generic_views.get_config(
    SHORT_NAME,
    S3Serializer
)

def _set_folder(node_addon, folder, auth):
    folder_id = folder['id']
    node_addon.set_folder(folder_id, auth=auth)
    node_addon.save()

s3_set_config = generic_views.set_config(
    SHORT_NAME,
    FULL_NAME,
    S3Serializer,
    _set_folder
)

@must_have_addon(SHORT_NAME, 'node')
@must_be_addon_authorizer(SHORT_NAME)
def s3_folder_list(node_addon, **kwargs):
    """ Returns all the subsequent folders under the folder id passed.
    """
    return node_addon.get_folders()

s3_root_folder = generic_views.root_folder(
    SHORT_NAME
)

@must_be_logged_in
def s3_add_user_account(auth, **kwargs):
    """Verifies new external account credentials and adds to user's list"""
    try:
        access_key = request.json['access_key']
        secret_key = request.json['secret_key']
    except KeyError:
        raise HTTPError(httplib.BAD_REQUEST)

    if not (access_key and secret_key):
        return {
            'message': 'All the fields above are required.'
        }, httplib.BAD_REQUEST

    user_info = utils.get_user_info(access_key, secret_key)
    if not user_info:
        return {
            'message': ('Unable to access account.\n'
                'Check to make sure that the above credentials are valid, '
                'and that they have permission to list buckets.')
        }, httplib.BAD_REQUEST

    if not utils.can_list(access_key, secret_key):
        return {
            'message': ('Unable to list buckets.\n'
                'Listing buckets is required permission that can be changed via IAM')
        }, httplib.BAD_REQUEST

    account = None
    try:
        account = ExternalAccount(
            provider=SHORT_NAME,
            provider_name=FULL_NAME,
            oauth_key=access_key,
            oauth_secret=secret_key,
            provider_id=user_info.id,
            display_name=user_info.display_name,
        )
        account.save()
    except KeyExistsException:
        # ... or get the old one
        account = ExternalAccount.find_one(
            Q('oauth_key', 'eq', access_key) &
            Q('oauth_secret', 'eq', secret_key)
        )
    assert account is not None

    if account not in auth.user.external_accounts:
        auth.user.external_accounts.append(account)

    # Ensure S3 is enabled.
    auth.user.get_or_add_addon('s3', auth=auth)
    auth.user.save()

    return {}


@must_be_addon_authorizer(SHORT_NAME)
@must_have_addon('s3', 'node')
@must_have_permission('write')
def create_bucket(auth, node_addon, **kwargs):
    bucket_name = request.json.get('bucket_name', '')
    bucket_location = request.json.get('bucket_location', '')

    if not utils.validate_bucket_name(bucket_name):
        return {
            'message': 'That bucket name is not valid.',
            'title': 'Invalid bucket name',
        }, httplib.BAD_REQUEST

    # Get location and verify it is valid
    if not utils.validate_bucket_location(bucket_location):
        return {
            'message': 'That bucket location is not valid.',
            'title': 'Invalid bucket location',
        }, httplib.BAD_REQUEST

    try:
        utils.create_bucket(node_addon, bucket_name, bucket_location)
    except exception.S3ResponseError as e:
        return {
            'message': e.message,
            'title': 'Problem connecting to S3',
        }, httplib.BAD_REQUEST
    except exception.S3CreateError as e:
        return {
            'message': e.message,
            'title': "Problem creating bucket '{0}'".format(bucket_name),
        }, httplib.BAD_REQUEST
    except exception.BotoClientError as e:  # Base class catchall
        return {
            'message': e.message,
            'title': 'Error connecting to S3',
        }, httplib.BAD_REQUEST

    return {}
