from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def handle_more_info_movie_popup(driver, movie_counter):
    # TODO: to enter the popup for each movie and get more info like genre, director, actors, description, etc.
    print("Opening popup for more movie info...")

    # find the button to open the popup and click it
    more_movie_info_button_class = "ipc-icon-button.li-info-icon.ipc-icon-button--base.ipc-icon-button--onAccent2"
    more_movie_info_button = driver.find_elements(By.CLASS_NAME, more_movie_info_button_class)[movie_counter]
    more_movie_info_button.click()
    time.sleep(5)  # wait for popup to load

    outer_popup_container_class = "sc-6ef24fae-0.doAmzT"
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, outer_popup_container_class)))
    popup_container = driver.find_element(By.CLASS_NAME, outer_popup_container_class)
    print("Popup container text:")
    # print(popup_container.text)


    # now partition the popup into sub-containers to get the info we want
    # first container
    first_sub_container = popup_container.find_elements(By.TAG_NAME, "div")[0]
    print(f"This is the text of the first container {first_sub_container.text}\n")

    # second container
    second_sub_container = popup_container.find_elements(By.TAG_NAME, "div")[1]
    print(f"This is the text of the second container {second_sub_container.text}\n")

    # third container
    third_sub_container = popup_container.find_elements(By.TAG_NAME, "div")[2]
    print(f"This is the text of the third container {third_sub_container.text}\n")


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
    data_inner_container = movie.find_elements(By.TAG_NAME, "div")[1]
    rating_and_voting_span = movie.find_element(By.TAG_NAME, "span") # this will return a span element
    inner_container_spans = data_inner_container.find_elements(By.TAG_NAME, "span")

    movie_title = movie.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "a").text.split(". ")[1]
    movie_year = inner_container_spans[0].text
    movie_duration = inner_container_spans[1].text
    pg_r_rating = inner_container_spans[2].text if len(inner_container_spans) > 2 else "Not Rated"
    movie_metascore = inner_container_spans[3].find_elements(By.TAG_NAME, "span")[0].text if len(inner_container_spans) > 3 else "No Metascore"

    # span > div > span > spans ( two of them )

    print(rating_and_voting_span.text)
    # movie_rating = rating_and_voting_span.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").find_elements(By.TAG_NAME, "span")[0].text
    # vote_count = rating_and_voting_span.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").find_elements(By.TAG_NAME, "span")[1].text
    # movie_description = driver.find_elements(By.CLASS_NAME, "ipc-html-content-inner-div")[movie_counter].text

    # todo: call the function to handle the popup for more movie info
    handle_more_info_movie_popup(driver, movie_counter)
    close_movie_popup(driver)

    # todo: add the info for each movie to a dictionary so that you can write the dictionary to a csv file for model training later
    # write_to_csv(movies, filename="movies.csv")



    print("Processing movie number:", movie_counter)
    print(f"The title of this movie is : {movie_title}\n")
    print(f"The year of this movie is : {movie_year}\n")
    print(f"The duration of this movie is : {movie_duration}\n")
    print(f"The R rating of this movie is : {pg_r_rating}\n")
    print(f"The metascore of this movie is : {movie_metascore}\n")
    # print(f"The description of this movie is : {movie_description}\n")
    print("-------------------------------------------------\n")

    movie_counter += 1


time.sleep(5)
driver.quit()

'''
span > div > span > spans ( two of them )

'''

