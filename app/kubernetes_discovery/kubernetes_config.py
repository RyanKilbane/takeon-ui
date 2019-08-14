import os
import json
import requests
from py_eureka_client import eureka_client
from flask import flash, Flask
import requests_mock
from app.mock_suite import mock_suite
from kubernetes import client, config

import hashlib


class KubernetesConfig:
    def __init__(self, namespace, mocking=True):
        self.mock = mocking
        if not self.mock:
            config.load_incluster_config()
            self.client = client.CoreV1Api()
            self.namespace = namespace

    def contributor_search(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip_addresss = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip_addresss + "/contributor/searchByLikePageable/{}".format(url_connect))
            return output.text
        print("Mocking search screen "+str(url_connect))
        return mock_contributor_search_screen(url_connect=url_connect).text
        # return mock_contributor_search_screen_no_error(url_connect=url_connect).text
        # return mock_contributor_search_screen_error_blank(url_connect=url_connect).text
        # return mock_contributor_search_screen_error_populated(url_connect=url_connect).text

    def contributor_search_without_paging(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip_address = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip_address + "/contributor/search/{}".format(url_connect))
            return output.text
        
        return mock_contributor_search(url_connect=url_connect).text

    def form_definition(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/FormDefinition/GetFormDefinition/{}".format(url_connect))

            return output.text
        
        return mock_form_definition(url_connect=url_connect).text

    def form_response(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/Response/QuestionResponse/{}".format(url_connect))
            return output.text

        return mock_form_response(url_connect=url_connect).text

    def update_response(self, url_connect, service_name, data):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            # output = requests.get("http://" + ip + "/Upsert/CompareResponses/{}".format(url_connect))
            requests.put("http://" + ip + "/Upsert/CompareResponses/{}".format(url_connect),
                         data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})
            # return output.text

        return None

    def get_validation(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/validation-pl/validations/return?{}".format(url_connect))
            return output.text

        return mock_get_validation(url_connect=url_connect).text

    def update_locked_status(self, url_connect, service_name, data):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            requests.put("http://" + ip + "/Update/LockedStatus/{}".format(url_connect),
                        data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})
        return None

    def run_validations(self, url_connect, service_name, data):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.put("http://" + ip + "/validation-bl/run-all/{}".format(url_connect),
                                  data=bytes(json.dumps(data), encoding="utf-8"),
                                  headers={"Content-Type": "Application/Json"})
            return output.text

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
    hash_value = hashlib.md5(url_connect.encode()).hexdigest()
   
    mocked_up_data = mock_suite.MockSuite("BDD/"+hash_value+".json").get_data()
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


@requests_mock.Mocker()
def mock_contributor_search_no_error(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_validation_outputs.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)


@requests_mock.Mocker()
def mock_contributor_search_error_blank(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_validation_outputs.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)


@requests_mock.Mocker()
def mock_contributor_search_error_populated(mock=None, url_connect=None):
    mocked_up_data = mock_suite.MockSuite("mock_validation_outputs.json").get_data()
    url = "http://localhost:8090/" + url_connect
    mock.get(url, text=mocked_up_data)
    return requests.get(url)
