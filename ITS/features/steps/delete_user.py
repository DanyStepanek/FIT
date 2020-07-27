"""
#defined in edit_user.py
@given(u'user list contains two users')
def step_impl(context):
"""

#Test1
@when(u'user is selected')
def step_impl(context):
    checkbox = context.browser.find_element_by_css_selector("tr:nth-child(2) input")
    checkbox.click()

@when(u'click \'delete\' button')
def step_impl(context):
    button = context.browser.find_element_by_css_selector(".btn-danger")
    button.click()
    context.browser.implicitly_wait(15)
    alert = context.browser.switch_to.alert
    alert.accept()

@then(u'user is deleted')
def step_impl(context):
    context.browser.implicitly_wait(15)
    alert = context.browser.find_element_by_css_selector(".alert")

    assert "Success" in alert.text

#Test2
@when(u'no user is selected')
def step_impl(context):
    pass

@then(u'no user is deleted')
def step_impl(context):
    context.browser.implicitly_wait(15)
    try:
        user = context.browser.find_element_by_css_selector("tr:nth-child(2)")
    except:
        return False

    return True
