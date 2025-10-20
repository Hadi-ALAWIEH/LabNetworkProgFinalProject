import time
import selenium.webdriver as webdriver
import selenium.webdriver.common.by as By

driver = webdriver.Chrome()
driver.get("https://www.booking.com/?aid=355028&chal_t=1760954378449&force_referer=")

search_for_location = driver.find_element(By.CLASS_NAME, "b915b8dc0b")
search_for_location.send_keys("Lebanon")

time.sleep(5)
driver.quit()
