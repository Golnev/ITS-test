import logging as logger
from faker import Faker

from src.requests_utilities import RequestUtilities


class UsersHelper:
    def __init__(self):
        self.request_utility = RequestUtilities()

    def create_user(self, auth_headers: dict):
        logger.debug("Create new user.")
        fake = Faker()
        payload = dict()
        payload["firstName"] = fake.first_name()
        payload["lastName"] = fake.last_name()
        payload["email"] = fake.email()
        payload["password"] = fake.password(length=8, special_chars=False)

        logger.debug(
            f"Fake user first name: {payload['firstName']}, "
            f"fake user last name: {payload['lastName']}, "
            f"fake user email: {payload['email']}"
        )

        create_user_json = self.request_utility.post(
            endpoint="users",
            payload=payload,
            headers=auth_headers,
            expected_status_code=201,
        )

        return create_user_json, payload

    def delete_user(self, auth_headers: dict):
        logger.debug("Delete user.")

        rs_del_user = self.request_utility.delete(
            endpoint="users/me", headers=auth_headers
        )

        return rs_del_user

    def get_user(self, auth_headers: dict):
        logger.debug("Get user.")

        rs_user_info = self.request_utility.get(
            endpoint="users/me", headers=auth_headers
        )

        return rs_user_info

    def update_user(self, auth_headers: dict):
        logger.debug("Update user.")

        fake = Faker()
        payload = dict()
        payload["firstName"] = fake.first_name()
        payload["lastName"] = fake.last_name()
        payload["email"] = fake.email()
        payload["password"] = fake.password(length=8, special_chars=False)

        logger.debug(
            f"Fake user update first name: {payload['firstName']}, "
            f"fake user update last name: {payload['lastName']}, "
            f"fake user update email: {payload['email']}"
        )

        create_user_json = self.request_utility.patch(
            endpoint="users/me", payload=payload, headers=auth_headers
        )

        return create_user_json, payload
