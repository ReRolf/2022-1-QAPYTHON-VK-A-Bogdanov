import os
import requests
import json
from exceptions import *


class ApiClient:

    def __init__(self, user, password):
        self.base_url = 'https://target.my.com/'
        self.user = user
        self.password = password

        self.session = requests.Session()

        self.csrf_token = None
        self.post_login()
        self.get_token()
        self.abs_path = os.path.abspath(os.path.join(__file__, os.path.pardir))
        self.headers_with_csrf = {
            'X-CSRFToken': self.csrf_token
        }

    def _request(self, method, url, headers=None, data=None, files=None, expected_status=200, jsonify=False, json=None,
                 params=None):
        response = self.session.request(method=method, url=url, headers=headers, data=data, files=files, json=json,
                                        params=params)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"')

        if jsonify:
            json_response = response.json()
            if json_response.get('bStateError', False):
                error = json_response['sErrorMsg'] or 'Unknown'
                raise RespondErrorException(f'Request {url} returned error {error}!')
            return json_response

        return response

    def get_token(self):
        cookies = self._request('GET', 'https://target.my.com/csrf/').headers['set-cookie'].split(";")
        self.csrf_token = [c for c in cookies if 'csrftoken' in c]
        if not cookies:
            raise CannotGetCSRFToken("CSRF not found")
        self.csrf_token = self.csrf_token[0].split('=')[-1]

    def post_login(self):
        headers = {
            'Referer': 'https://target.my.com/'
        }

        data = {
            'email': self.user,
            'password': self.password,
            'continue': 'https://target.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }
        self._request('POST', 'https://auth-ac.my.com/auth?lang=en&nosavelogin=0', headers=headers, data=data)
        self.get_token()

    def post_segment_create(self):
        data = {
            "name": "segment api1",
            "pass_condition": 1,
            "relations": [{
                "object_type": "remarketing_player",
                "params": {"type": "positive", "left": 365, "right": 0}
            }],
            "logicType": "or"
        }
        json_data = json.dumps(data)
        response = self._request('POST', 'https://target.my.com/api/v2/remarketing/segments.json',
                                 headers=self.headers_with_csrf,
                                 data=json_data)
        return response.json()['id']

    def segment_checker(self, segment_id):
        response = self._request('GET', 'https://target.my.com/api/v2/remarketing/segments.json')
        if not segment_id in [items['id'] for items in response.json()['items']]:
            raise SegmentIsNotCreated(Exception)
        return True

    def post_segment_delete(self, segment_id):
        response = self._request('DELETE', f'https://target.my.com/api/v2/remarketing/segments/{segment_id}.json',
                                 headers=self.headers_with_csrf, expected_status=204)
        return response.status_code

    def post_image_upload(self):
        url = 'https://target.my.com/api/v2/content/static.json'
        headers = {
            'X-CSRFToken': self.csrf_token
        }

        path = os.path.join(self.abs_path, 'obituary.jpg')
        files = {
            'file': open(path, 'rb')
        }
        response_image = self._request('POST', url, headers=headers, files=files, jsonify=True)['id']
        return response_image

    def post_campaign_create(self):
        # post request on reach typo
        url = 'https://target.my.com/api/v1/urls'
        params = {
            'url': 'https://obituary.cc'
        }
        response_url = self._request('GET', url, params=params, jsonify=True)['id']

        # post request with image
        response_image = self.post_image_upload()

        # post request on campaign creation
        url = 'https://target.my.com/api/v2/campaigns.json'
        headers = {
            'X-Campaign-Create-Action': 'new',
            'X-CSRFToken': self.csrf_token,
        }
        name = "Obituary"
        path = os.path.join(self.abs_path, 'json/campaign.json')
        with open(path) as json_file:
            data = json.loads(json_file.read())
        data["name"] = name
        data["banners"][0]["urls"]["primary"]["id"] = response_url
        data["banners"][0]["content"]["image_240x400"]["id"] = response_image
        response = self._request('POST', url, headers=headers, json=data, jsonify=True)
        return response['id']

    def post_campaign(self, campaign_id, request_type):
        if request_type == "POST":
            url = f'https://target.my.com/api/v2/campaigns/{campaign_id}.json'
            data = {
                "status": "deleted"
            }
            response = self._request("POST", url, headers=self.headers_with_csrf, json=data, expected_status=204)
        elif request_type == "GET":
            url = f'https://target.my.com/api/v2/campaigns/{campaign_id}.json'
            response = self._request('GET', url)
        else:
            raise UnknownRequestInMethod("Uknown request type in post_campaign() method")
        return response.status_code
