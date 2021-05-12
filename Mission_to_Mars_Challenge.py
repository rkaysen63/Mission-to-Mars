# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ## Visit Mars Nasa News Site and Set up HTML parser

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page (searches for elements w specific combination of tag div and attribute list_text)
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')
browser.quit()


# ### Begin scraping

# Begin scraping. (Set this to a variable but for now, don't so it will print out.)
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ## 10.3.4 JPL Space Images -  Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Convert the browser html to a soup object
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Quit browser.
browser.quit()


# ## 10.3.5 Mars Facts - Scrape Tables with Pandas

# Scrape entire table with Pandas
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Convert DataFrame back into HTML-ready code using .to_html() function.
df.to_html(classes="table table-striped")



# # Mission to Mars Challenge

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# 2. Create a list to hold the images and titles, i.e. list of "hemispheres" (see for loop).
hemisphere_image_urls = []

# Parse home page.
html = browser.html
results = soup(html, 'html.parser')

# Check browser
# print(browser.html)

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(0, 4):
    
    # Create an empty dictionary to hold the key:value pairs.
    hemispheres = {}
   
    # Click on each hemisphere link.
    page = browser.find_by_css('.thumb')[x]

    # Navigate to the full-resolution image page.
    page.click()
    
    # Parse new page.
    html = browser.html
    results = soup(html, 'html.parser')       

    # Retrieve the full-resolution title and image URL string for the hemispher image.

    parent_elem = results.find('li')
    link = parent_elem.find('a', target='_blank')['href']
    img_url = ('https://marshemispheres.com/' + link)

    # print(link)
    # print(img_url)
    
    title = results.find('h2', class_='title').text
    # print(title)
    
    # Save the full-resolution image URL string as the value for the img_url key. 
    # Save the hemisphere image title as the value for the title key
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    hemisphere_image_urls.append(hemispheres)

    # Use browser.back() to navigate back to the beginning to get the next hemisphere image.
    browser.back()
    
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()