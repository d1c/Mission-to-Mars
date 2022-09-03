#!/usr/bin/env python
# coding: utf-8

# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
	# Set up Splinter
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless=True)

	# Set news title & paragraph variables
	news_title, news_paragraph = mars_news(browser)

	# Run all scraping functions and store results in dictionary
	data = {
		"news_title": news_title,
    	"news_paragraph": news_paragraph,
    	"featured_image": featured_image(browser),
    	"facts": mars_facts(),
    	"last_modified": dt.datetime.now()
	}

	# Shut down the automated browser & return data.
	browser.quit()
	return data 


# Create mars_news function to visit & scrape data
def mars_news(browser):
	# Visit the Mars NASA news site.
	url = 'https://redplanetscience.com'
	browser.visit(url)

	# Optional delay for loading the page
	browser.is_element_present_by_css('div.list_text', wait_time=1)

	#Convert the browser html to a soup object
	html = browser.html
	news_soup = soup(html, 'html.parser')
	
	# Add error handling w/ try/except 
	try: 
		slide_elem = news_soup.select_one('div.list_text')
		# Use the parent element to find the first 'a' tag and save it in 'news_title'
		news_title = slide_elem.find('div', class_='content_title').get_text()
		# Use the parent element to find the paragraph text
		news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
	except AttributeError:
		return None, None
	return news_title, news_p


### Featured Images
def featured_image(browser):
	# Visit URL
	url = 'https://spaceimages-mars.com'
	browser.visit(url)

	# Find and click the full image button
	full_image_elem = browser.find_by_tag('button')[1]
	full_image_elem.click()

	# Parse the resulting html with soup
	html = browser.html
	img_soup = soup(html, 'html.parser')

	# Find the relative image url
	try:
		img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
	except:
		return None

	# Assemble the full URL to the image
	img_url = f'https://spaceimages-mars.com/{img_url_rel}'
	return img_url


### Mars Facts Table 
def mars_facts():
	try: 
		# Use Pandas to find and pull the Mars facts table into a DataFrame.
		df = pd.read_html('https://galaxyfacts-mars.com')[0]
	except BaseException:
		return None

	# Assign columns & set index of DataFrame
	df.columns=['description', 'Mars', 'Earth']
	df.set_index('description', inplace=True)

	# Convert the table back to HTML
	return df.to_html()

# Tell Flask the script is complete
if __name__ == "__main__":
	# If running as script, print scraped data
	print(scrape_all)

