"""
Module containing common function used in several tests-tests.
Functions that are not test or feature specific.
"""
from selenium import webdriver

from configfiles.config_test import CHROME_DRIVER_LOCATION
from configfiles.urlconfig import URL_CONFIG


class SeleniumCore:

    def initialize_the_browser(context, browser_type=None):
        """
        Function to start instance of the specified browser and navigate to the specified url.

        :param url: the url to navigate to
        :param browser_type: the type of browser to start (Default is Firefox)

        :return: driver: browser instance
        """
        if not browser_type:
            # create instance of the Chrome driver
            context.driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
        elif browser_type.lower() == 'firefox':
            # create instance of Firefox driver the browser type is not specified
            context.driver = webdriver.Firefox()
        else:
            raise Exception("The browser type '{}' is not supported".format(browser_type))

        # clean the url and go to the url
        # url = URL_CONFIG.get('env_url').strip()
        # context.driver.get(url)
        # context.driver.implicitly_wait(2)
        return context.driver

    def navigate_to_the_url(context):
        url = URL_CONFIG.get('env_url').strip()
        context.driver.get(url)
        context.driver.implicitly_wait(2)
