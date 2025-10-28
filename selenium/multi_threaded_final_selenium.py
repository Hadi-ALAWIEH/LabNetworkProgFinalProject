from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

columns = [
    "title", "release_date", "year", "original_language", "runtime", "genres",
    "budget", "revenue", "vote_average", "director", "top_actors", "overview",
    "pg_rating", "original_title", "movie_keywords"
]

# page_count_upper_limit = 10
page_count_upper_limit = 1 # keep this at 1 for testing; change to 50 for full run
csv_lock = Lock()


def scrape_movie(driver, url):
    """Scrape a single movie using an existing WebDriver instance."""
    driver.get(url)
    time.sleep(2)

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
        original_title = (
            original_title_element[0].text.replace("Original Title", "", 1).strip()
            if original_title_element else "No original title"
        )

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

        return {
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
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def scrape_page(page_url, writer):
    """Scrape one TMDB page sequentially for movies."""
    driver = webdriver.Chrome()
    driver.get(page_url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.card.style_1 h2 a"))
        )

        # Scroll to load all cards
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        movie_links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "div.card.style_1 h2 a")]
        print(f"[{page_url}] Found {len(movie_links)} movies.")

        for i, url in enumerate(movie_links[:20]):
            data = scrape_movie(driver, url)
            if data:
                with csv_lock:
                    writer.writerow(data)

        print(f"[{page_url}] Completed successfully.")
    except Exception as e:
        print(f"Error scraping page {page_url}: {e}")
    finally:
        driver.quit()


# Build list of page URLs
page_urls = [f"https://www.themoviedb.org/movie?page={i}" for i in range(1, page_count_upper_limit + 1)]

# MAIN EXECUTION
with open("parallel_pages_selenium_movies.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    # Parallelize by page
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(scrape_page, url, writer) for url in page_urls]
        for future in as_completed(futures):
            future.result()  # wait for each to finish safely
