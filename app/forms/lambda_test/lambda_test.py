import json
from flask import Blueprint, request, render_template, redirect, url_for
from app.setup import discovery_service
from app.utilities.helpers import decompose_data, build_uri, build_json, get_user, forms_connect_to_eureka, \
                                  forms_connect_to_eureka_validation, build_uri_2
import boto3

lambda_test_blueprint = Blueprint(name='lambda_test',
                                  import_name=__name__,
                                  url_prefix='/contributor_search')

@lambda_test_blueprint.route("/lambda_test/<name>")
def lambda_test(name):
    client = boto3.client("lambda")
    data = {"name": name}
    response = client.invoke(FunctionName="takeon-lambda-test", Payload=json.dumps(data).encode("utf-8"))
    return response
