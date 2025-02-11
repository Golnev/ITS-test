import logging
import os

import pytest
from dotenv import load_dotenv

from src.requests_utilities import RequestUtilities

load_dotenv()


def pytest_configure():
    logging.getLogger('faker').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


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
