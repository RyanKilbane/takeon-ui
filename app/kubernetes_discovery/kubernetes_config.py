import os
import json
import requests
from py_eureka_client import eureka_client
import requests_mock
from app.mock_suite import mock_suite
from kubernetes import client, config


class KubernetesConfig:
    def __init__(self, mocking=False):
        self.mock = mocking

    def contributor_search(self, url_connect):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "persistence-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/contributor/searchByLikePageable/{}".format(url_connect))
            return output.text

    def contributor_search_without_paging(self, url_connect):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "business-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/contributor/search/{}".format(url_connect))
            return output.text

    def form_definition(self, url_connect):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "business-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/FormDefinition/GetFormDefinition/{}".format(url_connect))

            return output.text

    def form_response(self, url_connect):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "persistence-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/Response/QuestionResponse/{}".format(url_connect))
            return output.text

    def update_response(self, url_connect, data):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "persistence-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/Upsert/CompareResponses/{}".format(url_connect))
            requests.put("http://" + ip + "/Response/QuestionResponse/{}".format(url_connect),
                         data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})
            return output.text

    def get_validation(self, url_connect):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "validation-persistence-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.get("http://" + ip + "/validation-pl/validations/return?{}".format(url_connect))
            return output.text

    @staticmethod
    def update_locked_status(url_connect, data):
        config.load_incluster_config()
        service_name = "persistence-layer"
        namespace = "default"
        v1 = client.CoreV1Api()
        service = v1.read_namespaced_service(namespace=namespace, name=service_name)
        ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
        requests.put("http://" + ip + "/Update/LockedStatus/{}".format(url_connect),
                     data=bytes(json.dumps(data), encoding="utf-8"), headers={"Content-Type": "Application/Json"})

    def run_validations(self, url_connect, data):
        if self.mock is False:
            config.load_incluster_config()
            service_name = "business-layer"
            namespace = "default"
            v1 = client.CoreV1Api()
            service = v1.read_namespaced_service(namespace=namespace, name=service_name)
            ip = service.spec.cluster_ip + ":" + str(service.spec.ports[0].port)
            output = requests.put("http://" + ip + "/validation-bl/run-all/{}".format(url_connect),
                                  data=bytes(json.dumps(data), encoding="utf-8"),
                                  headers={"Content-Type": "Application/Json"})
            return output.text
