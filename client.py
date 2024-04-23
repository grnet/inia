import requests

from boto3.session import Session
from requests_aws4auth import AWS4Auth


class AWSBaseClientMixin:
    AMZ_USER_AGENT = "aws-sdk-js/2.1467.0 promise"

    def __init__(
        self,
        access_key,
        secret_key,
        token=None,
        region=None,
        service=None,
        endpoint=None,
    ):
        self.headers = {
            "accept": "*/*",
            "content-type": "application/x-amz-json-1.1",
            "x-amz-user-agent": self.AMZ_USER_AGENT,
        }

        self.auth = None
        self.session = Session(access_key, secret_key, token)

        self.region = region
        self.service = service
        self.endpoint = endpoint

    def _auth(self):
        assert self.region is not None, "Region must be set before authenticating"
        assert self.service is not None, "Service must be set before authenticating"

        credentials = self.session.get_credentials().get_frozen_credentials()

        self.auth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            self.region,
            self.service,
            session_token=credentials.token,
        )

    def get(self, target):
        assert self.endpoint is not None, "Endpoint must be set before making a request"

        self.headers.update(
            {
                "x-amz-target": target,
            }
        )
        response = requests.get(self.endpoint, auth=self.auth, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def post(self, target, data):
        assert self.endpoint is not None, "Endpoint must be set before making a request"

        self.headers.update(
            {
                "x-amz-target": target,
            }
        )
        response = requests.post(
            self.endpoint, auth=self.auth, headers=self.headers, json=data
        )
        response.raise_for_status()

        return response.json()
