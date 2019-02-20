import json
from flask import url_for, redirect
from flask import render_template, Blueprint, request
from app.utilities.helpers import build_uri, build_uri_2, forms_connect_to_eureka_validation, forms_connect_to_eureka


view_form_blueprint = Blueprint(name='view_form',
                                import_name=__name__,
                                url_prefix='/contributor_search')


@view_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/viewform', methods=['GET', 'POST'])
def view_form(inqcode, period, ruref):
    print("entered view_form")
    url_parameters = dict(zip(["survey", "period", "reference"], [inqcode, period, ruref]))
    url_connect = build_uri(url_parameters)
    pl_url_connect = build_uri_2(url_parameters)
    question_definition, contributor_details, form_responses = forms_connect_to_eureka(url_connect)
    validations_output = forms_connect_to_eureka_validation(pl_url_connect)

    definition = json.loads(question_definition)
    contributor_data = json.loads(contributor_details)
    form_response = json.loads(form_responses)
    print("load json")
    validations_output = json.loads(validations_output)
    print(type(validations_output))
    print(validations_output)
    print(form_response)
    # if there is a request method called then there's been a request for edit form
    if request.method == "POST":
        return redirect(url_for("edit_form.edit_form", ruref=ruref, inqcode=inqcode,
                                period=period))

    # if form_response is empty, then we have a blank form and so return just the definition
    if not form_response:
        return render_template("./view_form/BlankFormView.html", survey=inqcode, period=period, ruref=ruref,
                               data=definition, contributor_details=contributor_data[0],
                               locked=contributor_data[0]["lockedBy"])

    return render_template("./view_form/FormView.html", survey=inqcode, period=period, ruref=ruref, data=definition,
                           contributor_details=contributor_data[0], responses=form_response,
                           locked=contributor_data[0]["lockedBy"], validation=validations_output)
