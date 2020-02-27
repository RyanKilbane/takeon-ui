from app.utilities.combine_response_validations import combine_response_validations

form_response_output = {"view_form_responses": [{"displaytext": "Comment on the figures included in your return", "instance": 0, "response": "2", "questioncode": "0146", "displayquestionnumber": "Q146", "type": "NUMERIC"}, 
{"displaytext": "New pits or quarries brought into use since date of last return", "instance": 0, "response": "1", "questioncode": "0147", "displayquestionnumber": "Q147", "type": "NUMERIC"}, 
{"displaytext": "Sand produced for asphalt (asphalting sand)", "instance": 0, "response": "4325", "questioncode": "0601", "displayquestionnumber": "Q601", "type": "NUMERIC"}, 
{"displaytext": "Sand produced for use in mortar (building or soft sand)", "instance": 0, "response": "234", "questioncode": "0602", "displayquestionnumber": "Q602", "type": "NUMERIC"}, 
{"displaytext": "Sand produced for concreting (sharp sand)", "instance": 0, "response": "5432", "questioncode": "0603", "displayquestionnumber": "Q603", "type": "NUMERIC"}, 
{"displaytext": "Gravel coated with bituminous binder (on or off site)", "instance": 0, "response": "324", "questioncode": "0604", "displayquestionnumber": "Q604", "type": "NUMERIC"}, 
{"displaytext": "Gravel produced for concrete aggregate (including sand/gravel mixes)", "instance": 0, "response": "3542", "questioncode": "0605", "displayquestionnumber": "Q605", "type": "NUMERIC"}, 
{"displaytext": "Other screened and graded gravels", "instance": 0, "response": "5600", "questioncode": "0606", "displayquestionnumber": "Q606", "type": "NUMERIC"}, 
{"displaytext": "Sand and gravel used for constructional fill", "instance": 0, "response": "543", "questioncode": "0607", "displayquestionnumber": "Q607", "type": "NUMERIC"}, 
{"displaytext": "TOTALS", "instance": 0, "response": "4352543", "questioncode": "0608", "displayquestionnumber": "Q608", "type": "NUMERIC"}, 
{"displaytext": "Derived Total of all sand and gravel (Q601 + Q602 + Q603 + Q604 + Q605 + Q606 + Q607)", "instance": 0, "response": "20000", "questioncode": "9001", "displayquestionnumber": "Q9001", "type": "NUMERIC"}]}

validation_output = {"validation_outputs": [{"severity": "E", "primaryquestion": "0601", "triggered": True, "instance": "0", "validationoutputid": 1490, "validationid": 6620, "lastupdateddate": "2020-02-19T10:21:57.354+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "4325 != 0 AND ( 4325 = 0 OR 0 = 0 ) AND abs(4325 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0602", "triggered": True, "instance": "0", "validationoutputid": 1491, "validationid": 6621, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "234 != 0 AND ( 234 = 0 OR 0 = 0 ) AND abs(234 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0603", "triggered": True, "instance": "0", "validationoutputid": 1492, "validationid": 6622, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "5432 != 0 AND ( 5432 = 0 OR 0 = 0 ) AND abs(5432 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0604", "triggered": True, "instance": "0", "validationoutputid": 1493, "validationid": 6623, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "324 != 0 AND ( 324 = 0 OR 0 = 0 ) AND abs(324 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0605", "triggered": True, "instance": "0", "validationoutputid": 1494, "validationid": 6624, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "3542 != 0 AND ( 3542 = 0 OR 0 = 0 ) AND abs(3542 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0606", "triggered": True, "instance": "0", "validationoutputid": 1495, "validationid": 6625, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "5600 != 0 AND ( 5600 = 0 OR 0 = 0 ) AND abs(5600 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0607", "triggered": True, "instance": "0", "validationoutputid": 1496, "validationid": 6626, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Period on Period Zero Continuity", "formula": "543 != 0 AND ( 543 = 0 OR 0 = 0 ) AND abs(543 - 0) > 0", "rule": "POPZC", "overridden": False}, 
{"severity": "E", "primaryquestion": "0146", "triggered": True, "instance": "0", "validationoutputid": 1497, "validationid": 6630, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Comment Present (BMI)", "formula": "2 = 2", "rule": "CPBMI", "overridden": False}, 
{"severity": "W", "primaryquestion": "0608", "triggered": True, "instance": "0", "validationoutputid": 1499, "validationid": 6650, "lastupdateddate": "2020-02-19T11:52:05.462+00:00", "lastupdatedby": "fisdba", "name": "Question vs Derived Question", "formula": "4352543 != 20000", "rule": "QVDQ", "overridden": False}]}

def test_valid_input_returns_valid_combined_output():
    expected_output = {"form_validation_outputs": [{"questioncode": "0146", "response": "2", "panel": "panel--info", "validation_info": [{"name": "Comment Present (BMI)", "overridden": False}]}, 
    {"questioncode": "0147", "response": "1", "panel": "panel--info", "validation_info": []}, 
    {"questioncode": "0601", "response": "4325", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0602", "response": "234", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0603", "response": "5432", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0604", "response": "324", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0605", "response": "3542", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0606", "response": "5600", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0607", "response": "543", "panel": "panel--info", "validation_info": [{"name": "Period on Period Zero Continuity", "overridden": False}]}, 
    {"questioncode": "0608", "response": "4352543", "panel": "panel--info", "validation_info": [{"name": "Question vs Derived Question", "overridden": False}]}, 
    {"questioncode": "9001", "response": "20000", "panel": "panel--info", "validation_info": []}]}
    assert combine_response_validations(form_response_output, validation_output) == expected_output
