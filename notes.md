# url to scrape from
https://www.imdb.com/search/title/?groups=top_1000
https://www.imdb.com/list/ls063676189/?page=4 ( for 100000 movies )

# columns to be used in the dataset
bedroom_nb = 'bedroom_number'
bathroom_nb = 'bathroom_number'


# steps to finish the project:
- we decided on the cars
- we will navigate directly to the car listings page
- from there we will have to select the start and end date for the rental and the currency
- we will sleep the thread to let the page make api calls and load the results
- we will then scrape the results


# get the movies for a certain genra
# get the number of movies
# get the movies for a cretain genra

# "ipc-link ipc-link--baseAlt" this is the class for the a tag inside the div tag
# anchor_class = "ipc-link.ipc-link--baseAlt"
# anchor_list = driver.find_elements(By.CLASS_NAME, anchor_class)

-- options when using wsl's chrome driver in headless mode
# opts = Options()
# opts.add_argument("--no-sandbox")
# opts.add_argument("--disable-dev-shm-usage")


# for i in range(0):
#     try:
#         button = wait.until(EC.element_to_be_clickable(
#             (By.CSS_SELECTOR, "button.ipc-see-more__button")
#         ))
#         # Scroll into view before clicking
#         driver.execute_script("arguments[0].scrollIntoView(true);", button)
#         time.sleep(1)  # short pause after scroll
#         button.click()
#         print(f"Clicked {i+1} times")
#         time.sleep(5)  # wait for movies to load
#     except Exception as e:
#         print(f"Stopped at click {i+1}: {e}")
#         break
#
# print("✅ Finished clicking 20 times.")


# columns
# title, year, duration, pg_rating, metascore, rating, vote_count, genre, description, director, stars (meaning actors)


Columns for the dataset:
------------------------
1- title
2- year
3- duration
4- pg_rating
5- metascore
6- rating
7- vote_count
8- genre
9- description
10- director
11- stars (meaning actors)
