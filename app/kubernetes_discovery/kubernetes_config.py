import os
import json
import requests
from py_eureka_client import eureka_client
import requests_mock
from app.mock_suite import mock_suite
from kubernetes import client, config


class KubernetesConfig:
    def __init__(self, namespace, mocking=False):
        self.mock = mocking
        config.load_incluster_config()
        self.client = client.CoreV1Api()
        self.namespace = namespace

    def contributor_search(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip_addresss = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip_addresss + "/contributor/searchByLikePageable/{}".format(url_connect))
            return output.text

    def contributor_search_without_paging(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip_address = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip_address + "/contributor/search/{}".format(url_connect))
            return output.text

    def form_definition(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/FormDefinition/GetFormDefinition/{}".format(url_connect))

            return output.text

    def form_response(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/Response/QuestionResponse/{}".format(url_connect))
            return output.text

    def update_response(self, url_connect, service_name, data):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/Upsert/CompareResponses/{}".format(url_connect))
            requests.put("http://" + ip + "/Response/QuestionResponse/{}".format(url_connect),
                         data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})
            return output.text

    def get_validation(self, url_connect, service_name):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/validation-pl/validations/return?{}".format(url_connect))
            return output.text

    def update_locked_status(self, url_connect, service_name, data):
        service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
        ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
        requests.put("http://" + ip + "/Update/LockedStatus/{}".format(url_connect),
                     data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})

    def run_validations(self, url_connect, service_name, data):
        if self.mock is False:
            service = self.client.read_namespaced_service(namespace=self.namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.put("http://" + ip + "/validation-bl/run-all/{}".format(url_connect),
                                  data=bytes(json.dumps(data), encoding="utf-8"),
                                  headers={"Content-Type": "Application/Json"})
            return output.text
