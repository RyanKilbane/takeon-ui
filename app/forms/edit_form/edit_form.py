import json
from flask import Blueprint, request, render_template, redirect, url_for
from app.setup import discovery_service
from app.utilities.helpers import decompose_data, build_uri, build_json, get_user, forms_connect_to_eureka, \
                                  forms_connect_to_eureka_validation, build_uri_2

edit_form_blueprint = Blueprint(name='edit_form',
                                import_name=__name__,
                                url_prefix='/contributor_search')


#################################################################################################
# ######################################## FLASK ENDPOINTS ######################################
#################################################################################################
@edit_form_blueprint.errorhandler(404)
def not_found(e):
    return render_template('./error_templates/404.html', message_header=e), 404


@edit_form_blueprint.errorhandler(403)
def not_auth(e):
    return render_template('./error_templates/403.html', message_header=e), 403


@edit_form_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('./error_templates/500.html', message_header=e), 500


@edit_form_blueprint.route('/Contributor/<inqcode>/<period>/<ruref>/editform', methods=['GET', 'POST'])
def edit_form(inqcode, period, ruref):

    # Init save_error to empty string
    status_message = ""

    # Build URI for business layer
    url_parameters = dict(zip(["survey", "period", "reference"], [inqcode, period, ruref]))
    url_connect = build_uri(url_parameters)
    pl_url_connect = build_uri_2(url_parameters)

    # attempt to connect to Eureka, except common errors

    question_definition, contributor_details, form_responses = forms_connect_to_eureka(url_connect)

    # validations_output = forms_connect_to_eureka_validation(pl_url_connect)
    # update contributor table to lock the form for editing
    discovery_service.update_locked_status(url_connect, "persistence-layer", data={"lockedBy": get_user()})

    # load the json to turn it into a usable form
    definition = json.loads(question_definition)
    contributor_data = json.loads(contributor_details)
    form_response = json.loads(form_responses)
    # validations_output = json.loads(validations_output)

    # Only run the following code if the UI has submitted a POST request
    if request.method == "POST":
        form = request.form
        print(form)
        # Only run the following code if saveForm is in the form, indicating that the save form button has been pressed
        if request.form['action'] == 'saveForm':
            print("saveform")
            # Get the form
            form = request.form
            print(form)
            print(form_response)
            # Build up a contributor key
            contributor_key_data = {'survey': inqcode, 'period': period, 'reference': ruref}
            # Get the data from the form
            data = {key: form[key] for key in form.keys()}

            # decompose the field names from questionCode:number|instance:number to
            # {questionCode: number, instance: number}
            response_data = decompose_data(data)
            original_data = build_json(form_response)
            # print("form response: {}".format(form_response))
            # print("original data: {}".format(original_data))

            # Append the original responses to the JSON
            response_data["Original Responses"] = original_data

            # Append the username
            response_data["user"] = {"user": get_user()}
            # Append contributor PK
            response_data["reference"] = ruref
            response_data["period"] = period
            response_data["survey"] = inqcode

            # Build the URL for the contributor responses to update
            url_connect = build_uri(contributor_key_data)

            # Send the data to the business layer for processing
            print("total json: {}".format(str(response_data)))
            try:
                discovery_service.update_response(url_connect, "business-layer", response_data)
            except Exception as error:
                status_message = {"Error": "There was an error when attempting to save new responses:\n{}".format(error)}
                return render_template("./edit_form/EditFormNew.html", survey=inqcode, period=period, ruref=ruref,
                                      data=definition, contributor_details=contributor_data[0], responses=form_response,
                                      validation={}, status_message=json.dumps(status_message))
                
            status_message = "New responses saved successfully"
            # Get the refreshed data from the responses table
            form_responses = discovery_service.form_response(url_connect, "persistence-layer")
            form_response = json.loads(form_responses)

            # Render the responses
            return render_template("./edit_form/EditFormNew.html", survey=inqcode, period=period, ruref=ruref,
                                   data=definition, contributor_details=contributor_data[0], responses=form_response,
                                   validation={}, status_message=status_message)

        if request.form['action'] == 'saveAndValidate':
            print("Save and validate")

            # Get the form
            form = request.form
            print(form)
            # Build up a contributor key
            contributor_key_data = {'survey': inqcode, 'period': period, 'reference': ruref}
            # Get the data from the form
            data = {key: form[key] for key in form.keys()}

            # decompose the field names from questionCode:number|instance:number to
            # {questionCode: number, instance: number}
            response_data = decompose_data(data)
            original_data = build_json(form_response)
            # print("form response: {}".format(form_response))
            # print("original data: {}".format(original_data))

            # Append the original responses to the JSON
            response_data["Original Responses"] = original_data

            # Append the username
            response_data["user"] = {"user": get_user()}
            # Append contributor PK
            response_data["reference"] = ruref
            response_data["period"] = period
            response_data["survey"] = inqcode

            # Build the URL for the contributor responses to update
            url_connect = build_uri(contributor_key_data)

            # Send the data to the business layer for processing
            print("total json: {}".format(str(response_data)))

            output_from_bl = discovery_service.run_validations(url_connect, "validation-persistence-layer", response_data)
            response_from_bl = json.loads(output_from_bl)
            if not response_from_bl["error"]:

                # Get the refreshed data from the responses table
                contributor_details = discovery_service.contributor_search_without_paging(url_connect, "business-layer")
                form_responses = discovery_service.form_response(url_connect, "persistence-layer")
                form_response = json.loads(form_responses)
                validations_output = forms_connect_to_eureka_validation(pl_url_connect)
                validations_output = json.loads(validations_output)
                contributor_data = json.loads(contributor_details)

                return render_template("./edit_form/EditFormNew.html", survey=inqcode, period=period, ruref=ruref,
                                       data=definition, contributor_details=contributor_data[0],
                                       responses=form_response,
                                       validation={})

            else:
                return render_template("./404.html", message_header="Error in Validate on Save",
                                       error_message=response_from_bl["error"])

        # If the form doesn't have saveForm, then the exit button must have been pressed
        # Update the contributor table to unlock the form
        discovery_service.update_locked_status(url_connect, "persistence-layer", data={"lockedBy": ""})
        # return the user to the view form screen
        return redirect(url_for("view_form.view_form", ruref=ruref, inqcode=inqcode,
                                period=period))

    # Render the screen
    return render_template("./edit_form/EditFormNew.html", survey=inqcode, period=period, ruref=ruref, data=definition,
                           contributor_details=contributor_data[0], responses=form_response,
                           locked=contributor_data[0]["lockedBy"], validation={}, status_message=json.dumps(status_message))
