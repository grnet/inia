import uuid

from inia.client import AWSBotoClientMixin, AWSCustomClientMixin


class SSOClient(AWSCustomClientMixin):
    SAML_APP_ID = "app-520727d4117d1647"

    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        super().__init__(
            session=session,
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

        self.service = "sso"
        self.endpoint = f"https://sso.{region}.amazonaws.com/control/"

        self._auth()

    def get_sso_configuration(self, instance_arn):
        return self.post(
            "SWBService.GetSsoConfiguration",
            {"instanceArn": instance_arn},
        )

    def list_directory_associations(self, instance_arn):
        return self.post(
            "SWBService.ListDirectoryAssociations",
            {"instanceArn": instance_arn},
        )

    def list_applications(self):
        applications = []

        payload = {}

        while True:
            response = self.post("SWBService.ListApplications", payload)
            applications.extend(response["applications"])

            marker = response.get("marker")
            if not marker:
                break

            payload["marker"] = marker

        return applications

    def list_application_instances(self, filter):
        instances = []

        payload = {
            "filter": filter,
        }

        while True:
            response = self.post("SWBService.ListApplicationInstances", payload)
            instances.extend(response["applicationInstances"])

            marker = response.get("marker")
            if not marker:
                break

            payload["marker"] = marker

        return instances

    def list_instances(self):
        instances = []

        response = self.post("SWBExternalService.ListInstances", {})
        instances.extend(response["Instances"])

        return instances

    def list_external_applications(self, payload={}):
        applications = []

        while True:
            response = self.post("SWBExternalService.ListApplications", payload)
            applications.extend(response["Applications"])

            marker = response.get("marker")
            if not marker:
                break

            payload["marker"] = marker

        return applications

    def list_profiles(self, instance_id):

        payload = {
            "instanceId": instance_id,
        }

        return self.post("SWBService.ListProfiles", payload)

    def describe_application(self, application_arn):
        return self.post(
            "SWBExternalService.DescribeApplication",
            {"ApplicationArn": application_arn},
        )

    def delete_profile(self, profile_id, instance_id):
        return self.post(
            "SWBService.DeleteProfile",
            {
                "profileId": profile_id,
                "instanceId": instance_id,
            },
        )

    def delete_application_instance(self, instance_id):
        return self.post(
            "SWBService.DeleteApplicationInstance",
            {
                "instanceId": instance_id,
            },
        )

    def list_application_assignments(self, application_arn):
        return self.post(
            "SWBExternalService.ListApplicationAssignments",
            {"ApplicationArn": application_arn},
        )

    def list_application_templates(self, application_id):
        return self.post(
            "SWBService.ListApplicationTemplates",
            {"applicationId": application_id},
        )

    def create_application_instance(self, template_id, name):
        return self.post(
            "SWBService.CreateApplicationInstance",
            {
                "templateId": template_id,
                "name": name,
            },
        )

    def update_app_instance_display_data(self, description, display_name, instance_id):
        return self.post(
            "SWBService.UpdateApplicationInstanceDisplayData",
            {
                "description": description,
                "displayName": display_name,
                "instanceId": instance_id,
            },
        )

    def update_app_instance_service_provider_config(
        self, instance_id, service_provider_config
    ):
        return self.post(
            "SWBService.UpdateApplicationInstanceServiceProviderConfiguration",
            {
                "instanceId": instance_id,
                "serviceProviderConfig": service_provider_config,
            },
        )

    def update_app_instance_response_config(self, instance_id, response_config):
        return self.post(
            "SWBService.UpdateApplicationInstanceResponseConfiguration",
            {
                "instanceId": instance_id,
                "responseConfig": response_config,
            },
        )

    def update_app_instance_response_schema_config(
        self, instance_id, response_schema_config
    ):
        return self.post(
            "SWBService.UpdateApplicationInstanceResponseSchemaConfiguration",
            {
                "instanceId": instance_id,
                "responseSchemaConfig": response_schema_config,
            },
        )

    def update_app_instance_status(self, instance_id, status):
        return self.post(
            "SWBService.UpdateApplicationInstanceStatus",
            {
                "instanceId": instance_id,
                "status": status,
            },
        )


class SSODirectoryClient(AWSCustomClientMixin):
    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        super().__init__(
            session=session,
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

        self.service = "sso-directory"
        self.endpoint = f"https://pvs-controlplane.{region}.prod.authn.identity.aws.dev"

        self._auth()

    def verify_email(self, user_id, sso_id):
        return self.post(
            "AWSPasswordControlPlaneService.StartEmailVerification",
            {"UserId": user_id, "IdentityStoreId": sso_id},
            json_version="1.0",
        )


class UserPoolClient(AWSCustomClientMixin):
    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        super().__init__(
            session=session,
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

        self.service = "userpool"
        self.endpoint = f"https://up.sso.{region}.amazonaws.com/"

        self._auth()

    def describe_users(self, user_ids):
        response = self.post("SWBUPService.DescribeUsers", {"UserIds": user_ids})
        return response["Users"]

    def update_password(self, user_id, mode="EMAIL"):
        return self.post(
            "SWBUPService.UpdatePassword", {"UserId": user_id, "PasswordMode": mode}
        )


class SingleSignOnClient(AWSBotoClientMixin):
    def __init__(
        self,
        session=None,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        super().__init__(
            session=session,
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

        self.sso_admin = self.session.client("sso-admin")
        self.identitystore = self.session.client("identitystore")
        self.userpool = UserPoolClient(session=self.session, region=region)
        self.sso_directory = SSODirectoryClient(session=self.session, region=region)

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
        return self.userpool.describe_users(user_ids)

    def update_password(self, user_id, mode="EMAIL"):
        return self.userpool.update_password(user_id, mode)

    def verify_email(self, user_id, sso_id):
        return self.sso_directory.verify_email(user_id, sso_id)
