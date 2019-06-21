import json
from flask import Blueprint
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
