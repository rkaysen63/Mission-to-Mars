# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Function to connect to Mongo and establish communication between code and database
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Function to scrape Mars NASA News site
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    # url = 'https://redplanetscience.com/'
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first <a> tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# Function to scrape JPL Space Images Featured Image
def featured_image(browser):
    # Visit URL
    # url = 'https://spaceimages-mars.com'
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

# Function to scrape Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        # df = pd.read_html('https://galaxyfacts-mars.com')[0]
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
      return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert DataFrame back into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# Function to scrape Mars Images
def mars_hemispheres(browser):

    # Visit Mars Hemispheres site
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the dictionaries of image_urls and titles
    hemisphere_image_urls = []

    # Parse home page.
    html = browser.html
    results = soup(html, 'html.parser')

    # Retrieve the image urls and titles for each hemisphere.
    try:
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
    
            title = results.find('h2', class_='title').text
    
            # Save the full-resolution image URL string as the value for the img_url key. 
            # Save the hemisphere image title as the value for the title key
            hemispheres['img_url'] = img_url
            hemispheres['title'] = title
    
            hemisphere_image_urls.append(hemispheres)

            # Use browser.back() to navigate back to the beginning to get the next hemisphere image.
            browser.back()
    except:
        # print('Error in Mars Hemispheres')
        raise

    print(hemisphere_image_urls)

    return hemisphere_image_urls
    

    
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())