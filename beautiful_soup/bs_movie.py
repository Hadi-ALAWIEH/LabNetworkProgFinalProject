# TODO: you still need to handle the budget, the revenue and the original language, and the director and writer of the movie, all other fields are done
'''
# columns that I have scraped in beutiful soup:
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
budget
revenue
director
original language

# columns that are in the api dataset but not in selenium or bs4:
popularity
vote_count

'''
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()
page_counter = 2
base_url = f"https://www.themoviedb.org/movie?page={page_counter}"

driver.get(base_url)


soup = BeautifulSoup(driver.page_source, 'html5lib')


# find the reject cookies button and click it
# reject_all_cookies_button = soup.find("button", { "class" : "onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon" })
# reject_all_cookies_button.click()
# time.sleep(2)  # wait for the page to load after cookies are rejected

page = soup.find_all('div', { "class" : "page_wrapper" })[0]
movies = page.find_all('div', { "class" : "card style_1"})
time.sleep(2)  # wait for the page to load

# driver.get(f"{base_url}{soup.find_all("p", { "class" : "load_more" })[1].find("a").get_attribute_list("href")[0]}"))
# next_url_segement = soup.find_all("p", { "class" : "load_more" })[1].find("a").get_attribute_list("href")[0]
# print(next_url_segement)

time.sleep(2)  # wait for the page to load after clicking load more
print(f"Found {len(movies)} movies.\n")
for movie in movies:
    h2_tag = movie.find('h2')
    a_tag = h2_tag.find('a')
    relative_url = a_tag['href']
    full_url = f"https://www.themoviedb.org{relative_url}"

    driver.get(full_url)
    inner_movie = inner_soup = BeautifulSoup(driver.page_source, 'html5lib')

    # TODO: scrape movie details here...
    title = None
    pg_rating = None
    date_and_country_of_release = None
    duration = None
    overview = None
    director = None
    top_stars = None
    original_title = None
    status = None
    original_language = None
    budget = None
    revenue = None
    movie_keywords = None

    # outer_container = inner_movie.find('div', { "class" : "title ott_false" })
    title = inner_movie.find('div', { "class" : "title ott_false" }).find('h2').find('a').text
    year = inner_movie.find('div', { "class" : "title ott_false" }).find('h2').find('span').text
    user_score = inner_movie.find('div', { "class" : "user_score_chart" }).get_attribute_list("data-percent")[0]
    pg_rating = inner_movie.find('span', { "class" : "certification" }).text.strip() if inner_movie.find('span', { "class" : "certification" }) else "Not Rated"
    release = inner_movie.find('span', { "class" : "release" }).text.strip() if inner_movie.find('span', { "class" : "release" }) else "No release date"
    genres = inner_movie.find('span', { "class" : "genres" }).text.strip() if inner_movie.find('span', { "class" : "genres" }) else "No genres"
    duration = inner_movie.find('span', { "class" : "runtime" }).text.strip() if inner_movie.find('span', { "class" : "runtime" }) else "No duration"
    overview = inner_movie.find('div', { "class" : "overview" }).find('p').text.strip() if inner_movie.find('div', { "class" : "overview" }) else "No overview"
    side_facts = inner_movie.find('section', { "class" : "facts left_column" })
    original_title = side_facts.find('p', { "class" : "wrap" }).text if side_facts.find('p', { "class" : "wrap" }) else "No original title"
    status = side_facts.find_all('p')[1].text.replace("Status", "", 1).strip() if len(side_facts.find_all('p')) > 1 and original_title != "No original title" else side_facts.find_all('p')[0].text.replace("Status", "", 1).strip()
    original_language = side_facts.find_all('p')[1].text.replace("Original Language", "", 1).strip() if len(side_facts.find_all('p')) > 1 and original_title == "No original title" else side_facts.find_all('p')[2].text.replace("Original Language", "", 1).strip()
    budget = side_facts.find_all('p')[2].text.replace("Budget", "", 1).strip() if len(side_facts.find_all('p')) > 2 else "No budget"
    revenue = side_facts.find_all('p')[3].text.replace("Revenue", "", 1).strip() if len(side_facts.find_all('p')) > 3 else "No revenue"

    director = inner_movie.find("ol", {"class": "people no_image"}).find("li").find("p").find("a").text

    # finding the keywords for the movie
    keywords_section = inner_movie.find("section", {"class": "keywords right_column"})
    if keywords_section:
        ul_tag = keywords_section.find("ul")
        if ul_tag:  # movie has keywords
            movie_keywords = [li.get_text(strip=True) for li in ul_tag.find_all("li")]
        else:  # no <ul> → movie has no keywords
            movie_keywords = ["No keywords"]
    else:
        movie_keywords = ["No keywords"]

    # finding the top 3 stars of the movie
    top_stars = inner_movie.find("ol", {"class": "people scroller"}).find_all("li", limit=3)
    top_stars_list = [top_star.find("p").find("a").text for top_star in top_stars]



    # year = inner_movie.find('h2', { "class" : "9" }).find('span').text
    print("title: ", title)
    print("year: ", year)
    print("user score: ", user_score)
    print("pg_rating: ", pg_rating)
    print("release:", release)
    print("genres:", genres)
    print("duration:", duration)
    print("overview:", overview)
    print("original_title:", original_title)
    print("original_language:", original_language)
    print("status:", status)
    print("movie keywords: ", movie_keywords)
    print("top stars: ", top_stars_list)
    print("budget:", budget)
    print("revenue", revenue)
    print("director:", director)
    print(("-------------------------------------------------\n"))


driver.quit()

# load the initial page of movies
# access the details of each movie from the page and scrape the required information
# write the scraped information to a row in a CSV file

'''
title - done
year - done
user score - done
pg_rating - done
release - done
genres - done
duration - done
overview - done
director
top_actors
original title - done
status - done
original language - done
budget
revenue
movie_keywords - done
'''


'''
DevTools listening on ws://127.0.0.1:54290/devtools/browser/e689f49d-e44e-4f94-9377-9a31d3ab4b75
Found 20 movies.

<div class="card style_1">
 <div class="image">
  <div class="wrapper glyphicons_v2 picture grey no_image_holder">
   <a class="image" href="/movie/1156594-culpa-nuestra" title="Our Fault">
    <img alt="Our Fault" class="poster w-full" loading="lazy" src="https://media.themoviedb.org/t/p/w220_and_h330_face/yzqHt4m1SeY9FbPrf
Z0C2Hi9x1s.jpg" srcset="https://media.themoviedb.org/t/p/w220_and_h330_face/yzqHt4m1SeY9FbPrfZ0C2Hi9x1s.jpg 1x, https://media.themoviedb
.org/t/p/w440_and_h660_face/yzqHt4m1SeY9FbPrfZ0C2Hi9x1s.jpg 2x"/>
   </a>
  </div>
  <div class="options" data-id="1156594" data-media-type="movie" data-object-id="64c12f901cfe3a0eb30bf2b5" data-role="tooltip">
   <a aria-label="View Item Options" class="no_click" href="#">
    <div class="glyphicons_v2 circle-more white">
    </div>
   </a>
  </div>
 </div>
 <div class="content">
  <div class="consensus tight">
   <div class="outer_ring">
    <div class="user_score_chart 64c12f901cfe3a0eb30bf2b5" data-bar-color="#21d07a" data-percent="77" data-track-color="#204529">
     <div class="percent">
      <span class="icon icon-r77">
      </span>
     </div>
     <canvas height="40" style="height: 34px; width: 34px;" width="40">
     </canvas>
    </div>
   </div>
  </div>
  <h2>
   <a href="/movie/1156594-culpa-nuestra" title="Our Fault">
    Our Fault
   </a>
  </h2>
  <p>
   Oct 15, 2025
  </p>
 </div>
 <div class="hover 1156594">
 </div>
</div>
'''

# soup.find_all("p", { "class" : "load_more" })[2].find("a").click()


'''

essentially we used boosting and bagging

- list out the actos of each row
- keep the actors with the highest occurences
- take the top 100 actors
- use multi hot encoding to represent the presence of each actor in the movie
- target encoding for the rest of the actors what is it ?


tmom hanks1: 40
tom hanks2: 35
tom hanks3: 30

then multihot encoding

a1 a2 a3 other_column
1 1 0 0 0
0 0 0 0 1

those 100 columsn are a seperate dataframe and then you concatinate it to the original dataframe,
this allows to know for each movie which, if any, one of the top 100 actors are in the movie

target encoding:
I accessed all rows where the column for which the tomhanks actor is 1, and calculated the average of the rating for those rows, this essentially gives me the average rating for movies with tom hanks in them ( its as if it's a rating for the actor itself )

we access movie 1,
we saw the actors of the movie,
we compared the averages of the actors for a given movie,

max_rating, min_rating, average_rating

max_rating is the one for the most succeffull actor
min_rating is the ...
average is the avergage of those

after this process, for each row, the model will now for a given max_rating, min_rating and average_rating

hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35
hadi, [hadi1, hadi2, hadi3], 50, 20, 35

what is cross validation?
Cross-validation is a statistical method used to estimate the skill of machine learning models. It is primarily used in scenarios where the goal is to assess how the results of a predictive model will generalize to an independent dataset. The most common form of cross-validation is k-fold cross-validation, where the dataset is divided into 'k' subsets (or folds). The model is trained on 'k-1' folds and tested on the remaining fold. This process is repeated 'k' times, with each fold being used as the test set once. The results from each iteration are then averaged to produce a single performance metric. This technique helps in mitigating overfitting and provides a more reliable estimate of model performance compared to a single train-test split.

'''
