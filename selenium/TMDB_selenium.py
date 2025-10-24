# TODO: you still need to handle the budget, the revenue and the original language, and the director and writer of the movie, all other fields are done
'''
# columns that I have scraped in selenium:
title
year
user score
pg_rating
release
genres
duration
overview
original_title
status
movie keywords
top stars

# columns that I still need to scrape in selenium:
budget
revenue
original language
director
writer
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()
driver.get("https://www.themoviedb.org/movie")

# wait until the movie titles appear
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.style_1 h2 a"))
)

# scroll to load all movie cards (TMDB loads more as you scroll)
last_height = driver.execute_script("return document.body.scrollHeight")
for _ in range(2):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# get all movie URLs safely ( I can update this later by adding a loop that paginates through all the pages, to get even a larger list of movie links)
movie_links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "div.card.style_1 h2 a")]
print(f"Found {len(movie_links)} movies.")

for i, url in enumerate(movie_links[:20]):  # limit to first 5
    driver.get(url)
    time.sleep(2)

    print(f"\n=== Movie {i+1} ===")

    try:
        title = driver.find_element(By.CSS_SELECTOR, "div.title.ott_false h2 a").text
        year = driver.find_element(By.CSS_SELECTOR, "div.title.ott_false h2 span").text
        user_score = driver.find_element(By.CSS_SELECTOR, "div.user_score_chart").get_attribute("data-percent")

        pg_rating = driver.find_element(By.CSS_SELECTOR, "span.certification").text.strip() if driver.find_elements(By.CSS_SELECTOR, "span.certification") else "Not Rated"
        release = driver.find_element(By.CSS_SELECTOR, "span.release").text.strip() if driver.find_elements(By.CSS_SELECTOR, "span.release") else "No release date"
        genres = driver.find_element(By.CSS_SELECTOR, "span.genres").text.strip() if driver.find_elements(By.CSS_SELECTOR, "span.genres") else "No genres"
        duration = driver.find_element(By.CSS_SELECTOR, "span.runtime").text.strip() if driver.find_elements(By.CSS_SELECTOR, "span.runtime") else "No duration"
        overview = driver.find_element(By.CSS_SELECTOR, "div.overview p").text.strip() if driver.find_elements(By.CSS_SELECTOR, "div.overview p") else "No overview"
        # locate the "Facts" section on the left column
        side_facts = driver.find_element(By.CSS_SELECTOR, "section.facts.left_column")

        # try to get the "original title"
        original_title_element = side_facts.find_elements(By.CSS_SELECTOR, "p.wrap")
        if original_title_element:
            original_title = original_title_element[0].text.replace("Original Title", "", 1).strip()
        else:
            original_title = "No original title"

        # keywords
        try:
            keywords_section = driver.find_element(By.CSS_SELECTOR, "section.keywords.right_column")
            ul_tag = keywords_section.find_element(By.TAG_NAME, "ul")
            movie_keywords = [li.text for li in ul_tag.find_elements(By.TAG_NAME, "li")]
        except:
            movie_keywords = ["No keywords"]

        # top 3 stars
        try:
            top_stars_ol = driver.find_element(By.CSS_SELECTOR, "ol.people.scroller")
            top_stars_li = top_stars_ol.find_elements(By.TAG_NAME, "li")[:3]  # limit to 3
            top_stars_list = [li.find_element(By.TAG_NAME, "p").find_element(By.TAG_NAME, "a").text for li in top_stars_li]
        except:
            top_stars_list = ["No stars found"]

        print("Title:", title)
        print("Year:", year)
        print("User Score:", user_score)
        print("PG Rating:", pg_rating)
        print("Release:", release)
        print("Genres:", genres)
        print("Duration:", duration)
        print("Overview:", overview)
        print("Original Title:", original_title)
        print("Keywords", movie_keywords)
        print("Top stars", top_stars_list)

    except Exception as e:
        print(f"Error scraping movie {i+1}: {e}")

driver.quit()
