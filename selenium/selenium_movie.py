from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)

def handle_more_info_movie_popup(driver, movie_counter):
    # TODO: to enter the popup for each movie and get more info like genre, director, actors, description, etc.
    print("Opening popup for more movie info...")

    # find the button to open the popup and click it
    more_movie_info_button_class = "ipc-icon-button.li-info-icon.ipc-icon-button--base.ipc-icon-button--onAccent2"
    more_movie_info_button = driver.find_elements(By.CLASS_NAME, more_movie_info_button_class)[movie_counter]
    more_movie_info_button.click()
    time.sleep(5)  # wait for popup to load

    # wait for the popup container to be present and get it
    outer_popup_container_class = "sc-6ef24fae-0.doAmzT"
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, outer_popup_container_class)))
    popup_container = driver.find_element(By.CLASS_NAME, outer_popup_container_class)

    # the same class is used for both directors and stars lists, so we will get both and differentiate by index
    directors_and_stars_list_class = "ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--inline.baseAlt"
    directors_and_stars_list = popup_container.find_elements(By.CLASS_NAME, directors_and_stars_list_class)
    # print(f"Found {len(directors_and_stars_list)} lists for directors and stars.")

    directors_list = directors_and_stars_list[2]
    director_items = directors_list.find_elements(By.TAG_NAME, "li")
    directors = ", ".join([item.text for item in director_items if item.text]) or "Unknown Director"

    starts_list = directors_and_stars_list[3]
    star_items = starts_list.find_elements(By.TAG_NAME, "li")
    stars = ", ".join([item.text for item in star_items if item.text]) or "Unknown Stars"

    # print("Directors:", directors)
    # print("Stars:", stars)
    #

    # --- Extract the genre list from the popup ---
    genre_ul = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="btp_gl"]'))
    )
    genre_items = genre_ul.find_elements(By.TAG_NAME, "li")
    genres = ", ".join([item.text for item in genre_items if item.text]) or "No Genre Info"
    # print("Genres:", genres)
    return genres, directors, stars


def close_movie_popup(driver):
    close_popup_button = driver.find_elements(By.CSS_SELECTOR, '[title="Close Prompt"]')[0]
    close_popup_button.click()
    time.sleep(2)  # wait for popup to close


# this is a function to add a movie's info to the movies list as a dictionary
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
    print(f"Added movie: {movie_title} to the list.")


# this is a function to write the list of movie dictionaries to a csv file
def write_to_csv(movies, filename="movies.csv"):
    keys = movies[0].keys()
    with open (filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(movies)
    print(f"Wrote {len(movies)} movies to {filename}.")



# this is a list of dicts for all the movies
movies = []

driver = webdriver.Chrome()
# url = "https://www.imdb.com/search/title/?groups=top_1000"
url = "https://www.imdb.com/list/ls063676189/"
driver.get(url)

# create a wait object
wait = WebDriverWait(driver, 10)

# load the containers of the movies
movie_containers = driver.find_elements(By.CLASS_NAME, "sc-caa65599-0.irNIzX")

# print the number of movies found
print(f"Found {len(movie_containers)} movies.")

# this is a counter to keep track of which movie we are processing
movie_counter = 0

for movie in movie_containers:
    data_inner_container = movie.find_elements(By.TAG_NAME, "div")[1] # this is the inner container that contains the year, duration, pg/r rating, and metascore
    # rating_and_voting_span = movie.find_element(By.TAG_NAME, "span") # this will return a span element
    rating_and_voting_span = driver.find_elements(By.CLASS_NAME, "sc-caa65599-1.dBwcUJ")[movie_counter]
    rating_and_voting = rating_and_voting_span.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").find_elements(By.TAG_NAME, "span")
    # print(len(rating_and_voting))

    print(rating_and_voting_span.text)
    inner_container_spans = data_inner_container.find_elements(By.TAG_NAME, "span")

    # extract the movie title directly from the movie container
    movie_title = movie.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a").text.split(". ")[1]

    # extract the year, duration, pg/r rating, and metascore from the inner_container_spans inside the data_inner_container
    movie_year = inner_container_spans[0].text
    movie_duration = inner_container_spans[1].text
    pg_r_rating = inner_container_spans[2].text if len(inner_container_spans) > 2 else "Not Rated"
    movie_metascore = inner_container_spans[3].find_elements(By.TAG_NAME, "span")[0].text if len(inner_container_spans) > 3 else "No Metascore"

    # span > div > span > spans ( two of them )

    movie_rating = rating_and_voting[0].text
    vote_count =  rating_and_voting[1].text

    # movie_description = driver.find_elements(By.CLASS_NAME, "ipc-html-content-inner-div")[movie_counter].text

    # todo: call the function to handle the popup for more movie info
    genres_of_current_movie, directors_of_current_movie, stars_of_current_movie = handle_more_info_movie_popup(driver, movie_counter)
    close_movie_popup(driver)

    # todo: add the info for each movie to a dictionary so that you can write the dictionary to a csv file for model training later
    # write_to_csv(movies, filename="movies.csv")



    # make sure of the output of the 11 columns ( 10 of them being features and 1 of them being the target )
    print("Processing movie number:", movie_counter)
    print(f"The title of this movie is : {movie_title}\n")
    print(f"The year of this movie is : {movie_year}\n")
    print(f"The duration of this movie is : {movie_duration}\n")
    print(f"The R rating of this movie is : {pg_r_rating}\n")
    print(f"The metascore of this movie is : {movie_metascore}\n")
    print(f"The actual rating of this movie is : {movie_rating}\n")
    print(f"The vote count of this movie is : {vote_count}\n")
    print(f"The genres of this movie is : {genres_of_current_movie}\n")
    print(f"The description of this movie is : {movie_metascore}\n")
    print(f"The directors of this movie are : {directors_of_current_movie}\n")
    print(f"The stars of this movie are : {stars_of_current_movie}\n")
    print("-------------------------------------------------\n")

    movie_counter += 1
    scroll_into_view(driver, movie)


time.sleep(5)
driver.quit()

'''
span > div > span > spans ( two of them )
ipc-icon-button li-info-icon ipc-icon-button--base ipc-icon-button--onAccent2
ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline baseAlt
'''

