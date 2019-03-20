import os
import json
import requests
from py_eureka_client import eureka_client
import requests_mock
from app.mock_suite import mock_suite


class EurekaConfig:
    def __init__(self, mocking=False):
        self.mock = mocking

    def eureka_client_registration(self, application):
        if self.mock is False:
            eureka_client.init_registry_client(eureka_server="{}/eureka".format(os.environ["localEurekaServerURL"]),
                                               app_name=application.config['APP_NAME'],
                                               instance_port=application.config['PORT'])

            eureka_client.init_discovery_client("{}/eureka".format(os.environ["localEurekaServerURL"]))

    def contributor_search(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()
            data = cli.do_service(application_name="PERSISTENCELAYERAPP",
                                  service="/contributor/searchByLikePageable/{}".format(url_connect), timeout=20)

            return data

        return mock_contributor_search_screen(url_connect=url_connect).text

    def contributor_search_without_paging(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()
            data = cli.do_service(application_name="BusinessLogicLayer",
                                  service="/contributor/search/{}".format(url_connect), timeout=20)

            return data

        return mock_contributor_search(url_connect=url_connect).text

    def form_definition(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()

            question_data = cli.do_service(application_name="BusinessLogicLayer",
                                           service="/FormDefinition/GetFormDefinition/{}".format(url_connect),
                                           timeout=20)

            return question_data

        return mock_form_definition(url_connect=url_connect).text

    def form_response(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()

            response_data = cli.do_service(application_name="PERSISTENCELAYERAPP",
                                           service="/Response/QuestionResponse/{}".format(url_connect),
                                           timeout=40)

            return response_data

        return mock_form_response(url_connect=url_connect).text

    def update_response(self, url_connect, data):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()

            response_data = cli.do_service(application_name="BusinessLogicLayer",
                                           method="PUT",
                                           service="/Upsert/CompareResponses/{}".format(url_connect),
                                           timeout=20, headers={"Content-Type": "Application/Json"},
                                           data=bytes(json.dumps(data), encoding="utf-8"))

            return response_data

        return None

    def get_validation(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()
            print(url_connect)
            response_data = cli.do_service(application_name="VALIDATIONPERSISTENCELAYERAPP",
                                           method="GET",
                                           service="/validation-pl/validations/return?{}".format(url_connect),
                                           timeout=20, headers={"Content-Type": "Application/Json"})

            return response_data

        return mock_get_validation(url_connect=url_connect).text

    @staticmethod
    def update_locked_status(url_connect, data):
        cli = eureka_client.get_discovery_client()

        cli.do_service(application_name="PERSISTENCELAYERAPP",
                       method="PUT",
                       service="/Update/LockedStatus/{}".format(url_connect),
                       timeout=20, headers={"Content-Type": "Application/Json"},
                       data=bytes(json.dumps(data), encoding="utf-8"))

    def run_validations(self, url_connect):
        if self.mock is False:
            cli = eureka_client.get_discovery_client()
            validation_data = cli.do_service(application_name="BusinessLogicLayer",
                                             method="GET",
                                             service="/validation-bl/run-all/{}".format(url_connect),
                                             timeout=20, headers={"Content-Type": "Application/Json"})

            return validation_data

        return None


@requests_mock.Mocker()
def mock_form_definition(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_form_definition.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)


@requests_mock.Mocker()
def mock_contributor_search(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_contributor_search.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)

@requests_mock.Mocker()
def mock_contributor_search_screen(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_contributor_search_screen.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)


@requests_mock.Mocker()
def mock_form_response(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_form_response.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)


@requests_mock.Mocker()
def mock_get_validation(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_validation_outputs.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)
