import time
import warnings
from threading import Thread
import pytest
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service as firefoxService
import pytest_check as check # install pytest_check package


@pytest.fixture()
def driver():
    firefox_driver_binary = "./geckodriver.exe"
    ser_firefox = firefoxService(firefox_driver_binary)

    browser_name='firefox'
    if browser_name == "firefox":
        driver = webdriver.Firefox(service=ser_firefox)
    elif browser_name == "firefox":
        dc = {
            "browserName": "firefox",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc)

    elif browser_name == "MicrosoftEdge":
        dc = {
            "browserName": "MicrosoftEdge",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc)

    elif browser_name == "chrome":
        dc = {
            "browserName": "chrome",
            "platformName": "Windows 11"
        }
        driver = webdriver.Remote("http://localhost:4444", desired_capabilities=dc)
    elif browser_name == "firefox-mobile":
        firefox_options = FireFoxOptions()
        firefox_options.add_argument("--width=375")
        firefox_options.add_argument("--height=812")
        firefox_options.set_preference("general.useragent.override", "userAgent=Mozilla/5.0 "
                                                                     "(iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like "
                                                                     "Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1")
        # firefox_options.set_preference("general.useragent.override", "Nexus 7")

        driver = webdriver.Firefox(service=ser_firefox, options=firefox_options)
    else:
        raise Exception("driver doesn't exists")
    yield driver
    driver.close()


def test_registeration(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR,
                        "#header > div > nav > div.header.header-nav.container > div > div.navbar-header.d-flex.col-lg-5.p-0.justify-content-end.align-items-center > div.account-links.d-none.d-lg-flex.flex-shrink-0 > div > div > span.col-11.px-0 > a:nth-child(3)").click()
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#registration-form-fname").send_keys("Eitab")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-lname").send_keys("Keis")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-email").send_keys("caway99ggg88@syswift.com")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-password").send_keys("Eitabkeis123#")
    time.sleep(5)
    driver.execute_script(
        "document.getElementsByName('dwfrm_profile_customer_registerTermsAndConditions')[0].setAttribute('checked', 'true')")
    driver.find_element(By.CSS_SELECTOR, "#register > form > button").click()
    time.sleep(5)
    user_message = driver.find_element(By.CSS_SELECTOR, ".account-links > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > span:nth-child(2) > span:nth-child(1)").text
    time.sleep(5)
    assert "Hello Eitab," == user_message

def test_failed_login(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR,"div > .user a:nth-child(1) > .user-message").click()
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"#login-form-email").send_keys("eitab@com")
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,"#login > form > button").click()
    time.sleep(5)
    error_message = driver.find_element(By.CSS_SELECTOR, "#login-form-email-error").text
    assert 'Please enter a valid E-Mail address' == error_message

#Test Case 3: Verify error messages for mandatory fields.
def test_mandatory_fields(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR,
                        "#header > div > nav > div.header.header-nav.container > div > div.navbar-header.d-flex.col-lg-5.p-0.justify-content-end.align-items-center > div.account-links.d-none.d-lg-flex.flex-shrink-0 > div > div > span.col-11.px-0 > a:nth-child(3)").click()
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#registration-form-fname").send_keys("eitab")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#register > form > button").click()
    time.sleep(3)
    lname_err = driver.find_element(By.CSS_SELECTOR, "#form-lname-error").text
    email_err=driver.find_element(By.CSS_SELECTOR,"#form-email-error").text
    pswd_err = driver.find_element(By.CSS_SELECTOR,"#form-password-error").text
    checkbox_err = driver.find_element(By.CSS_SELECTOR,"#register > form > div.form-group.custom-control.custom-checkbox.pb-2.mb-7.mb-lg-4.mt-4.pt-2 > div.terms-error.pt-2").text
    assert ((check.equal('Please enter a last name',lname_err) and check.equal('Please enter an email',email_err) \
    and check.equal('Please enter a password',pswd_err) and check.equal('You must agree to our privacy policy and terms and conditions.',checkbox_err))== True)


#Test Case 4 - Verify error messages for entering incorrect values in fields.
def test_incorrect_password(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR,
                        "#header > div > nav > div.header.header-nav.container > div > div.navbar-header.d-flex.col-lg-5.p-0.justify-content-end.align-items-center > div.account-links.d-none.d-lg-flex.flex-shrink-0 > div > div > span.col-11.px-0 > a:nth-child(3)").click()
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#registration-form-fname").send_keys("eitab")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-lname").send_keys("Keis")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-email").send_keys("itab.keis@gmail.com")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-password").send_keys("Eitab5")
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#register > form > button").click()
    time.sleep(3)
    pswd_message_err=driver.find_element(By.CSS_SELECTOR,"#form-password-error").text
    assert 'Please ensure all password criteria is met' == pswd_message_err

# Test Case5 - Automate 'Search Product' feature of e-commerce website with Selenium
def test_search_product(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    women_element = driver.find_element(By.ID, "2000")
    actions = ActionChains(driver)
    actions.move_to_element(women_element).perform()
    time.sleep(2)
    driver.find_element(By.ID, "213510").click()  # hat catageroy
    time.sleep(2)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,
                                     "#product-search-results > div > div.pgp-grids.col-12.col-lg-9.pr-lg-0 > div.row.product-grid > div:nth-child(1) > div > div > div.image-container > a").click()
    time.sleep(3)
    hat_name=driver.find_element(By.CSS_SELECTOR,"#productDetails > div.col-lg-12.col-12.p-0.d-none.d-lg-block.mb-2 > div:nth-child(2) > div > h1").text
    driver.find_element(By.NAME, "q").clear()
    driver.find_element(By.NAME, "q").send_keys(hat_name)
    driver.find_element(By.CSS_SELECTOR, ".search .search-button > .icon").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,"#product-search-results > div > div.pgp-grids.col-12.col-lg-9.pr-lg-0 > div.row.product-grid > div.pgptiles.col-6.col-lg-4.px-1.px-lg-2 > div > div > div.image-container > a").click()
    res_hat_name=driver.find_element(By.CSS_SELECTOR,"h1.hidden-sm-down").text
    time.sleep(3)
    assert res_hat_name== hat_name


# Test Case 6.1 - Automate end-to-end "Buy Product" feature of the e-commerce website.
def test_buy_product(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "div > .user a:nth-child(1) > .user-message").click()
    driver.find_element(By.CSS_SELECTOR, "#login-form-email").send_keys("itab.keis@gmail.com")
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(5)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#login > form > button").click()
    time.sleep(5)
    women_element = driver.find_element(By.ID, "2000")
    actions = ActionChains(driver)
    actions.move_to_element(women_element).perform()
    time.sleep(3)
    driver.find_element(By.ID, "25016").click()  # shirt catageroy

    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".pgptiles:nth-child(4) .tile-image").click() # 4 tshirt
    time.sleep(3)
    driver.find_element(By.XPATH,"//*[@id='productAtributes']/div[3]/div/div/div[2]/div/div/button[2]/span[1]").click() # color
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".size-attribute:nth-child(2)").click() # size
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".button-label").click() # Add to cart btn
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".minicart-link > .icon").click() # click on cart
    time.sleep(3)
    my_quan = Select(driver.find_element(By.XPATH, "//select[contains(@class,'quantity')]")) # quantity
    my_quan.select_by_visible_text('2')
    time.sleep(3)
    driver.find_element(By.LINK_TEXT,"Checkout").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".mt-2 .form-control-label").click()
    time.sleep(3)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_firstName").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_firstName").send_keys("Eitab")
    time.sleep(2)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_lastName").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_lastName").send_keys("Keis")
    time.sleep(2)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_address1").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_address1").send_keys("Herzl Way")
    time.sleep(2)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_city").clear()
    driver.find_element(By.NAME,"dwfrm_shipping_shippingAddress_addressFields_city").send_keys("Beverly Hills")
    time.sleep(2)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_states_stateCode").click()
    dropdown = driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_states_stateCode")
    dropdown.find_element(By.XPATH, "//option[. = 'California']").click()

    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_postalCode").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_postalCode").send_keys("90211")

    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_phone").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_phone").send_keys("(054) 628-8867")

    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_email").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_email").send_keys("itab.keis@gmail.com")
    time.sleep(3)
    driver.find_element(By.NAME,"submit").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".paypal-tab > .custom-radio").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#paypal-content > fieldset > div.paypal-default-content.js_paypal_button_parent > div.row.sticky-button-warpper.mx-n3.mx-md-0 > div > div > div").click()


# Test Case 6.2 - Verify that 'Add to Wishlist' only works after login..
def test_add_to_wishlost(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    time.sleep(5)
    women_element = driver.find_element(By.ID, "2000")
    actions = ActionChains(driver)
    actions.move_to_element(women_element).perform()
    time.sleep(3)
    driver.find_element(By.ID, "25016").click()  # shirt catageroy
    time.sleep(3)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".pgptiles:nth-child(4) .tile-image").click() # 4 tshirt
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#productAtributes > div:nth-child(14) > div.row.wishlist-preorder > div > div.add-to-wishlist > button > span > u").click()  # add to wishlist
    time.sleep(3)
    wishlist_err=driver.find_element(By.CSS_SELECTOR,"#unique-id-pdp > div > div > div > div > div.modal-body > div.login-heading.font-weight-semibold.pl-lg-3").text
    assert "Log in or create an account to add items to your wish list." == wishlist_err


# Test Case 6.3 - Verify that Total Price is reflecting correctly if user changes quantity on 'Shopping Cart Summary' Page.
def test_total_price(driver):
    driver.get("https://www.newbalance.com/")
    driver.maximize_window()
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "div > .user a:nth-child(1) > .user-message").click()
    time.sleep(3)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    time.sleep(3)
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#login-form-email").send_keys("itab.keis@gmail.com")
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "#login > form > button").click()
    time.sleep(5)
    women_element = driver.find_element(By.ID, "2000")
    actions = ActionChains(driver)
    actions.move_to_element(women_element).perform()
    time.sleep(3)
    driver.find_element(By.ID, "25016").click()  # shirt catageroy
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".pgptiles:nth-child(4) .tile-image").click() # 4 tshirt
    time.sleep(3)
    driver.find_element(By.XPATH,"//*[@id='productAtributes']/div[3]/div/div/div[2]/div/div/button[2]/span[1]").click() # color
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".size-attribute:nth-child(2)").click() # size
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".button-label").click() # Add to cart btn
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".minicart-link > .icon").click() # click on cart
    time.sleep(3)
    qone_price=driver.find_element(By.CSS_SELECTOR,".line-item-total-price").text #26.99
    sub_total_one=driver.find_element(By.CSS_SELECTOR,".sub-total").text


    my_quan = Select(driver.find_element(By.XPATH, "//select[contains(@class,'quantity')]")) # quantity
    my_quan.select_by_visible_text('2')
    time.sleep(3)
    qtwo_price=driver.find_element(By.CSS_SELECTOR,".line-item-total-price").text # 53.98(str)
    sub_total_two = driver.find_element(By.CSS_SELECTOR, ".sub-total").text
    assert ((check.equal(qone_price,sub_total_one)) and (check.equal(qtwo_price,sub_total_two)) == True )
