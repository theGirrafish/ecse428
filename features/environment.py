from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

DEBUG = True

@fixture
def browser(context):
    options = Options()
    if not DEBUG:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
    context.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
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
