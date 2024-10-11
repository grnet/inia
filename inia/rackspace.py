import requests


class RackspaceClient:
    RACKSPACE_TOKEN_URL = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    AWS_ACCOUNTS_URL = "https://accounts.api.manage.rackspace.com/v0/awsAccounts"
    CREDENTIALS_URL_TEMPLATE = (
        "https://accounts.api.manage.rackspace.com/v0/awsAccounts/{}/credentials"
    )
    PROVISION_ACCOUNT_DEFAULTS_URL = "https://accounts.api.manage.rackspace.com/v0/awsAccounts/{}/provisioningWorkflows"
    GET_PROVISION_DETAILS_URL = "https://accounts.api.manage.rackspace.com/v0/awsAccounts/{}/provisioningDetails"

    def __init__(self, username, rackspace_api_key):
        self.username = username
        self.rackspace_api_key = rackspace_api_key

    def get_rackspace_token(self):
        data = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials": {
                    "username": self.username,
                    "apiKey": self.rackspace_api_key,
                }
            }
        }

        response = requests.post(self.RACKSPACE_TOKEN_URL, json=data)
        response.raise_for_status()
        return response.json()["access"]["token"]

    def get_aws_accounts(self, token_id, tenant_id):
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
        }
        response = requests.get(self.AWS_ACCOUNTS_URL, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_credentials(self, token_id, tenant_id, aws_account_number):
        url = self.CREDENTIALS_URL_TEMPLATE.format(aws_account_number)
        data = {"credential": {"duration": "3600"}}
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def rs_aws_provision_account_defaults(
        self, token_id, tenant_id, aws_account_number
    ):
        url = self.PROVISION_ACCOUNT_DEFAULTS_URL.format(aws_account_number)
        data = {"dryRun": False}
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def rs_aws_get_provision_details(self, token_id, tenant_id, aws_account_number):
        url = self.GET_PROVISION_DETAILS_URL.format(aws_account_number)
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
