# TODO: Create a IMBD Movie Scraper Script

# Imports
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from itertools import zip_longest

# TODO: Keep Chrome open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

# TODO: Instantiate the webdriver
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.imdb.com/')

# TODO: Click the "All" dropdown on IMDB
driver.find_element(By.CLASS_NAME, 'sc-dIvsgl').click()

# TODO: Click on the dropdown item 'Advanced Search' (wait 0,5 second)
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="navbar-search-category-select-contents"]/ul/a/span[1]').click()
# driver.find_element(By.LINK_TEXT, 'Advanced Search').click()

# TODO: Fill in the form with all the search inputs
# Click on 'Expand All' to show all the form entries
driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[1]/div/button/span').click()

# Select title types 'Movie' and 'TV Movies'
driver.find_element(By.XPATH, '//*[@id="accordion-item-titleTypeAccordion"]/div/section/button[1]').click()
driver.find_element(By.XPATH, '//*[@id="accordion-item-titleTypeAccordion"]/div/section/button[6]').click()

# Fill in release date from 1 January 1990 to 31 December 2020 (mm/dd/yyyy)
driver.find_element(By.NAME, 'release-date-start-input').send_keys('01/01/1990')
driver.find_element(By.NAME, 'release-date-end-input').send_keys('12/31/2020')

# Fill in IMDB rating from 7 to 10
driver.find_element(By.NAME, 'imdb-ratings-max-input').send_keys('6')
driver.find_element(By.NAME, 'imdb-ratings-min-input').send_keys('10')

# Select Awards & Recognitions: 'Oscar Nominated'
awards_section = driver.find_element(By.XPATH, '//*[@id="awardsAccordion"]/div[1]/label')
# Use javascript click instead of regular click because latter doesn't seem to work.
oscar_nominated = driver.find_element(By.XPATH, '//*[@id="accordion-item-awardsAccordion"]/div/section/button[4]')
driver.execute_script("arguments[0].click();", oscar_nominated)

# Select plot within topic 'Alternate Versions'.
# This code uses the imported 'Select' class for the dropdown <select>
topics_section = driver.find_element(By.XPATH, '//*[@id="pageTopicsAccordion"]/div[1]/label/span[1]/div')
select_plot = driver.find_element(By.ID, 'within-topic-dropdown-id')
dropdown_select_plot = Select(select_plot)
dropdown_select_plot.select_by_visible_text('Alternate Versions')

# Select language 'English'. Scroll down to that section.
language_section = driver.find_element(By.XPATH, '//*[@id="languagesAccordion"]/div[1]/label/span[1]/div')
select_language = driver.find_element(By.XPATH, '//*[@id="accordion-item-languagesAccordion"]/div/div/div[1]/div[1]/input')
driver.execute_script("arguments[0].click();", select_language)
select_language.send_keys('English')
select_language_english = driver.find_element(By.XPATH, '//*[@id="react-autowhatever-1--item-79"]/div/div/label')
driver.execute_script("arguments[0].click();", select_language_english)
driver.execute_script("arguments[0].scrollIntoView(true);", language_section)

# Click on 'See Results' e.g. submit the form
print("Working...")
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[1]/button[2]/span').click()

# TODO: Click the 'See More' text until all the results are loaded on the results page
while True:
    try:
        time.sleep(3)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        see_more_button = driver.find_element(By.CLASS_NAME, 'ipc-see-more__text')
        driver.execute_script("arguments[0].click();", see_more_button)

    except Exception as e:
        # print(f"Error: {e}")
        break

# TODO: Get the URL of the Results page
results_url = driver.current_url
print(f'↓↓↓ ... Scraping the results page ... ↓↓↓ \n {results_url}')

# TODO: Scrape the results page with Selenium
# Get all the movie titles
movie_titles = [title.text.split('. ')[1] for title in driver.find_elements(By.CSS_SELECTOR, 'a .ipc-title__text')]
# print(movie_titles)
print(f'Found {len(movie_titles)} movie titles...')

# Get all the movie descriptions
movie_descriptions = [description.text for description in driver.find_elements(By.CSS_SELECTOR, 'div .ipc-html-content-inner-div')]
# print(movie_descriptions)
print(f'Found {len(movie_descriptions)} movie descriptions...')

# Get all the movie_urls
movie_urls = [url.get_attribute('href') for url in driver.find_elements(By.CSS_SELECTOR, 'div .ipc-title-link-wrapper')]
# print(movie_urls)
print(f'Found {len(movie_urls)} movie Urls...')

# Get all the movie_ratings
movie_ratings = [rating.text.split('\n')[0] for rating in driver.find_elements(By.CSS_SELECTOR, 'span .ratingGroup--imdb-rating')]
# print(movie_ratings)
print(f'Found {len(movie_ratings)} movie ratings...')

# Get all the movie_metascores
movie_metascores = [metascore.text for metascore in driver.find_elements(By.CSS_SELECTOR, 'span .metacritic-score-box')]
# print(movie_metascores)
print(f'Found {len(movie_metascores)} movie metascores...')

# Get all the movie_no_votes
movie_no_votes = [int(no_votes.text.split('s')[1].replace(',', '')) for no_votes in driver.find_elements(By.CSS_SELECTOR, '.sc-53c98e73-0')]
# print(movie_no_votes)
print(f'Found {len(movie_no_votes)} movies with user votes...')

driver.quit()

# TODO: Save the results in a CSV file
print("Saving results to CSV...")
lists = [movie_titles, movie_ratings, movie_metascores, movie_no_votes, movie_urls, movie_descriptions]
zipped_lists = zip_longest(*lists, fillvalue=None)
df = pd.DataFrame(zipped_lists, columns=['Title', 'Rating', 'Metascore', 'No Votes', 'Url', 'Description'])
df.to_csv('output.csv')
print("Done!")
