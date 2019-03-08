from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

from gmail import Gmail

DEBUG = True
HEADLESS = False

@fixture
def browser(context):
    options = ChromeOptions()
    # options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    if HEADLESS:
        options.add_argument('--headless')
        if DEBUG:
            options.add_argument('--remote-debugging-port=9222')
    context.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)
    yield context.browser
    context.browser.quit()

def before_all(context):
    context.gmail = Gmail(context, timeout=30)

def after_all(context):
    use_fixture(browser, context)
    delete_emails(context)

def before_scenario(context, scenario):
    use_fixture(browser, context)

def after_step(context, step):
    if DEBUG and step.status == 'failed':
        step_name = step.name.replace(' ', '_')
        image_name = os.path.join(context.gmail.debug_dir, f'{step.step_type}_{step_name}.png')
        context.browser.save_screenshot(image_name)

def delete_emails(context):
    # Delete sender emails
    use_fixture(browser, context)
    wait = WebDriverWait(context.browser, context.gmail.timeout)

    context.gmail.log_in(context.gmail.sender['email'], context.gmail.sender['password'])

    context.gmail.context.browser.get(context.gmail.base_url + '#sent')
    wait.until(ec.title_contains('Sent'))
    context.gmail.select_all_and_delete(wait)

    context.gmail.empty_trash(wait)

    # Delete recipientA emails
    use_fixture(browser, context)
    wait = WebDriverWait(context.browser, context.gmail.timeout)

    context.gmail.log_in(context.gmail.recipientA['email'], context.gmail.recipientA['password'])

    context.gmail.context.browser.get(context.gmail.base_url + '#inbox')
    wait.until(ec.title_contains('Inbox'))
    context.gmail.select_all_and_delete(wait)

    context.gmail.empty_trash(wait)

    # Delete recipientB emails
    use_fixture(browser, context)
    wait = WebDriverWait(context.browser, context.gmail.timeout)

    context.gmail.log_in(context.gmail.recipientB['email'], context.gmail.recipientB['password'])

    context.gmail.context.browser.get(context.gmail.base_url + '#inbox')
    wait.until(ec.title_contains('Inbox'))
    context.gmail.select_all_and_delete(wait)

    context.gmail.empty_trash(wait)
