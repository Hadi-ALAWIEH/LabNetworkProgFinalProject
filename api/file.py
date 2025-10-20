import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.booking.com/cars/index.en-gb.html?label=gen173rf-10EgRjYXJzKIICOOgHSDNYA2iCAYgBApgBM7gBCcgBEdgBA-gBAfgBAYgCAZgCIqgCAbgCzLbYxwbAAgHSAiRiZGEwN2YyMS1iYjFjLTQ2MjItOTkxOC01ZDhkZGY0N2UyZmLYAgHgAgE&sid=472edebd96db9eef5fdd82da82446bfe&aid=304142&adplat=cross_product_bar&selected_currency=USD")

# # go to the home page and search for Lebanon as a location for accommodation
# search_for_location = driver.find_element(By.CSS_SELECTOR, ".b915b8dc0b")
# search_for_location.send_keys("Lebanon")
#
# # try to select dates from the date picker
# # start_date_button_class = ".bui-calendar__date.bui-calendar__date--selected"
# # end_date_button_class = ".bui-calendar__date.bui-calendar__date--selected"
#
#
# # find the button that lets you select currency
# select_usa_currency_class = "CurrencyPicker_currency.CurrencyPicker_currency--active"
# select_currency_button_class = "de576f5064.b46cd7aad7.e26a59bb37.dda427e6b5.acb3638563"
#
# select_currency_button = driver.find_element(By.CSS_SELECTOR, f".{select_currency_button_class}")
# select_currency_button.click()
#
# time.sleep(2)  # wait for the currency options to load
#
# select_usa_currency_button = driver.find_element(By.CSS_SELECTOR, f".{select_usa_currency_class}")
# select_usa_currency_button.click()
#
# time.sleep(2)  # wait for the search button to be clickable
#
# # hit the search button after selecting the dates
# search_button_class = "ca2ca5203b"
# search_button = driver.find_element(By.CSS_SELECTOR, f".{search_button_class}")
# search_button.click()
#
#
# # time.sleep(5)
# # find and print the first apartment div
# # apartment_div_class = ".c3bdfd4ac2.a0ab5da06c.d46ff48a92.f728e61e72.d0acd69e66.c256f1a28a.bc2204a477.fd0a104462.f74ae46b12"
# # first_apartment = driver.find_elements(By.CSS_SELECTOR, apartment_div_class)[0]
# # print(first_apartment)

time.sleep(10)
driver.quit()
