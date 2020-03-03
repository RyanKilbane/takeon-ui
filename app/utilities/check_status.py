def check_status(status):
    status_code = {
        'No form sent'          : 'status status--dead',
        'Form Sent Out'         : 'status status--info',
        'Saved - run validation': 'status status--error',
        'Check Needed'          : 'status status--error',
        'Clear'                 : 'status status--success',
        'Clear - Overridden'    : 'status status--success'
    }
    return status_code.get(status, 'status status--info')
