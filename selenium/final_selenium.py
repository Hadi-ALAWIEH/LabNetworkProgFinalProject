from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

# columns that I have scraped in selenium:
columns = [
    "title",
    "release_date",
    "year",
    "original_language",
    "runtime",
    "genres",
    "budget",
    "revenue",
    "vote_average",
    "director",
    "top_actors",
    "overview",
    "pg_rating",
    "original_title",
    "movie_keywords"
]

page_count_upper_limit = 10  # this should reach 50 so that we have 1000 movies

driver = webdriver.Chrome()

# open CSV file for writing
with open("tmdb_movies_continued.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    for page_counter in range(9, page_count_upper_limit): # tweak this to incrementally get more data from a "middle" page, for now keep this for a single page for testing
        driver.get(f"https://www.themoviedb.org/movie?page={page_counter}")

        # wait until the movie titles appear
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.style_1 h2 a"))
        )

        # scroll to load all movie cards
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        movie_links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "div.card.style_1 h2 a")]
        print(f"Found {len(movie_links)} movies.")

        for i, url in enumerate(movie_links[:20]):
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

                ordered_list_managers = driver.find_element(By.CSS_SELECTOR, "ol.people.no_image").find_elements(By.TAG_NAME, "li")
                director = ordered_list_managers[0].find_element(By.CSS_SELECTOR, "p").text.strip()

                side_facts = driver.find_element(By.CSS_SELECTOR, "section.facts.left_column")

                original_title_element = side_facts.find_elements(By.CSS_SELECTOR, "p.wrap")
                if original_title_element:
                    original_title = original_title_element[0].text.replace("Original Title", "", 1).strip()
                else:
                    original_title = "No original title"

                try:
                    original_language = side_facts.find_elements(By.TAG_NAME, "p")[1].text if original_title == "No original title" else side_facts.find_elements(By.TAG_NAME, "p")[2].text
                    original_language = original_language.replace("Original Language", "", 1).strip()
                    original_languages = original_language.split(";")
                except:
                    original_languages = "No original language found"

                try:
                    budget = side_facts.find_elements(By.TAG_NAME, "p")[2].text if original_title == "No original title" else side_facts.find_elements(By.TAG_NAME, "p")[3].text
                    budget = budget.replace("Budget", "", 1).strip()
                    if budget == " -":
                        budget = "No budget found"
                except:
                    budget = "No budget found"

                try:
                    revenue = side_facts.find_elements(By.TAG_NAME, "p")[3].text if original_title == "No original title" else side_facts.find_elements(By.TAG_NAME, "p")[4].text
                    revenue = revenue.replace("Revenue", "", 1).strip()
                    if revenue == " -":
                        revenue = "No revenue found"
                except:
                    revenue = "No revenue found"

                try:
                    keywords_section = driver.find_element(By.CSS_SELECTOR, "section.keywords.right_column")
                    ul_tag = keywords_section.find_element(By.TAG_NAME, "ul")
                    movie_keywords = [li.text for li in ul_tag.find_elements(By.TAG_NAME, "li")]
                except:
                    movie_keywords = ["No keywords"]

                try:
                    top_stars_ol = driver.find_element(By.CSS_SELECTOR, "ol.people.scroller")
                    top_stars_li = top_stars_ol.find_elements(By.TAG_NAME, "li")[:3]
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
                print("Original Languages:", original_languages)
                print("Original Title:", original_title)
                print("Budget:", budget)
                print("Revenue:", revenue)
                print("Keywords", movie_keywords)
                print("Director:", director)
                print("Top stars", top_stars_list)

                # Write movie to CSV
                writer.writerow({
                    "title": title,
                    "release_date": release,
                    "year": year,
                    "original_language": ", ".join(original_languages) if isinstance(original_languages, list) else original_languages,
                    "runtime": duration,
                    "genres": genres,
                    "budget": budget,
                    "revenue": revenue,
                    "vote_average": user_score,
                    "director": director,
                    "top_actors": ", ".join(top_stars_list),
                    "overview": overview,
                    "pg_rating": pg_rating,
                    "original_title": original_title,
                    "movie_keywords": ", ".join(movie_keywords),
                })

            except Exception as e:
                print(f"Error scraping movie {i+1}: {e}")

        print(f"Completed page {page_counter}. Moving to next page...")
        time.sleep(2)

driver.quit()
