#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
import sys

# instantiate the app
app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    # render_template('error.html', error=e) # render the edit template
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug

# set up the routes

# route for the home page
@app.route('/')
def home():
    """
    Route for the home page
    """
    return render_template("home.html")
@app.route('/search', methods=['GET'])
def search_inventory():
    name = request.args.get('name')
    docs = db.exampleapp.find({"name": {"$regex": name, "$options": "i"}})
    if not docs:
        return jsonify({'error': 'item not found'})
    
    return render_template("searchpage.html", page="Search")


@app.route('/items/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete_one(item)
    db.session.commit()
    return redirect(url_for('index'))
    
    
# route to add to the inventory
@app.route('/inventories/add_item', methods=['GET','POST'])
def add_item():
    if request.method == 'POST':
        itemName = request.form['iname']
        qty = request.form.get('quantity',type=int)

        # create a new document with the data the user entered
        doc = {
            "name": itemName,
            "quantity": qty, 
            "added_at": datetime.datetime.utcnow()
        }
        db.exampleapp.insert_one(doc) # insert a new document

    return render_template('addpage.html')

@app.route('/items/edit/<int:item_id>', methods = ['POST'])
def edit_inventory(item_id):
    item = Item.query.get_or_404(item_id)
    new_in = request.form.get('edited quantity value',type=int)
    item.qty = new_in
    db.session.commit()
