import json

from urllib.error import URLError
#from content_management import Content
from flask import request, Blueprint, redirect, url_for, render_template, render_template_string
from flask_jwt_extended import jwt_required

from app.utilities.helpers import create_form_class, create_new_dict, clean_search_parameters, build_uri
from app.utilities.graphql_data import GraphData
from app.setup import discovery_service

contributor_search_blueprint = Blueprint(name='contributor_search',
                                         import_name=__name__,
                                         url_prefix='/contributor_search')

contributor_search_blueprint_post = Blueprint(name='contributor_search_post',
                                              import_name=__name__,
                                              url_prefix='/contributor_search')

# headers here double as url parameters
headers = ['reference', 'period', 'survey', 'status', 'formId']


#################################################################################################
# ######################################## FLASK ENDPOINTS ######################################
#################################################################################################
@contributor_search_blueprint.errorhandler(404)
def not_found(e):
    return render_template('./error_templates/404.html', message_header=e), 404


@contributor_search_blueprint.errorhandler(403)
def not_auth(e):
    return render_template('./error_templates/403.html', message_header=e), 403


@contributor_search_blueprint.errorhandler(500)
def internal_server_error(e):
    return render_template('./error_templates/500.html', message_header=e), 500


@contributor_search_blueprint.route('/')
# Redirect to from the landing page to the GeneralSearchScreen
def landing_page():
    return redirect(url_for('contributor_search.general_search_screen_selection'))


# ####################### SIMPLE SEARCH SCREEN, EXPOSES ALL FIELDS #############################
@contributor_search_blueprint.route('/Contributor/searchSelection', methods=['GET', 'POST'])
# @jwt_required
# Selection options, just pull out the values that have been selected, join
# them all together in a semi-colon delimited string
def general_search_screen_selection():
    if request.method == "POST":
        criteria = ';'.join(i for i in request.form.keys())
        # redirect to general search screen, criteria is added as a url parameter. ?criteria=VALUE1;VALUE2
        return redirect(url_for("contributor_search.general_search_screen", criteria=criteria))

    return render_template('./search_screen_choice/GeneralSearchScreenChoice.html')


@contributor_search_blueprint_post.route('/Contributor/GeneralSearch', methods=['POST'])
def general_search_screen():
    criteria = request.args['criteria'].split(";")
    # Build class for the forms that are passed in, this must be done dynamically
    selection_form = create_form_class(criteria)
    # create form object
    form = selection_form(request.form)
    mutable_form = create_new_dict(request.form)
    clean_parameters = clean_search_parameters(mutable_form)

    url_connect = build_uri(clean_parameters)
    print(url_connect)

    data = GraphData(discovery_service.contributor_search(url_connect, "persistence-layer"))
    output_data = data.nodes
    links = data.page_info

    return render_template("./contributor_search/GeneralSearchScreenGQL.html", form=form,
                           records=output_data,
                           header=output_data[0],
                           fields=dict(form.__dict__['_fields']),
                           links=links)


@contributor_search_blueprint.route('/Contributor/GeneralSearch', methods=['GET'])
# Main search screen
def general_search_screen():
    criteria = request.args['criteria'].split(";")
    # Build class for the forms that are passed in, this must be done dynamically
    selection_form = create_form_class(criteria)
    # create form object
    form = selection_form(request.form)
    # On search, and if form object passes validation enter block
    current_page = -1
    last_page = -1


    # if request.method == "POST":
    #
    #     if "nextButton" in request.form:
    #         button_value = request.form['nextButton']
    #         url_connect = button_value.split('/')[-1]
    #         data = discovery_service.contributor_search(url_connect, "persistence-layer")
    #
    #         output_data = json.loads(data)
    #         links = output_data['links']
    #         content = output_data['content']
    #
    #         # Remove individual links key from dictionary as this is blank and not needed on results table
    #         for i in content:
    #             del i['links']
    #
    #         page_info = output_data['page']
    #
    #         total_records = page_info['totalElements']
    #         current_page = page_info['number']
    #         last_page = page_info['totalPages'] - 1
    #         print("Current Page: " + str(current_page))
    #
    #         first_link = build_links(links, 'first')
    #         next_link = build_links(links, 'next')
    #         prev_link = build_links(links, 'prev')
    #         last_link = build_links(links, 'last')
    #
    #         return render_template("./contributor_search/GeneralSearchScreen.html", next_url=next_link, form=form,
    #                                prev_url=prev_link,
    #                                first_url=first_link,
    #                                last_url=last_link,
    #                                total_records=total_records,
    #                                current_page=current_page,
    #                                last_page=last_page,
    #                                records=content,
    #                                header=content[0],
    #                                fields=dict(form.__dict__['_fields']))
    #
    #     if "prevButton" in request.form:
    #         button_value = request.form['prevButton']
    #         url_connect = button_value.split('/')[-1]
    #         data = discovery_service.contributor_search(url_connect, "persistence-layer")
    #
    #         output_data = json.loads(data)
    #         links = output_data['links']
    #         content = output_data['content']
    #
    #         # Remove individual links key from dictionary as this is blank and not needed on results table
    #         for i in content:
    #             del i['links']
    #
    #         page_info = output_data['page']
    #
    #         total_records = page_info['totalElements']
    #         current_page = page_info['number']
    #         last_page = page_info['totalPages'] - 1
    #
    #         print("Current Page: " + str(current_page))
    #
    #         first_link = build_links(links, 'first')
    #         next_link = build_links(links, 'next')
    #         prev_link = build_links(links, 'prev')
    #         last_link = build_links(links, 'last')
    #
    #         return render_template("./contributor_search/GeneralSearchScreen.html", next_url=next_link, form=form,
    #                                prev_url=prev_link,
    #                                first_url=first_link,
    #                                last_url=last_link,
    #                                total_records=total_records,
    #                                current_page=current_page,
    #                                last_page=last_page,
    #                                records=content,
    #                                header=content[0],
    #                                fields=dict(form.__dict__['_fields']))
    #
    #     if "firstButton" in request.form:
    #         button_value = request.form['firstButton']
    #         url_connect = button_value.split('/')[-1]
    #         data = discovery_service.contributor_search(url_connect, "persistence-layer")
    #
    #
    #         output_data = json.loads(data)
    #         links = output_data['links']
    #         content = output_data['content']
    #
    #         # Remove individual links key from dictionary as this is blank and not needed on results table
    #         for i in content:
    #             del i['links']
    #
    #         page_info = output_data['page']
    #
    #         total_records = page_info['totalElements']
    #         current_page = page_info['number']
    #         last_page = page_info['totalPages'] - 1
    #
    #         print("Current Page: " + str(current_page))
    #
    #         first_link = build_links(links, 'first')
    #         next_link = build_links(links, 'next')
    #         prev_link = build_links(links, 'prev')
    #         last_link = build_links(links, 'last')
    #
    #         return render_template("./contributor_search/GeneralSearchScreen.html", next_url=next_link, form=form,
    #                                prev_url=prev_link,
    #                                first_url=first_link,
    #                                last_url=last_link,
    #                                total_records=total_records,
    #                                current_page=current_page,
    #                                last_page=last_page,
    #                                records=content,
    #                                header=content[0],
    #                                fields=dict(form.__dict__['_fields']))
    #
    #     if "lastButton" in request.form:
    #         button_value = request.form['lastButton']
    #         url_connect = button_value.split('/')[-1]
    #         data = discovery_service.contributor_search(url_connect, "persistence-layer")
    #
    #         output_data = json.loads(data)
    #         links = output_data['links']
    #         content = output_data['content']
    #
    #         # Remove individual links key from dictionary as this is blank and not needed on results table
    #         for i in content:
    #             del i['links']
    #
    #         page_info = output_data['page']
    #
    #         total_records = page_info['totalElements']
    #         current_page = page_info['number']
    #         last_page = page_info['totalPages'] - 1
    #         print("Current Page: " + str(current_page))
    #
    #         first_link = build_links(links, 'first')
    #         next_link = build_links(links, 'next')
    #         prev_link = build_links(links, 'prev')
    #         last_link = build_links(links, 'last')
    #
    #         return render_template("./contributor_search/GeneralSearchScreen.html", next_url=next_link, form=form,
    #                                prev_url=prev_link,
    #                                first_url=first_link,
    #                                last_url=last_link,
    #                                total_records=total_records,
    #                                current_page=current_page,
    #                                last_page=last_page,
    #                                records=content,
    #                                header=content[0],
    #                                fields=dict(form.__dict__['_fields']))
    #
    #     # Clean inputs and build URL
    #     mutable_form = create_new_dict(request.form)
    #     clean_parameters = clean_search_parameters(mutable_form)
    #     url_connect = build_uri(clean_parameters)
    #     # Hard coding the sort conditions, to be changed in future
    #     url_connect += "?page=0&size=10&sort=period,asc"
    #
    #     # Make a get request from the built up URL, when the request
    #     # is made, the url is passed over to the Persistence layer
    #
    #     data = discovery_service.contributor_search(url_connect, "persistence-layer")
    #
    # # take the JSON string and turn is into a Python object, the resulting object should be a list of dictionaries
    # # Extracting content and links for pagination
    #     output_data = json.loads(data)
    #     links = output_data['links']
    #     content = output_data['content']
    #
    #     # Remove individual links key from dictionary as this is blank and not needed on results table
    #     for i in content:
    #         del i['links']
    #
    #     page_info = output_data['page']
    #
    #     total_records = page_info['totalElements']
    #     current_page = page_info['number']
    #     last_page = page_info['totalPages'] - 1
    #
    #     print("Current Page: " + str(current_page))
    #
    #
    #     first_link = build_links(links, 'first')
    #     next_link = build_links(links, 'next')
    #     prev_link = build_links(links, 'prev')
    #     last_link = build_links(links, 'last')
    #
    #     print(len(content))
    #
    #     # Check if the python object does not contains the key "error" and if the length of the list is > 0
    #     # This means that there have been no errors and the query returned at least one result
    #     if 'error' not in content and content:
    #         return render_template("./contributor_search/GeneralSearchScreen.html", next_url=next_link, form=form,
    #                                prev_url=prev_link,
    #                                first_url=first_link,
    #                                last_url=last_link,
    #                                total_records=total_records,
    #                                current_page=current_page,
    #                                last_page=last_page,
    #                                records=content,
    #                                header=content[0],
    #                                fields=dict(form.__dict__['_fields']))
    #
    #     # Now check that the object doesn't contain the key "error" and if the length of the list is 0
    #     # This means that there have been no errors and the query returned no results
    #     if 'error' not in content and not content:
    #         current_page = -1
    #         return render_template("./contributor_search/GeneralSearchScreen.html", form=form,
    #                                fields=dict(form.__dict__['_fields']), message="No results found",
    #                                current_page=current_page,
    #                                last_page=last_page,)
    #
    #     # If the two above checks failed, then the query must have returned an error
    #     dummy_list = [content]
    #     return render_template("./contributor_search/GeneralSearchScreen.html", form=form, records=dummy_list,
    #                            fields=dict(form.__dict__['_fields']))

    # before any searches are done, return just the webpage with the search fields.
    return render_template("./contributor_search/GeneralSearchScreen.html",
                           form=form, fields=dict(form.__dict__['_fields']), current_page=current_page,
                           last_page=last_page)
