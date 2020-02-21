# Combine Response and Validation data for new UI Layout

def combine_response_validations(view_form_data, validations):
    combined_array = []
    for i in view_form_data['view_form_responses']:
        overridden_count = 0
        combined_output = {}
        validation_info_array = []
        qcode = i['questioncode']
        response = i['response']
        combined_output['questioncode'] = qcode
        combined_output['response'] = response
        combined_output['displayquestionnumber'] = i['displayquestionnumber']
        combined_output['displaytext'] = i['displaytext']
        for j in validations['validation_outputs']:
            validation_failure = {}
            if j['primaryquestion'] == qcode:
                validation_failure['name'] = j['name']
                validation_failure['overridden'] = j['overridden']
                validation_failure['validationoutputid'] = j['validationoutputid']
                validation_failure['triggered'] = j['triggered']
                if j['overridden'] == True:
                    overridden_count += 1
                validation_info_array.append(validation_failure)
            if overridden_count == len(validation_info_array):
                combined_output['panel'] = 'panel--info'
            else:
                combined_output['panel'] = 'panel--error'
        combined_output['validation_info'] = validation_info_array
        combined_array.append(combined_output)
    combined_dictionary_output = {}

    combined_dictionary_output['form_validation_outputs'] = combined_array
    return combined_dictionary_output
