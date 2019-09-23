import json
from app.utilities.helpers import find_nodes


class GraphData:
    def __init__(self, data):
        self.data = self.load_data(data)
        self.nodes = find_nodes(self.data, "data")
        self.page_info = find_nodes(self.data, "pageInfo")
        # self.edges = find_nodes(self.data, "edges")

    @staticmethod
    def load_data(data):
        try:
            return json.loads(data)
        except Exception as error:
            return error
