# IMBD Movie Scraper Script
# TODO: Imports
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
import pandas as pd

# Unused imports
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# from request_header import headers

results_url_test = 'https://www.imdb.com/search/title/?title_type=feature,tv_movie&user_rating=6,10&release_date=1990-01-01,2020-12-31&groups=oscar_nominee&languages=en'

# TODO: Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

# TODO: Instantiate the webdriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(results_url_test)

# TODO: Scrape the results page with Selenium
# Get all the movie titles
movie_titles = [title.text.split('. ')[1] for title in driver.find_elements(By.CSS_SELECTOR, 'a .ipc-title__text')]
# print(movie_titles)

# Get all the movie descriptions
movie_descriptions = [description.text for description in driver.find_elements(By.CSS_SELECTOR, 'div .ipc-html-content-inner-div')]
# print(movie_descriptions)

# Get all the movie_urls
movie_urls = [url.get_attribute('href') for url in driver.find_elements(By.CSS_SELECTOR, 'div .ipc-title-link-wrapper')]
# print(movie_urls)

# Get all the movie_ratings
movie_ratings = [rating.text.split('\n')[0] for rating in driver.find_elements(By.CSS_SELECTOR, 'span .ratingGroup--imdb-rating')]
# print(movie_ratings)

# Get all the movie_metascores
movie_metascores = [metascore.text for metascore in driver.find_elements(By.CSS_SELECTOR, 'span .metacritic-score-box')]
# print(movie_metascores)

# Get all the movie_no_votes
movie_no_votes = [int(no_votes.text.split('s')[1].replace(',', '')) for no_votes in driver.find_elements(By.CSS_SELECTOR, '.sc-53c98e73-0')]
# print(movie_no_votes)

driver.quit()

# TODO: Save the results in a CSV file
data = {
    'title': movie_titles,
    'rating': movie_ratings,
    'metascore': movie_metascores,
    'number of votes': movie_no_votes,
    'url': movie_urls,
    'description': movie_descriptions,
}

df = pd.DataFrame(data)
df.to_csv('output.csv')

print("Done!")