# Use Flask to render a template, redirecting to another url and creating a URL
from flask import Flask, render_template, redirect, url_for

# Use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo

# Convert from Jupyter notebook to Python
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML homepage.
@app.route("/")
def index():
   # Use PyMongo to find "mars" collection in database
   mars = mongo.db.mars.find_one()
   # Tell Flask to return an HTML template and use "mars" collection in MongoDB.
   return render_template("index.html", mars=mars)

# Define route to scrape updated data when told to from homepage 
@app.route("/scrape")
def scrape():
   # Assign a new variable that points to Mongo database
   mars = mongo.db.mars
   # Create new variable to hold newly scraped data
   mars_data = scraping.scrape_all()
   # Update the database
   mars.update({}, mars_data, upsert=True)
   # Navigate back to homepage to see updated content
   return redirect('/', code=302)

# Run Flask.
if __name__ == "__main__":
   app.run()