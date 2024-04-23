import base64

from inia.client import AWSBaseClientMixin


class CodeCommit(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, region, token=None):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "codecommit"
        self.endpoint = f"https://codecommit.{region}.amazonaws.com/"

        self._auth()

    def get_references(self, repository_name):
        payload = {"repositoryName": "aft-account-request"}
        response = self.make_request("CodeCommit_20150413.GetReferences", payload)
        return response["references"][0]["commitId"]

    def get_object_identifier(self, commit_id):
        payload = {
            "repositoryName": "aft-account-request",
            "path": "terraform/account-requests.tf",
            "commitSpecifier": commit_id,
        }
        response = self.make_request("CodeCommit_20150413.GetObjectIdentifier", payload)
        return response["identifier"]

    def get_blob(self, blob_id):
        payload = {"repositoryName": "aft-account-request", "blobId": blob_id}
        response = self.make_request("CodeCommit_20150413.GetBlob", payload)
        return response["content"]

    def put_file(
        self,
        file_content,
        commit_message,
        parent_commit_id,
        repository_name="aft-account-request",
        branch_name="main",
        file_path="terraform/account-requests.tf",
        name="DevOps Bot",
        email="platform_dev@lists.grnet.gr",
    ):
        payload = {
            "fileContent": base64.b64encode(file_content).decode("utf-8"),
            "repositoryName": repository_name,
            "commitMessage": commit_message,
            "branchName": branch_name,
            "parentCommitId": parent_commit_id,
            "filePath": file_path,
            "name": name,
            "email": email,
        }
        response = self.make_request("CodeCommit_20150413.PutFile", payload)
        return response
