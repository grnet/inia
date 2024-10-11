import json
import logging
import os
import sys

from awscli.customizations.cloudformation import exceptions
from awscli.customizations.cloudformation.artifact_exporter import Template
from awscli.customizations.cloudformation.yamlhelper import yaml_dump
from awscli.customizations.s3uploader import S3Uploader
from inia.client import AWSBotoClientMixin

logger = logging.getLogger(__name__)


class CloudFormationClient(AWSBotoClientMixin):
    def __init__(
        self,
        access_key=None,
        secret_key=None,
        token=None,
        region="eu-central-1",
    ):
        super().__init__(
            access_key=access_key,
            secret_key=secret_key,
            token=token,
            region=region,
        )

    def cloudformation_package(
        self,
        template_file,
        s3_bucket,
        s3_prefix,
        output_file,
        kms_key_id=None,
        metadata=None,
        force_upload=None,
        use_json=None,
    ):

        self.s3_client = self.session.client("s3")

        if not os.path.isfile(template_file):
            raise exceptions.InvalidTemplatePathError(template_path=template_file)

        self.s3_uploader = S3Uploader(
            self.s3_client,
            s3_bucket,
            s3_prefix,
            kms_key_id,
            force_upload,
        )
        self.s3_uploader.artifact_metadata = metadata

        exported_str = self._export(template_file, use_json)

        sys.stdout.write("\n")
        self.write_output(output_file, exported_str)

        logger.info(
            f"Successfully packaged artifacts and wrote output template to file {output_file}."
        )

    def _export(self, template_path, use_json):
        template = Template(template_path, os.getcwd(), self.s3_uploader)
        exported_template = template.export()

        if use_json:
            exported_str = json.dumps(exported_template, indent=4, ensure_ascii=False)
        else:
            exported_str = yaml_dump(exported_template)

        return exported_str

    def write_output(self, output_file, data):
        if output_file is None:
            sys.stdout.write(data)
            return

        with open(output_file, "w") as fp:
            fp.write(data)