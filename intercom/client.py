import json
from urllib.parse import urlencode

import requests

from intercom.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.intercom.io/"
    AUTH_URL = "https://app.intercom.com/oauth?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, client_id=None, client_secret=None, access_token=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        if access_token is not None:
            self.headers.update(Authorization=f"Bearer {access_token}")

    def authorization_url(self, redirect_uri=None, state=None):
        params = {"response_type": "code", "client_id": self.CLIENT_ID}
        if state:
            params["state"] = state
        if redirect_uri:
            params["redirect_uri"] = redirect_uri

        return self.AUTH_URL + urlencode(params)

    def get_access_token(self, code):
        body = {"client_id": self.CLIENT_ID, "client_secret": self.CLIENT_SECRET, "code": code}
        return self.post("auth/eagle/token", data=json.dumps(body))

    def set_token(self, access_token):
        self.headers.update(Authorization=f"Bearer {access_token}")

    def get_current_user(self):
        return self.get("me")

    def list_all_admins(self):
        return self.get("admins")

    def list_all_contacts(self):
        return self.get("contacts")

    def list_data_attributes(self, model, include_archived: bool = False):
        """
        model options are: contact, company, conversation
        """
        params = {"model": model, "include_archived": include_archived}
        return self.get("data_attributes", params=params)

    def list_tags(self):
        return self.get("tags")

    def filter_contacts(self, field, operator, value):
        """
        field options: https://developers.intercom.com/intercom-api-reference/reference/searchcontacts
        operator options: =, !=, IN, NIN, <, >, ~, !~, ^, $
        """
        body = {"query": {"field": field, "operator": operator, "value": value}}
        return self.post("contacts/search", data=json.dumps(body))

    def create_contact(
        self,
        role: str,
        email: str,
        external_id: str = None,
        phone: str = None,
        name: str = None,
        avatar: str = None,
        signed_up_at: int = None,
        last_seen_at: int = None,
        owner_id: int = None,
        unsubscribed: bool = None,
        custom_attributes: dict = None,
    ):
        """
        role options are: 'user' and 'lead'
        signed_up_at and last_seen_at use epoch time stamp. For example: 1685986703 equals Monday, 5 June 2023 17:38:23
        custom_attributes dict structure:
            {"field_name": "field_value", "field_name": "field_value", ...}
        """
        args = locals()
        body = self.set_form_data(args)
        return self.post("contacts", data=json.dumps(body))

    def add_tag_to_contact(self, contact_id, tag_id):
        body = {"id": tag_id}
        return self.post(f"contacts/{contact_id}/tags", data=json.dumps(body))

    def create_note(self, contact_id, text):
        body = {"body": text}
        return self.post(f"contacts/{contact_id}/notes", data=json.dumps(body))

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def put(self, endpoint, **kwargs):
        response = self.request("PUT", endpoint, **kwargs)
        return self.parse(response)

    def patch(self, endpoint, **kwargs):
        response = self.request("PATCH", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, **kwargs):
        return requests.request(method, self.URL + endpoint, headers=self.headers, **kwargs)

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 406:
            raise ContactsLimitExceededError(r)
        if status_code == 500:
            raise Exception
        return r

    def set_form_data(self, args):
        data = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                data.update({f"{arg}": args[arg]})
        return data
