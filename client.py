import requests
from boto3.session import Session
from requests_aws4auth import AWS4Auth


class AWSBotoClientMixin:
    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        self.region = region
        if session:
            self.session = session
        else:
            self.session = Session(
                access_key, secret_key, token, region_name=self.region
            )


class AWSCustomClientMixin(AWSBotoClientMixin):
    AMZ_JSON_VERSION = "1.1"
    AWS_SDK_VERSION = "2.1467.0"

    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
        service=None,
        endpoint=None,
    ):
        super().__init__(
            session=session,
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

        self.auth = None
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

    def _headers(self, target, json_version, sdk_version):
        self.headers = {
            "accept": "*/*",
            "content-type": f"application/x-amz-json-{json_version}",
            "x-amz-user-agent": f"aws-sdk-js/{sdk_version} promise",
            "x-amz-target": target,
        }

    def get(self, target, json_version=AMZ_JSON_VERSION, sdk_version=AWS_SDK_VERSION):
        assert self.endpoint is not None, "Endpoint must be set before making a request"

        self._headers(target, json_version, sdk_version)

        response = requests.get(self.endpoint, auth=self.auth, headers=self.headers)
        response.raise_for_status()

        return response.json()

    def post(
        self, target, data, json_version=AMZ_JSON_VERSION, sdk_version=AWS_SDK_VERSION
    ):
        assert self.endpoint is not None, "Endpoint must be set before making a request"

        self._headers(target, json_version, sdk_version)

        response = requests.post(
            self.endpoint, auth=self.auth, headers=self.headers, json=data
        )
        response.raise_for_status()

        return response.json()
