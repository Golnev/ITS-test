import logging as logger
import pytest

from src.helpers.contacts_helper import ContactsHelper


@pytest.mark.comtacts
@pytest.mark.check
def test_add_contact(auth_headers, pytestconfig):
    logger.info('TEST: Add new contact')

    contacts_helper = ContactsHelper()
    contact_rs_api, contact_info = contacts_helper.create_contact(auth_headers=auth_headers)

    assert contact_rs_api, 'Request is empty'
    assert contact_rs_api['lastName'] == contact_info['lastName'], \
        f'Last name from request nad from payload are different'

    rm_flag = pytestconfig.getoption('--rm')
    if rm_flag:
        contacts_helper.delete_contact(auth_headers=auth_headers, contact_id=contact_rs_api['_id'])


@pytest.mark.comtacts
@pytest.mark.negative
def test_add_contact_without_mandatory_data():
    pass


@pytest.mark.comtacts
@pytest.mark.negative
def test_contact_with_wrong_int_data():
    pass


@pytest.mark.comtacts
@pytest.mark.nehative
def test_add_contact_with_existing_last_name_and_first_name():
    pass
