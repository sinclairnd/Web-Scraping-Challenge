# Mission to Mars - Webscraping

# get_ipython().system('pip install splinter')
# get_ipython().system('pip install webdriver_manager')

# Import libraries
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
import scrapes
# from bson.objectid import ObjectId

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# client = MongoClient(port = 27017)
# db = client["mars_app"]
# app_db = mongo["mars"]


@app.route("/")
def home_page():
    value = mongo.db.mars.find_one()

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
    data = scrapes.scrape_all()

# Update db
    mongo.db.mars.update({}, data, upsert=True)

    return redirect("/")

if __name__ == "__main__": 
    app.run(debug=True)
