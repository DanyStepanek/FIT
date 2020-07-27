from func_lib import fill_unchanged_rows

#Test1
@when(u'click \'add new\' button')
def step_impl(context):
    context.browser.implicitly_wait(15)
    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()

@when(u'fill all required columns correctly')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dany@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[1]")
    option.click()

    fill_unchanged_rows(context)


@when(u'save changes')
def step_impl(context):
    context.browser.execute_script("window.scrollTo(0, 0);")
    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()


@then(u'user is added')
def step_impl(context):
    context.browser.implicitly_wait(15)
    alert = context.browser.find_element_by_css_selector(".alert")

    assert "Success" in alert.text

@then(u'user is shown in table of users')
def step_impl(context):
    context.browser.implicitly_wait(15)
    try:
        user = context.browser.find_element_by_css_selector("tr:nth-child(2)")
    except:
        return False

    return True

#Test2
@when(u'set nick as already used nick in current user group')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dan@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[1]")
    option.click()

    fill_unchanged_rows(context)


@then(u'user is not added')
def step_impl(context):
    context.browser.implicitly_wait(15)
    try:
        alert = context.browser.find_elements_by_class_name("text-danger")
    except:
        return True
        
    return False

@then(u'the page is not changed')
def step_impl(context):
    context.browser.implicitly_wait(15)
    try:
        field = context.browser.find_element_by_id("input-username")
    except:
        return False

    return True

#Test3
@when(u'set nick as already used nick in another user group')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dan@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[2]")
    option.click()

    fill_unchanged_rows(context)

#Test4
@when(u'fill all required columns correctly except email')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[2]")
    option.click()

    fill_unchanged_rows(context)

#Test5
@when(u'fill all required columns correctly except nick')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("-1")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dan@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[2]")
    option.click()

    fill_unchanged_rows(context)

#Test6
@when(u'fill all required columns correctly except password')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dan@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[2]")
    option.click()

    fill_unchanged_rows(context)

#Test7
@when(u'fill all required columns correctly except confirm password')
def step_impl(context):
    context.browser.implicitly_wait(15)
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("danny")

    field = context.browser.find_element_by_id("input-email")
    field.click()
    field.clear()
    field.send_keys("dan@email.cz")

    field = context.browser.find_element_by_id("input-password")
    field.click()
    field.clear()
    field.send_keys("ahoj")

    field = context.browser.find_element_by_id("input-confirm")
    field.click()
    field.clear()
    field.send_keys("")

    option = context.browser.find_element_by_xpath("//select[@id='input-user-group']/option[2]")
    option.click()

    fill_unchanged_rows(context)
