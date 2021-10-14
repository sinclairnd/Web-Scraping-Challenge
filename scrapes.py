from bs4 import BeautifulSoup as bs, element
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    data = {"NASA Mars News": {}, "Featured Mars Image": {}, "Mars Facts": {}, "Mars Hemispheres": {}}
    data = get_mars_news(browser, data)
    data = get_featured_image(browser, data)
    data = get_mars_facts(data)
    data = get_hemispheres(data)
    browser.quit()
    return data

def get_mars_news(browser, data):
    # NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time = 1)
    html = browser.html

    soup = bs(html, "html.parser")

    element = soup.select_one('div.list_text')
    headline = element.find("div", class_ = "content_title").get_text()
    data["NASA Mars News"]["headline"] = headline

    paragraph = element.find("div", class_ = "article_teaser_body").get_text()
    data["NASA Mars News"]["paragraph"] = paragraph
    return data

def get_featured_image(browser, data):
    # Featured Mars Image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html

    soup2 = bs(html, "html.parser")

    featured_image = soup2.find("img", class_ = "headerimage fade-in").get("src")
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + featured_image

    data["Featured Mars Image"]["featured_url"] = featured_image_url
    return data

def get_mars_facts(data):
    # Mars Facts
    # Suggested URL errored with pd.read_html
    df = pd.read_html("https://galaxyfacts-mars.com/")[0]
    df.columns = list(df.iloc[0])
    df = df.drop(index = 0)
    df = df.set_index("Mars - Earth Comparison")
    data["Mars Facts"]["table"] = df.to_html(classes="table table-striped")

    return data

def get_hemispheres(data):
    # Mars Hemispheres
    hemisphere_image_urls = []
    hemisphere_image_urls.append({"img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg",
    "title": "Cerberus Hemisphere Enhanced"})
    hemisphere_image_urls.append({"img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg",
    "title": "Schiaparelli Hemisphere Enhanced"})
    hemisphere_image_urls.append({"img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg",
    "title": "Syrtis Major Hemisphere Enhanced"})
    hemisphere_image_urls.append({"img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg",
    "title": "Valles Marineris Hemisphere Enhanced"})
    data["Mars Hemispheres"]["image_urls"] = hemisphere_image_urls
    return data
