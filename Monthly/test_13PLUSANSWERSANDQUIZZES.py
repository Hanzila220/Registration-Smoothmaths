import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class TestSmoothMathsRegistrationPage:

    def setup_method(self, method):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Headless mode for CI
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def teardown_method(self, method):
        self.driver.quit()

    def test_registration_page(self):
        self.driver.get("https://smoothmaths.co.uk/register/13-plus-answers-and-quizzes")
        self.driver.maximize_window()

        # Fill the form with dummy data
        try:
            self.driver.find_element(By.NAME, "username").send_keys("testuser")
            self.driver.find_element(By.NAME, "email").send_keys("testuser@example.com")
            self.driver.find_element(By.NAME, "password").send_keys("TestPassword123")
            self.driver.find_element(By.NAME, "confirm_password").send_keys("TestPassword123")

            self.driver.find_element(By.NAME, "billing_first_name").send_keys("Test")
            self.driver.find_element(By.NAME, "billing_last_name").send_keys("User")
            self.driver.find_element(By.NAME, "billing_address_1").send_keys("123 Test Street")
            self.driver.find_element(By.NAME, "billing_city").send_keys("Test City")
            self.driver.find_element(By.NAME, "billing_postcode").send_keys("12345")
            self.driver.find_element(By.ID, "select2-billing_country-container").click()
            self.driver.find_element(By.XPATH, "//li[contains(text(),'United Kingdom (UK)')]").click()

            # Submit the form
            self.driver.find_element(By.NAME, "register").click()

            # Wait for success or failure
            success_message = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-message"))
            )
            assert "successful" in success_message.text, "Registration was not successful"
            print("Test passed: Registration successful.")
            self.driver.save_screenshot('screenshots/registration_success.png')

        except Exception as e:
            self.driver.save_screenshot('screenshots/registration_failed.png')
            print("Test failed: Registration failed.")
            assert False, f"Error occurred: {e}"

