from func_lib import add_user, add_user_group

@given(u'user list contains two users')
def step_impl(context):
    context.browser.implicitly_wait(15)
    try:
        user = context.browser.find_element_by_css_selector("tr:nth-child(2)")
        return True
    except:
        pass

    add_user(context)

@when(u'click \'edit\' button')
def step_impl(context):
    context.browser.implicitly_wait(15)
    checkbox = context.browser.find_element_by_css_selector("tr:nth-child(2) .fa")
    checkbox.click()

#Test1
@when(u'edit some columns correctly')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dany123@email.cz")

    field = context.browser.find_element_by_id("input-firstname")
    field.click()
    field.clear()
    field.send_keys("Daniel")

@then(u'users informations are actualized')
def step_impl(context):
    context.browser.implicitly_wait(15)
    alert = context.browser.find_element_by_css_selector(".alert")

    assert "Success" in alert.text

@given(u'there are two or more user groups')
def step_impl(context):
    context.browser.implicitly_wait(15)
    button = context.browser.find_element_by_id("button-menu")
    button.click()

    button = context.browser.find_element_by_xpath("//a[contains(text(),'User Groups')]")
    button.click()

    try:
        user = context.browser.find_element_by_css_selector("tr:nth-child(2) input")
    except:
        add_user_group(context)

    button = context.browser.find_element_by_xpath("//a[contains(text(),'Users')]")
    button.click()

    button = context.browser.find_element_by_id("button-menu")
    button.click()

#Test3
@when(u'change email to invalid email')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dany@")

@then(u'users informations are not changed')
def step_impl(context):
    pass

"""
#already defined in 'add_user.py'
@then(u'the page is not changed')
def step_impl(context):
"""

#Test4
@when(u'change nick to invalid nick')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    #length = 21
    field.send_keys("-aaaa-aaaa-aaaa-aaaa-")

#Test5
@when(u'change password to invalid password')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("a")


#Test6
@when(u'change password')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("test123")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("test123")

#Test7
@when(u'fill column confirm password incorrect')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("a")
