from inia.client import AWSBotoClientMixin


class CodeSuiteClient(AWSBotoClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(
            access_key=access_key, secret_key=secret_key, token=token, region=region
        )

        self.repository = None
        self.branch = None
        self.name = None
        self.email = None

        self.codecommit = self.session.client("codecommit")
        self.codebuild = self.session.client("codebuild")
        self.logs = self.session.client("logs")

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

    def list_builds(self):
        ids = []

        if self.codebuild.can_paginate("list_builds"):
            paginator = self.codebuild.get_paginator("list_builds")
            for page in paginator.paginate():
                ids.extend(page["ids"])
        else:
            ids = self.codebuild.list_builds()["ids"]

        return ids

    def batch_get_builds(self, ids):
        builds = []

        if self.codebuild.can_paginate("batch_get_builds"):
            paginator = self.codebuild.get_paginator("batch_get_builds")
            for page in paginator.paginate(ids=ids):
                builds.extend(page["builds"])
        else:
            builds = self.codebuild.batch_get_builds(ids=ids)["builds"]

        return builds

    def get_log_events(self, log_group_name, log_stream_name):
        events = []

        if self.logs.can_paginate("get_log_events"):
            paginator = self.logs.get_paginator("get_log_events")
            for page in paginator.paginate(
                logGroupName=log_group_name, logStreamName=log_stream_name
            ):
                events.extend(page["events"])
        else:
            events = self.logs.get_log_events(
                logGroupName=log_group_name, logStreamName=log_stream_name
            )["events"]

        return events
