Feature: Send email with image attachment

    Background: At inbox page
        Given we have logged into gmail
        And we are on the inbox page

    Scenario Outline: Normal Flow: Send an email with "<subject>" as subject to <recipient> with <image> attachment
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "<subject>"
        And a sample text is entered in the body
            """
            Hello, this email contains an image.

            Regards,
            Sender
            """
        And we attached "<image>" to the email
        When we send the email
        Then "<recipient>" should receive the email with subject "<subject>"
        And it should be from the Sender
        And the body should match the sample text
        And the attachment should match "<image>"

        Examples:
            | subject       | recipient  | image       |
            | Normal Flow 1 | recipientA | imageA.jpg  |
            | Normal Flow 2 | recipientB | imageB.jpg  |
            | Normal Flow 3 | recipientA | imageB.jpg  |
            | Normal Flow 4 | recipientB | imageA.jpg  |
            | Normal Flow 5 | recipientA | imageC1.png |

    Scenario Outline: Alternative Flow: Send an email with "<subject>" as subject to <recipient> with <images> attachment too large
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "<subject>"
        And a sample text is entered in the body
            """
            Hello, this email should not send.

            Regards,
            Sender
            """
        When we attached "<images>" to the email
        Then we should be prompted to upload to Google Drive

        Examples:
            | subject            | recipient  | images                              |
            | Alternative Flow 1 | recipientA | imageLarge.jpg                      |
            | Alternative Flow 2 | recipientB | imageLarge.jpg                      |
            | Alternative Flow 3 | recipientA | imageC1.png imageC2.png imageC3.jpg |
            | Alternative Flow 4 | recipientB | imageC1.png imageC2.png imageC3.jpg |
            | Alternative Flow 5 | recipientA | imageA.jpg imageLarge.jpg           |

    Scenario Outline: Error Flow: Send an email with "<subject>" as subject to <recipient> with invalid email address and <image> attachment
        Given we are composing an email
        And it is addressed to "<recipient>"
        And the subject contains "<subject>"
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
            | subject      | recipient            | image      |
            | Error Flow 1 | @not.valid.gmail@com | imageA.jpg |
            | Error Flow 2 | wotisdis             | imageB.jpg |
            | Error Flow 3 | abc.123.gmail.com    | imageB.jpg |
            | Error Flow 4 | ilikecucumbers@gmail | imageA.jpg |
            | Error Flow 5 | gherkin@.gmail.com   | imageB.jpg |
