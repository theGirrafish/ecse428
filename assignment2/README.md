# Assignment 2

UI-based testing for sending emails with image attachments in Gmail.

## Requirements

- Python 3.6 or higher.
- Chrome
- Only tested on Linux, scripts may not run on Windows.

## Setup

- Clone the repo and `cd` into the project directory.
- (Optional) Activate your virtualenv.
- Run `pip install -r requirements.txt` to install all dependencies.

## Running Tests

- Run `behave` to start the test suite.
- Script should automatically download the Chrome Web Driver for your platform.
- All tests will run and you will receive a summary in the console upon completion.

## Adding New Tests

To add new Gherkin tests, first add your Gherkin acceptance test definition as a `.feature` file under `features`. Then create a `.py` file with the same name under `features/steps`. Use the decorators provided by behave to link your Gherkin steps with the functions you define in this file. For example:

Gherkin step:

```gherkin
Given we are at the login page
```

Python step:

```python
@given('we are at the login page')
def step_given_login(context):
    pass
```

Please see the [Behave docs](https://behave.readthedocs.io/en/latest/) for more information.

## Environment Description

This suite uses [Behave](https://github.com/behave/behave), which is a behaviour-driven development (BDD) based testing framework built on the [Gherkin](https://docs.cucumber.io/gherkin/) language. The Gherkin feature file that describes the scenario outlines for our acceptance tests can be found at `features/email.feature`. The step definitions for this feature file are found at `features/steps/email.py`. The `features/environment.py` file defines before and after functions for Gherkin steps, as well as instantiating the web driver object for our tests. It also includes methods like `delete_emails` to help return the system to its initial state after running all tests.

The UI component of the testing is implemented using [Selenium](https://pypi.org/project/selenium/) and the Chrome Web Driver. We use [Webdriver Manager](https://pypi.org/project/webdriver-manager/) to automatically download the required Web Driver for the user's platform. We also use [Retrying](https://pypi.org/project/retrying/) for adding retry decorators to certain methods. All relevant dependency information for the project can be found in `requirements.txt`.

Additionally, `gmail.py` implements many helper methods needed for our UI tests, like `check_email_received`, a method to verify an email was sent by the sender and received by the recipient. All UI element mappings can be found in `locators.py`. This is to make the suite easier to update in the event that UI elements change.
