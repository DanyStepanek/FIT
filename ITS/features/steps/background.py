# -*- coding: utf-8 -*-
# Remote Control
import selenium
import unittest, time, re

# WebDriver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException


@given(u'admin is logged')
def step_impl(context):
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


@given(u'actual page is users page')
def step_impl(context):
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
