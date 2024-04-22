from inia.base_client import AWSBaseClientMixin


class SingleSignOnClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, region, token=None):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "userpool"
        self.endpoint = f"https://up.sso.{region}.amazonaws.com/"

        self._auth()

        self.sso_admin = self.session.client("sso-admin")
        self.identitystore = self.session.client("identitystore")

    def list_instances(self):
        instances = []

        if self.sso_admin.can_paginate("list_instances"):
            paginator = self.sso_admin.get_paginator("list_instances")
            for page in paginator.paginate():
                instances.extend(page["Instances"])
        else:
            instances = self.sso_admin.list_instances()["Instances"]

        return instances

    def list_permission_sets(self, instance_arn):
        permission_set_arns = []

        if self.sso_admin.can_paginate("list_permission_sets"):
            paginator = self.sso_admin.get_paginator("list_permission_sets")
            for page in paginator.paginate(InstanceArn=instance_arn):
                permission_set_arns.extend(page["PermissionSets"])
        else:
            permission_set_arns = self.sso_admin.list_permission_sets(
                InstanceArn=instance_arn
            )["PermissionSets"]

        permission_sets = []
        for ps_arn in permission_set_arns:
            ps = self.sso_admin.describe_permission_set(
                InstanceArn=instance_arn, PermissionSetArn=ps_arn
            )
            permission_sets.append(ps["PermissionSet"])

        return permission_sets

    def list_accounts_for_provisioned_permission_set(
        self, instance_arn, permission_set_arn
    ):
        accounts = []

        if self.sso_admin.can_paginate("list_accounts_for_provisioned_permission_set"):
            paginator = self.sso_admin.get_paginator(
                "list_accounts_for_provisioned_permission_set"
            )
            for page in paginator.paginate(
                InstanceArn=instance_arn, PermissionSetArn=permission_set_arn
            ):
                accounts.extend(page["AccountIds"])
        else:
            accounts = self.sso_admin.list_accounts_for_provisioned_permission_set(
                InstanceArn=instance_arn, PermissionSetArn=permission_set_arn
            )["AccountIds"]

        return accounts

    def list_account_assignments(self, instance_arn, permission_set_arn, account_id):
        assignments = []

        if self.sso_admin.can_paginate("list_account_assignments"):
            paginator = self.sso_admin.get_paginator("list_account_assignments")
            for page in paginator.paginate(
                InstanceArn=instance_arn,
                PermissionSetArn=permission_set_arn,
                AccountId=account_id,
            ):
                assignments.extend(page["AccountAssignments"])
        else:
            assignments = self.sso_admin.list_account_assignments(
                InstanceArn=instance_arn,
                PermissionSetArn=permission_set_arn,
                AccountId=account_id,
            )["AccountAssignments"]

        return assignments

    def list_users(self, identity_store_id):
        users = []

        if self.identitystore.can_paginate("list_users"):
            paginator = self.identitystore.get_paginator("list_users")
            for page in paginator.paginate(IdentityStoreId=identity_store_id):
                users.extend(page["Users"])
        else:
            users = self.identitystore.list_users(IdentityStoreId=identity_store_id)[
                "Users"
            ]

        return users

    def list_groups(self, identity_store_id):
        groups = []

        if self.identitystore.can_paginate("list_groups"):
            paginator = self.identitystore.get_paginator("list_groups")
            for page in paginator.paginate(IdentityStoreId=identity_store_id):
                groups.extend(page["Groups"])
        else:
            groups = self.identitystore.list_groups(IdentityStoreId=identity_store_id)[
                "Groups"
            ]

        return groups

    def list_group_memberships(self, identity_store_id, group_id):
        memberships = []

        if self.identitystore.can_paginate("list_group_memberships"):
            paginator = self.identitystore.get_paginator("list_group_memberships")
            for page in paginator.paginate(
                IdentityStoreId=identity_store_id, GroupId=group_id
            ):
                memberships.extend(page["GroupMemberships"])
        else:
            memberships = self.identitystore.list_group_memberships(
                IdentityStoreId=identity_store_id, GroupId=group_id
            )["GroupMemberships"]

        return memberships

    def describe_users(self, user_ids):
        response = self.make_request(
            "SWBUPService.DescribeUsers", {"UserIds": user_ids}
        )
        return response["Users"]

    def verify_email(self, user_id, email_id):
        response = self.make_request(
            "SWBUPService.VerifyEmail", {"UserId": user_id, "EmailId": email_id}
        )
        return response
