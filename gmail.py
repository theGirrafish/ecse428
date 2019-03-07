from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import os

class Gmail:
    def __init__(self, context, timeout):
        self.context = context
        self.timeout = timeout

        self.new_ui = False

        self.images_dir = os.path.join(os.getcwd(), 'images')
        self.debug_dir = os.path.join(os.getcwd(), 'debug')
        if not os.path.exists(self.debug_dir):
            os.makedirs(self.debug_dir)
            
        self.sender = {'email': 'sender.ecse428@gmail.com',
                'password': 'Ecse428AssignmentB'}
        self.recipientA = {'email': 'recipienta.ecse428@gmail.com',
                    'password': 'Ecse428AssignmentB'}
        self.recipientB = {'email': 'recipientb.ecse428@gmail.com',
                    'password': 'Ecse428AssignmentB'}
        self.invalidRecipient = {'email': 'notvalid.1.gmail@com'}

        self.login_url = 'https://www.gmail.com'
        self.inbox_url = 'https://mail.google.com/mail/#inbox'

    def log_in(self, username, password):
        self.context.browser.get(self.login_url)

        wait = WebDriverWait(self.context.browser, self.timeout)

        # Check if we are given the new signin form
        if 'https://accounts.google.com/signin/v2/identifier?' in self.context.browser.current_url:
            self.new_ui = True

            self.context.browser.find_element(By.ID, 'identifierId').send_keys(username)

            self.context.browser.find_element(By.ID, 'identifierNext').click()

            password_field = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#password  input')))
            password_field.send_keys(password)

            self.context.browser.find_element(By.ID, 'passwordNext').click()
        else:
            self.context.browser.find_element(By.ID, 'Email').send_keys(username)
            self.context.browser.find_element(By.NAME, 'signIn').click()

            password_field = wait.until(ec.element_to_be_clickable((By.ID, 'Passwd')))
            password_field.send_keys(password)

            self.context.browser.find_element(By.ID, 'signIn').click()

        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[title="Inbox"]')))

    def fill_field(self, method, field_path, text):
        field = self.context.browser.find_element(method, field_path)
        field.send_keys(text)

    def get_credentials(self, user):
        if user == 'recipientA':
            return self.recipientA
        if user == 'recipientB':
            return self.recipientB
        if user == 'invalidRecipient':
            return self.invalidRecipient
        if user == 'Sender':
            return self.sender
        return Exception('User %s not defined' % user)

    def compose_email(self):
        self.context.browser.find_element(By.XPATH, '//*[@role="button"][text()="Compose"]').click()
        wait = WebDriverWait(self.context.browser, self.timeout)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[text()="New Message"]')))

    def attach_image(self, image_file, expect_failure=False):
        image_path = os.path.join(self.images_dir, image_file)
        attach = self.context.browser.find_element(By.NAME, 'Filedata')
        attach.send_keys(image_path)

        if not expect_failure:
            wait = WebDriverWait(self.context.browser, self.timeout)
            wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label*="Attachment: %s"]' % image_file)))

    def send_email(self, expect_failure=False):
        wait = WebDriverWait(self.context.browser, self.timeout)
        self.context.browser.find_element(By.CSS_SELECTOR, '[role="button"][aria-label~="Send"]').click()
        if not expect_failure:
            # wait.until(ec.element_to_be_clickable((By.ID, 'link_undo')))
            wait.until(ec.element_to_be_clickable((By.XPATH, '//*[text()="Message sent."]')))

    def check_email_received(self, recipient):
        pass

    def delete_emails(self):
        pass
