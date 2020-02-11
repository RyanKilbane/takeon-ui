import json
from flask import Blueprint, request, render_template, redirect, url_for
from app.utilities.helpers import build_uri, get_user
from app.utilities.filter_validations import filter_validations
from app.setup import log, api_caller, api_caller_pl

edit_form_blueprint = Blueprint(name='edit_form', import_name=__name__, url_prefix='/contributor_search')

# Flask Endpoints
@edit_form_blueprint.errorhandler(404)
def not_found(error):
    return render_template('./error_templates/404.html', message_header=error), 404


@edit_form_blueprint.errorhandler(403)
def not_auth(error):
    return render_template('./error_templates/403.html', message_header=error), 403


@edit_form_blueprint.errorhandler(500)
def internal_server_error(error):
    return render_template('./error_templates/500.html', message_header=error), 500


@edit_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/editform', methods=['GET', 'POST'])
def edit_form(inqcode, period, ruref):
    log.info("Edit Form -- START --")

    # Build URI for business layer
    url_parameters = dict(zip(["survey", "period", "reference"], [inqcode, period, ruref]))
    parameters = build_uri(url_parameters)

    contributor_details = api_caller.contributor_search(parameters=parameters)
    validation_outputs = api_caller.validation_outputs(parameters=parameters)
    view_forms = api_caller.view_form_responses(parameters=parameters)

    # load the json to turn it into a usable form
    contributor_data = json.loads(contributor_details)
    validations = json.loads(validation_outputs)
    view_form_data = json.loads(view_forms)

    # Only run the following code if the UI has submitted a POST request
    if request.method != "POST":
        # Render the screen
        return render_template(
            "./edit_form/EditForm.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=view_form_data,
            contributor_details=contributor_data['data'][0],
            validation=filter_validations(validations),
            status_message=json.dumps(""))


    # Only run the following code if saveForm is in the form, indicating that the save form button has been pressed
    if request.form['action'] != 'saveForm':
        # If the form doesn't have saveForm, then the exit button must have been pressed
        # return the user to the view form screen
        return redirect(url_for("view_form.view_form", ruref=ruref, inqcode=inqcode, period=period))

    log.info('Starting form save')

    # Extract response data from UI elements
    response_data = extract_responses(request.form)
    log.info('Response data: %s', response_data)

    # Build up JSON structure to save
    json_output = {}
    json_output["responses"] = response_data
    json_output["user"] = get_user()
    json_output["reference"] = ruref
    json_output["period"] = period
    json_output["survey"] = inqcode

    # Send the data to the business layer for processing
    log.info("Output JSON: %s", str(json_output))
    # api_caller.update_response(parameters=parameters, data=json_output)
    # New API call for save in business layer which uses GraphQL
    api_caller.save_response(parameters=parameters, data=json_output)

    # Get the refreshed data from the responses table
    view_forms_gql = api_caller.view_form_responses(parameters=parameters)

    return render_template(
        "./edit_form/EditForm.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=json.loads(view_forms_gql),
        contributor_details=contributor_data['data'][0],
        validation=filter_validations(validations),
        status_message=json.dumps('New responses saved successfully'))


def extract_responses(data) -> dict:
    output = []
    for key in data.keys():
        if key != "action":
            output.append({'question': key, 'response': data[key], 'instance': 0})
    return output
