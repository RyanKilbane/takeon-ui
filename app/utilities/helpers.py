from os import getlogin
from collections import OrderedDict
from socket import timeout
from urllib.error import URLError
from flask import render_template
from wtforms import StringField, Form  # validators <-- Re-add when/if validation is required



# ###################################### UTILITY FUNCTIONS ###########################################
# Create class for forms dynamically
def create_form_class(iterable):
    var_dict = {}
    for variable_name in iterable:
        print("adding {} to dict".format(variable_name))
        # var_dict[variable_name] = StringField("{}".format(variable_name), [validators.DataRequired()])
        var_dict[variable_name] = StringField("{}".format(variable_name))
    class_output = type("SearchSelect", (Form,), var_dict)
    # At this point we have a class that analogous to SearchForm
    return class_output


# To clean inputs, we need to create a mutable dictionary
def create_new_dict(url_paramaters):
    mutable_dict = {}
    for key in url_paramaters.keys():
        mutable_dict[key] = url_paramaters[key]
    return mutable_dict


# Remove arbitary spaces from the inputs
def clean_search_parameters(url_parameters):
    for key in url_parameters.keys():
        url_parameters[key] = url_parameters[key].replace(" ", "")
    return url_parameters


# Build the URI to connect to the business layer. The strings that are appended to the
# urlConnect string are search parameters, of the form PARAMETER=VALUE;
def build_uri(url_parameters):
    """
    :param url_parameters: dictionary
    :return: String
    Takes a dict and constructs the URL to the business layer
    """
    url_connect = ""
    for keys in url_parameters.keys():
        if url_parameters[keys] == "":
            continue
        url_connect += "{}={};".format(keys, url_parameters[keys])
    url_connect = url_connect[:-1]
    return url_connect


def build_uri_2(url_parameters):
    """
    :param url_parameters: dictionary
    :return: String
    Takes a dict and constructs the URL to the business layer
    """
    url_connect = ""
    for keys in url_parameters.keys():
        if url_parameters[keys] == "":
            continue
        url_connect += "{}={}&".format(keys, url_parameters[keys])
    url_connect = url_connect[:-1]
    return url_connect


# Takes a string which should be either True or False and returns the bool value or ValueError
def str_to_bool(string_to_convert):
    """

    :param string_to_convert: String
    :return: boolean
    Takes a string which should be either True or False and returns the bool value or ValueError
    """
    if string_to_convert == 'True':
        return True
    if string_to_convert == 'False':
        return False
    raise ValueError


def decompose_data(data: dict) -> dict:
    """
    :param data: Dictionary of the form {"qCode:Number|inst:Number":"Response"}
    :return: Dictionary of the form {Updated Responses: {qCode: {instance: Responce}}}
    """

    data_atoms = []
    # Create tuple to hold data atoms
    for key in sorted(data.keys()):
        if key == "action":
            continue
        # data_atoms.append((hold_data[0], hold_data[1], data[key]))

        data_atoms.append({key: data[key]})

    print("Output data: " + str(data_atoms))
    return {"Updated Responses": data_atoms}


def build_json(data):
    data_atoms = []
    data = OrderedDict(data)
    # print(data)
    for key in data.keys():
        data_atoms.append({form_key: data[key].get(form_key) for form_key in data[key].keys()})
        data_atoms[-1]["questionCode"] = key
    return data_atoms


def get_user():
    # For the moment, this just returns getLogin(), in the future this will get a cookie from the browser
    return "fisdba"


def forms_connect_to_eureka(url):
    from app.setup import discovery_service
    # This was moved here because it's used in a couple of different forms
    try:
        return discovery_service.form_definition(url), \
               discovery_service.contributor_search_without_paging(url), \
               discovery_service.form_response(url)
    except URLError as error:
        return render_template("UrlNotFoundError.html", error_message=error)

    except timeout as error:
        return render_template("TimeOutError.html", error_message=error)


def forms_connect_to_eureka_validation(url):
    from app.setup import discovery_service
    # This was moved here because it's used in a couple of different forms
    try:
        return discovery_service.get_validation(url)
    except URLError as error:
        return render_template("UrlNotFoundError.html", error_message=error)

    except timeout as error:
        return render_template("TimeOutError.html", error_message=error)


def build_links(links_list, name_of_link):
    """

    :param links_list: List, name_of_link: String
    :return: String
    Takes a list of links which and returns the correct one depending on parameter
    """
    extracted_link = ''
    for link in links_list:
        if link['rel'] == name_of_link:
            extracted_link = link['href']
    return extracted_link
