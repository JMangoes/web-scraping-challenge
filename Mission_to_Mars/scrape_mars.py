from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #Obtaining article title and paragraph
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(1)
    news_title = soup.find("div", class_="content_title").find("a").text
    news_p = soup.find("div", class_="article_teaser_body").text

    #Getting featured picture
    image_link = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_link)

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    time.sleep(1)
    new_link = "https://www.jpl.nasa.gov"
    featured_image_path = image_soup.find("img", class_="thumb")["src"]
    featured_image_url = new_link + featured_image_path

    #Scraping twitter for Mars weather
    twitter_link = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_link)

    time.sleep(1)
    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text

    #Using pandas scrape to gather facts about Mars
    mars_facts_url = "https://space-facts.com/mars/"
    mars_information = pd.read_html(mars_facts_url)
    mars_df = mars_information[0]
    mars_df.columns = ["Description", "Values"]
    mars_df.set_index("Description", inplace=True)
    mars_facts = mars_df.to_html()
    

    #Scrape hemisphere photos
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html_hemispheres = browser.html

    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    items = soup.find_all('div', class_='item')
 
    hemisphere_image_urls = []

    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    for i in items: 
        time.sleep(1)

        title = i.find('h3').text
    
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        browser.visit(hemispheres_main_url + partial_img_url)
    
        partial_img_html = browser.html
     
        soup = BeautifulSoup(partial_img_html, 'html.parser')
    
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "mars_hemisphere": hemisphere_image_urls
    }

    browser.quit()

    return mars_info

