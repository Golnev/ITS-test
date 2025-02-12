import logging
import os

import pytest
from dotenv import load_dotenv

from src.helpers.contacts_helper import ContactsHelper
from src.requests_utilities import RequestUtilities

load_dotenv()


def pytest_configure():
    logging.getLogger('faker').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def pytest_addoption(parser):
    parser.addoption('--rm', action='store_true', default=False, help='Delete a created contact after a test')


@pytest.fixture(scope='module')
def auth_headers():
    my_email: str = os.getenv('MY_EMAIL')
    my_pass: str = os.getenv('MY_PASS')

    request_utility = RequestUtilities()

    logging.debug('Login with My Email.')
    response_json = request_utility.post(endpoint='users/login',
                                         payload={'email': my_email, 'password': my_pass})

    token = response_json['token']

    yield {'Authorization': f'Bearer {token}'}

    logging.debug('Logout.')
    request_utility.post(endpoint='users/logout',
                         headers={'Authorization': f'Bearer {token}'})


@pytest.fixture()
def cleanup_after_test(auth_headers, pytestconfig):
    contacts_helper = ContactsHelper()
    created_contacts = []

    def create_contact():
        contact_rs_api, contact_info = contacts_helper.create_contact(auth_headers=auth_headers)
        create_contact_id = contact_rs_api['_id']
        created_contacts.append(create_contact_id)
        return contact_rs_api, contact_info

    yield create_contact

    if pytestconfig.getoption('--rm'):
        for contact_id in created_contacts:
            contacts_helper.delete_contact(auth_headers=auth_headers, contact_id=contact_id)
            logging.debug(f'Delete contact: {contact_id}')
