from inia.client import AWSBotoClientMixin


class ServiceCatalogClient(AWSBotoClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(
            access_key=access_key, secret_key=secret_key, token=token, region=region
        )

        self.servicecatalog = self.session.client("servicecatalog")

    def _search_provisioned_products(self):
        return self.servicecatalog.search_provisioned_products(
            AccessLevelFilter={"Key": "Account", "Value": "self"}
        )

    def get_provisioned_product(self, product_name):
        pp = self._search_provisioned_products()
        return next(
            (
                product
                for product in pp["ProvisionedProducts"]
                if product["Name"] == product_name
            ),
            None,
        )

    def get_provisioned_product_detail(self, pp_id):
        response = self.servicecatalog.describe_provisioned_product(Id=pp_id)
        return response["ProvisionedProductDetail"]["Status"]

    def get_provisioned_product_outputs(self, pp_id):
        outputs = self.servicecatalog.get_provisioned_product_outputs(
            ProvisionedProductId=pp_id
        )
        return next(
            (
                output["OutputValue"]
                for output in outputs["Outputs"]
                if output["OutputKey"] == "AccountId"
            ),
            None,
        )
