import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import HtmlTestRunner
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from random import randint

class IgaveestiTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(ChromeDriverManager().install())
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_01_header_text_present(self):
        driver = self.driver
        driver.get("https://igavesti-ou.myshopify.com/")
        driver.find_element_by_xpath("//div[@class='header-bar__module header-bar__message']").is_displayed()
        time.sleep(1)

    @unittest.skip("Due to reCAPTCHA skip it")
    def test_02_valid_login(self):
        driver =self.driver
        Login_link = driver.find_element_by_id('customer_login_link')
        Login_link.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CustomerEmail"))
        )
        driver.find_element_by_id("CustomerEmail").send_keys('azadtestlio@gmail.com')
        driver.find_element_by_id("CustomerPassword").send_keys('Tester1234')
        driver.find_element_by_xpath("//form[@id='customer_login']//input[@class='btn']").click()
        driver.find_element_by_xpath("//h1[contains(text(),'My Account')]").is_displayed()
        driver.find_element_by_xpath("//h2[contains(text(),'Account Details')]").is_displayed()
        driver.find_element_by_id('customer_logout_link').click()

    @unittest.skip("Due to reCAPTCHA skip it")
    def test_002_invalid_login(self):
        driver =self.driver
        Login_link = driver.find_element_by_id('customer_login_link')
        Login_link.click()
        driver.find_element_by_id("CustomerEmail").send_keys('azadtestlioyy@gmail.com')
        driver.find_element_by_id("CustomerPassword").send_keys('Tester1234')
        driver.find_element_by_xpath("//form[@id='customer_login']//input[@class='btn']").click()
        assert 'Incorrect email or password.' in driver.page_source

    @unittest.skip("Due to reCAPTCHA skip it")
    def test_03_create_account(self):
        driver = self.driver
        driver.find_element_by_id("customer_register_link").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn"))
        )
        name_generator = 'Azad'+str(random.randint(0, 99))
        password_generator = 'Tester'+str(random.randint(0, 99))
        driver.find_element_by_id("FirstName").send_keys(name_generator)
        driver.find_element_by_id("LastName").send_keys(name_generator)
        driver.find_element_by_id("Email").send_keys(name_generator+'@gmail.com')
        driver.find_element_by_id("CreatePassword").send_keys(password_generator)
        driver.find_element_by_xpath("//form[@id='create_customer']//input[@class='btn']").click()
        time.sleep(2)

    def test_04_empty_cart(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_class_name("cart-page-link").click()
        assert "Your cart is currently empty" in driver.page_source
        assert driver.find_elements_by_css_selector("p.cart--empty-message") == "Your cart is currently empty."

    def test_05_add_product_to_cart(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_link_text('Products').click()
        all_items = driver.find_elements_by_css_selector('p.grid-link__title')
        item = all_items[randint(0, len(all_items) - 1)]
        print(item.text)
        item.click()
        driver.find_element_by_id('AddToCart').click()
        assert "Your Shopping Cart" in driver.title
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn"))
        )
        driver.find_element_by_class_name('cart__remove').click()
        assert "Your cart is currently empty" in driver.page_source

    def test_06_valid_search(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        search_term = 'Chicken'
        search_field = driver.find_element_by_xpath("//div[@class='header-bar__right post-large--display-table-cell']//input[@placeholder='Search']")
        search_field.send_keys(search_term)
        search_field.send_keys(Keys.RETURN)
        try:
            assert search_term in driver.title
            print("Assertion Test Passed")
        except Exception as e:
            print("Assertion Test Failed", format(e))

    def test_07_homepage_redirection(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        assert 'Home' in driver.title

    def test_08_products_page_redirection(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_link_text('Products').click()
        assert 'Products' in driver.title


    def test_09_recipe_page_redirection(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_link_text('Recipe').click()
        assert 'Recipe' in driver.title

    def test_10_about_us_page_redirection(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_link_text('About Us').click()
        assert 'About Us' in driver.title

    @unittest.skip("Due to reCAPTCHA skip it")
    def test_11_contact_us_form_submission(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_xpath("//a[@class='site-nav__link'][contains(text(),'Contact Us')]").click()
        name_generator = 'Azad' + str(random.randint(0, 99))
        driver.find_element_by_id('ContactFormName').send_keys(name_generator)
        driver.find_element_by_id('ContactFormEmail').send_keys(name_generator+'@gmail.com')
        driver.find_element_by_id('ContactFormMessage').send_keys('Test message, please ignore')
        driver.find_element_by_xpath("//input[@class='btn right']").click()
        assert "Thanks for contacting us. We'll get back to you as soon as possible." in driver.page_source

    def test_12_all_collections(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        collections = ["Meat", "Fish", "Spices", "Ghee", "Vegetable", "Frozen", "Rice", "Sweets"]
        for collection_name in collections:
            driver.find_element_by_link_text('Home').click()
            driver.find_element_by_partial_link_text(collection_name).click()
            assert collection_name in driver.title

    def test_13_latest_news(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        driver.find_element_by_link_text('Latest News').click()
        assert 'News' in driver.title

    def test_14_links_from_footer(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        footer_partial_link_text = ["Search", "Contact", "Privacy", "Terms", "Delivery"]
        for link in footer_partial_link_text:
            driver.find_element_by_link_text('Home').click()
            driver.find_element_by_partial_link_text(link).click()
            assert link in driver.title

    def test_15_follow_us_from_footer(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        try:
            driver.find_elements_by_xpath("//ul[@class='inline-list social-icons']")
        except NoSuchElementException:
            return False
        return True

    @unittest.skip("Due to reCAPTCHA skip it")
    def test_16_subscribe(self):
        driver = self.driver
        driver.find_element_by_link_text('Home').click()
        email_generator = 'username'+str(random.randint(0, 999))+'@gmail.com'
        driver.find_element_by_id('Email').clear()
        driver.find_element_by_id('Email').send_keys(email_generator)
        driver.find_element_by_id('subscribe').click()
        if driver.find_elements_by_css_selector('p.note form-success'):
            print ("Element exists")
        else:
            print("No such element exist")


    def test_17_complete_checkout_cash_on_delivery(self):
        driver = self.driver
        driver.find_element_by_xpath("//a[@class='site-nav__link'][contains(text(),'Products')]").click()
        all_items = driver.find_elements_by_css_selector('p.grid-link__title')
        item = all_items[randint(0, len(all_items) - 1)]
        print(item.text)
        item.click()
        driver.find_element_by_id('AddToCartText').click()
        driver.find_element_by_name('checkout').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout_email_or_phone"))
        )
        driver.find_element_by_xpath("//input[@id='checkout_email_or_phone']").send_keys('username'+str(random.randint(0,999))+'@gmail.com')
        driver.find_element_by_id('checkout_shipping_address_last_name').send_keys('LastName'+str(random.randint(0,99)))
        driver.find_element_by_id('checkout_shipping_address_address1').send_keys('Tester Lane'+str(random.randint(0,99)))
        city = ["Tallinn", "Tartu", "Parnu"]
        driver.find_element_by_id('checkout_shipping_address_city').send_keys(random.choice(city))
        driver.find_element_by_id('checkout_shipping_address_zip').send_keys(random.randint(10000,15000))
        driver.find_element_by_xpath("//button[@id='continue_button']").click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "continue_button"))
        )
        driver.find_element_by_xpath("//button[@id='continue_button']").click()

        driver.find_element_by_xpath("//input[@id='checkout_payment_gateway_47481028746']").click()
        time.sleep(1)
        driver.find_element_by_id("continue_button").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "os-order-number"))
        )
        assert 'Thank you for your purchase' in driver.title
        print(driver.find_element_by_class_name('os-order-number'))
        driver.find_element_by_link_text("Continue shopping").click()

    def test_18_complete_checkout_by_discount_code(self):
        driver = self.driver
        driver.find_element_by_xpath("//a[@class='site-nav__link'][contains(text(),'Products')]").click()
        all_items = driver.find_elements_by_css_selector('p.grid-link__title')
        item = all_items[randint(0, len(all_items) - 1)]
        print(item.text)
        item.click()
        driver.find_element_by_id('AddToCartText').click()
        driver.find_element_by_name('checkout').click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout_email_or_phone"))
        )
        driver.find_element_by_id('checkout_reduction_code').send_keys('TALTECH')
        driver.find_element_by_id('checkout_reduction_code').send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//input[@id='checkout_email_or_phone']").send_keys('username'+str(random.randint(0,999))+'@gmail.com')
        driver.find_element_by_id('checkout_shipping_address_last_name').send_keys('LastName'+str(random.randint(0,99)))
        driver.find_element_by_id('checkout_shipping_address_address1').send_keys('Tester Lane'+str(random.randint(0,99)))
        city = ["Tallinn", "Tartu", "Parnu"]
        driver.find_element_by_id('checkout_shipping_address_city').send_keys(random.choice(city))
        driver.find_element_by_id('checkout_shipping_address_zip').send_keys(random.randint(10000,15000))

        driver.find_element_by_xpath("//button[@id='continue_button']").click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "continue_button"))
        )
        driver.find_element_by_xpath("//button[@id='continue_button']").click()
        driver.find_element_by_id("continue_button").click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "os-order-number"))
        )
        assert 'Thank you for your purchase' in driver.title
        print(driver.find_element_by_class_name('os-order-number'))


    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='/Users/azad/Desktop/IgavestiWithoutPOM/Reports'))