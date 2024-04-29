from inia.client import AWSBaseClientMixin


class CodeSuiteClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.repository = None
        self.branch = None
        self.name = None
        self.email = None

        self.codecommit = self.session.client("codecommit")

    def get_repository(self, repository_name):
        response = self.codecommit.get_repository(repositoryName=repository_name)
        metadata = response["repositoryMetadata"]

        self.repository = metadata["repositoryName"]
        self.branch = metadata["defaultBranch"]

        return metadata

    def set_commiter(self, name, email):
        self.name = name
        self.email = email

    def get_file(self, file_path):
        response = self.codecommit.get_file(
            repositoryName=self.repository, filePath=file_path
        )
        return {k: v for k, v in response.items() if k not in ["ResponseMetadata"]}

    def put_file(
        self,
        file_content,
        file_path,
        file_mode,
        parent_commit_id,
        commit_message,
    ):
        response = self.codecommit.put_file(
            repositoryName=self.repository,
            branchName=self.branch,
            fileContent=file_content,
            filePath=file_path,
            fileMode=file_mode,
            parentCommitId=parent_commit_id,
            commitMessage=commit_message,
            name=self.name,
            email=self.email,
        )
        return {k: v for k, v in response.items() if k not in ["ResponseMetadata"]}
