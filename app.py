import os
from flask import Flask, render_template, request
from pymongo import MongoClient


app = Flask(__name__)

MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    raise ValueError("Missing MONGODB_URI environment variable")

client = MongoClient(
    MONGODB_URI,
    connectTimeoutMS=60000, 
    socketTimeoutMS=None)
db = client['FORMDATACOLLECTION']
Details = db['CONTACTS']

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.form.get('query', '')
    search_filter = {}

    if query:
        search_filter = {
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'phone': {'$regex': query, '$options': 'i'}}
            ]
        }

    contacts = list(Details.find(search_filter, {'_id': 0, 'name': 1, 'phone': 1, 'date_created': 1}))
    return render_template('index.html', contacts=contacts, query=query)
