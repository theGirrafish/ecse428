Feature: Send email with image attachment

    Background: At inbox page
        Given we have logged into gmail
        And we are on the inbox page

    Scenario Outline: Normal Flow: Send an email to <recipient> with <image>
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "Normal flow"
        And a sample text is entered in the body
            """
            Hello, this email contains an image.

            Regards,
            Sender
            """
        And we attached "<image>" to the email
        When we send the email
        Then "<recipient>" should receive the email
        And it should be from the Sender
        And it should be addressed to "<recipient>"
        And the subject should match
        And the body should match the sample text
        And the attachment should match the image

        Examples:
            | recipient    | image       |
            | recipientA   | imageA.jpg  |
            | recipientB   | imageB.jpg  |
            | recipientA   | imageB.jpg  |
            | recipientB   | imageA.jpg  |
            | recipientA   | imageC1.png |

    Scenario Outline: Alternative Flow: Send an email to <recipient> with <images> attachment too large
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "Alternative Flow"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        When we attach "<images>" to the email
        Then we should be prompted to upload to Google Drive

        Examples:
            | recipient  | images                              |
            | recipientA | imageLarge.jpg                      |
            | recipientB | imageLarge.jpg                      |
            | recipientA | imageC1.png imageC2.png imageC3.jpg |
            | recipientB | imageC1.png imageC2.png imageC3.jpg |
            | recipientA | imageA.jpg imageLarge.jpg           |

    Scenario Outline: Error Flow: Send an email to <recipient> with invalid email address and <image>
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "Error Flow"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        And we attached "<image>" to the email
        When we try to send the email
        Then we should receive an email error

        Examples:
            | recipient            | image      |
            | @not.valid.gmail@com | imageA.jpg |
            | wotisdis             | imageB.jpg |
            | abc.123.gmail.com    | imageB.jpg |
            | ilikecucumbers@gmail | imageA.jpg |
            | gherkin@.gmail.com   | imageB.jpg |
