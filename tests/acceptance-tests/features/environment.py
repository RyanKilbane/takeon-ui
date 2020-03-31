from base.selenium_core import SeleniumCore


def before_feature(context, feature):
    context.driver = SeleniumCore.initialize_the_browser(context)


def before_scenario(context, feature):
    SeleniumCore.navigate_to_the_url(context)


# After all the tests we need to close the browser
def after_feature(context, feature):
    context.driver.quit()
