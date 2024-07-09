import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


client = MongoClient(
    'mongodb+srv://ChefsBhojan:usX7ZS8kPz4Pv@cluster0.eikei2d.mongodb.net/',
    connectTimeoutMS=30000, 
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

    contacts = list(Details.find(search_filter, {'_id': 0, 'name': 1, 'phone': 1, 'date_created': 1, 'redeemed': 1,'discount':1}))
    return render_template('index.html', contacts=contacts, query=query)


@app.route('/redeem', methods=['POST'])
def redeem():
    data = request.json
    contact_phone = data.get('contact_phone')
    discount = data.get('discount')

    if not contact_phone or not discount:
        return jsonify({"error": "Contact phone and discount are required"}), 400

    Details.update_one({'phone': contact_phone}, {'$set': {'redeemed': True, 'discount': int(discount)}})
    return jsonify({"success": True}), 200