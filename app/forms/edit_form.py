import json
from flask import Blueprint, request, render_template, redirect, url_for
from app.utilities.helpers import decompose_data, build_uri, build_json, get_user
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

    question_definition = api_caller.form_definition(parameters=parameters)
    contributor_details = api_caller.contributor_search(parameters=parameters)
    form_responses = api_caller_pl.form_response(parameters=parameters)

    # load the json to turn it into a usable form
    contributor_data = json.loads(contributor_details)
    form_response = json.loads(form_responses)

    # Only run the following code if the UI has submitted a POST request
    if request.method != "POST":
        # Render the screen
        return render_template(
            "./edit_form/EditForm.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=json.loads(question_definition),
            contributor_details=contributor_data['data'][0],
            responses=form_response,
            validation={},
            status_message=json.dumps(""))


    # Only run the following code if saveForm is in the form, indicating that the save form button has been pressed
    if request.form['action'] != 'saveForm':
        # If the form doesn't have saveForm, then the exit button must have been pressed
        # return the user to the view form screen
        return redirect(url_for("view_form.view_form", ruref=ruref, inqcode=inqcode, period=period))

    log.info("Starting form save")
    form = request.form
    log.info("UI Form: %s", form)

    # Build up a contributor key
    # contributor_key_data = {'survey': inqcode, 'period': period, 'reference': ruref}

    # Extract response data from UI elements
    data = {key: form[key] for key in form.keys()}

    # decompose the field names from questionCode:number|instance:number to
    # {questionCode: number, instance: number}
    response_data = decompose_data(data)
    original_data = build_json(form_response)

    # Build up JSON structure to save
    response_data["Original Responses"] = original_data
    response_data["user"] = {"user": get_user()}
    response_data["reference"] = ruref
    response_data["period"] = period
    response_data["survey"] = inqcode

    # Build the URL for the contributor responses to update
    # url_connect = build_uri(contributor_key_data)

    # Send the data to the business layer for processing
    log.info("Combined JSON: %s", str(response_data))
    #try:
    api_caller.update_response(parameters=parameters, data=response_data)
    #except Exception as error:
    #    status_message = {"Error": "There was an error when attempting to save new responses:\n{}".format(error)}
    #    return render_template("./edit_form/EditForm.html", survey=inqcode, period=period, ruref=ruref,
    #                           data=definition, contributor_details=contributor_data['data'][0], responses=form_response,
    #                           validation={}, status_message=json.dumps(status_message))

    status_message = "New responses saved successfully"
    # Get the refreshed data from the responses table
    ## form_responses = discovery_service.form_response(parameters=url_connect)
    form_responses = api_caller_pl.form_response(parameters=parameters)

    return render_template(
        "./edit_form/EditForm.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=json.loads(question_definition),
        contributor_details=contributor_data['data'][0],
        responses=json.loads(form_responses),
        validation={},
        status_message=json.dumps(status_message))
