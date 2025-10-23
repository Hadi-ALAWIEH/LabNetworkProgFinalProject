from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.chrome.options import Options


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def handle_more_info_movie_popup(driver, movie):
    try:
        # Click "More Info" button
        more_info_button = movie.find_element(By.CSS_SELECTOR, "button.ipc-btn")
        driver.execute_script("arguments[0].click();", more_info_button)

        # Wait until popup appears (was sleep(5))
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-6ef24fae-0.doAmzT"))
        )

        # Extract description
        description_elem = movie.find_element(By.CSS_SELECTOR, ".ipc-html-content-inner-div")
        description = description_elem.text if description_elem else "No description"

        # Close popup
        close_button = movie.find_element(By.CSS_SELECTOR, "button.ipc-icon-button")
        driver.execute_script("arguments[0].click();", close_button)

        # Wait for popup to disappear (was sleep(2))
        WebDriverWait(driver, 1).until_not(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-6ef24fae-0.doAmzT"))
        )

        return description

    except Exception:
        return "No description"


# ---------------- MAIN EXECUTION ----------------

# Headless mode for faster execution
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(1)  # small global implicit wait

url = "https://www.imdb.com/search/title/?genres=action&explore=title_type,genres"
driver.get(url)

# Wait until movie list loads
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ipc-metadata-list-summary-item"))
)

movies = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item")
print(f"Found {len(movies)} movies.\n")

# Optional: limit for testing
# movies = movies[:20]

data = []

for movie_counter, movie in enumerate(movies, start=1):
    scroll_into_view(driver, movie)

    try:
        title_elem = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text")
        movie_title = title_elem.text if title_elem else "No Title"

        inner_container_spans = movie.find_elements(By.CSS_SELECTOR, ".cli-title-metadata-item")
        movie_year = inner_container_spans[0].text if len(inner_container_spans) > 0 else "No Year"
        movie_duration = inner_container_spans[1].text if len(inner_container_spans) > 1 else "No Duration"
        pg_r_rating = inner_container_spans[2].text if len(inner_container_spans) > 2 else "Not Rated"
        movie_metascore = (
            inner_container_spans[3].find_elements(By.TAG_NAME, "span")[0].text
            if len(inner_container_spans) > 3 else "No Metascore"
        )

        description = handle_more_info_movie_popup(driver, movie)

        print(f"{movie_counter}. {movie_title} | {movie_year} | {movie_duration} | {pg_r_rating} | {movie_metascore}")

        data.append([movie_title, movie_year, movie_duration, pg_r_rating, movie_metascore, description])

    except Exception as e:
        print(f"Error on movie {movie_counter}: {e}")

# Save to CSV
with open("movies.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Year", "Duration", "Rating", "Metascore", "Description"])
    writer.writerows(data)

driver.quit()
print("\nScraping completed and saved to movies.csv ✅")
