from inia.client import AWSBaseClientMixin


class CostExplorerClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "ce"
        self.endpoint = f"https://ce.{region}.amazonaws.com/"
        self._auth()
        self.ce = self.session.client("ce")

    def get_cost_and_usage(
        self,
        time_period,
        granularity,
        filter,
        metrics,
        group_by,
    ):
        results = []
        if self.ce.can_paginate("get_cost_and_usage"):
            paginator = self.ce.get_paginator("get_cost_and_usage")
            for page in paginator.paginate(
                TimePeriod=time_period,
                Granularity=granularity,
                Filter=filter,
                Metrics=metrics,
                GroupBy=group_by,
            ):
                results.extend(page["results"])
        else:
            results = self.ce.get_cost_and_usage(
                TimePeriod=time_period,
                Granularity=granularity,
                Filter=filter,
                Metrics=metrics,
                GroupBy=group_by,
            )

        return results
