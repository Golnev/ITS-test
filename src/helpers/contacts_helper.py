import logging as logger

from faker import Faker

from src.requests_utilities import RequestUtilities


class ContactsHelper:
    def __init__(self):
        self.request_utility = RequestUtilities()
        self.FULL_CONTACT: int = 11

    def create_contact(self, auth_headers: dict):
        logger.debug("Create new contact.")
        fake = Faker()

        payload = dict()
        payload["firstName"] = fake.first_name()
        payload["lastName"] = fake.last_name()
        payload["birthdate"] = (
            fake.date_of_birth(minimum_age=6, maximum_age=110)
        ).strftime("%Y-%m-%d")
        payload["email"] = fake.email()
        payload["phone"] = fake.basic_phone_number()
        payload["street1"] = fake.street_name()
        payload["street2"] = fake.street_name()
        payload["city"] = fake.city()
        payload["stateProvince"] = fake.state()
        payload["postalCode"] = fake.postalcode()
        payload["country"] = fake.country()

        logger.debug("Fake contact created")

        create_contact_json = self.request_utility.post(
            endpoint="contacts",
            payload=payload,
            headers=auth_headers,
            expected_status_code=201,
        )

        return create_contact_json, payload

    def delete_contact(self, auth_headers: dict, contact_id: str):
        logger.debug(f"Delete contact id={contact_id}")

        rs_del_contact = self.request_utility.delete(
            endpoint=f"contacts/{contact_id}", headers=auth_headers
        )

        return rs_del_contact

    def get_contacts(
        self,
        auth_headers: dict,
        contact_id: str | None = None,
        expected_status_code: int = 200,
    ):
        if contact_id is None:
            logger.debug("Get contacts")

            rs_get_contacts = self.request_utility.get(
                endpoint="contacts",
                headers=auth_headers,
                expected_status_code=expected_status_code,
            )
            return rs_get_contacts
        else:
            logger.debug(f"Get contact by id={contact_id}")

            rs_get_contact = self.request_utility.get(
                endpoint=f"contacts/{contact_id}",
                headers=auth_headers,
                expected_status_code=expected_status_code,
            )
            return rs_get_contact

    def update(
        self,
        auth_headers: dict,
        payload: dict,
        contact_id: str,
        expected_status_code: int = 200,
    ):
        if len(payload) == self.FULL_CONTACT:
            logger.debug("Update contact with PUT.")

            rs_update_contact = self.request_utility.put(
                endpoint=f"contacts/{contact_id}",
                payload=payload,
                headers=auth_headers,
                expected_status_code=expected_status_code,
            )
            return rs_update_contact

        if len(payload) < self.FULL_CONTACT:
            logger.debug("Update contact with PATCH.")

            rs_update_contact = self.request_utility.patch(
                endpoint=f"contacts/{contact_id}",
                payload=payload,
                headers=auth_headers,
                expected_status_code=expected_status_code,
            )
            return rs_update_contact
