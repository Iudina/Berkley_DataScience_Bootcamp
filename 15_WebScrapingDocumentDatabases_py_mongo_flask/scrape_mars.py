#import libraries
from splinter import Browser
from bs4 import BeautifulSoup
import requests

def scrape():
    ######################################################################################
    #1.1 Scrape the NASA Mars News Site, collect the latest News Title and Paragraph Text
    ######################################################################################

    # establish connection with the browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    news_title = None
    news_p = None
    retry = 3
    while retry != 0:
        retry -= 1
        try:
            html = browser.html
            soup0 = BeautifulSoup(html, 'html.parser')

            # Choose the latest news 
            news_title = soup0.find_all('div', class_="content_title")[0].text
            news_p = soup0.find_all('div', class_="article_teaser_body")[0].text
            break
        except:
            print("request failed")
            browser.reload()    

    browser.quit()

    ###################
    # 1.2 Scrape images
    ###################

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response1 = requests.get(img_url)
    soup1 = BeautifulSoup(response1.text, 'html.parser')

    # Using bs4 we extracted relative links to compressed images
    images = soup1.find_all('img', class_="thumb")

    # With split method we reconstructed the url to a full sized images using the extracted number of picture
    img_list = []
    for image in images[:30]:
        img_name = str(image['src']).split('/')[4].split('-')[0]
        img_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/' + img_name + '_hires.jpg'
        img_list.append(img_url)

    # Let random choose picture
    import random
    featured_image_url = random.choice(img_list)
    # print(featured_image_url)

    #########################################################################
    #1.3 Scrape the latest Mars weather from the Mars Weather twitter account
    #########################################################################

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response2 = requests.get(twitter_url)
    soup2 = BeautifulSoup(response2.text, 'html.parser')

    tweets  = soup2.find_all('p', class_="js-tweet-text")

    # Choose tweet with weather
    for tweet in tweets:
        if tweet.text.startswith('Sol '):
            mars_weather = tweet.text
            # print(mars_weather)
            break

    ################
    # 1.2 Mars Facts
    ################

    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    import pandas as pd

    facts_url = 'https://space-facts.com/mars/'
    df = pd.read_html(facts_url)[0]

    df.columns = ['Description', 'Value']
    df.set_index("Description", inplace=True)
    df

    # Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html()
    html_table
    df.to_html('table.html')

    #######################
    # 1.2 Mars Hemispheres
    ######################

    # establish connection with the browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    url_hemisph = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemisph)
    
    hemisphere_image_urls = []
    # Create bs4 object of parced out html
    soup = BeautifulSoup(browser.html, 'html.parser')

    # Scrape names of hemispheres
    h_names = soup.find_all('h3')
    for h_name in h_names:

        browser.click_link_by_partial_text(h_name.text) # Follow link to page with a particular Hemisphere
        h_name = h_name.text.replace(' Enhanced','')
        
        soup = BeautifulSoup(browser.html, 'html.parser') # Create new bs4 object of a current page

        find_a = soup.find_all('a') # Find all <a> - tags containing "Sample" text - this is a link to an image
        
        for img_url in find_a:

            if (img_url.text == "Sample"):
                x = img_url['href'] # Withdraw img source
                a = {"title": h_name, "img_url": x} # Store values in dictionary
            
        browser.back()
        hemisphere_image_urls.append(a) # Append dictionary to a list
    browser.quit()      
    # print(hemisphere_image_urls)

    dictionary = {'news_title': news_title, 'news_paragraph': news_p, 'featured_image_url': featured_image_url, 
                    'mars_weather': mars_weather, 'hemispheres': hemisphere_image_urls}

    return dictionary
    
scrape()
