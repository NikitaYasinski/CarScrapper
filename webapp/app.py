from __future__ import unicode_literals

import json
import requests
import time
import pymongo

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


params = {
    "request": {
        "url": "https://ab.onliner.by"
    }, 
    "spider_name": "cars"
}

@app.route('/home', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        brand = request.form["brand"]
        model = request.form["model"]
        params["request"]["url"] += "/{brand}/{model}".format(brand=brand, model=model)
        return redirect(url_for("crawl"))
    else:
        return render_template("home.html")   

@app.route('/crawl')
def crawl():
    
    requests.post('http://localhost:9080/crawl.json', json=params)
    conn = pymongo.MongoClient(
            'localhost',
            27017
        )
    
    cars = []
    db = conn['cars']
    collection = db['cars_tb']
    for car in collection.find({}, {"_id":0, "name": 1, "price": 1, "img": 1}):
        cars.append(car)
    
    return render_template("index.html", cars=cars)

if __name__ == '__main__':
    app.run(debug=True)