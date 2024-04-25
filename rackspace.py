import json
from typing import Any, Dict

import requests


class RackspaceClient:
    RACKSPACE_TOKEN_URL = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    AWS_ACCOUNTS_URL = "https://accounts.api.manage.rackspace.com/v0/awsAccounts"
    CREDENTIALS_URL_TEMPLATE = (
        "https://accounts.api.manage.rackspace.com/v0/awsAccounts/{}/credentials"
    )
    DEFAULT_REGION = "eu-central-1"

    def __init__(self, username: str, rackspace_api_key: str):
        self.username = username
        self.rackspace_api_key = rackspace_api_key

    def get_rackspace_token(self) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        data = json.dumps(
            {
                "auth": {
                    "RAX-KSKEY:apiKeyCredentials": {
                        "username": self.username,
                        "apiKey": self.rackspace_api_key,
                    }
                }
            }
        )
        response = requests.post(self.RACKSPACE_TOKEN_URL, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access"]["token"]

    def get_aws_accounts(self, token_id: str, tenant_id: str) -> Dict[str, Any]:
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
            "Content-Type": "application/json",
        }
        response = requests.get(self.AWS_ACCOUNTS_URL, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_credentials(
        self, token_id: str, tenant_id: str, aws_account_number: str
    ) -> Dict[str, Any]:
        url = self.CREDENTIALS_URL_TEMPLATE.format(aws_account_number)
        data = '{"credential": {"duration": "3600"}}'
        headers = {
            "X-Auth-Token": token_id,
            "X-Tenant-Id": tenant_id,
            "Content-Type": "application/json",
        }
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
