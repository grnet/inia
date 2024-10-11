from inia.client import AWSCustomClientMixin


class ControlTowerClient(AWSCustomClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(
            access_key=access_key, secret_key=secret_key, token=token, region=region
        )

        self.service = "controltower"
        self.endpoint = f"https://prod.{region}.blackbeard.aws.a2z.com/"

        self._auth()

        self.organizations = self.session.client("organizations")

    def list_roots(self):
        roots = []
        if self.organizations.can_paginate("list_roots"):
            paginator = self.organizations.get_paginator("list_roots")
            for page in paginator.paginate():
                roots.extend(page["Roots"])
        else:
            roots = self.organizations.list_roots()["Roots"]

        return roots

    def list_organizational_units_for_parent(self, parent_id):
        ous = []
        if self.organizations.can_paginate("list_organizational_units_for_parent"):
            paginator = self.organizations.get_paginator(
                "list_organizational_units_for_parent"
            )
            for page in paginator.paginate(ParentId=parent_id):
                ous.extend(page["OrganizationalUnits"])
        else:
            ous = self.organizations.list_organizational_units_for_parent(
                ParentId=parent_id
            )["OrganizationalUnits"]

        return ous

    def list_accounts_for_parent(self, parent_id):
        accounts = []
        if self.organizations.can_paginate("list_accounts_for_parent"):
            paginator = self.organizations.get_paginator("list_accounts_for_parent")
            for page in paginator.paginate(ParentId=parent_id):
                accounts.extend(page["Accounts"])
        else:
            accounts = self.organizations.list_accounts_for_parent(ParentId=parent_id)[
                "Accounts"
            ]

        return accounts

    def describe_organizational_unit(self, ou_id):
        return self.organizations.describe_organizational_unit(
            OrganizationalUnitId=ou_id
        )

    def describe_account(self, account_id):
        return self.organizations.describe_account(AccountId=account_id)

    def list_delegated_administrators(self, service_principal="sso.amazonaws.com"):
        adminstrators = []
        if self.organizations.can_paginate("list_delegated_administrators"):
            paginator = self.organizations.get_paginator(
                "list_delegated_administrators"
            )
            for page in paginator.paginate(ServicePrincipal=service_principal):
                adminstrators.extend(page["DelegatedAdministrators"])
        else:
            adminstrators = self.organizations.list_delegated_administrators(
                ServicePrincipal=service_principal
            )["DelegatedAdministrators"]

        return adminstrators

    def register_delegated_administrator(
        self, account_id, service_principal="sso.amazonaws.com"
    ):
        return self.organizations.register_delegated_administrator(
            ServicePrincipal=service_principal,
            AccountId=account_id,
        )

    def deregister_delegated_administrator(
        self, account_id, service_principal="sso.amazonaws.com"
    ):
        return self.organizations.deregister_delegated_administrator(
            ServicePrincipal=service_principal,
            AccountId=account_id,
        )

    def list_managed_ous(self):
        response = self.post(
            "AWSBlackbeardService.ListManagedOrganizationalUnits",
            {"MaxResults": 100},
        )
        return response["ManagedOrganizationalUnitList"]

    def describe_managed_ou(self, ou_id):
        response = self.post(
            "AWSBlackbeardService.DescribeManagedOrganizationalUnit",
            {"OrganizationalUnitId": ou_id},
        )
        return response

    def manage_ou(self, ou_id, ou_name):
        response = self.post(
            "AWSBlackbeardService.ManageOrganizationalUnit",
            {"OrganizationalUnitId": ou_id, "OrganizationalUnitName": ou_name},
        )
        return response["OperationArn"]

    def describe_register_ou_operation(self, operation_id):
        response = self.post(
            "AWSBlackbeardService.DescribeRegisterOrganizationalUnitOperation",
            {"OperationId": operation_id},
        )
        return response

    def deregister_managed_account(self, account_id):
        response = self.post(
            "AWSBlackbeardService.DeregisterManagedAccount",
            {"AccountId": account_id},
        )
        return response

    def deregister_ou(self, ou_id):
        response = self.post(
            "AWSBlackbeardService.DeregisterOrganizationalUnit",
            {"OrganizationalUnitId": ou_id},
        )
        return response
