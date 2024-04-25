from inia.client import AWSBaseClientMixin


class CodeCommitClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.repository_name = None

        self.service = "codecommit"
        self.endpoint = f"https://codecommit.{region}.amazonaws.com/"
        self._auth()

    def set_repo(self, repository_name):
        self.repository_name = repository_name

    def make_payload(self, **kwargs):
        payload = {"repositoryName": self.repository_name}
        payload.update(kwargs)
        return payload

    def get_repository(self):
        payload = self.make_payload()
        response = self.post("CodeCommit_20150413.GetRepository", payload)
        return response["repositoryMetadata"]

    def get_references(self):
        payload = self.make_payload()
        response = self.post("CodeCommit_20150413.GetReferences", payload)
        return response["references"][0]["commitId"]

    def get_object_identifier(self, path, commit_id):
        payload = self.make_payload(
            path=path, commitSpecifier=commit_id
        )
        response = self.post("CodeCommit_20150413.GetObjectIdentifier", payload)
        return response["identifier"]

    def get_blob(self, blob_id):
        payload = self.make_payload(blobId=blob_id)
        response = self.post("CodeCommit_20150413.GetBlob", payload)
        return response["content"]

    def put_file(
        self,
        file_content,
        commit_message,
        parent_commit_id,
        branch_name,
        file_path,
        name,
        email,
    ):
        payload = self.make_payload(
            fileContent=file_content,
            commitMessage=commit_message,
            branchName=branch_name,
            parentCommitId=parent_commit_id,
            filePath=file_path,
            name=name,
            email=email,
        )
        response = self.post("CodeCommit_20150413.PutFile", payload)
        return response
