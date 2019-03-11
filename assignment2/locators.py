from selenium.webdriver.common.by import By

# Provides locators for login page
class LoginLocators():
    USER_V1 = (By.ID, 'identifierId')
    PASSWORD_V1 = (By.CSS_SELECTOR, '#password  input')
    NEXT_V1 = (By.ID, 'identifierNext')
    LOGIN_V1 = (By.ID, 'passwordNext')

    USER_V2 = (By.ID, 'Email')
    PASSWORD_V2 = (By.ID, 'Passwd')
    NEXT_V2 = (By.NAME, 'signIn')
    LOGIN_V2 = (By.ID, 'signIn')

# Provides locators for logout dialog
class LogoutLocators():
    ACCOUNT = (By.XPATH, '//*[@class="gb_x gb_Da gb_f"]')
    LOGOUT = (By.XPATH, '//*[@class="gb_0 gb_Vf gb_3f gb_Be gb_gb"]')

# Provides locators for compose email dialog
class ComposeEmailLocators():
    COMPOSE = (By.XPATH, '//*[@role="button"][text()="Compose"]')
    HEADER = (By.XPATH, '//*[text()="New Message"]')
    RECIPIENT = (By.NAME, 'to')
    SUBJECT = (By.CSS_SELECTOR, '[name="subjectbox"][placeholder="Subject"]')
    BODY = (By.CSS_SELECTOR, '[aria-label="Message Body"][role="textbox"]')
    ATTACH_PATH = (By.NAME, 'Filedata')
    SEND = (By.CSS_SELECTOR, '[role="button"][aria-label~="Send"]')
    SENT_PROMPT = (By.XPATH, '//*[text()="Message sent."]')

    def get_attachment_field(name):
        return (By.CSS_SELECTOR, f'[aria-label*="Attachment: {name}"]')

# Provides common page locators
class PageLocators():
    EMAIL_TABLE = (By.XPATH, '//*[@class="F cf zt"]')
    EMAIL_IN_TABLE = (By.XPATH, './/*[contains(@class,"zA")]')
    SUBJECT = (By.XPATH,  './/*[contains(@class,"bog")]')
    SENDER = (By.XPATH, './/*[@class="yX xY "]')
    BODY = (By.XPATH, './/*[@class="y2"]')
    ATTACHMENT = (By.XPATH, './/*[@class="brg"]')

    SEARCH_BOX = (By.CSS_SELECTOR, '[aria-label="Search mail"]')
    CHECK_BOX = (By.CSS_SELECTOR, 'div[role="button"][aria-label="Select"] span[role="checkbox"]')
    DISCARD_DRAFTS = (By.XPATH, '//*[text()="Discard drafts"]')
    DELETED_PROMPT = (By.XPATH, '//*[contains(text(),"deleted")]')
    DELETE = (By.CSS_SELECTOR, '[role="button"][aria-label="Delete"]')
    TRASH_PROMPT = (By.XPATH, '//*[contains(text(),"moved to")]')

    EMPTY_TRASH = (By.XPATH, '//*[@role="button"][contains(text(), "Empty")]')
    CONFIRM_EMPTY = (By.CSS_SELECTOR, '[role="alertdialog"]:not([aria-hidden]) [name="ok"]')
    EMPTY_PROMPT = (By.XPATH, '//*[text()="All messages have been deleted."]')

# Provides locators for alert dialogs
class AlertLocators():
    ALERT = (By.CSS_SELECTOR, '[role="alertdialog"]')
    DIALOG_UPLOAD = (By.XPATH, '//*[@role="dialog"] //span[@role="heading"][text()="Attaching File"]')
    DIALOG_FRAME = (By.CLASS_NAME, 'Qr-Mr-Jz-avO')
