import time
import selenium.webdriver as webdriver

driver = webdriver.Chrome()
driver.get("https://www.booking.com/?aid=355028&chal_t=1760954378449&force_referer=")

time.sleep(5)
driver.quit()
