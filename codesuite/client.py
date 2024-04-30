from inia.client import AWSBaseClientMixin


class CodeSuiteClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.repository = None
        self.branch = None
        self.name = None
        self.email = None

        self.codecommit = self.session.client("codecommit")
        self.codebuild = self.session.client("codebuild")
        self.cloudwatch_logs = self.session.client("logs")

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
        response = self.codebuild.list_builds()
        return response

    def get_batch_builds(self, ids):
        response = self.codebuild.batch_get_builds(ids=ids)
        return response

    def get_log_events(
        self,
        log_group_name,
        log_stream_name,
        start_from_head=True,
        unmask=True,
    ):
        logs = []
        if self.cloudwatch_logs.can_paginate("get_log_events"):
            paginator = self.cloudwatch_logs.get_paginator("get_log_events")
            for page in paginator.paginate(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                startFromHead=start_from_head,
                unmask=unmask,
            ):
                logs.extend(page["events"])
        else:
            logs = self.cloudwatch_logs.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name,
                startFromHead=start_from_head,
                unmask=unmask,
            )["events"]
        return logs
