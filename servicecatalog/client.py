import time

from inia.client import AWSBaseClientMixin


class ServiceCatalogClient(AWSBaseClientMixin):
    def __init__(self, access_key, secret_key, token=None, region="eu-central-1"):
        super().__init__(access_key, secret_key, token=token, region=region)

        self.service = "servicecatalog"
        self.servicecatalog = self.session.client(self.service)

    def search_provisioned_products(self):
        response = self.servicecatalog.search_provisioned_products(
            AccessLevelFilter={"Key": "Account", "Value": "self"}
        )
        return response

    def get_provisioned_product_id(self, product_name):
        pp = self.search_provisioned_products()
        for product in pp["ProvisionedProducts"]:
            if product["Name"] == product_name:
                return product["Id"]
        return None

    def check_pp(self, pp_id):
        while True:
            response = self.servicecatalog.describe_provisioned_product(Id=pp_id)
            state = response["ProvisionedProductDetail"]["Status"]

            if state == "AVAILABLE":
                print(f"Status: {state}, provisioning succeeded")
                break
            elif state == "TAINTED":
                print(f"Status: {state}, provisioning tainted")
                exit(1)
            elif state == "ERROR":
                print(f"Status: {state}, provisioning failed")
                exit(1)

            print(f"Status: {state}, sleeping for 30s ...")
            time.sleep(30)

        outputs = self.servicecatalog.get_provisioned_product_outputs(
            ProvisionedProductId=pp_id
        )
        for output in outputs["Outputs"]:
            if output["OutputKey"] == "AccountId":
                return output["OutputValue"]

        return None
