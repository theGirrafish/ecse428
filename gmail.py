from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import os.path as op

class Gmail:
    def __init__(self, context, timeout):
        self.context = context
        self.timeout = timeout

        self.new_ui = False

        ROOT_DIR = op.dirname(op.abspath(__file__))
        self.images_dir = op.join(ROOT_DIR, 'images')
        self.debug_dir = op.join(ROOT_DIR, 'debug')
        if not op.exists(self.debug_dir):
            os.makedirs(self.debug_dir)

        self.sender = {
            'email': 'sender.ecse428@gmail.com',
            'password': 'Ecse428AssignmentB'
        }
        self.recipientA = {
            'email': 'recipienta.ecse428@gmail.com',
            'password': 'Ecse428AssignmentB'
        }
        self.recipientB = {
            'email': 'recipientb.ecse428@gmail.com',
            'password': 'Ecse428AssignmentB'
        }
        self.invalidRecipient = {
            'email': 'notvalid.1.gmail@com'
        }

        self.login_url = 'https://accounts.google.com/signin/v2/identifier?service=mail&hl=en'
        self.base_url = 'https://mail.google.com/mail/'

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

        wait.until(ec.title_contains(username))

    def log_out(self):
        wait = WebDriverWait(self.context.browser, self.timeout)
        account_btn = self.context.browser.find_element(By.XPATH, '//*[@class="gb_x gb_Da gb_f"]')
        account_btn.click()

        log_out_btn = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@class="gb_0 gb_Vf gb_3f gb_Be gb_gb"]')))
        log_out_btn.click()

        self.context.browser.delete_all_cookies()

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
        return Exception(f'User {user} not defined')

    def compose_email(self):
        wait = WebDriverWait(self.context.browser, self.timeout)
        compose_btn = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@role="button"][text()="Compose"]')))
        compose_btn.click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[text()="New Message"]')))

    def attach_image(self, image_file, expect_failure=False):
        image_path = op.join(self.images_dir, image_file)
        attach = self.context.browser.find_element(By.NAME, 'Filedata')
        attach.send_keys(image_path)

        if not expect_failure:
            wait = WebDriverWait(self.context.browser, self.timeout)
            wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, f'[aria-label*="Attachment: {image_file}"]')))

    def send_email(self, expect_failure=False):
        wait = WebDriverWait(self.context.browser, self.timeout)
        self.context.browser.find_element(By.CSS_SELECTOR, '[role="button"][aria-label~="Send"]').click()
        if not expect_failure:
            wait.until(ec.element_to_be_clickable((By.XPATH, '//*[text()="Message sent."]')))

    def check_email_received(self, recipient, subject):
        emails_table = self.context.browser.find_element(By.XPATH, '//*[@class="F cf zt"]')

        emails = emails_table.find_elements(By.XPATH, '//*[contains(@class,"zA")]')
        for email in emails:
            subject = email.find_element(By.XPATH,  '//*[contains(@class,"bog")]').find_element(By.TAG_NAME, 'span')
            if subject.text == subject:
                return True

    def select_all_and_delete(self, wait, path, title, draft=False):
        search = self.context.browser.find_element(By.CSS_SELECTOR, '[aria-label="Search mail"]')
        search.clear()
        search.send_keys(path)
        search.send_keys(Keys.ENTER)
        wait.until(ec.title_contains(title))
        for elem in self.context.browser.find_elements(By.CSS_SELECTOR, 'div[role="button"][aria-label="Select"] span[role="checkbox"]'):
            if elem.is_displayed():
                elem.click()
                break
        if draft:
            self.context.browser.find_element(By.XPATH, '//*[text()="Discard drafts"]').click()
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[contains(text(),"deleted")]')))
        else:
            for elem in self.context.browser.find_elements(By.CSS_SELECTOR, '[role="button"][aria-label="Delete"]'):
                if elem.is_displayed():
                    elem.click()
                    break
            wait.until(ec.presence_of_element_located((By.XPATH, '//*[contains(text(),"moved to")]')))

    def empty_trash(self, wait):
        search = self.context.browser.find_element(By.CSS_SELECTOR, '[aria-label="Search mail"]')
        search.clear()
        search.send_keys('in:trash')
        search.send_keys(Keys.ENTER)
        wait.until(ec.title_contains('Trash'))
        empty_btn = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@role="button"][contains(text(), "Empty")]')))
        empty_btn.click()
        delete_btn = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '[role="alertdialog"]:not([aria-hidden]) [name="ok"]')))
        delete_btn.click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//*[text()="All messages have been deleted."]')))
