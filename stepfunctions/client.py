from inia.client import AWSBaseClientMixin


class StepFunctionsClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "stepfunctions"
        self.endpoint = f"https://states.{region}.amazonaws.com/"
        self._auth()
        self.sfn = self.session.client("stepfunctions")

    def list_state_machines(self, max_results=100):
        state_machines = []
        if self.sfn.can_paginate("list_state_machines"):
            paginator = self.sfn.get_paginator("list_state_machines")
            for page in paginator.paginate(maxResults=max_results):
                state_machines.extend(page["stateMachines"])
        else:
            state_machines = self.sfn.list_state_machines(maxResults=max_results)["stateMachines"]

        return state_machines

    def start_execution(self, state_machine_arn, input=None):
        response = self.sfn.start_execution(
            stateMachineArn=state_machine_arn,
            input=input,
        )

        return response

    def get_execution_history(
        self,
        execution_arn,
        max_results=300,
        reverse_order=False,
        include_execution_data=True,
    ):
        events = []
        if self.sfn.can_paginate("get_execution_history"):
            paginator = self.sfn.get_paginator("get_execution_history")
            for page in paginator.paginate(
                executionArn=execution_arn,
                maxResults=max_results,
                reverseOrder=reverse_order,
                includeExecutionData=include_execution_data,
            ):
                events.extend(page["events"])
        else:
            events = self.sfn.get_execution_history(
                executionArn=execution_arn,
                maxResults=max_results,
                reverseOrder=reverse_order,
                includeExecutionData=include_execution_data,
            )["events"]

        return events
