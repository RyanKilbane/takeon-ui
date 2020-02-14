# Config file to set up UI_URL, REFERENCE
# It assumes that chromedriver is already installed in $HOMEDIR/chromedriver
# After setting the variables run concurrent_test.sh

import os.path
HOMEDIR = os.path.expanduser("~")
CHROME_DRIVER_LOCATION = HOMEDIR + '/chromedriver'
UI_URL = 'http://a441d17a3499511ea9c2e0a5091216e0-e21bbc0eb23ae5b5.elb.eu-west-2.amazonaws.com:5001'
REFERENCE = '49900002387'