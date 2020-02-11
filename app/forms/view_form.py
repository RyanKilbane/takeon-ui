import json
import os
import requests
from flask import url_for, redirect, render_template, Blueprint, request
from requests.exceptions import HTTPError
from app.utilities.helpers import build_uri, get_user, filter_validations
from app.setup import log, api_caller, api_caller_pl

view_form_blueprint = Blueprint(name='view_form', import_name=__name__, url_prefix='/contributor_search')
url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')

# Flask Endpoints
@view_form_blueprint.errorhandler(404)
def not_found(error):
    return render_template('./error_templates/404.html', message_header=error), 404


@view_form_blueprint.errorhandler(403)
def not_auth(error):
    return render_template('./error_templates/403.html', message_header=error), 403


@view_form_blueprint.errorhandler(500)
def internal_server_error(error):
    return render_template('./error_templates/500.html', message_header=error), 500

# Main entry-point
@view_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/viewform', methods=['GET', 'POST'])
def view_form(inqcode, period, ruref):
    log.info("View_Form -- START --")

    url_parameters = dict(zip(["survey", "period", "reference"], [inqcode, period, ruref]))
    parameters = build_uri(url_parameters)

    contributor_details = api_caller.contributor_search(parameters=parameters)
    validation_outputs = api_caller.validation_outputs(parameters=parameters)
    view_forms = api_caller.view_form_responses(parameters=parameters)

    contributor_data = json.loads(contributor_details)
    validations = json.loads(validation_outputs)

    view_form_data = json.loads(view_forms)
    log.info("Contributor Details: %s", contributor_data)
    log.info("Contributor Details[0]: %s", contributor_data['data'][0])
    log.info("View Form Data: %s", view_form_data)
    log.info("Validations output: %s", validations)
    log.info("Filtered Validations output: %s", filter_validations(validations))

    # if there is a request method called then there's been a request for edit form
    if request.method == "POST" and request.form['action'] == "saveForm":
        return redirect(url_for("edit_form.edit_form", ruref=ruref, inqcode=inqcode, period=period))

    #validate button logic
    if request.method == "POST" and request.form['action'] == "validate":
        log.info('save validation button pressed')
        json_data = {"survey": inqcode, "period": period, "reference": ruref, "bpmId":"0"}
        header = {"x-api-key": api_key}
        status_message = 'Validation Run Successfully'
        try:
            response = api_caller.run_validation(url, json.dumps(json_data), header)
            log.info("Response from SQS: %s", response)
        except HTTPError as http_err:
            status_message = "Http Error. Unable to call URL"
            log.info('URL error occurred: %s', http_err)
        except ConnectionError as connection_err:
            status_message = "Connection Error. Unable to Connect to API Gateway"
            log.info('API request error occured: %s', connection_err)
        return render_template(
            template_name_or_list="./view_form/FormView.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=view_form_data,
            status_message=json.dumps(status_message),
            contributor_details=contributor_data['data'][0],
            validation=filter_validations(validations))

    # if form_response is empty, then we have a blank form and so return just the definition
    if not view_form_data:
        return render_template(
            template_name_or_list="./view_form/BlankFormView.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=view_form_data,
            contributor_details=contributor_data['data'][0],
            user=get_user())

    return render_template(
        template_name_or_list="./view_form/FormView.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=view_form_data,
        status_message=json.dumps(""),
        contributor_details=contributor_data['data'][0],
        validation=filter_validations(validations),
        user=get_user())


@view_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/override-validations', methods=['POST'])
def override_validations(inqcode, period, ruref):
    json_data = request.json
    log.info("Checkbox checked data: %s", str(json_data))
    ruref = json_data['reference']
    inqcode = json_data['survey']
    period = json_data['period']

    api_caller.validation_overrides(parameters='', data=json.dumps(json_data))
    url_parameters = dict(zip(["survey", "period", "reference"], [inqcode, period, ruref]))
    parameters = build_uri(url_parameters)

    contributor_details = api_caller.contributor_search(parameters=parameters)
    validation_outputs = api_caller.validation_outputs(parameters=parameters)
    view_forms = api_caller.view_form_responses(parameters=parameters)

    contributor_data = json.loads(contributor_details)
    validations = json.loads(validation_outputs)

    view_form_data = json.loads(view_forms)

    return render_template(
        template_name_or_list="./view_form/FormView.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=view_form_data,
        contributor_details=contributor_data['data'][0],
        validation=filter_validations(validations),
        user=get_user())
