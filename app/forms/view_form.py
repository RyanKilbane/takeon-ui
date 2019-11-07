import json
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

    question_definition = api_caller.form_definition(parameters=parameters)
    contributor_details = api_caller.contributor_search(parameters=parameters)
    form_responses = api_caller_pl.form_response(parameters=parameters)
    validation_outputs = api_caller.validation_outputs(parameters=parameters)

    definition = json.loads(question_definition)
    contributor_data = json.loads(contributor_details)
    form_response = json.loads(form_responses)
    validations = json.loads(validation_outputs)

    # log.info("Form Definition: %s", definition)
    # log.info("Form Response: %s", form_response)
    # log.info("Contributor Details: %s", contributor_data)
    # log.info("Contributor Details[0]: %s", contributor_data['data'][0])

    # if there is a request method called then there's been a request for edit form
    if request.method == "POST":
        return redirect(url_for("edit_form.edit_form", ruref=ruref, inqcode=inqcode, period=period))

    # if form_response is empty, then we have a blank form and so return just the definition
    if not form_response:
        return render_template(
            template_name_or_list="./view_form/BlankFormView.html",
            survey=inqcode,
            period=period,
            ruref=ruref,
            data=definition,
            contributor_details=contributor_data['data'][0])

    return render_template(
        template_name_or_list="./view_form/FormView.html",
        survey=inqcode,
        period=period,
        ruref=ruref,
        data=definition,
        contributor_details=contributor_data['data'][0],
        responses=form_response,
        validation=validations)
