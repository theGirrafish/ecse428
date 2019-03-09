from behave import given, when, then
from selenium.webdriver.common.by import By

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
    context.gmail.fill_field(By.NAME, 'to', email)

@given('the subject contains "{subject}"')
def step_given_subject(context, subject):
    context.gmail.fill_field(By.CSS_SELECTOR, '[name="subjectbox"][placeholder="Subject"]', subject)

@given('a sample text is entered in the body')
def step_given_body(context):
    context.gmail.fill_field(By.CSS_SELECTOR, '[aria-label="Message Body"][role="textbox"]', context.text)

@given('we attached "{image}" to the email')
def step_given_image(context, image):
    context.gmail.attach_image(image)

@when('we attach "{images}" to the email')
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

@then('"{recipient}" should receive the email')
def step_then_recipient(context, recipient):
    context.gmail.check_email_received(recipient)

@then('it should be from the Sender')
def step_then_sender(context):
    pass

@then('it should be addressed to "{recipient}"')
def step_then_recipient_address(context, recipient):
    pass

@then('the subject should match')
def step_then_subject(context):
    pass

@then('the body should match the sample text')
def step_then_body(context):
    pass

@then('the attachment should match the image')
def step_then_image(context):
    pass

@then('we should receive an email error')
def step_then_error_email(context):
    pass

@then('we should be prompted to upload to Google Drive')
def step_then_upload_attachment(context):
    pass
