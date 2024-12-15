from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv 

def wait_for_element(driver, by, value, condition=EC.presence_of_element_located, timeout=10):
    """
    Utility function to wait for a web element to meet a condition.
    """
    return WebDriverWait(driver, timeout).until(condition((by, value)))

# Step 1: Set up ChromeDriver
driver = webdriver.Chrome()

try:
    # Step 2: Navigate to the Books to Scrape website
    driver.get("http://books.toscrape.com/")

    scraped_data = []

    page_counter = 0
    while page_counter < 3:
        # Step 3: Extract data from the current page
        books = driver.find_elements(By.XPATH, "//article[@class='product_pod']")

        for book in books:
            # Re-locate elements for each book on the current page
            try:
                # Extract title
                title = book.find_element(By.TAG_NAME, "h3").text
                # Extract price
                price = book.find_element(By.CLASS_NAME, "price_color").text
                # Extract link
                link = book.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                scraped_data.append({"title": title, "price": price, "link": link})
            except Exception as e:
                print(f"Error processing book: {e}")
                continue

        # Step 4: Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow time for scrolling

        # Step 5: Check for and click the "Next" button if available
        try:
            next_button = wait_for_element(driver, By.LINK_TEXT, "next", EC.element_to_be_clickable)
            next_button.click()
            time.sleep(2)  # Allow time for the next page to load
        except Exception:
            print("No more pages to scrape.")
            break

        page_counter += 1

    # Print the scraped data
    # for i, book in enumerate(scraped_data, 1):
    #     print(f"{i}. Title: {book['title']}, Price: {book['price']}, Link: {book['link']}")

    # Step 6: Export the scraped data to a CSV file
    with open("scraped_books.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "price", "link"])
        writer.writeheader()
        writer.writerows(scraped_data)
    print("Data has been saved to scraped_books.csv")

finally:
    # Step 6: Close the browser
    driver.quit()
