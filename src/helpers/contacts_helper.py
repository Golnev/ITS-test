import logging as logger

from faker import Faker

from src.requests_utilities import RequestUtilities


class ContactsHelper:
    def __init__(self):
        self.request_utility = RequestUtilities()

    def create_contact(self, auth_headers: dict):
        logger.debug('Create new contact.')
        fake = Faker()

        payload = dict()
        payload['firstName'] = fake.first_name()
        payload['lastName'] = fake.last_name()
        payload['birthdate'] = (fake.date_of_birth(minimum_age=6, maximum_age=110)).strftime('%Y-%m-%d')
        payload['email'] = fake.email()
        payload['phone'] = fake.basic_phone_number()
        payload['street1'] = fake.street_name()
        payload['street2'] = fake.street_name()
        payload['city'] = fake.city()
        payload['stateProvince'] = fake.state()
        payload['postalCode'] = fake.postalcode()
        payload['country'] = fake.country()

        logger.debug('Fake contact created')

        create_contact_json = self.request_utility.post(endpoint='contacts',
                                                        payload=payload,
                                                        headers=auth_headers,
                                                        expected_status_code=201)

        return create_contact_json, payload

    def delete_contact(self, auth_headers: dict, contact_id: str):
        logger.debug('Delete contact.')

        rs_del_user = self.request_utility.delete(endpoint=f'contacts/{contact_id}',
                                                  headers=auth_headers)

        return rs_del_user
