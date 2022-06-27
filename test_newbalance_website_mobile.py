import time
import pytest
from selenium.common import NoSuchElementException, ElementNotInteractableException, TimeoutException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.firefox import webdriver
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as firefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import pytest_check as check # install pytest_check package

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FireFoxOptions

@pytest.fixture()
def driver():
    Firefox_driver_binary = "./geckodriver.exe"
    fire_fox_options = FireFoxOptions()
    fire_fox_options.add_argument("--width=414")
    fire_fox_options.add_argument("--height=896")
    fire_fox_options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS "
                                                                  "X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                                                                  "Version/14.0.3 Mobile/15E148 Safari/604.1")
    ser_firefox = FirefoxService(Firefox_driver_binary)
    driver = webdriver.Firefox(service=ser_firefox, options=fire_fox_options)
    yield driver
    driver.close()


def test_registeration(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID,"continue-country").click()
    driver.find_element(By.CSS_SELECTOR,"#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,"li.d-lg-none:nth-child(1) > div:nth-child(1) > span:nth-child(2) > a:nth-child(3)").click() # join link
    time.sleep(5)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,"#registration-form-fname").send_keys("Eitab")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-lname").send_keys("Keis")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-email").send_keys("cenobijhgfhgd493@runqx.com")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-password").send_keys("Eitabkeis123#")
    driver.execute_script(
         "document.getElementsByName('dwfrm_profile_customer_registerTermsAndConditions')[0].setAttribute('checked', 'true')")
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "button.nb-button:nth-child(10)").click()
    time.sleep(5)
    user_name=driver.find_element(By.CSS_SELECTOR,"dl.profile-firstname:nth-child(1) > dd:nth-child(2)").text
    time.sleep(5)
    assert 'Eitab' == user_name

def test_failed_login(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,"#sg-navbar-collapse > div > div > nav > div.menu-group > ul > div > ul > li:nth-child(1) > div > span.col-11.px-0 > a:nth-child(1)").click()
    time.sleep(2)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"#login-form-email").send_keys("eitab@com")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"button.nb-button:nth-child(7)").click()
    time.sleep(2)
    error_message = driver.find_element(By.ID, "login-form-email-error").text
    assert 'Please enter a valid E-Mail address' == error_message


def test_mandatory_fields(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,
                        "li.d-lg-none:nth-child(1) > div:nth-child(1) > span:nth-child(2) > a:nth-child(3)").click()  # join link
    time.sleep(5)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, "#registration-form-fname").send_keys("Eitab")
    driver.find_element(By.CSS_SELECTOR, "button.nb-button:nth-child(10)").click()
    time.sleep(3)
    lname_err = driver.find_element(By.CSS_SELECTOR, "#form-lname-error").text
    email_err = driver.find_element(By.CSS_SELECTOR, "#form-email-error").text
    pswd_err = driver.find_element(By.CSS_SELECTOR, "#form-password-error").text
    checkbox_err = driver.find_element(By.CSS_SELECTOR,
                                       "#register > form > div.form-group.custom-control.custom-checkbox.pb-2.mb-7.mb-lg-4.mt-4.pt-2 > div.terms-error.pt-2").text
    assert ((check.equal('Please enter a last name', lname_err) and check.equal('Please enter an email', email_err) \
             and check.equal('Please enter a password', pswd_err) and check.equal(
                'You must agree to our privacy policy and terms and conditions.', checkbox_err)) == True)


#Test Case 4 - Verify error messages for entering incorrect values in fields.
def test_incorrect_password(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,
                        "li.d-lg-none:nth-child(1) > div:nth-child(1) > span:nth-child(2) > a:nth-child(3)").click()  # join link
    time.sleep(5)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "#registration-form-fname").send_keys("Eitab")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-lname").send_keys("Keis")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-email").send_keys("fatiheh942@runqx.com")
    driver.find_element(By.CSS_SELECTOR, "#registration-form-password").send_keys("Eitab5")
    driver.find_element(By.CSS_SELECTOR, "button.nb-button:nth-child(10)").click()
    time.sleep(3)
    pswd_message_err = driver.find_element(By.CSS_SELECTOR, "#form-password-error").text
    assert 'Please ensure all password criteria is met' == pswd_message_err


# Test Case5 - Automate 'Search Product' feature of e-commerce website with Selenium
def test_search_product(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR,"li.linkAsset_item:nth-child(2) > a:nth-child(1)").click()
    time.sleep(2)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    driver.find_element(By.CSS_SELECTOR,"#mrefinement-categories li:nth-child(4) .body-regular").click() #Accessories & Gear
    driver.find_element(By.CSS_SELECTOR,"#mrefinement-categories li:nth-child(4) .body-regular").click() # hat catagory
    driver.find_element(By.CSS_SELECTOR,"div.pgptiles:nth-child(1) > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)").click()
    hat_name=driver.find_element(By.CSS_SELECTOR,"h1.font-header-1").text
    driver.find_element(By.CSS_SELECTOR, ".container > .site-search .form-control").clear()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".container > .site-search .form-control").send_keys(hat_name)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR,"a.button-primary").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".image-container > a:nth-child(1)").click()
    hat_res=driver.find_element(By.CSS_SELECTOR,"h1.font-header-1").text
    time.sleep(3)
    assert hat_res == hat_name


# Test Case 6.1 - Automate end-to-end "Buy Product" feature of the e-commerce website.
def test_buy_product(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,
                        "#sg-navbar-collapse > div > div > nav > div.menu-group > ul > div > ul > li:nth-child(1) > div > span.col-11.px-0 > a:nth-child(1)").click()
    time.sleep(2)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#login-form-email").send_keys("itab.keis@gmail.com")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.nb-button:nth-child(7)").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    time.sleep(2)
    driver.find_element(By.XPATH,"//a[@id='2000']/span").click() #women
    driver.find_element(By.ID,"25000").click() #clothes
    driver.find_element(By.ID,"25016").click() #shirts
    driver.find_element(By.CSS_SELECTOR, ".pgptiles:nth-child(4) .tile-image").click()  # 4 tshirt
    driver.find_element(By.XPATH,"//*[@id='productAtributes']/div[3]/div/div/div[2]/div/div/button[2]/span[1]").click() # color
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".size-attribute:nth-child(2)").click() # size
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR,".button-label").click() # Add to cart btn
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "a.text-center").click()  # click on cart
    time.sleep(3)
    my_quan = Select(driver.find_element(By.XPATH, "//select[contains(@class,'quantity')]"))  # quantity
    my_quan.select_by_visible_text('2')
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Checkout").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".mt-2 .form-control-label").click()
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
    driver.find_element(By.NAME,"dwfrm_shipping_shippingAddress_addressFields_city").clear()
    driver.find_element(By.NAME,"dwfrm_shipping_shippingAddress_addressFields_city").send_keys("Beverly Hills")
    time.sleep(2)
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_states_stateCode").click()
    dropdown = driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_states_stateCode")
    dropdown.find_element(By.XPATH, "//option[. = 'California']").click()

    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_postalCode").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_postalCode").send_keys("90211")

    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_phone").clear()
    driver.find_element(By.NAME, "dwfrm_shipping_shippingAddress_addressFields_phone").send_keys("(054) 628-8867")
    time.sleep(3)
    driver.find_element(By.NAME,"submit").click()
    time.sleep(3)
    # driver.find_element(By.CSS_SELECTOR, ".paypal-tab").click()
    # time.sleep(3)
    # driver.find_element(By.CSS_SELECTOR, ".paypal-button").click()
    # time.sleep(3)

# Test Case 6.2 - Verify that 'Add to Wishlist' only works after login..
def test_add_to_wishlost(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.XPATH, "//a[@id='2000']/span").click()  # women
    driver.find_element(By.ID, "25000").click()  # clothes
    driver.find_element(By.ID, "25016").click()  # shirts
    time.sleep(3)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    driver.find_element(By.CSS_SELECTOR, ".pgptiles:nth-child(4) .tile-image").click()  # 4 tshirt
    driver.find_element(By.CSS_SELECTOR,
                        "#productAtributes > div:nth-child(14) > div.row.wishlist-preorder > div > div.add-to-wishlist > button > span > u").click()  # add to wishlist
    time.sleep(3)
    wishlist_err=driver.find_element(By.CSS_SELECTOR,"#unique-id-pdp > div > div > div > div > div.modal-body > div.login-heading.font-weight-semibold.pl-lg-3").text
    assert "Log in or create an account to add items to your wish list." == wishlist_err



# Test Case 6.3 - Verify that Total Price is reflecting correctly if user changes quantity on 'Shopping Cart Summary' Page.
def test_total_price(driver):
    driver.get("https://www.newbalance.com/")
    driver.find_element(By.ID, "continue-country").click()
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    driver.find_element(By.CSS_SELECTOR,
                        "#sg-navbar-collapse > div > div > nav > div.menu-group > ul > div > ul > li:nth-child(1) > div > span.col-11.px-0 > a:nth-child(1)").click()
    time.sleep(2)
    e = driver.find_element(By.CSS_SELECTOR, "#discountPopUpCloseBtn > img:nth-child(1)")
    actions = ActionChains(driver)
    actions.move_to_element(e).click().perform()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#login-form-email").send_keys("itab.keis@gmail.com")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("Eitabkeis123#")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.nb-button:nth-child(7)").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#hamburger-icon-custom").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//a[@id='2000']/span").click()  # women
    driver.find_element(By.ID, "25000").click()  # clothes
    driver.find_element(By.ID, "25016").click()  # shirts
    driver.find_element(By.CSS_SELECTOR, ".pgptiles:nth-child(4) .tile-image").click()  # 4 tshirt
    driver.find_element(By.XPATH,
                        "//*[@id='productAtributes']/div[3]/div/div/div[2]/div/div/button[2]/span[1]").click()  # color
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".size-attribute:nth-child(2)").click()  # size
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".button-label").click()  # Add to cart btn
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, "a.text-center").click()  # click on cart
    time.sleep(3)
    qone_price = driver.find_element(By.CSS_SELECTOR, ".line-item-total-price").text  # 26.99
    sub_total_one = driver.find_element(By.CSS_SELECTOR, ".sub-total").text

    my_quan = Select(driver.find_element(By.XPATH, "//select[contains(@class,'quantity')]"))  # quantity
    my_quan.select_by_visible_text('2')
    time.sleep(3)
    qtwo_price = driver.find_element(By.CSS_SELECTOR, ".line-item-total-price").text  # 53.98(str)
    sub_total_two = driver.find_element(By.CSS_SELECTOR, ".sub-total").text
    assert ((check.equal(qone_price, sub_total_one)) and (check.equal(qtwo_price, sub_total_two)) == True)





