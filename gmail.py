from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import os

timeout = 10
images_dir = './images'
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

    username_field = context.browser.find_element(By.ID, 'identifierId')
    username_field.send_keys(username)

    next_button = context.browser.find_element(By.ID, 'identifierNext')
    next_button.click()

    wait = WebDriverWait(context.browser, timeout)

    password_field = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#password  input')))
    password_field.send_keys(password)

    next_button = context.browser.find_element(By.ID, 'passwordNext')
    next_button.click()

    wait.until(ec.title_contains(username))

def fill_field(context, method, field_path, text):
    field = context.browser.find_element(method, field_path)
    field.send_keys(text)

def get_credentials(user):
    if user == 'recipientA':
        return recipientA
    if user == 'recipientB':
        return recipientB
    if user == 'invalidRecipient':
        return invalidRecipient
    if user == 'Sender':
        return sender
    return Exception('User %s not defined' % user)

def attach_image(context, image_file):
    image_path = os.path.join(images_dir, image_file)
    attach = context.browser.find_element(By.NAME, 'Filedata')
    attach.send_keys(image_path)

    wait = WebDriverWait(context.browser, timeout)
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, '[aria-label*="Attachment: %s"]' % image_file)))

def check_email_received(context, recipient):
    pass

def delete_emails(context):
    pass
