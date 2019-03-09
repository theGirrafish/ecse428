from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from retrying import retry
import os
import os.path as op

from locators import LoginLocators, LogoutLocators, ComposeEmailLocators, PageLocators, AlertLocators

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

        self.body = ""

        self.login_url = 'https://accounts.google.com/signin/v2/identifier?service=mail&hl=en'
        self.base_url = 'https://mail.google.com/mail/'

    def log_in(self, username, password):
        self.context.browser.get(self.login_url)

        wait = WebDriverWait(self.context.browser, self.timeout)

        # Check if we are given the new signin form
        if 'https://accounts.google.com/signin/v2/identifier?' in self.context.browser.current_url:
            self.new_ui = True

            self.context.browser.find_element(*LoginLocators.USER_V1).send_keys(username)

            self.context.browser.find_element(*LoginLocators.NEXT_V1).click()

            password_field = wait.until(ec.element_to_be_clickable(LoginLocators.PASSWORD_V1))
            password_field.send_keys(password)

            self.context.browser.find_element(*LoginLocators.LOGIN_V1).click()
        else:
            self.context.browser.find_element(*LoginLocators.USER_V2).send_keys(username)
            self.context.browser.find_element(*LoginLocators.NEXT_V2).click()

            password_field = wait.until(ec.element_to_be_clickable(LoginLocators.PASSWORD_V2))
            password_field.send_keys(password)

            self.context.browser.find_element(*LoginLocators.LOGIN_V2).click()

        wait.until(ec.title_contains(username))

    def log_out(self):
        wait = WebDriverWait(self.context.browser, self.timeout)
        account_btn = self.context.browser.find_element(*LogoutLocators.ACCOUNT)
        account_btn.click()

        log_out_btn = wait.until(ec.element_to_be_clickable(LogoutLocators.LOGOUT))
        log_out_btn.click()

        self.context.browser.delete_all_cookies()

    def fill_field(self, locator, text):
        field = self.context.browser.find_element(*locator)
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
        raise Exception(f'User {user} not defined')

    def compose_email(self):
        wait = WebDriverWait(self.context.browser, self.timeout)
        compose_btn = wait.until(ec.element_to_be_clickable(ComposeEmailLocators.COMPOSE))
        compose_btn.click()
        wait.until(ec.element_to_be_clickable(ComposeEmailLocators.HEADER))

    def attach_image(self, image_file, expect_failure=False):
        image_path = op.join(self.images_dir, image_file)
        attach = self.context.browser.find_element(*ComposeEmailLocators.ATTACH_PATH)
        attach.send_keys(image_path)

        if not expect_failure:
            wait = WebDriverWait(self.context.browser, self.timeout)
            wait.until(ec.element_to_be_clickable(ComposeEmailLocators.get_attachment_field(image_file)))

    def send_email(self, expect_failure=False, share_prompt=False):
        wait = WebDriverWait(self.context.browser, self.timeout)
        try:
            self.context.browser.find_element(*ComposeEmailLocators.SEND).click()
        except TimeoutException:
            return False
        if share_prompt:
            try:
                share_dialog = wait.until(ec.presence_of_element_located(AlertLocators.DIALOG_SHARE))
                send_btn = share_dialog.find_element(By.XPATH, '//*[text()="Send"]')
                send_btn.click()
                # self.context.browser.execute_script('arguments[0].click();', send_btn)
                wait.until_not(ec.element_to_be_clickable(AlertLocators.DIALOG_SHARE))
            except TimeoutException:
                return False
        if not expect_failure:
            try:
                wait.until(ec.element_to_be_clickable(ComposeEmailLocators.SENT_PROMPT))
            except TimeoutException:
                return False
        return False

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
    def check_email_received(self, subject):
        emails_table = self.context.browser.find_element(*PageLocators.EMAIL_TABLE)

        emails = emails_table.find_elements(*PageLocators.EMAIL_IN_TABLE)
        if len(emails) == 0:
            raise Exception("No emails in inbox")
        for email in emails:
            subject_span = email.find_element(*PageLocators.SUBJECT).find_element(By.TAG_NAME, 'span')
            if subject_span.text == subject:
                return True
            else:
                raise Exception("No email found with matching subject")

    def check_email_sender(self, subject):
        emails_table = self.context.browser.find_element(*PageLocators.EMAIL_TABLE)

        emails = emails_table.find_elements(*PageLocators.EMAIL_IN_TABLE)
        for email in emails:
            subject_span = email.find_element(*PageLocators.SUBJECT).find_element(By.TAG_NAME, 'span')
            if subject_span.text == subject:
                sender_span = email.find_element(*PageLocators.SENDER).find_element(By.XPATH, './/*[@class="zF"]')
                if sender_span.get_attribute('email') == self.sender['email']:
                    return True
        return False

    def check_email_body(self, subject, text):
        emails_table = self.context.browser.find_element(*PageLocators.EMAIL_TABLE)

        emails = emails_table.find_elements(*PageLocators.EMAIL_IN_TABLE)
        for email in emails:
            subject_span = email.find_element(*PageLocators.SUBJECT).find_element(By.TAG_NAME, 'span')
            if subject_span.text == subject:
                body_span = email.find_element(*PageLocators.BODY)
                text = text.replace('\n', '').replace(' ', '')
                body_text = body_span.text
                body_text = body_text.strip().replace('\n', '').replace(' ', '').replace('-', '')
                if body_text == text:
                    return True
        return False

    def check_email_attachment(self, subject, image):
        emails_table = self.context.browser.find_element(*PageLocators.EMAIL_TABLE)

        emails = emails_table.find_elements(*PageLocators.EMAIL_IN_TABLE)
        for email in emails:
            subject_span = email.find_element(*PageLocators.SUBJECT).find_element(By.TAG_NAME, 'span')
            if subject_span.text == subject:
                attachments_span = email.find_elements(*PageLocators.ATTACHMENT)
                for attachment in attachments_span:
                    if attachment.text == image:
                        return True
        return False

    def upload_to_drive(self):
        wait = WebDriverWait(self.context.browser, self.timeout)
        attachment_alert = self.context.browser.find_elements(*AlertLocators.ALERT)
        if len(attachment_alert) != 0:
            alert_text = attachment_alert[0].find_element(By.CSS_SELECTOR, 'span[role="heading"]')

            if 'Large files must be shared with Google Drive' in alert_text.text:
                attachment_alert[0].find_element(By.CSS_SELECTOR, 'button[name="ok"]').click()
                wait.until_not(ec.presence_of_element_located(AlertLocators.ALERT))

        attachment_dialog = wait.until(ec.presence_of_element_located(AlertLocators.DIALOG_UPLOAD))
        if 'Attaching File' not in attachment_dialog.text:
            return False
        try:
            wait.until_not(ec.presence_of_element_located(AlertLocators.DIALOG_UPLOAD))
        except TimeoutException:
            return False
        return True

    def select_all_and_delete(self, wait, path, title, draft=False):
        search = self.context.browser.find_element(*PageLocators.SEARCH_BOX)
        search.clear()
        search.send_keys(path)
        search.send_keys(Keys.ENTER)
        wait.until(ec.title_contains(title))
        for elem in self.context.browser.find_elements(*PageLocators.CHECK_BOX):
            if elem.is_displayed():
                elem.click()
                break
        if draft:
            self.context.browser.find_element(*PageLocators.DISCARD_DRAFTS).click()
            wait.until(ec.presence_of_element_located(PageLocators.DELETED_PROMPT))
        else:
            for elem in self.context.browser.find_elements(*PageLocators.DELETE):
                if elem.is_displayed():
                    elem.click()
                    break
            wait.until(ec.presence_of_element_located(PageLocators.TRASH_PROMPT))

    def empty_trash(self, wait):
        search = self.context.browser.find_element(*PageLocators.SEARCH_BOX)
        search.clear()
        search.send_keys('in:trash')
        search.send_keys(Keys.ENTER)
        wait.until(ec.title_contains('Trash'))
        empty_btn = wait.until(ec.element_to_be_clickable(PageLocators.EMPTY_TRASH))
        empty_btn.click()
        delete_btn = wait.until(ec.element_to_be_clickable(PageLocators.CONFIRM_EMPTY))
        delete_btn.click()
        wait.until(ec.element_to_be_clickable(PageLocators.EMPTY_PROMPT))
