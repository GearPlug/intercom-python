import json
from urllib.parse import urlencode

import requests

from intercom.exceptions import UnauthorizedError, WrongFormatInputError, ContactsLimitExceededError


class Client(object):
    URL = "https://api.rd.services/"
    AUTH_ENDPOINT = "https://app.intercom.com/oauth?"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, client_id=None, client_secret=None, access_token=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        if access_token is not None:
            self.headers.update(Authorization=f"Bearer {access_token}")

    def authorization_url(self, redirect_uri, state=None):
        params = {"response_type": "code", "client_id": self.CLIENT_ID, "redirect_uri": redirect_uri}
        if state:
            params["state"] = state
        return self.URL + self.AUTH_ENDPOINT + urlencode(params)

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

    def filter_contacts(self, field, operator, value):
        """
        field options: https://developers.intercom.com/intercom-api-reference/reference/searchcontacts  
        operator options: =, !=, IN, NIN, <, >, ~, !~, ^, $
        """
        body = {"field": field, "operator": operator, "value": value}
        return self.post("auth/eagle/token", data=json.dumps(body))

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
