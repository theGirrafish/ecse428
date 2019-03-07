from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time

from gmail import delete_emails

@fixture
def browser(context):
    options = ChromeOptions()
    # options = FirefoxOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    # options.add_argument('--headless')
    context.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    # context.browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=options)
    yield context.browser
    context.browser.quit()

def before_scenario(context, scenario):
    use_fixture(browser, context)

def after_scenario(context, scenario):
    delete_emails(context)

# def after_step(context, step):
#     time.sleep(5)
