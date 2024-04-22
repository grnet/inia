from inia.base_client import AWSBaseClientMixin


class ControlTowerClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, region, token=None):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "controltower"
        self.endpoint = f"https://prod.{region}.blackbeard.aws.a2z.com/"

        self._auth()

    def register_ou(self, ou_id, ou_name):
        response = self.make_request(
            "AWSBlackbeardService.ManageOrganizationalUnit",
            {"OrganizationalUnitId": ou_id, "OrganizationalUnitName": ou_name},
        )
        return response["OperationArn"]

    def describe_register_ou(self, operation_id):
        response = self.make_request(
            "AWSBlackbeardService.DescribeRegisterOrganizationalUnitOperation",
            {"OperationId": operation_id},
        )
        return response
