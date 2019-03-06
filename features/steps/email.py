from behave import given, when, then
from gmail import *

@given('we have logged into gmail')
def step_logged_in(context):
    log_in(context, sender['email'], sender['password'])

@given('we are on the inbox page')
def step_at_inbox(context):
    context.browser.get(inbox_url)

@given('we are composing an email')
def step_given_composing(context):
    pass

@given('it is addressed to "{recipient}"')
def step_given_recipient(context, recipient):
    pass

@given('the subject contains "{subject}"')
def step_given_subject(context, subject):
    pass

@given('a sample text is entered in the body')
def step_given_body(context):
    pass

@given('we attached "{image}" to the email')
def step_given_image(context, image):
    pass

@when('we send the email')
def step_when_send_email(context):
    pass

@then('"{recipient}" should receive the email')
def step_then_recipient(context, recipient):
    pass

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

@then('we should receive an attachment error')
def step_then_error_attachment(context):
    pass
