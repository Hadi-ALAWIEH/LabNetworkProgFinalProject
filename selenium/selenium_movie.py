from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
url = "https://www.imdb.com/search/title/?groups=top_1000"
driver.get(url)

wait = WebDriverWait(driver, 10)

for i in range(3):
    try:
        button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.ipc-see-more__button")
        ))
        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)  # short pause after scroll
        button.click()
        print(f"Clicked {i+1} times")
        time.sleep(5)  # wait for movies to load
    except Exception as e:
        print(f"Stopped at click {i+1}: {e}")
        break

print("✅ Finished clicking 20 times.")


movie_containers = driver.find_elements(By.CLASS_NAME, "sc-caa65599-0.irNIzX")
print(f"Found {len(movie_containers)} movies.")
for movie in movie_containers:
    movie_title = movie.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a").text.split(". ")[1]
    print(f"The title of this movie is : {movie_title}")

    date_inner_container = movie.find_elements(By.TAG_NAME, "div")[1]
    inner_container_spans = date_inner_container.find_elements(By.TAG_NAME, "span")

    movie_year = inner_container_spans[0].text
    movie_duration = inner_container_spans[1].text
    pg_r_rating = inner_container_spans[2].text if len(inner_container_spans) > 2 else "Not Rated"
    movie_metascore = inner_container_spans[3].find_elements(By.TAG_NAME, "span")[0].text if len(inner_container_spans) > 3 else "No Metascore"

    # todo: add the info for each movie to a dictionary so that you can write the dictionary to a csv file for model training later

    print(f"The year of this movie is : {movie_year}\n")
    print(f"The duration of this movie is : {movie_duration}\n")
    print(f"The R rating of this movie is : {pg_r_rating}\n")
    print(f"The metascore of this movie is : {movie_metascore}\n")
    print("-------------------------------------------------\n")

time.sleep(5)
driver.quit()
