
def fill_unchanged_rows(context):
    field = context.browser.find_element_by_id("input-firstname")
    field.click()
    field.clear()
    field.send_keys("Danny")

    field = context.browser.find_element_by_id("input-lastname")
    field.click()
    field.clear()
    field.send_keys("Ahoj")

    field = context.browser.find_element_by_id("input-status")
    field.click()

    option = context.browser.find_element_by_xpath("//select[@id='input-status']/option[2]")
    option.click()



def add_user_group(context):
    context.browser.implicitly_wait(15)
    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()

    field = context.browser.find_element_by_id("input-name")
    field.click()
    field.clear()
    field.send_keys("demo")

    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()

    alert = context.browser.find_element_by_css_selector(".alert")
    print(alert.text)
    assert "Success" in alert.text


def fill_rows(context):
    field = context.browser.find_element_by_id("input-username")
    field.click()
    field.clear()
    field.send_keys("dan")

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

    field = context.browser.find_element_by_id("input-firstname")
    field.click()
    field.clear()
    field.send_keys("Danny")

    field = context.browser.find_element_by_id("input-lastname")
    field.click()
    field.clear()
    field.send_keys("Ahoj")

    field = context.browser.find_element_by_id("input-status")
    field.click()

    option = context.browser.find_element_by_xpath("//select[@id='input-status']/option[2]")
    option.click()

def click_save(context):
    context.browser.execute_script("window.scrollTo(0, 0);")
    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()

def add_user(context):
    context.browser.implicitly_wait(15)
    button = context.browser.find_element_by_css_selector(".btn-primary")
    button.click()

    context.browser.implicitly_wait(15)
    fill_rows(context)
    context.browser.implicitly_wait(15)
    click_save(context)
    context.browser.implicitly_wait(15)

    alert = context.browser.find_element_by_css_selector(".alert")
    print(alert.text)
    assert "Success" in alert.text
