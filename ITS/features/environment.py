
#https://www.techbeamers.com/selenium-python-test-suite-unittest/
#https://behave.readthedocs.io/en/latest/practical_tips.html

# -- FILE: features/environment.py
# CONTAINS: Browser fixture setup and teardown
from behave import fixture, use_fixture
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

@fixture
def browser_firefox(context):
    # -- BEHAVE-FIXTURE: Similar to @contextlib.contextmanager
    # create a new Firefox session
    dp = {'browserName': 'firefox', 'marionette': 'true',
            'javascriptEnabled': 'true'}
    context.browser = webdriver.Remote(
            command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
            desired_capabilities=dp)
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    teardown(context)

    context.browser.quit()

def before_all(context):
    use_fixture(browser_firefox, context)
    # -- NOTE: CLEANUP-FIXTURE is called after after_all() hook.

def teardown(context):
    log_and_goto_userspage(context)

    checkbox = context.browser.find_element_by_css_selector("tr:nth-child(2) input")
    checkbox.click()

    button = context.browser.find_element_by_css_selector(".btn-danger")
    button.click()
    context.browser.implicitly_wait(15)
    alert = context.browser.switch_to.alert
    alert.accept()


def log_and_goto_userspage(context):
    context.browser.implicitly_wait(15)
    context.browser.get("http://mat.fit.vutbr.cz:8105/admin/")
    username_field = context.browser.find_element_by_id("input-username")
    username_field.click()
    username_field.clear()
    username_field.send_keys("admin")

    pwd_field = context.browser.find_element_by_id("input-password")
    pwd_field.click()
    pwd_field.clear()
    pwd_field.send_keys("admin")
    pwd_field.send_keys(Keys.ENTER)

    context.browser.implicitly_wait(15)
    button = context.browser.find_element_by_id("button-menu")
    button.click()
    button = context.browser.find_element_by_xpath("//li[@id='system']/a/span")
    button.click()
    button = context.browser.find_element_by_xpath("//a[contains(text(),'Users')]")
    button.click()
    button = context.browser.find_element_by_xpath("//li[@id='system']/ul/li[2]/ul/li/a")
    button.click()
    button = context.browser.find_element_by_id("button-menu")
    button.click()
