import json
import urllib3
import logging
import requests

class ApiError(Exception):
    pass

class IpaApi:
    def __init__(self, server, user, password):
        urllib3.disable_warnings()
        self.cookies = {}
        self.server = server
        self._connect(user, password)

    def _connect(self, user, password):
        logging.debug("IpaApi._connect()")
        # Authenticate and get the session cookie
        login_url = f'https://{self.server}/ipa/session/login_password'
        headers_login = {
            'Referer': f'https://{self.server}/ipa',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/plain'
        }
        data = {
            'user': user,
            'password': password
        }
        response = requests.post(
            login_url, headers=headers_login, data=data, verify=False)
        response.raise_for_status()

        # Extract the session cookie from the response
        self.cookies = {'ipa_session': response.cookies.get('ipa_session')}

    def post(self, method, params, options={}):
        logging.debug(
            f"IpaApi.post(method: {method}, params: {params}, options: {options})")
        # Make a JSON request using the obtained session cookie
        json_url = f'https://{self.server}/ipa/session/json'
        headers_json = {
            'Referer': f'https://{self.server}/ipa',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        merged_options = {"version": "2.251"}
        merged_options.update(options)

        json_data = {
            "id": 0,
            "method": method,
            "params": [
                params,
                merged_options
            ]
        }

        # Use the session cookie in the request
        response = requests.post(json_url, headers=headers_json,
                                 json=json_data, verify=False, cookies=self.cookies)
        response.raise_for_status()

        result = json.loads(response.text)

        if (
            'error' in result and
            result['error'] is not None and
            'code' in result['error'] and
            result['error']['code'] is not None and
            result['error']['code'] > 0
        ):
            logging.debug(result)
            raise ApiError(result['error']['message'])

        return result
