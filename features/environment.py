from behave import fixture, use_fixture
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

@fixture
def browser(context):
    context.browser = webdriver.Chrome(ChromeDriverManager().install())
    yield context.browser
    context.browser.quit()

# Probably don't need all of these
def before_all(context):
    pass

def after_all(context):
    pass

def before_feature(context, feature):
    pass

def after_feature(context, feature):
    pass

def before_scenario(context, scenario):
    use_fixture(browser, context)
    pass

def after_scenario(context, scenario):
    # Should delete all emails sent/received here
    # time.sleep(5)
    pass
