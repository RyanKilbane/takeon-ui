import os


class MockSuite:
    def __init__(self, data_filename):
        '''
        :param data_filename: The name of the flat file that contains the needed data, with file extension.
        '''
        self.path_to_data = None
        self.data = None
        self.data_filename = data_filename

    def get_data(self):
        self.build_path()
        with open(self.path_to_data) as file:
            self.data = file.read()
        return self.data

    def build_path(self):
        current_directory = os.path.dirname(__file__)
        self.path_to_data = os.path.join(current_directory, "dummy_data", self.data_filename)
