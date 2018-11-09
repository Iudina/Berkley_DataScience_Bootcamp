from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    dictionary = mongo.db.dictionary.find_one()
    return render_template("index.html", dictionary = dictionary)

@app.route("/scrape")
def scraper():
    dictionary = mongo.db.dictionary
    
    # assignt results of function 'scrape' from scrape_mars.py to a variable
    dictionary_data = scrape_mars.scrape()
   
    # Modifies an existing document in a collection. 
    # - {} selection criteria
    # - dictionary_data: modifications to apply (an update parameter)
    # - upsert - optional. If set to true, creates a new document when no document matches the query criteria.
    dictionary.update({}, dictionary_data, upsert=True)

    # "silently" return to a home directory
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
