Feature: send email with image attachment

    Background: at inbox page
        Given we have logged into gmail
        And we are on the inbox page

    Scenario: 1. Send an email to recipientA with imageA
        Given we are composing an email
        And it is addressed to "recipientA"
        And the subject contains "Scenario1"
        And a sample text is entered in the body
            """
            Hello, this email contains imageA.jpg.

            Regards,
            Sender
            """
        And we attached "imageA.jpg" to the email
        When we send the email
        Then "recipientA" should receive the email
        And it should be from the Sender
        And it should be addressed to "recipientA"
        And the subject should match
        And the body should match the sample text
        And the attachment should match the image

    Scenario: 2. Send an email to recipientB with imageB
        Given we are composing an email
        And it is addressed to "recipientB"
        And the subject contains "Scenario2"
        And a sample text is entered in the body
            """
            Hello, this email contains imageB.jpg.

            Regards,
            Sender
            """
        And we attached "imageB.jpg" to the email
        When we send the email
        Then "recipientB" should receive the email
        And it should be from the Sender
        And it should be addressed to "recipientB"
        And the subject should match
        And the body should match the sample text
        And the attachment should match the image

    Scenario: 3. Send an email to recipient with invalid email address
        Given we are composing an email
        And it is addressed to "invalidRecipient"
        And the subject contains "Scenario3"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        And we attached "imageA.jpg" to the email
        When we try to send the email
        Then we should receive an email error

    Scenario: 4. Send an email to recipientA with too large attachment (>25MB)
        Given we are composing an email
        And it is addressed to "recipientA"
        And the subject contains "Scenario4"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        When we attach "imageLarge.jpg" to the email
        Then we should receive an attachment error

    Scenario: 5. Send an email to recipientA with multiple attachments (total>25MB)
        Given we are composing an email
        And it is addressed to "recipientA"
        And the subject contains "Scenario5"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        And we attached "imageC1.png" to the email
        And we attached "imageC2.png" to the email
        When we attach "imageC3.jpg" to the email
        Then we should receive an attachment error
