# Takeon-Ui Layer

This app is a front-end web interface to view and edit responses of surveys as part of the 'Takeon Legacy Uplift'. It also allows to validate the survey responses based on data driven formula as well as overrideen functionality to override validations.

## Using Gunicorn as web server
This app was initially developed as flask APP. Currently Gunicorn is used as web server both in cluster and local minikube environment. The Gunicorn configs are defined in **gunicorn_config.py** file. For minikube environment **workers** value with 1 gives fast response. In the cluster it is set to 5, considering 2 cores in the node which gives 2\*2+1=5. The formula to set up **workers** is **(2\*CPU Cores +1)**

## Load Testing with selenium
The scripts for load testing with selenium is available in the directory **tests/load_test**. It requires to install chrome driver in the **$HOMEDIR/chromedriver** location. The parameter values like CHROME_DRIVER_LOCATION, UI_URL and REFERENCE are defined in **config_test.py**. Then **concurrency_test.sh** can be run which currently sends upto 18 requests for load testing.