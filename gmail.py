from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

timeout = 10
sender = {'email': 'sender.ecse428@gmail.com',
          'password': 'Ecse428AssignmentB'}
recipientA = {'email': 'recipienta.ecse428@gmail.com',
              'password': 'Ecse428AssignmentB'}
recipientB = {'email': 'recipientb.ecse428@gmail.com',
              'password': 'Ecse428AssignmentB'}
invalidRecipient = {'email': 'notvalid.1.gmail@com'}

login_url = 'https://accounts.google.com/AccountChooser?service=mail&continue=https://mail.google.com/mail/'
inbox_url = 'https://mail.google.com/mail/#inbox'


def log_in(context, username, password):
    context.browser.get(login_url)

    username_field = context.browser.find_element_by_id('identifierId')
    username_field.send_keys(username)

    next_button = context.browser.find_element_by_id('identifierNext')
    next_button.click()

    wait = WebDriverWait(context.browser, timeout)

    password_field = wait.until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#password  input')))
    password_field.send_keys(password)

    next_button = context.browser.find_element_by_id('passwordNext')
    next_button.click()

    wait.until(ec.title_contains(username))
