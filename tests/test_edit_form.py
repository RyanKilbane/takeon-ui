from app.forms.edit_form import extract_responses

def test__extract_responses__valid_input__valid_output():
    input_data = {'q900':'123', 'q901':'456', 'action':'saveForm'}
    expected = [{'question':'q900', 'response':'123', 'instance': 0}, {'question':'q901', 'response':'456', 'instance': 0}]
    output = extract_responses(input_data)
    assert expected == output
