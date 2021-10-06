# Mission to Mars - Webscraping

# get_ipython().system('pip install splinter')
# get_ipython().system('pip install webdriver_manager')

# Import libraries
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bson.objectid import ObjectId
from flask import Flask, render_template

client = MongoClient(port = 27017)
db = client["mars_app"]
app_db = db["mars"]

app = Flask(__name__)

@app.route("/")
def home_page():
    value = app_db.find_one({'_id': ObjectId('614e4bdacdc203aefe1e682d')})

    headline = value["NASA Mars News"]["headline"]
    paragraph = value["NASA Mars News"]["paragraph"]
    featured_url = value["Featured Mars Image"]
    table = value["Mars Facts"]["table"]

    mars1 = value["Mars Hemispheres"]["image_urls"][0]["img_url"]
    title1 = value["Mars Hemispheres"]["image_urls"][0]["title"]

    mars2 = value["Mars Hemispheres"]["image_urls"][1]["img_url"]
    title2 = value["Mars Hemispheres"]["image_urls"][1]["title"]

    mars3 = value["Mars Hemispheres"]["image_urls"][2]["img_url"]
    title3 = value["Mars Hemispheres"]["image_urls"][2]["title"]

    mars4 = value["Mars Hemispheres"]["image_urls"][3]["img_url"]
    title4 = value["Mars Hemispheres"]["image_urls"][3]["title"]


    return render_template("index.html", 
    headline = headline,
    paragraph = paragraph,
    featured_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars1.jpg",
    table = table,
    mars1 = mars1,
    title1 = title1,
    mars2 = mars2,
    title2 = title2,
    mars3 = mars3,
    title3 = title3,
    mars4 = mars4,
    title4 = title4
    )

@app.route("/scrape")
def scrape():

    data = {"NASA Mars News": {}, "Featured Mars Image": {}, "Mars Facts": {}, "Mars Hemispheres": {}}

    # NASA Mars News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    req = requests.get(url, verify=True)

    soup = bs(req.content, "html.parser")

    headlines = soup.find_all(class_ = "content_title")

    data["NASA Mars News"]["headline"] = headlines[0].a.text.strip("\n")

    paragraph = soup.find_all(class_ = "article_teaser_body")

    data["NASA Mars News"]["paragraph"] = paragraph

    # Featured Mars Image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    browser.visit(url)

    browser.html

    soup2 = bs(browser.html, "html.parser")

    featured_image = soup2.find_all("img", class_ = "headerimage fade-in")[0]["src"]

    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + featured_image

    data["Featured Mars Image"]["featured_url"] = featured_image_url

    # Mars Facts

    tables = pd.read_html(requests.get("https://space-facts.com/mars/").text)

    df = tables[2]

    html_table = df.to_html()

    data["Mars Facts"]["table"] = html_table.replace("\n", "")

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

    # Update db
    app_db.replace_one({'_id': ObjectId('614e4bdacdc203aefe1e682d')}, data)

if __name__ == "__main__": 
    app.run(debug=True)
