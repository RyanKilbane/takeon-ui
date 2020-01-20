import json
import time
from flask import url_for, redirect, render_template, Blueprint, request
from app.utilities.helpers import build_uri
from app.setup import log, api_caller, api_caller_pl

view_form_blueprint = Blueprint(name='view_form', import_name=__name__, url_prefix='/contributor_search')

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

    # if there is a request method called then there's been a request for edit form
    if request.method == "POST" and request.form['action'] == "saveForm":
        return redirect(url_for("edit_form.edit_form", ruref=ruref, inqcode=inqcode, period=period))
    if request.method == "POST" and request.form['action'] == "validate":
        # validation logic goes here
        print("validate!!!!!")

    # if form_response is empty, then we have a blank form and so return just the definition
    if not view_form_data:
        return render_template(
            template_name_or_list="./view_form/BlankFormView.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=view_form_data,
            contributor_details=contributor_data['data'][0])

    return render_template(
        template_name_or_list="./view_form/FormView.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=view_form_data,
        contributor_details=contributor_data['data'][0],
        validation=validations)


@view_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/override-validations', methods=['POST'])
def override_validations(inqcode, period, ruref):
    json_data = request.json
    print("Checkbox checked data: " + str(json_data))
    ruref = json_data['reference']
    inqcode = json_data['survey']
    period = json_data['period']
    api_caller.validation_overrides(parameters='', data=json.dumps(json_data))
    time.sleep(2)
    return view_form(inqcode, period, ruref)
    # return redirect(url_for("view_form.view_form", ruref=ruref, inqcode=inqcode, period=period))
