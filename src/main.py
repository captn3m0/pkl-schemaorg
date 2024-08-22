import datetime
import json
import os
import shutil
from http.client import HTTPResponse
from pathlib import Path
import sys
from urllib import request

from constants import data_type_map, PACKAGE_NAME, data_type_specificity
from jinja import jinja_env
from schema_org import SchemaOrg

THIS_PATH = Path(__file__).parent


def copy_utils():
    os.makedirs(f"{PACKAGE_NAME}/ISO8601", exist_ok=True)
    for file in os.listdir(f"{THIS_PATH}/ISO8601"):
        if file.endswith(".py"):
            shutil.copy(f"{THIS_PATH}/ISO8601/{file}", f"{PACKAGE_NAME}/ISO8601")


def init_package():
    shutil.rmtree(PACKAGE_NAME)
    os.makedirs(PACKAGE_NAME, exist_ok=True)
    copy_utils()


if __name__ == "__main__":
    init_package()
    # write_base_class()
    # schema_org_request: HTTPResponse = request.urlopen(
    #     "https://schema.org/version/latest/schemaorg-current-https.jsonld"
    # )
    # schema_data = json.loads(schema_org_request.read().decode("utf-8"))

    jsonld_fn = sys.argv[1]
    with open(jsonld_fn, "r") as f:
        schema_data = json.load(f)
        schema_data = {node["@id"]: node for node in schema_data["@graph"]}
        schema_org_api = SchemaOrg(schema_data, data_type_map, data_type_specificity)
        for class_ in schema_org_api.get_all_classes():
            schema_org_api.load_type(class_)
        schema_org_api.write_init()
