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
@app.route('/search', methods=['GET'])
def query_inventory():
    #not fully done - I put some variables in place of what they might actually be
    #not sure about what you all might have named things
    name = request.args.get('name')
    item = Items.objects(name=record['name'])
    if not item:
        returnjsonify({'error': 'item not found'})
    return jsonify(item.to/_json())
    
    return render_template("search.html", page="Search")