# app.py
# KU Data Bootcamp
# Module: 10.5.1

# Import Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Set up connection to Mongo using PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set up Flask routes

# Define route for index.html
@app.route("/")
def index():
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)

# Scraping route. This function will go & scrape web pages for updated information.
@app.route("/scrape")
def scrape():
	mars = mongo.db.mars
	mars_data = scraping.scrape_all()
	mars.update_one({}, {"$set":mars_data}, upsert=True)
	return redirect('/', code=302)

# Run Flask
if __name__ == "__main__":
   app.run()