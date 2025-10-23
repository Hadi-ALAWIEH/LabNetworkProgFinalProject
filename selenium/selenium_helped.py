from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, csv

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)

def handle_more_info_movie_popup(driver, movie_counter):
    print("Opening popup for more movie info...")

    more_movie_info_buttons = driver.find_elements(By.CSS_SELECTOR, "button.li-info-icon")
    scroll_into_view(driver, more_movie_info_buttons[movie_counter])
    more_movie_info_buttons[movie_counter].click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sc-6ef24fae-0.doAmzT")))
    popup_container = driver.find_element(By.CLASS_NAME, "sc-6ef24fae-0.doAmzT")

    # Genre
    genre_list = popup_container.find_elements(By.CSS_SELECTOR, 'ul[data-testid="btp_gl"] li')
    genres = ", ".join([g.text for g in genre_list]) if genre_list else "No Genre Info"

    # Director(s)
    director_elems = popup_container.find_elements(By.CSS_SELECTOR, 'a[href*="/name/"]')
    directors = director_elems[0].text if director_elems else "Unknown Director"

    # Stars (in popup, same pattern as directors)
    stars = ", ".join([a.text for a in director_elems[1:4]]) if len(director_elems) > 1 else "Unknown Stars"

    close_movie_popup(driver)
    return genres, directors, stars

def close_movie_popup(driver):
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Close Prompt"]')))
    close_button.click()
    time.sleep(1)

def add_to_dict_list(movie_title, movie_year, movie_duration, pg_r_rating, movie_metascore, genre, director, actors, description):
    movie_dict = {
        "title": movie_title,
        "year": movie_year,
        "duration": movie_duration,
        "rating": pg_r_rating,
        "metascore": movie_metascore,
        "genre": genre,
        "director": director,
        "actors": actors,
        "description": description
    }
    movies.append(movie_dict)
    print(f"Added movie: {movie_title}")

def write_to_csv(movies, filename="movies.csv"):
    keys = movies[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(movies)
    print(f"Wrote {len(movies)} movies to {filename}.")

# --- MAIN LOGIC ---
driver = webdriver.Chrome()
url = "https://www.imdb.com/list/ls063676189/"
driver.get(url)
wait = WebDriverWait(driver, 10)
movies = []

movie_containers = driver.find_elements(By.CLASS_NAME, "irNIzX")
print(f"Found {len(movie_containers)} movies.\n")

for movie_counter, movie in enumerate(movie_containers):
    scroll_into_view(driver, movie)

    # Movie title
    movie_title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split(". ")[1]
    inner_spans = movie.find_elements(By.CSS_SELECTOR, "span.dli-title-metadata-item")

    movie_year = inner_spans[0].text if len(inner_spans) > 0 else "N/A"
    movie_duration = inner_spans[1].text if len(inner_spans) > 1 else "N/A"
    pg_r_rating = inner_spans[2].text if len(inner_spans) > 2 else "Not Rated"
    movie_metascore = movie.find_elements(By.CSS_SELECTOR, ".metacritic-score-box")
    movie_metascore = movie_metascore[0].text if movie_metascore else "No Metascore"
    print("Title:", movie_title)
    print("Year:", movie_year)
    print("Duration:", movie_duration)
    print("PG/R Rating:", pg_r_rating)
    print("Metascore:", movie_metascore)


    # Description
    description_elems = movie.find_elements(By.CSS_SELECTOR, ".ipc-html-content-inner-div, .ipc-html-content.ipc-html-content--base")
    description = description_elems[0].text if description_elems else "No Description"
    print("The description is:", description)

    # Directors & Stars from movie card
    directors = ", ".join([a.text for a in movie.find_elements(By.CSS_SELECTOR, ".title-description-credit a")[:1]]) or "Unknown Director"
    stars = ", ".join([a.text for a in movie.find_elements(By.CSS_SELECTOR, ".title-description-credit a")[1:4]]) or "Unknown Stars"
    print("Directors from card:", directors)
    print("Stars from card:", stars)


    # Get genre, director, stars from popup
    genre, popup_director, popup_stars = handle_more_info_movie_popup(driver, movie_counter)

    add_to_dict_list(movie_title, movie_year, movie_duration, pg_r_rating,
                     movie_metascore, genre, popup_director or directors,
                     popup_stars or stars, description)

    print(f"Processed movie #{movie_counter + 1}: {movie_title}")
    print("--------------------------------------------------\n")

write_to_csv(movies)
driver.quit()
