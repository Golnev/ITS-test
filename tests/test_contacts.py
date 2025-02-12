import logging as logger
import pytest
from faker.proxy import Faker

from src.helpers.contacts_helper import ContactsHelper
from src.requests_utilities import RequestUtilities


@pytest.mark.contacts
def test_add_contact(auth_headers, manage_contacts):
    logger.info('TEST: Add new contact')

    contact_rs_api, contact_info = manage_contacts()

    assert contact_rs_api, 'Request is empty'
    assert contact_rs_api['lastName'] == contact_info['lastName'], \
        f'Last name from request nad from payload are different'


@pytest.mark.contacts
@pytest.mark.negative
def test_add_contact_without_mandatory_data(faker: Faker, auth_headers):
    logger.info('TEST: Add new contact without mandatory data.')

    payload = dict()
    payload['firstName'] = ''
    payload['lastName'] = ''
    payload['birthdate'] = (faker.date_of_birth(minimum_age=6, maximum_age=110)).strftime('%Y-%m-%d')
    payload['email'] = faker.email()
    payload['phone'] = faker.basic_phone_number()
    payload['street1'] = faker.street_name()
    payload['street2'] = faker.street_name()
    payload['city'] = faker.city()
    payload['stateProvince'] = faker.state()
    payload['postalCode'] = faker.postalcode()
    payload['country'] = faker.country()

    request_utility = RequestUtilities()

    create_contact_json = request_utility.post(endpoint='contacts',
                                               payload=payload,
                                               headers=auth_headers,
                                               expected_status_code=400)

    assert create_contact_json['_message'] == 'Contact validation failed', \
        'Validation without mandatory data was successful.'


@pytest.mark.contacts
@pytest.mark.negative
def test_contact_with_wrong_phone_number(faker: Faker, auth_headers):
    logger.info('TEST: Add new contact with wrong phone number.')

    payload = dict()
    payload['firstName'] = faker.first_name()
    payload['lastName'] = faker.last_name()
    payload['birthdate'] = (faker.date_of_birth(minimum_age=6, maximum_age=110)).strftime('%Y-%m-%d')
    payload['email'] = faker.email()
    payload['phone'] = 'No phone'
    payload['street1'] = faker.street_name()
    payload['street2'] = faker.street_name()
    payload['city'] = faker.city()
    payload['stateProvince'] = faker.state()
    payload['postalCode'] = faker.postalcode()
    payload['country'] = faker.country()

    request_utility = RequestUtilities()

    create_contact_json = request_utility.post(endpoint='contacts',
                                               payload=payload,
                                               headers=auth_headers,
                                               expected_status_code=400)

    assert create_contact_json['message'] == 'Contact validation failed: phone: Phone number is invalid', \
        'Validation with string phone was successful.'


@pytest.mark.contacts
@pytest.mark.negative
@pytest.mark.xfail
def test_add_contact_with_existing_last_name_and_first_name(faker: Faker, auth_headers, manage_contacts):
    logger.info('TEST: Add contact with existing last name amd first name')

    contact_rs_api, _ = manage_contacts()

    payload = dict()
    payload['firstName'] = contact_rs_api['firstName']
    payload['lastName'] = contact_rs_api['lastName']
    payload['birthdate'] = (faker.date_of_birth(minimum_age=6, maximum_age=110)).strftime('%Y-%m-%d')
    payload['email'] = faker.email()
    payload['phone'] = faker.basic_phone_number()
    payload['street1'] = faker.street_name()
    payload['street2'] = faker.street_name()
    payload['city'] = faker.city()
    payload['stateProvince'] = faker.state()
    payload['postalCode'] = faker.postalcode()
    payload['country'] = faker.country()

    request_utility = RequestUtilities()

    try:
        request_utility.post(endpoint='contacts',
                             payload=payload,
                             headers=auth_headers,
                             expected_status_code=400)
    except AssertionError as e:
        logger.error(f'Response status code not equal 400: {e}')
        create_contact_json = request_utility.response_api.json()
        contacts_helper = ContactsHelper()
        contacts_helper.delete_contact(auth_headers=auth_headers, contact_id=create_contact_json['_id'])


@pytest.mark.contacts
def test_get_contacts_list(auth_headers):
    logger.info('TEST: Get all contacts')

    contacts_helper = ContactsHelper()

    contacts = contacts_helper.get_contacts(auth_headers=auth_headers)

    assert contacts, 'Contacts list is empty'


@pytest.mark.contacts
def test_get_contact(auth_headers, manage_contacts):
    logger.info('TEST: Get contact')

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api['_id']

    contacts_helper = ContactsHelper()
    contact = contacts_helper.get_contacts(auth_headers=auth_headers, contact_id=contact_id)

    assert contact_rs_api['lastName'] == contact['lastName']


@pytest.mark.contacts
@pytest.mark.negative
@pytest.mark.check
def test_get_not_existing_contact(auth_headers, manage_contacts):
    logger.info('TEST: Get nonexistent contact')

    contact_rs_api, _ = manage_contacts()
    contact_id = contact_rs_api['_id']

    contacts_helper = ContactsHelper()
    contacts_helper.delete_contact(auth_headers=auth_headers, contact_id=contact_id)

    deleted_contact = contacts_helper.get_contacts(auth_headers=auth_headers,
                                                   contact_id=contact_id,
                                                   expected_status_code=404)

    assert deleted_contact.status_code == 404, 'Unexpected status code.'


@pytest.mark.contacts
def test_update_contact(auth_headers, manage_contacts):
    pass


@pytest.mark.contacts
@pytest.mark.negative
def test_update_not_existing_contact(auth_headers, manage_contacts):
    pass


@pytest.mark.contacts
@pytest.mark.negative
def test_update_contact_with_wrong_data(auth_headers, manage_contacts):
    pass


@pytest.mark.contacts
def test_update_last_name_contact(auth_headers, manage_contacts):
    pass


@pytest.mark.contacts
def test_update_email_contact(auth_headers, manage_contacts):
    pass


@pytest.mark.contacts
@pytest.mark.negative
def test_update_last_name_contact_with_wrong_data(auth_headers, manage_contacts):
    pass
