# Combine Question Form Response and Validation data

class combine_data:

    def __init__(self, form_data, validation_data):
        self.form_data = form_data
        self.validation_data = form_data

    def extract_question_data(self, index):
        question_data = {}
        qcode = self.form_data[index]['questioncode']
        response = self.form_data[index]['response']
        question_data['questioncode'] = qcode
        question_data['response'] = response
        question_data['displayquestionnumber'] = self.form_data[index]['displayquestionnumber']
        question_data['displaytext'] = self.form_data[index]['displaytext']
        return question_data

    def extract_validation_data(self, extracted_form_data, validation_data):
        validation_info_array = []
        overridden_count = 0
        for validation in validation_data['validation_outputs']:
            validation_failure = {}
            if validation['primaryquestion'] == self.extracted_form_data['questioncode']:
                validation_failure['name'] = validation['name']
                validation_failure['overridden'] = validation['overridden']
                validation_failure['validationoutputid'] = validation['validationoutputid']
                validation_failure['triggered'] = validation['triggered']
                validation_failure['validationmessage'] = validation['validationmessage']
                if validation['overridden']:
                    overridden_count += 1
                validation_info_array.append(validation_failure)
        validation_failure['overriden_count'] = overridden_count
        return validation_info_array

    def decide_panel_colour(self, overridden_count, validation_info_array):
        if overridden_count == len(validation_info_array):
            panel = 'panel--info'
        else:
            panel = 'panel--error'
        return panel

    def combine_data():
        combined_array = []
        formObj = 


    
