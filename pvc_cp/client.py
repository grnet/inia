from inia.client import AWSBaseClientMixin


class EmailVerificationClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "sso-directory"
        self.endpoint = f"https://pvs-controlplane.{region}.prod.authn.identity.aws.dev"

        self._auth()

    def verify_email(self, user_id, sso_id):
        response = self.post(
            "AWSPasswordControlPlaneService.StartEmailVerification",
            {"UserId": user_id, "IdentityStoreId": sso_id},
            {"content-type": "application/x-amz-json-1.0"},
        )
        return response
