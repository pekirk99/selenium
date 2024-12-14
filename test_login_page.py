from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, by, value, condition=EC.presence_of_element_located, timeout=10):
    """
    Waits for a specific condition on a web element.

    Parameters:
        driver (WebDriver): The Selenium WebDriver instance.
        by (By): The method to locate the element (e.g., By.ID, By.XPATH).
        value (str): The value to locate the element (e.g., ID or XPath string).
        condition (expected_conditions): The expected condition to wait for (default is presence_of_element_located).
        timeout (int): The maximum time to wait (in seconds). Default is 10 seconds.

    Returns:
        WebElement: The located WebElement after the condition is met.
    """
    return WebDriverWait(driver, timeout).until(condition((by, value)))


# Set up ChromeDriver
driver = webdriver.Chrome()  # ChromeDriver is automatically picked up from /usr/local/bin

try:
    # Navigate to the Practice Testing website
    driver.get("https://practice.expandtesting.com/")

    # Locate the web login link
    # Use the By class to locate the element based on its text attributes
    web_login_link = wait_for_element(driver, By.LINK_TEXT, "Test Login Page", EC.element_to_be_clickable)
    web_login_link.click()

    # Wait for login form to appear
    username_input = wait_for_element(driver, By.NAME, "username", EC.presence_of_element_located)
    password_input = wait_for_element(driver, By.NAME, "password", EC.presence_of_element_located)
    login_button = wait_for_element(driver, By.XPATH, "//button[text()='Login']", EC.element_to_be_clickable)

    # Add username and password to fields
    username_input.send_keys("practice")
    password_input.send_keys("SuperSecretPassword!")

    # Submit credentials
    login_button.click()

    # Verify successful login 
    success_message = wait_for_element(driver, By.XPATH, "//b[text()='You logged into a secure area!']", EC.presence_of_element_located )
    print("Login successful:", success_message.text)


finally:
    # Step 6: Close the browser
    driver.quit()