from behave import given, when, then
from selenium.webdriver.common.by import By

from locators import ComposeEmailLocators, AlertLocators

@given('we have logged into gmail')
def step_logged_in(context):
    sender = context.gmail.get_credentials('Sender')
    context.gmail.log_in(sender['email'], sender['password'])

@given('we are on the inbox page')
def step_at_inbox(context):
    context.browser.get(context.gmail.base_url + '#inbox')

@given('we are composing an email')
def step_given_composing(context):
    context.gmail.compose_email()

@given('it is addressed to "{recipient}"')
def step_given_recipient(context, recipient):
    try:
        email = context.gmail.get_credentials(recipient)['email']
    except:
        email = recipient
    context.gmail.fill_field(ComposeEmailLocators.RECIPIENT, email)

@given('the subject contains "{subject}"')
def step_given_subject(context, subject):
    context.gmail.fill_field(ComposeEmailLocators.SUBJECT, subject)

@given('a sample text is entered in the body')
def step_given_body(context):
    context.gmail.body = context.text
    context.gmail.fill_field(ComposeEmailLocators.BODY, context.text)

@given('we attached "{image}" to the email')
def step_given_image(context, image):
    context.gmail.attach_image(image)

@when('we attached "{images}" to the email')
def step_when_image(context, images):
    img_lst = images.strip().split(' ')
    end = len(img_lst) - 1
    for i, img in enumerate(img_lst):
        if i == end:
            context.gmail.attach_image(img, expect_failure=True)
        else:
            context.gmail.attach_image(img)

@when('we send the email')
def step_when_send_email(context):
    context.gmail.send_email()

@when('we try to send the email')
def step_when_try_email(context):
    context.gmail.send_email(expect_failure=True)

@then('"{recipient}" should receive the email with subject "{subject}"')
def step_then_recipient(context, recipient, subject):
    context.gmail.log_out()
    recipient = context.gmail.get_credentials(recipient)
    context.gmail.log_in(recipient['email'], recipient['password'])
    try:
        assert context.gmail.check_email_received(subject), 'Email subject does not match'
    except:
        assert False

@then('it should be from the Sender')
def step_then_sender(context):
    subject = context.active_outline[0]
    assert context.gmail.check_email_sender(subject), 'Sender email does not match'

@then('the body should match the sample text')
def step_then_body(context):
    subject = context.active_outline[0]
    assert context.gmail.check_email_body(subject, context.gmail.body), 'Email body does not match'

@then('the attachment/s should match "{images}"')
def step_then_attachments(context, images):
    img_lst = images.strip().split(' ')
    subject = context.active_outline[0]
    for img in img_lst:
        assert context.gmail.check_email_attachment(subject, img), 'Image attachment does not match'

@then('we should receive an email error')
def step_then_error_email(context):
    email_alert = context.browser.find_element(*AlertLocators.ALERT)
    alert_text = email_alert.find_element(By.CSS_SELECTOR, 'span[role="heading"]')
    assert 'Error' in alert_text.text, 'Failed to find email error'

@then('we should be prompted to upload to Google Drive')
def step_then_upload_attachment(context):
    assert context.gmail.upload_to_drive(), 'Failed to upload to Drive'

@then('we should be able to send the email')
def step_then_send_email(context):
    assert context.gmail.send_email(share_prompt=True), 'Failed to send email'
