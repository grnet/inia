from inia.client import AWSBaseClientMixin


class ControlTowerClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, region, token=None):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "userpool"
        self.endpoint = f"https://up.sso.{region}.amazonaws.com/"

        self._auth()
